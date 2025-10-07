# whatsapp/models.py
from django.db import models
from users.models import Member

class MessageLog(models.Model):
    DIRECTION_CHOICES = (("in","in"), ("out","out"))
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    direction = models.CharField(max_length=3, choices=DIRECTION_CHOICES)
    content = models.TextField()
    raw_payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.direction} - {self.member.phone if self.member else 'unknown'} - {self.created_at.isoformat()}"