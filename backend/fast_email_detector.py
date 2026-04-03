import joblib
from utils import extract_features, preprocess_text
import numpy as np

class FastEmailPhishingDetector:
    def __init__(self, model_path='phishing_email_logreg.pkl'):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        import os
        try:
            if not os.path.exists(self.model_path):
                print(f"[ERROR] Model file not found: {self.model_path}")
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            self.model = joblib.load(self.model_path)
            print(f"[INFO] Loaded model from {self.model_path}")
        except Exception as e:
            print(f"[ERROR] Failed to load model from {self.model_path}: {e}")
            raise

    def predict(self, text):
        features = extract_features(preprocess_text(text))
        X = np.array([list(features.values())])
        pred = self.model.predict(X)[0]
        proba = self.model.predict_proba(X)[0][pred]
        return ('Phishing' if pred == 1 else 'Legitimate', float(proba))
