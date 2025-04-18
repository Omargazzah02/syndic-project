from django.shortcuts import render
from rest_framework import generics , status
from auth_app.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from properties_app.models import Property
from .models import PropertyCharge
from rest_framework.response import Response

# Create your views here.

class ChargesListView(generics.ListAPIView) :
    permission_classes = [IsAuthenticated , IsOwner]
    def get (self , request , residence_id) :
       properties =  Property.objects.filter(owner = request.user , residence_id = residence_id)
       data = []
       for property in properties :
          property_data =  {
               "property_id" : property.id,
               "property_tiltle" : property.property_type + str(property.property_number),
               "charges" : []

             }
          properties_charges = PropertyCharge.objects.filter(property = property )
          for property_charge in properties_charges :
               property_data["charges"].append({
                  "charge_title" : property_charge.charge.title,
                  "part" : property_charge.part
                  
               })
          data.append(property_data)
       return Response (data )
               


           


        