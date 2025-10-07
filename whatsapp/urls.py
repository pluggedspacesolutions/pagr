from django.urls import path
from . import views

urlpatterns = [
    path("webhook/", views.whatsapp_webhook, name="whatsapp-webhook"),
    path("logs/", views.MessageLogListView.as_view(), name="whatsapp-logs"),
]