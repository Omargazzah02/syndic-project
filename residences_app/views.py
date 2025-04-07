from rest_framework import generics
from .models import Residence
from .serializers import ResidenceSerializer
from auth_app.permissions import IsOwner

class ResidenceListView(generics.ListAPIView):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer
    permission_classes = [IsOwner]  