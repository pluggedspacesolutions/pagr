from rest_framework import serializers
from .models import Payment
from users.serializers import MemberSerializer

class PaymentSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ("id", "member", "paystack_reference", "amount", "currency", "status", "created_at", "updated_at")
        read_only_fields = ("id", "member", "paystack_reference", "status", "created_at", "updated_at")