"""
Script to extract URLs from email dataset and create URL-specific dataset
"""
import re
import pandas as pd
import os

def extract_urls_from_text(text):
    """Extract all URLs from text"""
    return re.findall(r'http[s]?://[^\s]+', text)

def create_url_dataset():
    """Extract URLs from phishing_emails.csv and create phishing_urls.csv"""
    dataset_path = 'dataset/phishing_emails.csv'
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return
    
    # Read email dataset
    df = pd.read_csv(dataset_path)
    
    # Extract URLs and their labels
    url_data = []
    for idx, row in df.iterrows():
        text = str(row['text'])
        label = row['label']
        urls = extract_urls_from_text(text)
        
        for url in urls:
            url_data.append({'url': url, 'label': label})
    
    if len(url_data) >= 10:
        url_df = pd.DataFrame(url_data)
        url_df.to_csv('dataset/phishing_urls.csv', index=False)
        print(f"Created phishing_urls.csv with {len(url_df)} URLs")
        print(url_df.head(10))
    else:
        print(f"Only {len(url_data)} URLs found in dataset (need >=10). Creating expanded URL dataset...")
        # Create expanded URL dataset for reliable training
        mock_urls = {
            'url': [
                # Phishing URLs (label=1)
                'http://fake-bank.com/secure/login',
                'http://malicious-reset-password.com/urgent/update',
                'http://192.168.1.1/admin/setup',
                'http://amaz0n-secure.xyz/verify-account',
                'http://g00gle-login.tk/signin-now',
                'http://secure-entry.paypal.p-ayp.al/verify',
                'http://apple-id.secure-check.ga/verify',
                'http://netflix-account-update.cf/login',
                'http://inst-agram-secure.gq/login',
                'http://ebay-member-confirm.ml/account',
                'http://paypa1-login.xyz/verify',
                'http://micros0ft-support.pw/reset',
                'http://10.0.0.1/phish/login.php',
                'http://facebok-security.cc/confirm',
                'http://netfl1x-billing.top/update',
                'http://secure-wells-farg0.work/signin',
                'http://bankofamerica-verify.click/urgent',
                'http://chase-confirm.stream/password',
                'http://apple-id-suspended.download/verify',
                'http://172.16.0.1:8443/admin/login',
                'http://paypal-confirm-identity.ml/secure/update',
                'http://amazon-order-problem.ga/verify-now',
                'http://linkedin-security-alert.cf/signin',
                'http://dropbox-shared-document.gq/view',
                'http://microsoft-365-verify.tk/login',
                # Legitimate URLs (label=0)
                'https://www.legitimate-bank.com',
                'https://secure.paypal.com',
                'https://amazon.com/account/settings',
                'https://google.com/search',
                'https://microsoft.com/en-us/support',
                'https://facebook.com/login.php',
                'https://github.com/login',
                'https://twitter.com/home',
                'https://linkedin.com/feed',
                'https://chase.com/personal',
                'https://www.bankofamerica.com/online-banking',
                'https://www.wellsfargo.com/checking',
                'https://www.apple.com/shop',
                'https://www.netflix.com/browse',
                'https://www.dropbox.com/home',
                'https://outlook.office365.com/mail',
                'https://www.instagram.com/accounts/login',
                'https://www.reddit.com',
                'https://www.stackoverflow.com/questions',
                'https://www.wikipedia.org/wiki/Main_Page',
                'https://mail.google.com/mail/inbox',
                'https://drive.google.com/drive/my-drive',
                'https://www.youtube.com/feed/subscriptions',
                'https://www.ebay.com/myb/Summary',
                'https://www.nytimes.com',
            ],
            'label': [
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]
        }
        url_df = pd.DataFrame(mock_urls)
        url_df.to_csv('dataset/phishing_urls.csv', index=False)
        print(f"Created mock phishing_urls.csv with {len(url_df)} URLs")
        print(url_df.head(10))

if __name__ == '__main__':
    create_url_dataset()
