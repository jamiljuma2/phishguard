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
    phishing = sum(1 for s in history if s.get('result') == 'Phishing')
    legitimate = sum(1 for s in history if s.get('result') == 'Legitimate')
    total = len(history)
    return {
        'total_scans': total,
        'phishing': phishing,
        'legitimate': legitimate,
        'recent': history[:10],
    }
