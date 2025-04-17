from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsOwner
from residences_app.models import Residence
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentSerializer
# Create your views here.


class CategoryDocumentsListView (APIView) :
    permission_classes = [IsOwner , IsAuthenticated]
    def get(self, request , residence_id ) :
       residence = Residence.objects.filter(
        id=residence_id,
        properties__owner=request.user
      ).first()
       if residence is None:
         return Response({"error": "Cette résidance n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
       documents = residence.documents.all()
       categories = set (doc.category for doc in documents)
     
       return Response(categories)


class DocumentsByCategoryListView (APIView) : 
   permission_classes = [IsOwner , IsAuthenticated]
   def get (self , request , residence_id , category) : 
       residence = Residence.objects.filter(
        id=residence_id,
        properties__owner=request.user
      ).first()
       if residence is None:
         return Response({"error": "Cette résidance n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
       documents = residence.documents.filter(category = category)
       serialized_documents = DocumentSerializer(documents ,many = True)
       return Response(serialized_documents.data, status=status.HTTP_200_OK)



         
      
       
          
        
