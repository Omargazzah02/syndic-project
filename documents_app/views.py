from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsOwner ,IsManager
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


class DocumentUploadView(APIView):
    permission_classes = [IsAuthenticated, IsManager]
    
    def post(self, request, residence_id):
        # Debug info - helpful for troubleshooting
        print("Request data:", request.data)
        print("Request FILES:", request.FILES)
        
        # Check if residence exists
        try:
            residence = Residence.objects.get(id=residence_id)
        except Residence.DoesNotExist:
            return Response({"error": "Cette résidence n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if file is in request
        if 'pdf_file' not in request.FILES:
            return Response({"error": "Aucun fichier PDF trouvé dans la requête."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare data
        data = {
            'title': request.data.get('title'),
            'category': request.data.get('category'),
            'pdf_file': request.FILES.get('pdf_file')
        }
        
        # Check for required fields
        if not data['title']:
            return Response({"error": "Le titre est requis."}, status=status.HTTP_400_BAD_REQUEST)
        if not data['category']:
            return Response({"error": "La catégorie est requise."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create and validate serializer
        serializer = DocumentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(residence=residence)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return detailed error information
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
          
        


class AllDocumentsListView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, residence_id):
        residence = Residence.objects.filter(
            id=residence_id,
            properties__owner=request.user
        ).first()
        
        if residence is None:
            return Response({"error": "Cette résidence n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

        documents = residence.documents.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def delete(self, request, residence_id, document_id):
        from .models import Document  # If not already imported at the top

        try:
            document = Document.objects.get(id=document_id, residence__id=residence_id)
        except Document.DoesNotExist:
            return Response({"error": "Document introuvable pour cette résidence."}, status=status.HTTP_404_NOT_FOUND)

        document.delete()
        return Response({"message": "Document supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)

