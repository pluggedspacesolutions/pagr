from django.contrib import admin
from .models import MessageLog

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ("id", "member", "direction", "content", "created_at")
    search_fields = ("member__phone", "content")
    list_filter = ("direction", "created_at")