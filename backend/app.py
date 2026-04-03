
import os
import json
from dotenv import load_dotenv
load_dotenv()
from threading import Thread
from flask import Flask, request, jsonify
from utils import preprocess_text
import fast_url_detector
import fast_email_detector
import history_utils
from flask_cors import CORS

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
    try:
        print("/predict endpoint called")
        uid = get_local_uid()
        data = request.json
        print(f"Request data: {data}")
        if not data or 'text' not in data or 'type' not in data:
            print("Missing required fields in request data")
            return jsonify({"error": "Missing required fields: 'text' and 'type'"}), 400

        input_text = data['text']
        input_type = data['type'].lower()  # 'email', 'sms', or 'url'
        print(f"Input text: {input_text}, Input type: {input_type}")
        processed_text = preprocess_text(input_text)
        print(f"Processed text: {processed_text}")

        # Select model and prediction logic
        if input_type == 'email' or input_type == 'sms':
            label, confidence = email_model_instance.predict(input_text)
        elif input_type == 'url':
            label, confidence = url_model_instance.predict(input_text)
        else:
            print(f"Unknown input type: {input_type}")
            return jsonify({"error": f"Unknown input type: {input_type}"}), 400

        result = {
            "result": label,
            "confidence": confidence,
            "input": input_text,
            "input_type": input_type,
            "email": data.get('email', ''),
            "subject": data.get('subject', '')
        }
        print("Returning result to client.")
        return jsonify(result)
    except Exception as e:
        import traceback
        print("Exception in /predict endpoint:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Dashboard stats endpoint for frontend
@app.route('/dashboard_stats', methods=['GET'])
def dashboard_stats():
    uid = get_local_uid()
    stats = history_utils.get_dashboard_stats(uid)
    return jsonify(stats)

# Entrypoint for local development (must be at end of file)
if __name__ == '__main__':
    print("Starting Flask backend on http://0.0.0.0:5000 ...")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)



