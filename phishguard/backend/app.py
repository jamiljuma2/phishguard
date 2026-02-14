from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
from utils import preprocess_text, extract_features
from history_utils import load_history, add_scan_to_history, get_dashboard_stats

app = Flask(__name__)
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
    data = request.json
    if not data or 'email_text' not in data:
        return jsonify({"error": "No email text provided"}), 400
    email_text = data['email_text']
    processed_text = preprocess_text(email_text)
    heuristics = extract_features(email_text)
    result = {"result": "Unknown", "confidence": 0.0, "heuristics": heuristics, "email": data.get('email', ''), "subject": data.get('subject', '')}
    if model:
        try:
            prediction = model.predict([processed_text])[0]
            proba = model.predict_proba([processed_text])[0]
            result['result'] = "Phishing" if prediction == 1 else "Legitimate"
            result['confidence'] = float(max(proba))
            suspicious_words_found = [word for word in ['urgent', 'verify', 'login'] if word in email_text.lower()]
            result['suspicious_words'] = suspicious_words_found
        except Exception as e:
            return jsonify({"error": f"Prediction failed: {e}"}), 500
    else:
        return jsonify({"error": "Model not loaded"}), 503
    # Save to history
    add_scan_to_history(result)
    return jsonify(result)


@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(load_history())


@app.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    return jsonify(get_dashboard_stats())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
