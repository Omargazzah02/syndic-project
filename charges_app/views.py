from django.shortcuts import render
from rest_framework import generics , status
from auth_app.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from properties_app.models import Property
from .models import PropertyCharge
from rest_framework.response import Response
from documents_app.models import Invoice
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
               formatted_date = property_charge.charge.date_creation.strftime("%d/%m/%Y : %H:%M")
               try:
                   invoice = Invoice.objects.get(charge = property_charge.charge)
                   invoice_url = invoice.pdf_file.url

               except Invoice.DoesNotExist:
                   invoice_url = None
                   
               
               

               property_data["charges"].append({
                  "charge_title" : property_charge.charge.title,
                  "part" : property_charge.part,
                  "date_creation" : formatted_date,
                  "invoice_url" : invoice_url

               })
          data.append(property_data)
       return Response (data )
               


           


        