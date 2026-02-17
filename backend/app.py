import os
import json
from dotenv import load_dotenv

load_dotenv()

import firebase_admin
from firebase_admin import credentials, db, auth
from threading import Thread

# Support both JSON env var (for Render/production) and file path (for local dev)

# Always use serviceAccountKey.json from the backend directory by default
service_account_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "serviceAccountKey.json")
cred = credentials.Certificate(service_account_path)

firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ.get("FIREBASE_DATABASE_URL")
})

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
from utils import preprocess_text, extract_features
from history_utils import load_history, add_scan_to_history, get_dashboard_stats
from email_sending.sender import send_phishing_alert_email

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend', 'dist'))
app = Flask(__name__, static_folder=FRONTEND_DIST, static_url_path='')
CORS(app)  # Enable CORS for all routes


# Load model (lazy loading or on startup)
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

def verify_firebase_token():
    """Verify the Firebase ID token from the Authorization header."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split('Bearer ')[1]
    try:
        decoded = auth.verify_id_token(token)
        return decoded.get('uid')
    except Exception:
        return None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})



@app.route('/predict', methods=['POST'])
def predict():
    uid = verify_firebase_token()
    if not uid:
        return jsonify({"error": "Authentication required"}), 401
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
        "subject": data.get('subject', '')
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
    add_scan_to_history(result, uid)
    return jsonify(result)


@app.route('/history', methods=['GET'])
def get_history():
    uid = verify_firebase_token()
    if not uid:
        return jsonify({"error": "Authentication required"}), 401
    return jsonify(load_history(uid))


@app.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    uid = verify_firebase_token()
    if not uid:
        return jsonify({"error": "Authentication required"}), 401
    return jsonify(get_dashboard_stats(uid))


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

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
