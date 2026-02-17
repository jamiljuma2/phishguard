from datetime import datetime
from firebase_admin import db

def get_history_ref(user_id):
    return db.reference(f'user_scans/{user_id}')

def add_scan_to_history(user_id, scan):
    if not user_id:
        print("Cannot add scan to history: user_id is missing.")
        return
    
    # Generate a unique key for the new scan entry
    new_scan_ref = get_history_ref(user_id).push()
    scan['id'] = new_scan_ref.key  # Store the Firebase generated key as 'id'
    scan['timestamp'] = datetime.now().isoformat()
    
    new_scan_ref.set(scan)
    print(f"Scan added to Firebase for user {user_id} with ID {scan['id']}")

def load_history(user_id):
    if not user_id:
        return []
    
    try:
        history_data = get_history_ref(user_id).order_by_child('timestamp').limit_to_last(100).get() # Fetch last 100 scans
        if not history_data:
            return []
        
        # Convert dictionary of scans to a list, and sort by timestamp in descending order
        history_list = list(history_data.values())
        history_list.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return history_list
    except Exception as e:
        print(f"Error loading history from Firebase for user {user_id}: {e}")
        return []

def get_dashboard_stats(user_id):
    if not user_id:
        return {
            'total_scans': 0,
            'phishing_email': 0,
            'phishing_sms': 0,
            'phishing_url': 0,
            'legitimate_email': 0,
            'legitimate_sms': 0,
            'legitimate_url': 0,
            'recent': [],
        }
    
    history = load_history(user_id)
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
