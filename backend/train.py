import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from utils import preprocess_text
from url_model import url_model_instance
from extract_urls import create_url_dataset

# Mock Dataset if no file exists
def create_mock_dataset():
    data = {
        'text': [
            "Urgent: Verify your account now at http://fake-bank.com/secure/login",
            "Dear user, your account has been suspended. Click here to login.",
            "Win a free iPhone! Claim your prize now.",
            "Meeting reminder for tomorrow at 10 AM.",
            "Project update: tasks completed successfully.",
            "Hey, let's grab lunch later today?",
            "Security Alert: Unusual login attempt detected.",
            "Please reset your password immediately at http://malicious-reset-password.com/urgent/update",
            "Attached is the invoice for your recent purchase at https://amazon.com/account/settings",
            "Urgent! Please update your payment info at http://g00gle-login.tk/signin-now",
            "Meeting check-in for the team sync.",
            "Your order has shipped from https://www.legitimate-bank.com",
            "URGENT: Your PayPal account has been limited. Verify now at http://paypa1-secure.xyz/verify",
            "Congratulations! You have won $1,000,000. Click here to claim your prize immediately.",
            "Your Netflix subscription is about to expire. Update payment at http://netfl1x-billing.top/update",
            "Hi team, please review the Q4 report attached. Thanks!",
            "Reminder: dentist appointment tomorrow at 3 PM.",
            "Your Amazon order #12345 has been delivered. Track at https://amazon.com/orders",
            "ALERT: Suspicious activity on your bank account. Confirm identity at http://secure-wells-farg0.work/signin",
            "Hey, are you coming to the party this weekend?",
            "Your Apple ID has been locked for security reasons. Verify at http://apple-id-suspended.download/verify",
            "The quarterly budget meeting is rescheduled to next Wednesday.",
            "Dear customer, your account password expires today. Reset at http://micros0ft-support.pw/reset",
            "Thanks for your purchase! Your receipt is attached.",
            "IMPORTANT: Verify your email address to continue using your account http://facebok-security.cc/confirm",
            "Can you send me the slides from yesterday's presentation?",
            "Your LinkedIn account may have been compromised. Secure it now at http://linkedin-security-alert.cf/signin",
            "Don't forget to submit your timesheet by Friday.",
            "WARNING: Unauthorized login attempt detected on your account. Change password now!",
            "Happy birthday! Hope you have a great day!",
        ],
        'label': [1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    os.makedirs('dataset', exist_ok=True)
    df.to_csv('dataset/phishing_emails.csv', index=False)
    print("Email Mock dataset created.")
    return df

def train_email_model():
    print("\n--- Training Email/Text Model ---")
    dataset_path = 'dataset/phishing_emails.csv'
    if not os.path.exists(dataset_path):
        df = create_mock_dataset()
    else:
        df = pd.read_csv(dataset_path)

    # Preprocessing
    print("Preprocessing text data...")
    df['text'] = df['text'].astype(str).apply(preprocess_text)
    
    X = df['text']
    y = df['label']
    
    # Simple split (if data is small, split might be very tiny)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Pipeline: TF-IDF -> Naive Bayes
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])
    
    print("Fitting text classifier...")
    pipeline.fit(X_train, y_train)
    
    print("Evaluating text model...")
    # Add defensive check for test set size
    if len(X_test) > 0:
        predictions = pipeline.predict(X_test)
        print(f"Text Model Accuracy: {accuracy_score(y_test, predictions):.2f}")
    
    # Save model
    joblib.dump(pipeline, 'phishing_model.pkl')
    print("Text model saved to phishing_model.pkl")

def train_url_model():
    """
    Train URL-Specific Model using Random Forest
    
    Why Random Forest for URLs?
    - Handles diverse features: URL length, subdomains, special characters
    - Reduces overfitting: Ensemble of decision trees for robustness
    - Feature importance: Shows which URL characteristics indicate phishing
    """
    print("\n" + "="*60)
    print("Training URL-Specific Model (Random Forest)")
    print("="*60)
    
    # First, refresh URL dataset from email data
    print("\nExtracting URLs from email dataset...")
    create_url_dataset()
    
    # Then train using the URL model class
    print("\nTraining Random Forest classifier...")
    url_model_instance.train()
    
    # Demo predictions
    print("\n" + "="*60)
    print("Testing URL Model with Sample URLs")
    print("="*60)
    
    test_urls = [
        "https://www.paypal.com/signin",
        "http://paypa1-secure.xyz/verify-account",
        "https://192.168.1.1/admin",
        "https://www.google.com/search",
        "http://amaz0n-update-billing.tk/urgent/click-now",
        "https://www.microsoft.com/en-us/",
        "http://g00gle-login.ml/signin?redirect=hack"
    ]
    
    for url in test_urls:
        result = url_model_instance.predict_with_details(url)
        print(f"\nURL: {result['url'][:60]}")
        print(f"Prediction: {result['prediction'].upper()}")
        print(f"Confidence: {result['confidence']:.2%}")
        if result.get('risk_factors'):
            print("Risk Factors:")
            for factor in result['risk_factors'][:3]:  # Show top 3
                print(f"  - {factor}")

if __name__ == '__main__':
    print("="*60)
    print("PhishGuard Model Training Suite")
    print("="*60)
    print("\nTraining 2 models:")
    print("1. Email/Text Model (Naive Bayes)")
    print("2. URL Model (Random Forest)")
    print("="*60)
    
    train_email_model()
    train_url_model()
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    print("\nModels saved:")
    print("  - phishing_model.pkl (Email/Text Classification)")
    print("  - phishing_url_model.pkl (URL Classification)")
    print("  - url_feature_names.pkl (Feature metadata)")

