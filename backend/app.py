import os
from dotenv import load_dotenv

load_dotenv()

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

# Demo mode: set DEMO_MODE=true in environment to enable unauthenticated local history.
# Do NOT enable in production without proper authentication.
DEMO_MODE = os.environ.get('DEMO_MODE', 'false').lower() == 'true'

# Load model (lazy loading or on startup)
MODEL_PATH = os.path.join(BASE_DIR, 'phishing_model.pkl')
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            app.logger.info("Model loaded successfully.")
        except Exception as e:
            app.logger.error("Error loading model: %s", e)
            model = None
    else:
        app.logger.warning("Model file not found. Please train the model first.")

load_model()

def get_local_uid():
    """Return a fixed UID for demo/dev mode. Only enabled when DEMO_MODE=true."""
    if not DEMO_MODE:
        raise RuntimeError("get_local_uid() called outside of demo mode. Set DEMO_MODE=true (case-insensitive) to enable.")
    return "demo_user"

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})




@app.route('/predict', methods=['POST'])
def predict():
    app.logger.debug("/predict endpoint called")
    uid = get_local_uid()
    data = request.json
    if not data or 'text' not in data or 'type' not in data:
        app.logger.warning("Missing required fields in request data")
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
            app.logger.error("Prediction failed: %s", e)
            return jsonify({"error": f"Prediction failed: {e}"}), 500
    else:
        app.logger.error("Model not loaded")
        return jsonify({"error": "Model not loaded"}), 503
    # Save to history
    add_scan_to_history(result, uid)
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
        return jsonify({'error': 'Not found'}), 404
    file_path = os.path.join(FRONTEND_DIST, path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, 'index.html')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
