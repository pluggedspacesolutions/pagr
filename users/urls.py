from django.urls import path
from . import views

urlpatterns = [
    path("", views.MemberListCreateView.as_view(), name="member-list-create"),
    path("<int:pk>/", views.MemberRetrieveUpdateView.as_view(), name="member-detail"),
]