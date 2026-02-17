import re
from urllib.parse import urlparse

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

def analyze_url_risk(text):
    """
    Analyzes URLs in text for suspicious patterns.
    Returns risk score and patterns found.
    """
    urls = re.findall(r'http[s]?://[^\s]+', text)
    risk_score = 0
    suspicious_patterns = []
    
    for url in urls:
        domain = urlparse(url).netloc
        
        # 1. Check for suspicious domain extensions
        suspicious_tlds = ['.xyz', '.tk', '.ml', '.ga', '.cf', '.gq']
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            risk_score += 3
            suspicious_patterns.append(f"Suspicious domain: {domain}")
        
        # 2. Check if using IP address instead of domain name
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
            risk_score += 5
            suspicious_patterns.append(f"IP address used: {domain}")
        
        # 3. Check for misspelled popular domains
        fake_domains = ['paypa1', 'g00gle', 'amaz0n', 'micros0ft', 'netfl1x']
        if any(fake in domain.lower() for fake in fake_domains):
            risk_score += 10
            suspicious_patterns.append(f"Fake domain detected: {domain}")
        
        # 4. Check for overly long URLs
        if len(url) > 100:
            risk_score += 2
            suspicious_patterns.append("Unusually long URL")
        
        # 5. Check for @ symbol in URL
        if '@' in url:
            risk_score += 8
            suspicious_patterns.append("@ symbol in URL (suspicious)")
    
    return {
        'url_count': len(urls),
        'url_risk_score': risk_score,
        'suspicious_patterns': suspicious_patterns
    }

def extract_url_features(url):
    """
    Extracts lexical features from a single URL for machine learning.
    Returns a dictionary of features.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    
    features = {
        'url_length': len(url),
        'domain_length': len(domain),
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'num_subdomains': domain.count('.'),
        'num_queries': url.count('?'),
        'is_https': 1 if parsed_url.scheme == 'https' else 0,
        'has_ip': 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain) else 0,
        'num_digits': sum(c.isdigit() for c in url),
        'special_chars_count': sum(1 for c in url if not c.isalnum() and c not in ['/', ':', '.', '-', '_', '?']),
        'num_params': len(parsed_url.query.split('&')) if parsed_url.query else 0,
        'path_depth': path.count('/') if path else 0
    }
    
    return features

def extract_features(text):
    """
    Extracts manual features for heuristic analysis.
    Returns a dictionary of features.
    """
    suspicious_keywords = ['urgent', 'verify', 'account', 'security', 'suspended', 'click here', 'password', 'login', 'confirm', 'update', 'expire', 'limited time']
    
    # Get URL analysis
    url_analysis = analyze_url_risk(text)
    
    features = {
        'url_count': url_analysis['url_count'],
        'url_risk_score': url_analysis['url_risk_score'],
        'suspicious_patterns': url_analysis['suspicious_patterns'],
        'suspicious_keyword_count': sum(1 for word in suspicious_keywords if word in text.lower())
    }
    
    return features
