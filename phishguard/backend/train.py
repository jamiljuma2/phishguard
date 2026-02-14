import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from utils import preprocess_text

# Mock Dataset if no file exists
def create_mock_dataset():
    data = {
        'text': [
            "Urgent: Verify your account now at http://fake-bank.com",
            "Dear user, your account has been suspended. Click here to login.",
            "Win a free iPhone! Claim your prize now.",
            "Meeting reminder for tomorrow at 10 AM.",
            "Project update: tasks completed successfully.",
            "Hey, let's grab lunch later today?",
            "Security Alert: Unusual login attempt detected.",
            "Please reset your password immediately.",
            "Attached is the invoice for your recent purchase."
        ],
        'label': [1, 1, 1, 0, 0, 0, 1, 1, 0]  # 1 = Phishing, 0 = Legitimate
    }
    df = pd.DataFrame(data)
    os.makedirs('dataset', exist_ok=True)
    df.to_csv('dataset/phishing_emails.csv', index=False)
    print("Mock dataset created.")
    return df

def train_model():
    dataset_path = 'dataset/phishing_emails.csv'
    if not os.path.exists(dataset_path):
        df = create_mock_dataset()
    else:
        df = pd.read_csv(dataset_path)

    # Preprocessing
    print("Preprocessing data...")
    df['text'] = df['text'].astype(str).apply(preprocess_text)
    
    X = df['text']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Pipeline: TF-IDF -> Naive Bayes
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    print("Evaluating model...")
    predictions = pipeline.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, predictions)}")
    print(classification_report(y_test, predictions))
    
    # Save model
    joblib.dump(pipeline, 'phishing_model.pkl')
    print("Model saved to phishing_model.pkl")

if __name__ == '__main__':
    train_model()
