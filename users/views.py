from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Member
from .serializers import MemberSerializer

class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all().order_by("-joined_at")
    serializer_class = MemberSerializer

    def perform_create(self, serializer):
        member = serializer.save()
        # Firebase sync removed - only saving to Django database

class MemberRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer