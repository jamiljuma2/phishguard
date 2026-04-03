
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

def get_local_uid():
    """Stub for user identification (no auth). Returns a fixed UID for demo purposes."""
    return "demo_user"

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})
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
    # Heuristics and model logic can be added here if needed
    result = {
        "result": "Unknown",
        "confidence": 0.0,
        "input": input_text,
        "input_type": input_type,
        "email": data.get('email', ''),
        "subject": data.get('subject', '')
    }
    # Save to history (stub)
    print("Returning result to client.")
    return jsonify(result)



@app.route('/history', methods=['GET'])
def history():
    uid = get_local_uid()
    # Return empty history for now (stub)
    return jsonify([])



@app.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    uid = get_local_uid()
    # Return empty stats for now (stub)
    return jsonify({"total_scans": 0, "phishing_email": 0, "phishing_sms": 0, "phishing_url": 0, "legitimate_email": 0, "legitimate_sms": 0, "legitimate_url": 0, "recent": []})



