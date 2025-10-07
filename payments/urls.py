from django.urls import path
from . import views

urlpatterns = [
    path("initiate/", views.InitiatePaymentView.as_view(), name="initiate-payment"),
    path("webhook/", views.paystack_webhook, name="paystack-webhook"),  # convenience local mapping
]