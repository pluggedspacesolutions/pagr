# whatsapp/utils.py
import requests
import json
from django.conf import settings

BASE_URL = "https://graph.facebook.com"

def send_text_message(to_phone, message_text):
    """
    to_phone must be E.164 (e.g. 2348012345678)
    """
    url = f"{BASE_URL}/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message_text}
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    # return response object / json for debugging
    try:
        return resp.json()
    except Exception:
        return {"status_code": resp.status_code, "text": resp.text}