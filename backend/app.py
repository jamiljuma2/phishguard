import os
    """Stub for user identification (no auth). Returns a fixed UID for demo purposes."""
    return "demo_user"

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})


<<<<<<< HEAD
=======


>>>>>>> 8b707b27 (Fix: Ensure backend /dashboard_stats includes recent field for dashboard, code audit for Python compliance)
@app.route('/predict', methods=['POST'])
def predict():
    print("/predict endpoint called")
    uid = get_local_uid()
    data = request.json
    print(f"Request data: {data}")
    if not data or 'text' not in data or 'type' not in data:
        print("Missing required fields in request data")
        return jsonify({"error": "Missing required fields: 'text' and 'type'"}), 400
    input_text = data['text']
    input_type = data['type']  # 'email', 'sms', or 'url'
    print(f"Input text: {input_text}, Input type: {input_type}")
    processed_text = preprocess_text(input_text)
    print(f"Processed text: {processed_text}")
    heuristics = extract_features(input_text)
    print(f"Heuristics: {heuristics}")
    result = {
        "result": "Unknown",
        "confidence": 0.0,
        "heuristics": heuristics,
        "input": input_text,
        "input_type": input_type,
        "email": data.get('email', ''),
        "subject": data.get('subject', '')
    }
    if model:
        try:
            print("Model loaded, running prediction...")
            prediction = model.predict([processed_text])[0]
            print(f"Prediction: {prediction}")
            proba = model.predict_proba([processed_text])[0]
            print(f"Probabilities: {proba}")
            result['result'] = "Phishing" if prediction == 1 else "Legitimate"
            result['confidence'] = float(max(proba))
            suspicious_words_found = [word for word in ['urgent', 'verify', 'login'] if word in input_text.lower()]
            result['suspicious_words'] = suspicious_words_found
        except Exception as e:
            print(f"Prediction failed: {e}")
            return jsonify({"error": f"Prediction failed: {e}"}), 500
    else:
        print("Model not loaded")
        return jsonify({"error": "Model not loaded"}), 503
    # Save to history
    print("Saving scan to history...")
    add_scan_to_history(result, uid)
    print("Returning result to client.")
    return jsonify(result)



@app.route('/history', methods=['GET'])
def get_history():
    uid = get_local_uid()
    return jsonify(load_history(uid))



@app.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    uid = get_local_uid()
    return jsonify(get_dashboard_stats(uid))


# Serve React frontend (index.html) for all non-API routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path.startswith(('api', 'predict', 'history', 'dashboard_stats', 'health')):

import os
import json
from dotenv import load_dotenv
load_dotenv()
from threading import Thread
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import preprocess_text
import fast_url_detector
import fast_email_detector
import history_utils

app = Flask(__name__)
CORS(app)

# Use fast logistic regression for email/SMS
email_model_instance = fast_email_detector.FastEmailPhishingDetector()
url_model_instance = fast_url_detector.FastURLPhishingDetector()

        return jsonify({'error': 'Not found'}), 404
    file_path = os.path.join(FRONTEND_DIST, path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):

@app.route('/predict', methods=['POST'])
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, 'index.html')

if __name__ == '__main__':
    app.run(port=5000)
=======
from firebase_admin import credentials
from flask import Flask, request, jsonify
from firebase_admin import auth as firebase_auth
import history_utils
from flask_cors import CORS
from utils import preprocess_text

import fast_url_detector
import fast_email_detector

# Use GOOGLE_CREDENTIALS_JSON environment variable for credentials (Render best practice)
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
if not creds_json:
    raise RuntimeError("GOOGLE_CREDENTIALS_JSON environment variable is not set. Please add your serviceAccountKey.json contents as an environment variable in Render.")
cred = credentials.Certificate(json.loads(creds_json))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://phish-guard-94030-default-rtdb.europe-west1.firebasedatabase.app'
})

app = Flask(__name__)
CORS(app)


# Use fast logistic regression for email/SMS
email_model_instance = fast_email_detector.FastEmailPhishingDetector()

url_model_instance = fast_url_detector.FastURLPhishingDetector()
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text')
    input_type = data.get('type')
    uid = get_uid_from_request()
    if not text or not input_type:
        return jsonify({'error': 'Missing text or type'}), 400


    import traceback
    # Email prediction
    if input_type == 'email':
        try:
            result, confidence = email_model_instance.predict(text)
        except Exception as e:
            print('EMAIL MODEL ERROR:', str(e))
            traceback.print_exc()
            return jsonify({'error': f'Email model not loaded: {str(e)}'}), 500
        scan = {
            'input_type': 'email',
            'subject': text[:50],
            'email': '',
            'result': result,
            'confidence': float(confidence),

@app.route("/", methods=["GET"])
        }
    # SMS prediction (use fast email model)

@app.route('/history', methods=['GET'])
    elif input_type == 'sms':
        try:
            result, confidence = email_model_instance.predict(text)

@app.route('/dashboard_stats', methods=['GET'])
        except Exception as e:
            print('SMS MODEL ERROR:', str(e))
            traceback.print_exc()
            return jsonify({'error': f'SMS model not loaded: {str(e)}'}), 500
        scan = {
            'input_type': 'sms',
            'input': text[:50],
            'result': result,
            'confidence': float(confidence),
        }
    # URL prediction
    elif input_type == 'url':
        try:
            result, confidence = url_model_instance.predict(text)
        except Exception as e:
            print('URL MODEL ERROR:', str(e))
            traceback.print_exc()
            return jsonify({'error': f'URL model not loaded: {str(e)}'}), 500
        scan = {
            'input_type': 'url',
            'input': text,
            'result': result,
            'confidence': float(confidence),
        }
    else:
        print('INVALID TYPE:', input_type)
        return jsonify({'error': 'Invalid type'}), 400

    # Save scan to history if user is authenticated
    if uid:
        history_utils.add_scan_to_history(scan, uid)

    return jsonify(scan)

@app.route("/")
def index():
    return "PhishGuard backend is running!"

def get_uid_from_request():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    id_token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token['uid']
    except Exception:
        return None

@app.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    uid = get_uid_from_request()
    if not uid:
        return jsonify({'error': 'Unauthorized'}), 401
    stats = history_utils.get_dashboard_stats(uid)
    return jsonify(stats)

@app.route('/history', methods=['GET'])
def history():
    uid = get_uid_from_request()
    if not uid:
        return jsonify({'error': 'Unauthorized'}), 401
    history = history_utils.load_history(uid)
    return jsonify(history)
>>>>>>> cbbd4905 (Fix: ensure os import at top of app.py, backend/frontend run scripts)
