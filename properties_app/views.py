
from django.shortcuts import render
from rest_framework import generics
from auth_app.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from .models import Property
from .serializers import PropertySerializer
from rest_framework.response import Response



# Create your views here.
class PropertiesListView (generics.ListAPIView) : 
    permission_classes = [IsOwner , IsAuthenticated]
    def get(self , request , residence_id) : 
      properties = Property.objects.filter(residence_id = residence_id, owner = request.user) 
      serializer = PropertySerializer(properties , many = True)
      return Response(serializer.data)
            

    

class PropertyDetailsView (generics.ListAPIView) : 
   permission_classes = [IsOwner , IsAuthenticated] 
   def get (self , request , property_id) : 
      property = Property.objects.get(id = property_id)
      serializer = PropertySerializer(property)
      return Response(serializer.data)