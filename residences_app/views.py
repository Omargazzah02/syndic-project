from rest_framework import generics
from .models import Residence
from .serializers import ResidenceSerializer
from auth_app.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsOwner
from .models import Residence
from rest_framework.response import Response

class ResidenceListView(generics.ListAPIView):
  permission_classes = [IsAuthenticated, IsOwner]
  def get(self , request): 
    residences = Residence.objects.filter(properties__owner=request.user).distinct()
    serializer = ResidenceSerializer(residences,many=True)
    return Response(serializer.data)
  


class ResidenceDetailsView (generics.ListAPIView) :
  permission_classes = [ IsAuthenticated,IsOwner]
  def get(self , request , residence_id):
    residence = Residence.objects.get(id = residence_id)
    serializer = ResidenceSerializer (residence)
    return Response(serializer.data)
    
      
    