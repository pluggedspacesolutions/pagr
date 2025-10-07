# pagr_backend/firebase_utils.py
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore

def get_firestore_client():
    # Initialize only once
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        if not cred_path:
            raise RuntimeError("FIREBASE_CREDENTIALS not set in env")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def save_member_to_firestore(member):
    
    #member: instance of users.models.Member
    
    db = get_firestore_client()
    doc_ref = db.collection("members").document(member.phone)
    data = {
        "phone": member.phone,
        "name": member.name,
        "is_paid": member.is_paid,
        "joined_at": member.joined_at.isoformat(),
        "referral_code": member.referral_code,
        "referrer": member.referrer.phone if member.referrer else None,
    }
    doc_ref.set(data, merge=True)

def save_payment_to_firestore(payment):
    db = get_firestore_client()
    doc_ref = db.collection("payments").document(payment.paystack_reference)
    data = {
        "member_phone": payment.member.phone,
        "amount": payment.amount,
        "currency": payment.currency,
        "status": payment.status,
        "created_at": payment.created_at.isoformat(),
        "updated_at": payment.updated_at.isoformat(),
    }
    doc_ref.set(data, merge=True)
"""    
    
# pagr_backend/firebase_utils.py
import os
import logging

logger = logging.getLogger(__name__)

# Mock implementation - remove when firebase-admin is installed
def get_firestore_client():
    logger.warning("Using mock Firestore client - Firebase not installed")
    return None

def save_member_to_firestore(member):
    logger.info(f"Mock: Would save member {member.phone} to Firestore")
    # Add actual implementation later
    pass

def save_payment_to_firestore(payment):
    logger.info(f"Mock: Would save payment {payment.paystack_reference} to Firestore")
    # Add actual implementation later
    pass