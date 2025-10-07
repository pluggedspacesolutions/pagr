from rest_framework import serializers
from .models import MessageLog
from users.serializers import MemberSerializer

class MessageLogSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    class Meta:
        model = MessageLog
        fields = ("id", "member", "direction", "content", "raw_payload", "created_at")
        read_only_fields = ("id", "member", "raw_payload", "created_at")