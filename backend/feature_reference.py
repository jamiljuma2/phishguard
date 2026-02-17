"""
Quick Reference: Random Forest URL Features
--------------------------------------------
This file documents all features extracted for Random Forest classification.
See utils.py:93 for suspicious TLD list reference.
"""

# ==============================================================================
# FEATURE CATEGORIES (25+ features total)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. LEXICAL FEATURES (Character-based analysis)
# ------------------------------------------------------------------------------
lexical_features = {
    'url_length': 'Total characters in URL',
    'domain_length': 'Length of domain portion',
    'num_digits': 'Count of numeric characters (0-9)',
    'digit_letter_ratio': 'Ratio of digits to letters (high = suspicious)',
    'num_dots': 'Period count (subdomain indicator)',
    'num_hyphens': 'Hyphen count in URL',
    'num_underscores': 'Underscore count',
    'num_percent': '% signs (URL encoding indicator)',
    'num_ampersand': '& signs (query parameter complexity)',
    'special_chars_count': 'Non-alphanumeric characters',
    'entropy': 'Shannon entropy (randomness: >4.5 suspicious)'
}

# ------------------------------------------------------------------------------
# 2. ANATOMICAL FEATURES (URL structure)
# ------------------------------------------------------------------------------
anatomical_features = {
    'num_subdomains': 'Subdomain nesting level (>3 suspicious)',
    'path_depth': 'Directory depth in path (/a/b/c = 3)',
    'num_queries': 'Query string count (?query)',
    'num_params': 'Individual parameter count (&key=value)',
    'has_at_symbol': 'Presence of @ (phishing obfuscation)',
    'has_double_slash_redirect': 'Multiple // beyond protocol',
    'has_port': 'Custom port specified',
    'suspicious_port': 'Port not in [80, 443, 8080]'
}

# ------------------------------------------------------------------------------
# 3. DOMAIN FEATURES (Domain-specific checks)
# ------------------------------------------------------------------------------
domain_features = {
    'is_https': 'Uses HTTPS protocol (0=HTTP, 1=HTTPS)',
    'has_ip': 'IP address instead of domain (CRITICAL)',
    'domain_has_digits': 'Digits in domain name',
    'domain_hyphen_count': 'Hyphens in domain',
    
    # High-risk TLDs (see utils.py:93)
    'suspicious_tld': '''
        High-risk top-level domains:
        .xyz, .tk, .ml, .ga, .cf, .gq, .pw, .cc,
        .top, .work, .click, .link, .stream, .download
    ''',
    
    # Typosquatting patterns
    'fake_domain_pattern': '''
        Common typosquatting:
        paypa1 (PayPal), g00gle (Google), amaz0n (Amazon),
        micros0ft (Microsoft), netfl1x (Netflix), facebok (Facebook)
    '''
}

# ------------------------------------------------------------------------------
# 4. CONTENT FEATURES (Keyword-based)
# ------------------------------------------------------------------------------
content_features = {
    'has_suspicious_keywords': '''
        Count of suspicious keywords:
        login, signin, verify, secure, update, confirm,
        password, suspended, urgent
    '''
}

# ==============================================================================
# FEATURE IMPORTANCE (Typical ranking after training)
# ==============================================================================

feature_importance_typical = """
Top 10 Most Important Features (example):
1. has_ip                    : 0.1523  ← IP address vs domain
2. suspicious_tld            : 0.1284  ← High-risk TLD
3. fake_domain_pattern       : 0.1156  ← Typosquatting
4. url_length               : 0.0892  ← Length anomaly
5. entropy                  : 0.0834  ← Randomness measure
6. has_suspicious_keywords   : 0.0765  ← Content keywords
7. num_subdomains           : 0.0698  ← Subdomain nesting
8. has_at_symbol            : 0.0645  ← URL obfuscation
9. domain_length            : 0.0589  ← Domain size
10. suspicious_port          : 0.0523  ← Non-standard port
"""

# ==============================================================================
# RISK THRESHOLDS
# ==============================================================================

risk_thresholds = {
    'url_length': {
        'safe': '< 75 characters',
        'suspicious': '75-120 characters',
        'dangerous': '> 120 characters'
    },
    'num_subdomains': {
        'safe': '0-2 subdomains',
        'suspicious': '3-4 subdomains',
        'dangerous': '> 4 subdomains'
    },
    'entropy': {
        'safe': '< 3.5 (regular patterns)',
        'suspicious': '3.5-4.5 (some randomness)',
        'dangerous': '> 4.5 (high randomness)'
    },
    'has_suspicious_keywords': {
        'safe': '0-1 keywords',
        'suspicious': '2-3 keywords',
        'dangerous': '> 3 keywords'
    }
}

# ==============================================================================
# EXAMPLE FEATURE EXTRACTION
# ==============================================================================

