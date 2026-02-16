import json
import os
from datetime import datetime

HISTORY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scan_history.json')

def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_history(history):
    with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_scan_to_history(scan):
    history = load_history()
    scan['id'] = len(history) + 1
    scan['timestamp'] = datetime.now().isoformat()
    history.insert(0, scan)
    save_history(history)

def get_dashboard_stats():
    history = load_history()
    # Separate counts for each input type and result
    stats = {
        'total_scans': len(history),
        'phishing_email': 0,
        'phishing_sms': 0,
        'phishing_url': 0,
        'legitimate_email': 0,
        'legitimate_sms': 0,
        'legitimate_url': 0,
        'recent': history[:10],
    }
    for s in history:
        input_type = s.get('input_type', 'email')
        result = s.get('result', '')
        if result == 'Phishing':
            if input_type == 'email':
                stats['phishing_email'] += 1
            elif input_type == 'sms':
                stats['phishing_sms'] += 1
            elif input_type == 'url':
                stats['phishing_url'] += 1
        elif result == 'Legitimate':
            if input_type == 'email':
                stats['legitimate_email'] += 1
            elif input_type == 'sms':
                stats['legitimate_sms'] += 1
            elif input_type == 'url':
                stats['legitimate_url'] += 1
    return stats
