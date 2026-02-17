import firebase_admin
from firebase_admin import credentials, db, auth # Import auth
from threading import Thread

cred = credentials.Certificate(os.path.join(BASE_DIR, "serviceAccountKey.json"))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://phish-guard-94030-default-rtdb.europe-west1.firebasedatabase.app/'
})

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import joblib
from utils import preprocess_text, extract_features
from history_utils import load_history, add_scan_to_history, get_dashboard_stats
from email_sending.sender import send_phishing_alert_email # Import the email sending function

import pathlib
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend', 'dist'))
app = Flask(__name__, static_folder=FRONTEND_DIST, static_url_path='')
CORS(app)  # Enable CORS for all routes


# Load model (lazy loading or on startup)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'phishing_model.pkl')
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None
    else:
        print("Model file not found. Please train the model first.")

load_model()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})



@app.route('/predict', methods=['POST'])
def predict():
    user_id = request.headers.get('X-User-ID') # Get user ID from header
    if not user_id:
        return jsonify({"error": "Unauthorized: Missing X-User-ID header"}), 401

    data = request.json
    if not data or 'text' not in data or 'type' not in data:
        return jsonify({"error": "Missing required fields: 'text' and 'type'"}), 400
    input_text = data['text']
    input_type = data['type']  # 'email', 'sms', or 'url'
    processed_text = preprocess_text(input_text)
    heuristics = extract_features(input_text)
    result = {
        "result": "Unknown",
        "confidence": 0.0,
        "heuristics": heuristics,
        "input": input_text,
        "input_type": input_type,
        "email": data.get('email', ''),
        "subject": data.get('subject', ''),
        "userId": user_id # Add userId to the scan result
    }
    if model:
        try:
            prediction = model.predict([processed_text])[0]
            proba = model.predict_proba([processed_text])[0]
            result['result'] = "Phishing" if prediction == 1 else "Legitimate"
            result['confidence'] = float(max(proba))
            suspicious_words_found = [word for word in ['urgent', 'verify', 'login'] if word in input_text.lower()]
            result['suspicious_words'] = suspicious_words_found
        except Exception as e:
            return jsonify({"error": f"Prediction failed: {e}"}), 500
    else:
        return jsonify({"error": "Model not loaded"}), 503
    # Save to history
    add_scan_to_history(user_id, result)
    return jsonify(result)


@app.route('/history', methods=['GET'])
def get_history():
    user_id = request.headers.get('X-User-ID') # Get user ID from header
    if not user_id:
        return jsonify({"error": "Unauthorized: Missing X-User-ID header"}), 401
    return jsonify(load_history(user_id))


@app.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    user_id = request.headers.get('X-User-ID') # Get user ID from header
    if not user_id:
        return jsonify({"error": "Unauthorized: Missing X-User-ID header"}), 401
    return jsonify(get_dashboard_stats(user_id))


# Serve React frontend (index.html) for all non-API routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path.startswith(('api', 'predict', 'history', 'dashboard_stats', 'health')):
        return jsonify({'error': 'Not found'}), 404
    file_path = os.path.join(FRONTEND_DIST, path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, 'index.html')

def listen_for_sms_changes(event):
    print(f"SMS Data changed: {event.event_type}")
    print(f"SMS Data: {event.data}")
    
    if event.event_type == 'put' and event.data:
        # Assuming event.data is the full SMS object or a dictionary
        sms_id = event.path.split('/')[-1] # Extract smsId from path /sms_logs/{userId}/{smsId}
        user_id = event.path.split('/')[-2] if len(event.path.split('/')) > 2 else None

        if not user_id:
            print("Warning: SMS event without a user ID. Cannot process.")
            return

        sms_data = event.data
        sms_text = sms_data.get('messageBody', '') # Assuming the SMS text is in 'messageBody'
        timestamp = sms_data.get('timestamp')

        if not sms_text:
            print(f"Skipping empty SMS from user {user_id} with ID {sms_id}")
            return

        print(f"Processing new SMS from user {user_id}, ID {sms_id}: {sms_text[:50]}...")

        result = {
            "result": "Unknown",
            "confidence": 0.0,
            "heuristics": {},
            "input": sms_text,
            "input_type": "sms",
            "timestamp": timestamp,
            "userId": user_id
        }

        if model:
            try:
                processed_text = preprocess_text(sms_text)
                heuristics = extract_features(sms_text)
                
                prediction = model.predict([processed_text])[0]
                proba = model.predict_proba([processed_text])[0]

                result['result'] = "Phishing" if prediction == 1 else "Legitimate"
                result['confidence'] = float(max(proba))
                result['heuristics'] = heuristics
                suspicious_words_found = [word for word in ['urgent', 'verify', 'login', 'prize', 'winner'] if word in sms_text.lower()]
                result['suspicious_words'] = suspicious_words_found

                # Update the Realtime Database with the processing result
                db.reference(f'sms_logs/{user_id}/{sms_id}').update({
                    'scanResult': result['result'],
                    'confidence': result['confidence'],
                    'heuristics': result['heuristics'],
                    'suspicious_words': result['suspicious_words'],
                    'processed': True,
                    'processedTimestamp': db.SERVER_TIMESTAMP
                })

                # TODO: Integrate email notification here if result['result'] == "Phishing"
                if result['result'] == "Phishing":
                    print(f"Phishing SMS detected for user {user_id}. Sending email notification.")
                    try:
                        user_record = auth.get_user(user_id)
                        recipient_email = user_record.email
                        if recipient_email:
                            send_phishing_alert_email(
                                recipient_email,
                                sms_text,
                                result['result'],
                                result['suspicious_words']
                            )
                        else:
                            print(f"User {user_id} has no email associated for notifications.")
                    except Exception as e:
                        print(f"Error fetching user email or sending email for {user_id}: {e}")

            except Exception as e:
                print(f"Error processing SMS for user {user_id}, ID {sms_id}: {e}")
                db.reference(f'sms_logs/{user_id}/{sms_id}').update({
                    'processingError': str(e),
                    'processed': False,
                    'processedTimestamp': db.SERVER_TIMESTAMP
                })
        else:
            print("Model not loaded, cannot process SMS.")
            db.reference(f'sms_logs/{user_id}/{sms_id}').update({
                'processingError': 'Model not loaded',
                'processed': False,
                'processedTimestamp': db.SERVER_TIMESTAMP
            })

# Start listening in a separate thread
def start_db_listener():
    ref = db.reference('sms_logs')
    ref.listen(listen_for_sms_changes)

# Start the listener thread when the Flask app starts
@app.before_request
def before_request():
    if not hasattr(app, '_db_listener_started'):
        thread = Thread(target=start_db_listener)
        thread.daemon = True
        thread.start()
        app._db_listener_started = True

if __name__ == '__main__':
    app.run(port=5000)
