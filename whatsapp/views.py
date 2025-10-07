import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import MessageLog
from .serializers import MessageLogSerializer
from .utils import send_text_message
from users.models import Member

import logging
logger = logging.getLogger("webhook")

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        verify_token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if verify_token == settings.WHATSAPP_VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponseForbidden("Invalid verify token")

    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))
            logger.info(f"Incoming WhatsApp payload: {payload}")
        except Exception:
            return HttpResponse(status=400)

        # Process entries defensively
        entries = payload.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages") or []
                for message in messages:
                    phone = message.get("from")
                    text = None
                    if "text" in message:
                        text = message["text"].get("body")
                    elif message.get("type") == "interactive":
                        interactive = message.get("interactive", {})
                        if interactive.get("type") == "button_reply":
                            text = interactive.get("button_reply", {}).get("title")
                        else:
                            text = json.dumps(interactive)

                    # ensure E.164 style is stored; WhatsApp usually sends international phone without +
                    # create or get
                    member, created = Member.objects.get_or_create(phone=phone)
                    # Firebase sync removed - only saving to Django database

                    MessageLog.objects.create(member=member, direction="in", content=text or "", raw_payload=message)

                    # Basic keyword routing
                    if text:
                        lower = text.strip().lower()
                        if lower in ("hi", "hello", "hey"):
                            send_text_message(phone, f"Welcome to PAGR! Reply 'join' to get the payment link.")
                        elif lower == "join":
                            # In production we'd return a payment link from our frontend; for now send info
                            send_text_message(phone, "To pay ₦2,000 and join, visit: [open your app link] or use the API to generate a Paystack link.")
                        else:
                            send_text_message(phone, "Thanks for your message. An admin will respond if needed.")
        return HttpResponse(status=200)

# Admin-only view to list message logs (useful for debugging)
class MessageLogListView(generics.ListAPIView):
    queryset = MessageLog.objects.all().order_by("-created_at")
    serializer_class = MessageLogSerializer
    permission_classes = [IsAdminUser]