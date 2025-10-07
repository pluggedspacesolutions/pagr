from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/users/", include("users.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/whatsapp/", include("whatsapp.urls")),  # Note: whatsapp.urls has webhook/ and logs/
    # OR if you prefer webhook at root:
    # path("webhooks/whatsapp/", include("whatsapp.urls")),
]