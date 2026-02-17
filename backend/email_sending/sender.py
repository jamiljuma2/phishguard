import requests
import os

ZEPTOMAIL_API_KEY = os.environ.get("ZEPTOMAIL_API_KEY")
ZEPTOMAIL_SENDER_EMAIL = os.environ.get("ZEPTOMAIL_SENDER_EMAIL", "PhishGuard@coursehubkenya.com")

def send_phishing_alert_email(recipient_email, sms_content, scan_result, suspicious_words):
    if not ZEPTOMAIL_API_KEY:
        print("ZeptoMail API key not configured. Skipping email.")
        return

    if not recipient_email:
        print("No recipient email provided. Skipping email.")
        return

    subject = "PhishGuard Alert: Potentially Malicious SMS Detected!"
    
    html_body = f"""
    <html>
    <body>
        <p>Dear User,</p>
        <p>PhishGuard has detected a potentially malicious SMS:</p>
        <p><strong>SMS Content:</strong> {sms_content}</p>
        <p><strong>Scan Result:</strong> <span style="color: red;">{scan_result}</span></p>
        <p><strong>Suspicious Keywords:</strong> {', '.join(suspicious_words) if suspicious_words else 'None'}</p>
        <p>Please exercise extreme caution with this message. Do not click on any links, reply, or share any personal information.</p>
        <p>For more details, please log in to your PhishGuard dashboard.</p>
        <p>Sincerely,</p>
        <p>The PhishGuard Team</p>
    </body>
    </html>
    """

    data = {
        "bounce_address": ZEPTOMAIL_SENDER_EMAIL,
        "from": {
            "address": ZEPTOMAIL_SENDER_EMAIL
        },
        "to": [
            {
                "email_address": {
                    "address": recipient_email,
                    "name": "PhishGuard User"
                }
            }
        ],
        "subject": subject,
        "htmlbody": html_body
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {ZEPTOMAIL_API_KEY}"
    }

    try:
        response = requests.post("https://api.zeptomail.com/v1.1/email", headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        print(f"Email sent successfully to {recipient_email}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending email to {recipient_email}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")

if __name__ == '__main__':
    # Example usage (for testing purposes)
    # You would typically get recipient_email, sms_content, etc. dynamically
    test_email = "test@example.com"  # Replace with a real email for testing
    test_sms_content = "Congratulations! You've won a prize. Click here: evil.link/prize"
    test_scan_result = "Phishing"
    test_suspicious_words = ['prize', 'won', 'click here']
    send_phishing_alert_email(test_email, test_sms_content, test_scan_result, test_suspicious_words)
