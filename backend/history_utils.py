import os
import json
import fcntl
import tempfile
from datetime import datetime

# Storage directory for history files. Override with PHISHGUARD_HISTORY_DIR env var.
_DEFAULT_HISTORY_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_DIR = os.environ.get('PHISHGUARD_HISTORY_DIR', _DEFAULT_HISTORY_DIR)


def get_history_ref(uid):
    """Return the file path for the given user's history file."""
    os.makedirs(HISTORY_DIR, exist_ok=True)
    return os.path.join(HISTORY_DIR, f"history_{uid}.json")


def add_scan_to_history(scan, uid):
    """Add a scan result to the user's history using file locking and atomic writes."""
    scan['timestamp'] = datetime.now().isoformat()
    path = get_history_ref(uid)
    lock_path = path + '.lock'
    with open(lock_path, 'w', encoding='utf-8') as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            history = []
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    try:
                        history = json.load(f)
                    except Exception:
                        history = []
            history.append(scan)
            dir_name = os.path.dirname(path)
            with tempfile.NamedTemporaryFile(
                mode='w', encoding='utf-8', dir=dir_name, delete=False, suffix='.tmp'
            ) as tmp_file:
                json.dump(history, tmp_file)
                tmp_path = tmp_file.name
            os.replace(tmp_path, path)
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def load_history(uid):
    """Load all scan history for a user from a local JSON file."""
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
        'recent': history[:10]  # last 10 scans, already sorted by timestamp desc
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
