from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "name", "is_paid", "joined_at", "referral_code", "referrer")
    search_fields = ("phone", "name", "referral_code")
    list_filter = ("is_paid",)