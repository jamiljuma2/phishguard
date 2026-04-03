import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os
from utils import extract_features

def load_url_data():
    dataset_path = 'dataset/phishing_urls.csv'
    df = pd.read_csv(dataset_path)
    # Use only features, not text
    X = df['url'].astype(str).apply(extract_features).apply(pd.Series)
    y = df['label']
    return X, y

def train_logistic_model():
    X, y = load_url_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f'Logistic Regression accuracy: {acc:.4f}')
    joblib.dump(model, 'phishing_url_logreg.pkl')
    print('Model saved to phishing_url_logreg.pkl')

if __name__ == '__main__':
    train_logistic_model()
