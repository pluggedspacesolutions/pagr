# payments/models.py
from django.db import models
from django.utils import timezone
from users.models import Member

class Payment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payments")
    paystack_reference = models.CharField(max_length=128, unique=True)
    amount = models.PositiveIntegerField()  # in NGN
    currency = models.CharField(max_length=8, default="NGN")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_success(self):
        self.status = "success"
        self.save()

    def mark_failed(self):
        self.status = "failed"
        self.save()

    def __str__(self):
        return f"{self.paystack_reference} - {self.member.phone} - {self.status}"