# whatsapp/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MessageLog
from firebase_config import db


@receiver(post_save, sender=MessageLog)
def sync_message_to_firestore(sender, instance, **kwargs):
    doc_ref = db.collection("message_logs").document(str(instance.id))
    doc_ref.set({
        "member_id": str(instance.member.id) if instance.member else None,
        "member_phone": instance.member.phone if instance.member else None,
        "direction": instance.direction,
        "content": instance.content,
        "raw_payload": instance.raw_payload,
        "created_at": instance.created_at.isoformat(),
    }, merge=True)


@receiver(post_delete, sender=MessageLog)
def delete_message_from_firestore(sender, instance, **kwargs):
    db.collection("message_logs").document(str(instance.id)).delete()