examples = {
    'legitimate': {
        'url': 'https://www.paypal.com/signin',
        'features': {
            'url_length': 32,
            'has_ip': 0,
            'suspicious_tld': 0,
            'fake_domain_pattern': 0,
            'has_at_symbol': 0,
            'entropy': 3.1,
            'num_subdomains': 1,
            'is_https': 1
        },
        'prediction': 'legitimate',
        'confidence': 0.98
    },
    
    'phishing': {
        'url': 'http://paypa1-secure.xyz/verify-account?user=admin@urgent',
        'features': {
            'url_length': 58,
            'has_ip': 0,
            'suspicious_tld': 1,      # .xyz
            'fake_domain_pattern': 1,  # paypa1
            'has_at_symbol': 1,        # @urgent
            'entropy': 4.2,
            'num_subdomains': 0,
            'is_https': 0,
            'has_suspicious_keywords': 2  # verify, urgent
        },
        'prediction': 'phishing',
        'confidence': 0.94,
        'risk_factors': [
            'Suspicious top-level domain (.xyz)',
            'Potential domain typosquatting detected',
            'Contains @ symbol (URL obfuscation)',
            'Multiple suspicious keywords (2)'
        ]
    }
}

# ==============================================================================
# MODEL PARAMETERS
# ==============================================================================

model_config = """
RandomForestClassifier(
    n_estimators=100,     # 100 decision trees
    max_depth=20,         # Max tree depth (prevents overfitting)
    random_state=42,      # Reproducibility
    n_jobs=-1,           # Use all CPU cores
    criterion='gini'     # Gini impurity for splits
)

Training Configuration:
- Train/Test Split: 80/20 (stratified)
- Cross-validation: Optional (can be added)
- Feature scaling: Not required (tree-based model)
"""

# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

usage_code = '''
from url_model import url_model_instance

# Load trained model
url_model_instance.load_model()

# Simple prediction
result, confidence = url_model_instance.predict(
    "http://paypa1-login.xyz/verify"
)
print(f"{result}: {confidence:.1%}")
# Output: Phishing: 94.2%

# Detailed analysis
details = url_model_instance.predict_with_details(
    "http://paypa1-login.xyz/verify"
)

print(f"URL: {details['url']}")
print(f"Prediction: {details['prediction']}")
print(f"Confidence: {details['confidence']:.2%}")
print(f"Phishing Probability: {details['phishing_probability']:.2%}")
print("Risk Factors:")
for factor in details['risk_factors']:
    print(f"  - {factor}")

# Output:
# URL: http://paypa1-login.xyz/verify
# Prediction: phishing
# Confidence: 94.23%
# Phishing Probability: 94.23%
# Risk Factors:
#   - Suspicious top-level domain (.xyz)
#   - Potential domain typosquatting detected
#   - Contains suspicious keywords
'''

# ==============================================================================
# REFERENCES
# ==============================================================================

references = """
Code References:
- Feature extraction: backend/url_model.py (line 40-116)
- Basic features: backend/utils.py (line 76-100)
- Suspicious TLDs: backend/utils.py (line 93)
- Training script: backend/train.py
- Documentation: backend/URL_MODEL_EXPLANATION.md

Key Functions:
- extract_advanced_features(): Extracts all 25+ features
- prepare_data(): Converts URLs to feature DataFrame
- train(): Trains Random Forest model
- predict(): Simple prediction
- predict_with_details(): Detailed analysis with risk factors

Model Files:
- phishing_url_model.pkl: Trained Random Forest model
- url_feature_names.pkl: Feature names for consistency
"""

if __name__ == '__main__':
    print("="*70)
    print("Random Forest URL Feature Reference")
    print("="*70)
    
    print("\n1. LEXICAL FEATURES")
    print("-" * 70)
    for feature, description in lexical_features.items():
        print(f"  {feature:25s}: {description}")
    
    print("\n2. ANATOMICAL FEATURES")
    print("-" * 70)
    for feature, description in anatomical_features.items():
        print(f"  {feature:25s}: {description}")
    
    print("\n3. DOMAIN FEATURES")
    print("-" * 70)
    for feature, description in domain_features.items():
        if isinstance(description, str) and '\n' in description:
            print(f"  {feature:25s}:")
            for line in description.strip().split('\n'):
                print(f"    {line.strip()}")
        else:
            print(f"  {feature:25s}: {description}")
    
    print("\n4. CONTENT FEATURES")
    print("-" * 70)
    for feature, description in content_features.items():
        print(f"  {feature:25s}:")
        for line in description.strip().split('\n'):
            print(f"    {line.strip()}")
    
    print("\n" + feature_importance_typical)
    
    print("\n" + "="*70)
    print("See URL_MODEL_EXPLANATION.md for complete documentation")
    print("="*70)
