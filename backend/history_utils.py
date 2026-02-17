from firebase_admin import db
from datetime import datetime


def get_history_ref(uid):
    """Get a Firebase Realtime Database reference for a user's scan history."""
    return db.reference(f'scan_history/{uid}')


def add_scan_to_history(scan, uid):
    """Add a scan result to the user's history in Firebase."""
    ref = get_history_ref(uid)
    scan['timestamp'] = datetime.now().isoformat()
    ref.push(scan)


def load_history(uid):
    """Load all scan history for a user from Firebase."""
    ref = get_history_ref(uid)
    data = ref.get()
    if not data:
        return []
    history = []
    for key, val in data.items():
        val['id'] = key
        history.append(val)
    history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return history


def get_dashboard_stats(uid):
    """Get dashboard statistics for a user from Firebase."""
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
