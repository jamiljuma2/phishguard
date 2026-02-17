# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import joblib
from utils import preprocess_text, extract_features, extract_url_features
from history_utils import load_history, add_scan_to_history, get_dashboard_stats
from url_model import url_model_instance

import pathlib
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend', 'dist'))
app = Flask(__name__, static_folder=FRONTEND_DIST, static_url_path='')
CORS(app)  # Enable CORS for all routes


# Load models (lazy loading or on startup)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'phishing_model.pkl')
model = None

def load_models():
    global model
    # Load Email Model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print("Email model loaded successfully.")
        except Exception as e:
            print(f"Error loading email model: {e}")
            model = None
    
    # Load URL Model
    if url_model_instance.load_model():
        print("URL model loaded successfully.")
    else:
        print("URL model file not found. Please train first.")

load_models()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "email_model_loaded": model is not None,
        "url_model_loaded": url_model_instance.model is not None
    })



@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not data or 'text' not in data or 'type' not in data:
        return jsonify({"error": "Missing required fields: 'text' and 'type'"}), 400
    
    input_text = data['text']
    input_type = data['type']  # 'email', 'sms', or 'url'
    
    heuristics = extract_features(input_text)
    
    result = {
        "result": "Unknown",
        "confidence": 0.0,
        "heuristics": heuristics,
        "input": input_text,
        "input_type": input_type,
        "email": data.get('email', ''),
        "subject": data.get('subject', ''),
        "suspicious_words": []
    }

    try:
        if input_type == 'url':
            # Use specialized URL Random Forest model
            pred, conf = url_model_instance.predict(input_text)
            if pred:
                result['result'] = pred
                result['confidence'] = conf
                # Add lexical features for URLs as extra context
                result['url_features'] = extract_url_features(input_text)
        else:
            # Use text model (Email/SMS)
            if model:
                processed_text = preprocess_text(input_text)
                prediction = model.predict([processed_text])[0]
                proba = model.predict_proba([processed_text])[0]
                result['result'] = "Phishing" if prediction == 1 else "Legitimate"
                result['confidence'] = float(max(proba))
                result['suspicious_words'] = [word for word in ['urgent', 'verify', 'login'] if word in input_text.lower()]
            else:
                return jsonify({"error": "Email model not loaded"}), 503
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {e}"}), 500

    # Save to history
    add_scan_to_history(result)
    return jsonify(result)


@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(load_history())


@app.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    return jsonify(get_dashboard_stats())


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
    app.run(port=5000)
