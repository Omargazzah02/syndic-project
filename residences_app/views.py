from rest_framework import generics, status
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
    residence = Residence.objects.filter(
        id=residence_id,
        properties__owner=request.user
      ).first()
    if residence is None:
       return Response({"error": "Cette résidance n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ResidenceSerializer (residence)
    return Response(serializer.data , status=200)
  





class GetContactManagers (generics.ListAPIView) :
  permission_classes = [IsAuthenticated , IsOwner]
  def get (self , request , residence_id):
   residence = Residence.objects.filter(
        id=residence_id,
        properties__owner=request.user
      ).first()
   if residence is None:
     return Response({"error": "Cette résidance n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
   managers = residence.managers.all()
   data = []

  
   for manager in managers : 
      data.append({
         "id" : manager.id,
         "first_name" : manager.first_name,
         "last_name"  : manager.last_name,
         "email" : manager.email,
         "phone" : manager.phone
         
         
      })
   return Response(data )






class IsManagerView (generics.ListAPIView)  :
   permission_classes = [IsAuthenticated]

   def get (self , request , residence_id)  : 
     residence = Residence.objects.get(id = residence_id)
     if residence is None:
          return Response({"error": "Cette résidance n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
     
     managers = residence.managers.all()

     exists =  managers.filter(id=request.user.id).exists()

     data = {"is_manager" : exists}
     print(data)
     return Response(data )







       

      
    
      
    