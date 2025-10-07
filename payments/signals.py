# payments/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Payment
from firebase_config import db


@receiver(post_save, sender=Payment)
def sync_payment_to_firestore(sender, instance, **kwargs):
    doc_ref = db.collection("payments").document(str(instance.id))
    doc_ref.set({
        "member_id": str(instance.member.id),
        "member_phone": instance.member.phone,
        "amount": instance.amount,
        "currency": instance.currency,
        "status": instance.status,
        "paystack_reference": instance.paystack_reference,
        "created_at": instance.created_at.isoformat(),
        "updated_at": instance.updated_at.isoformat(),
    }, merge=True)


@receiver(post_delete, sender=Payment)
def delete_payment_from_firestore(sender, instance, **kwargs):
    db.collection("payments").document(str(instance.id)).delete()