# payments/views.py
import json
import hmac
import hashlib
import requests

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Member
from .models import Payment

import logging
logger = logging.getLogger("paystack") 

# Helper to create Paystack transaction
class InitiatePaymentView(APIView):
    """
    POST body: { "phone": "23480...", "name": "John Doe", "email": "john@example.com" (optional) }
    Returns authorization_url for payment page.
    """
    def post(self, request):
        data = request.data
        phone = data.get("phone")
        name = data.get("name", "")
        email = data.get("email")

        if not phone:
            return Response({"error": "phone is required"}, status=400)

        member, _ = Member.objects.get_or_create(phone=phone, defaults={"name": name})
        # Paystack requires an email field — if user has none, use a placeholder derived from phone
        if not email:
            email = f"{phone.replace('+','').replace(' ','')}@pagr.local"

        # Paystack expects amount in kobo. Convert NGN to kobo: NGN * 100
        amount_ngn = 2000  # membership fee
        amount_kobo = int(amount_ngn) * 100  # 2000 * 100 => 200000

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "email": email,
            "amount": amount_kobo,
            "callback_url": settings.PAYSTACK_CALLBACK_URL,
            "metadata": {
                "phone": phone,
                "member_id": member.id,
            }
        }
        r = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=payload, timeout=15)
        if r.status_code != 200 and r.status_code != 201:
            return Response({"error": "failed to initialize payment", "details": r.text}, status=500)

        resp = r.json()
        # create payment record (use reference when it's returned)
        reference = resp["data"]["reference"]
        Payment.objects.create(member=member, paystack_reference=reference, amount=amount_ngn, status="pending")

        return Response({"authorization_url": resp["data"]["authorization_url"], "reference": reference})


# Paystack webhook handler
@csrf_exempt
def paystack_webhook(request):
    """
    Configure Paystack to POST webhooks to this endpoint.
    We'll verify using signature header 'x-paystack-signature'
    """
    secret = settings.PAYSTACK_SECRET_KEY
    signature = request.headers.get("x-paystack-signature") or request.META.get("HTTP_X_PAYSTACK_SIGNATURE")
    payload = request.body

    # verify signature if header present
    if signature:
        computed = hmac.new(secret.encode("utf-8"), payload, hashlib.sha512).hexdigest()
        if computed != signature:
            return HttpResponseForbidden("Invalid signature")

    try:
        data = json.loads(payload.decode("utf-8"))
    except Exception:
        return HttpResponse(status=400)

    # Event structure varies. Try to find reference & status
    # Prefer data['data']['reference'] and data['event'] or data['data']['status']
    event = data.get("event")
    core = data.get("data") or {}
    # Paystack sometimes nests charge info under 'data'
    reference = core.get("reference") or (core.get("data") or {}).get("reference")
    status = core.get("status") or (core.get("data") or {}).get("status")

    if not reference:
        return HttpResponse(status=200)  # ignore

    try:
        payment = Payment.objects.get(paystack_reference=reference)
    except Payment.DoesNotExist:
        # nothing to update
        return HttpResponse(status=200)

    # Mark success if status known as success
    if str(status).lower() == "success" or event in ("charge.success", "transaction.success"):
        payment.status = "success"
        payment.save()
        member = payment.member
        member.is_paid = True
        member.save()

        logger.info(f"Paystack webhook verified for {member.phone}")

        # ✅ Referral credit logic
        if member.referrer:
            referrer = member.referrer
            # You could later extend this to add points, count, or commission logs.
            logger.info(f"Referral: {referrer.phone} referred {member.phone}")
        
        # Optional: notify user on WhatsApp after payment (via whatsapp utils)
        from whatsapp.utils import send_text_message
        try:
            send_text_message(
                member.phone,
                f"✅ Payment received! Welcome to PAGR Paid Membership. You'll receive your first training soon."
            )
        except Exception:
            pass

    else:
        # If failed/other statuses:
        payment.status = str(status).lower()
        payment.save()

    return HttpResponse(status=200)