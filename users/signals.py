# users/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Member
from firebase_config import db


@receiver(post_save, sender=Member)
def sync_member_to_firestore(sender, instance, **kwargs):
    """Sync or update member in Firestore."""
    doc_ref = db.collection("members").document(str(instance.id))
    doc_ref.set({
        "phone": instance.phone,
        "name": instance.name,
        "is_paid": instance.is_paid,
        "joined_at": instance.joined_at.isoformat(),
        "referral_code": instance.referral_code,
        "referrer_id": str(instance.referrer.id) if instance.referrer else None,
    }, merge=True)


@receiver(post_delete, sender=Member)
def delete_member_from_firestore(sender, instance, **kwargs):
    """Remove member from Firestore if deleted in Django."""
    doc_ref = db.collection("members").document(str(instance.id))
    doc_ref.delete()