from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "phone", "name", "is_paid", "joined_at", "referral_code", "referrer")
        read_only_fields = ("id", "is_paid", "joined_at", "referral_code")

    # allow nested representation for referrer
    referrer = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), allow_null=True, required=False)