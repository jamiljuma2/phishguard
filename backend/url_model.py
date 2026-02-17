"""
Random Forest model for URL-specific phishing detection

Why Random Forest?
- Handles diverse features: URL length, subdomains, special characters
- Reduces overfitting: Ensemble of decision trees for robustness  
- Feature importance: Shows which URL characteristics indicate phishing
"""
import joblib
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from urllib.parse import urlparse
import re
from utils import extract_url_features

class URLPhishingClassifier:
    def __init__(self, model_path='phishing_url_model.pkl', feature_names_path='url_feature_names.pkl'):
        self.model_path = os.path.join(os.path.dirname(__file__), model_path)
        self.feature_names_path = os.path.join(os.path.dirname(__file__), feature_names_path)
        self.model = None
        self.feature_names = None

    def load_model(self):
        """Loads model if exists, otherwise returns None"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                # Load feature names if available
                if os.path.exists(self.feature_names_path):
                    self.feature_names = joblib.load(self.feature_names_path)
                return True
            except Exception as e:
                print(f"Error loading URL model: {e}")
        return False

    def extract_advanced_features(self, url):
        """
        Extracts comprehensive features from a URL
        
        Features analyzed:
        - Lexical: URL length, digit-to-letter ratio, special characters
        - Anatomy: @ symbols, subdomains, path depth, port numbers
        - Domain: IP addresses, suspicious TLDs (high-risk domains)
        
        Args:
            url: URL string to analyze
            
        Returns:
            Dictionary of features
        """
        # Get basic features from utils.py
        features = extract_url_features(url)
        
        # Parse URL components
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            path = parsed_url.path
        except:
            # If URL parsing fails, return basic features with defaults
            features.update({
                'digit_letter_ratio': 0,
                'has_at_symbol': 0,
                'has_double_slash_redirect': 0,
                'num_underscores': 0,
                'num_percent': 0,
                'num_ampersand': 0,
                'suspicious_tld': 0,
                'fake_domain_pattern': 0,
                'suspicious_port': 0,
                'has_suspicious_keywords': 0,
                'entropy': 0
            })
            return features
        
        # Additional Lexical Features
        alpha_count = sum(c.isalpha() for c in url)
        features['digit_letter_ratio'] = features['num_digits'] / max(1, alpha_count)
        features['has_at_symbol'] = 1 if '@' in url else 0
        features['has_double_slash_redirect'] = 1 if url.count('//') > 1 else 0
        features['num_underscores'] = url.count('_')
        features['num_percent'] = url.count('%')
        features['num_ampersand'] = url.count('&')
        
        # Domain Features - Suspicious TLDs (high-risk extensions)
        suspicious_tlds = [
            '.xyz', '.tk', '.ml', '.ga', '.cf', '.gq', '.pw', '.cc',
            '.top', '.work', '.click', '.link', '.stream', '.download'
        ]
        features['suspicious_tld'] = 1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 0
        
        # Check for fake/misspelled domains (typosquatting)
        fake_patterns = ['paypa1', 'g00gle', 'amaz0n', 'micros0ft', 'netfl1x', 'facebok']
        features['fake_domain_pattern'] = 1 if any(p in domain.lower() for p in fake_patterns) else 0
        
        # Port analysis
        if ':' in domain and not domain.startswith('['):
            try:
                port = int(domain.split(':')[-1])
                features['suspicious_port'] = 1 if port not in [80, 443, 8080] else 0
            except:
                features['suspicious_port'] = 0
        else:
            features['suspicious_port'] = 0
        
        # Suspicious keywords in URL
        suspicious_keywords = ['login', 'signin', 'verify', 'secure', 'update', 'confirm', 'password', 'suspended', 'urgent']
        features['has_suspicious_keywords'] = sum(1 for kw in suspicious_keywords if kw in url.lower())
        
        # Calculate Shannon entropy (randomness measure - phishing URLs often more random)
        features['entropy'] = self._calculate_entropy(url)
        
        return features
    
    def _calculate_entropy(self, url):
        """Calculate Shannon entropy of URL string"""
        if not url:
            return 0
        char_counts = {}
        for char in url:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        entropy = 0
        url_len = len(url)
        for count in char_counts.values():
            probability = count / url_len
            entropy -= probability * np.log2(probability)
        return entropy

    def prepare_data(self, urls, labels=None):
        """
        Processes raw URLs into structured features for machine learning
        
        Args:
            urls: List of URL strings
            labels: Optional labels (for training)
            
        Returns:
            DataFrame with extracted features
        """
        features_list = []
        for url in urls:
            try:
                features = self.extract_advanced_features(url)
                features_list.append(features)
            except Exception as e:
                print(f"Error processing URL {url[:50]}...: {e}")
                features_list.append({})
        
        df = pd.DataFrame(features_list)
        
        # Store feature names on first preparation
        if self.feature_names is None and len(df.columns) > 0:
            self.feature_names = list(df.columns)
        
        # Ensure consistency with stored feature names
        if self.feature_names is not None:
            for feature in self.feature_names:
                if feature not in df.columns:
                    df[feature] = 0
            df = df[self.feature_names]
        
        return df


    def train(self, dataset_path='dataset/phishing_urls.csv'):
        """
        Trains Random Forest model on extracted URL features
        
        Random Forest advantages:
        - Handles non-linear patterns in URL features
        - Robust against overfitting via ensemble approach
        - Provides feature importance rankings
        
        Args:
            dataset_path: Path to CSV with 'url' and 'label' columns
            
        Returns:
            Accuracy score
        """
        full_path = os.path.join(os.path.dirname(__file__), dataset_path)
        if not os.path.exists(full_path):
            print(f"Dataset not found: {full_path}")
            return None
            
        df = pd.read_csv(full_path)
        print(f"Loaded {len(df)} URLs from dataset")
        print(f"Phishing URLs: {sum(df['label'] == 1)}")
        print(f"Legitimate URLs: {sum(df['label'] == 0)}")
        
        X = self.prepare_data(df['url'], df['label'])
        y = df['label']
        
        # Train-test split (80/20) with stratification
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nTraining set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Number of features: {len(self.feature_names)}")
        
        # Initialize Random Forest Classifier
        # n_estimators=100: Use 100 decision trees (good balance of performance/accuracy)
        # max_depth=20: Limit tree depth to prevent overfitting
        # n_jobs=-1: Use all CPU cores for faster training
        self.model = RandomForestClassifier(
            n_estimators=100, 
            max_depth=20, 
            random_state=42,
            n_jobs=-1
        )
        
        print("\nTraining Random Forest model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{'='*60}")
        print("Training Complete!")
        print(f"{'='*60}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
        print(f"\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature Importance Analysis
        print(f"\n{'='*60}")
        print("Top 10 Most Important Features:")
        print(f"{'='*60}")
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in feature_importance.head(10).iterrows():
            print(f"{row['feature']:30s}: {row['importance']:.4f}")
        
        # Save model and feature names
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.feature_names, self.feature_names_path)
        print(f"\nModel saved to {self.model_path}")
        print(f"Feature names saved to {self.feature_names_path}")
        
        return accuracy


    def predict(self, url):
        """
        Predicts risk for a single URL using the trained Random Forest model
        
        Args:
            url: URL string to analyze
            
        Returns:
            Tuple of (result_string, confidence_score)
        """
        if self.model is None and not self.load_model():
            return None, 0.0
            
        features = self.extract_advanced_features(url)
        features_df = pd.DataFrame([features])
        
        # Ensure feature consistency
        if self.feature_names is not None:
            for feature in self.feature_names:
                if feature not in features_df.columns:
                    features_df[feature] = 0
            features_df = features_df[self.feature_names]
        
        prediction = self.model.predict(features_df)[0]
        confidence = self.model.predict_proba(features_df)[0][prediction]
        
        result = "Phishing" if prediction == 1 else "Legitimate"
        return result, float(confidence)
    
    def predict_with_details(self, url):
        """
        Predicts URL risk with detailed analysis and risk factors
        
        Returns:
            Dictionary with prediction, confidence, probabilities, and risk factors
        """
        if self.model is None and not self.load_model():
            return {
                'url': url,
                'prediction': 'Unknown',
                'confidence': 0.0,
                'error': 'Model not loaded'
            }
        
        features = self.extract_advanced_features(url)
        features_df = pd.DataFrame([features])
        
        # Ensure feature consistency
        if self.feature_names is not None:
            for feature in self.feature_names:
                if feature not in features_df.columns:
                    features_df[feature] = 0
            features_df = features_df[self.feature_names]
        
        prediction = self.model.predict(features_df)[0]
        proba = self.model.predict_proba(features_df)[0]
        
        # Identify risk factors based on feature values
        risk_factors = []
        if features.get('has_ip', 0):
            risk_factors.append("Uses IP address instead of domain name")
        if features.get('suspicious_tld', 0):
            risk_factors.append("Suspicious top-level domain (.xyz, .tk, etc.)")
        if features.get('fake_domain_pattern', 0):
            risk_factors.append("Potential domain typosquatting detected")
        if features.get('has_at_symbol', 0):
            risk_factors.append("Contains @ symbol (URL obfuscation)")
        if features.get('url_length', 0) > 100:
            risk_factors.append(f"Unusually long URL ({features['url_length']} characters)")
        if features.get('has_suspicious_keywords', 0) > 2:
            risk_factors.append(f"Multiple suspicious keywords ({features['has_suspicious_keywords']})")
        if features.get('num_subdomains', 0) > 3:
            risk_factors.append(f"Excessive subdomains ({features['num_subdomains']})")
        if features.get('suspicious_port', 0):
            risk_factors.append("Non-standard port number")
        if features.get('has_double_slash_redirect', 0):
            risk_factors.append("Double slash redirect detected")
        if features.get('entropy', 0) > 4.5:
            risk_factors.append("High randomness in URL structure")
        
        return {
            'url': url,
            'prediction': 'phishing' if prediction == 1 else 'legitimate',
            'confidence': float(proba[prediction]),
            'phishing_probability': float(proba[1]),
            'legitimate_probability': float(proba[0]),
            'risk_factors': risk_factors,
            'feature_count': len(features)
        }

# Singleton instance for global backend usage
url_model_instance = URLPhishingClassifier()
