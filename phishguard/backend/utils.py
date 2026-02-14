import re

def preprocess_text(text):
    """
    Cleans and preprocesses email text.
    1. Lowercase
    2. Remove special characters/numbers
    3. Tokenize (simple split)
    """
    if not text:
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove special characters and numbers (keep letters and spaces)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # 3. Simple Tokenization (split by whitespace)
    tokens = text.split()
    
    # (Optional) Simple stopword removal list if needed, but skipping for now to be safe
    
    return " ".join(tokens)

def extract_features(text):
    """
    Extracts manual features for heuristic analysis.
    Returns a dictionary of features.
    """
    # Simple heuristics
    suspicious_keywords = ['urgent', 'verify', 'account', 'security', 'suspended', 'click here', 'password', 'login']
    
    features = {
        'url_count': len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)),
        'suspicious_keyword_count': sum(1 for word in suspicious_keywords if word in text.lower())
    }
    
    return features
