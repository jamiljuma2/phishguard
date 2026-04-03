
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
    print("/predict endpoint called")
    uid = get_local_uid()

# Entrypoint for local development (must be at end of file)
if __name__ == '__main__':
    print("Starting Flask backend on http://0.0.0.0:5000 ...")
    app.run(debug=True, host='0.0.0.0', port=5000)

# Entrypoint for local development (must be at end of file)
if __name__ == '__main__':
    print("Starting Flask backend on http://0.0.0.0:5000 ...")
    app.run(debug=True, host='0.0.0.0', port=5000)



