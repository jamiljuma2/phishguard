import os
import json
import firebase_admin
from firebase_admin import credentials

creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
if not creds_json:
    raise RuntimeError("GOOGLE_CREDENTIALS_JSON environment variable is not set. Please add your serviceAccountKey.json contents as an environment variable in Render.")

cred = credentials.Certificate(json.loads(creds_json))
print("Loaded Firebase credentials from environment variable.")
firebase_admin.initialize_app(cred)