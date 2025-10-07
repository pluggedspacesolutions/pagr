# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Path to your Firebase service account key
FIREBASE_CRED_PATH = os.path.join(os.path.dirname(__file__), "pagr_firebase.json")

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()