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
    # Expanded heuristics
    suspicious_keywords = ['urgent', 'verify', 'account', 'security', 'suspended', 'click here', 'password', 'login', 'bank', 'update', 'confirm', 'free', 'win', 'prize', 'alert', 'risk', 'unauthorized', 'limited', 'expire', 'reset', 'invoice', 'payment', 'refund', 'access', 'locked', 'breach']

    features = {
        'url_count': len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)),
        'suspicious_keyword_count': sum(1 for word in suspicious_keywords if word in text.lower()),
        'email_count': len(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)),
        'digit_count': sum(c.isdigit() for c in text),
        'length': len(text),
        'exclamation_count': text.count('!'),
        'question_count': text.count('?'),
        'uppercase_word_count': sum(1 for w in text.split() if w.isupper()),
        'word_count': len(text.split()),
        'contains_attachment': int('attachment' in text.lower()),
        'contains_html': int('<html>' in text.lower() or '</html>' in text.lower()),
        'contains_login_link': int('login' in text.lower() and 'http' in text.lower()),
        'contains_reset_link': int('reset' in text.lower() and 'http' in text.lower()),
        'contains_bank_link': int('bank' in text.lower() and 'http' in text.lower()),
    }
    return features
