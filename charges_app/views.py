from django.shortcuts import render
from rest_framework import generics , status
from auth_app.permissions import IsOwner, IsManager
from rest_framework.permissions import IsAuthenticated
from properties_app.models import Property
from .models import PropertyCharge, Charge
from rest_framework.response import Response
from documents_app.models import Invoice
from residences_app.models import Residence
from .serializers import ChargeSerializer

#  Create your views here.

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
               


class AddChargeView (generics.ListAPIView) :
   permission_classes = [IsAuthenticated , IsOwner]

   def post (self , request , residence_id) : 
       residence = Residence.objects.get(id = residence_id)
       if residence is None:
           return Response({"error": "Cette residance n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
       managers = residence.managers.all()
       exists =  managers.filter(id=request.user.id).exists()
       if (exists is not True  ) : 
          return Response({"error": "Vous n'avez pas un manager dans cette résidance."}, status=status.HTTP_401_UNAUTHORIZED)
       
       charge_title = request.data.get('charge_title')
       charge_price = float (request.data.get('charge_price'))


       charge_category = request.data.get('charge_category')

       print (charge_category , charge_price , charge_title)

       Charge.objects.create(residence = residence , title = charge_title , category = charge_category , price = charge_price)
       return Response({"message":"Vous avez bien créé un charge avec succès."}, status=status.HTTP_201_CREATED)




class ChargesManagingListView (generics.ListAPIView) :
    permission_classes = [IsAuthenticated , IsManager]
    def get (self , request , residence_id ) : 
        residence  = Residence.objects.get(id=residence_id)
        if residence is None  : 
             return Response({"error": "Cette residance n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        managers = residence.managers.all()
        exists = managers.filter(id = request.user.id).exists()
        if exists is not True : 
             return Response({"error": "Vous n'avez pas un manager dans cette résidance."}, status=status.HTTP_401_UNAUTHORIZED)
        charges = residence.charges.all()
        serialized_charges = ChargeSerializer(charges , many = True)
        return Response(serialized_charges.data, status=status.HTTP_200_OK)



class DeleteChargeView (generics.ListAPIView):
    
     permission_classes = [IsAuthenticated , IsManager]
     def delete (self , request , charge_id ) : 
        
        charge = Charge.objects.get(id = charge_id)
        if charge is None  : 
             return Response({"error": "Cette charge n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        managers = charge.residence.managers.all()
        exists = managers.filter(id = request.user.id).exists()
        if exists is not True : 
             return Response({"error": "Vous n'avez pas un manager dans cette résidance."}, status=status.HTTP_401_UNAUTHORIZED)
        charge.delete()
        return Response(status=status.HTTP_200_OK)

    
        

            

            
        

       
       

         
      

       
       
       

    
           


        