# users/models.py
from django.db import models
import uuid

class Member(models.Model):
    phone = models.CharField(max_length=20, unique=True)  # E.164 recommended (e.g. 23480...)
    name = models.CharField(max_length=120, blank=True)
    is_paid = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    referral_code = models.CharField(max_length=12, unique=True, blank=True)
    referrer = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="referrals")

    def save(self, *args, **kwargs):
        if not self.referral_code:
            # generate short code
            self.referral_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone} ({'paid' if self.is_paid else 'free'})"