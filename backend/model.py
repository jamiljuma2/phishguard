import joblib
import os

MODEL_PATH = 'phishing_model.pkl'

class PhishingModel:
    def __init__(self):
        self.model = None
        self.load()

    def load(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            return True
        return False

    def predict(self, text):
        if not self.model:
            return None
        return self.model.predict([text])[0]

    def predict_proba(self, text):
        if not self.model:
            return None
        return self.model.predict_proba([text])[0]
