def get_history_ref(uid):
    """Stub: No Firebase. Returns local file path for user history."""
    import os
    return os.path.join(os.path.dirname(__file__), f"history_{uid}.json")


def add_scan_to_history(scan, uid):
    """Add a scan result to the user's history in a local JSON file."""
    import json, os
    from datetime import datetime
    scan['timestamp'] = datetime.now().isoformat()
    path = get_history_ref(uid)
    history = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                history = json.load(f)
            except Exception:
                history = []
    history.append(scan)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(history, f)


def load_history(uid):
    """Load all scan history for a user from a local JSON file."""
    import json, os
    path = get_history_ref(uid)
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            history = json.load(f)
        history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return history
    except Exception:
        return []


def get_dashboard_stats(uid):
    """Get dashboard statistics for a user from local history."""
    history = load_history(uid)
    stats = {
        'total_scans': len(history),
        'phishing_email': 0,
        'phishing_sms': 0,
        'phishing_url': 0,
        'legitimate_email': 0,
        'legitimate_sms': 0,
        'legitimate_url': 0,
    # Send the most recent 20 for dashboard chart, but full history for scan history tab
    'recent': history[:20],
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
