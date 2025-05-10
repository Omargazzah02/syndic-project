from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsOwner ,IsManager
from residences_app.models import Residence
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentSerializer
from transformers import pipeline
import PyPDF2
import io
import time

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
    




    

# Initialize the summarizer model outside of the class to avoid reloading it for each request
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    print(f"Error loading summarization model: {str(e)}")
    summarizer = None

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
        
        # Get the PDF file
        pdf_file = request.FILES.get('pdf_file')
        
        # Check for required fields
        title = request.data.get('title')
        category = request.data.get('category')
        
        if not title:
            return Response({"error": "Le titre est requis."}, status=status.HTTP_400_BAD_REQUEST)
        if not category:
            return Response({"error": "La catégorie est requise."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a default summary in case everything fails
        default_summary = f"Document {title} ({category})"
        summary_text = default_summary
        
        # Extract text from the PDF
        try:
            # Create a copy of the file for text extraction
            pdf_content = pdf_file.read()
            pdf_file.seek(0)  # Reset file pointer for later serialization
            
            # Use BytesIO to create a file-like object from the content
            pdf_io = io.BytesIO(pdf_content)
            reader = PyPDF2.PdfReader(pdf_io)
            
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                    
            # Remove excessive whitespace and normalize text
            text = ' '.join(text.split())
            
            print(f"Extracted text length: {len(text)} characters")
            if len(text) > 0:
                print(f"Text sample: {text[:200]}...")
            
            # Check if we have enough text to summarize
            if not text or len(text) < 50:
                # If text is very short, just use it as is or default
                summary_text = text if text else default_summary
                print(f"Text too short, using as summary: {summary_text}")
            elif summarizer is None:
                # If the model failed to load, use first few sentences
                sentences = text.split('.')[:3]
                summary_text = '. '.join(sentences) + '.'
                print(f"No model available, using first sentences: {summary_text}")
            else:
                try:
                    # Clean up excessive whitespace and prepare for summarization
                    text_for_summary = text.strip()
                    
                    # Ensure text isn't too long for model
                    if len(text_for_summary) > 1000:
                        text_for_summary = text_for_summary[:1000]
                    
                    print("Attempting to summarize with model...")
                    # Generate summary with better parameters
                    result = summarizer(
                        text_for_summary, 
                        max_length=150,  # Maximum length of summary
                        min_length=30,   # Minimum length of summary
                        do_sample=False, # For more deterministic results
                        truncation=True  # Ensure we don't exceed model limits
                    )
                    
                    generated_summary = result[0]['summary_text'].strip()
                    print(f"Generated summary: {generated_summary}")
                    
                    # Only use the generated summary if it's not empty
                    if generated_summary and len(generated_summary) > 10:
                        summary_text = generated_summary
                    else:
                        # Fallback if summary is too short
                        sentences = text.split('.')[:3]
                        summary_text = '. '.join(sentences) + '.'
                        print(f"Generated summary too short, using first sentences: {summary_text}")
                        
                except Exception as e:
                    print(f"Summarization failed: {str(e)}")
                    # Fallback to first few sentences
                    sentences = text.split('.')[:3]
                    summary_text = '. '.join(sentences) + '.'
                    print(f"Error in summarization, using first sentences: {summary_text}")
                    
        except Exception as e:
            print(f"PDF processing error: {str(e)}")
            # Stick with default summary
            print(f"Using default summary due to error: {summary_text}")
        
        # Final check - ENSURE summary is not empty
        if not summary_text or len(summary_text.strip()) == 0:
            summary_text = default_summary
            print(f"Empty summary detected, using default: {summary_text}")
            
        print(f"Final summary to be saved: {summary_text}")
        
        # Create serializer with all data including summary
        data = {
            'title': title,
            'category': category,
            'pdf_file': pdf_file,
            'summary': summary_text  # This should never be blank
        }
        
        serializer = DocumentSerializer(data=data)
        
        if serializer.is_valid():
            # Save document with residence
            document = serializer.save(residence=residence)
            
            print(f"Document saved with ID: {document.id}")
            print(f"Saved summary: {document.summary}")
            
            return Response({
                'message': 'Document uploaded and summarized successfully.',
                'document_id': document.id,
                'summary': document.summary
            }, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            
            # Special handling for summary validation errors
            if 'summary' in serializer.errors:
                print("CRITICAL: Summary validation still failed!")
                # Force a guaranteed valid summary with timestamp to ensure uniqueness
                timestamp = int(time.time())
                data['summary'] = f"Document {title} ({timestamp})"
                
                serializer = DocumentSerializer(data=data)
                if serializer.is_valid():
                    document = serializer.save(residence=residence)
                    return Response({
                        'message': 'Document uploaded with fallback summary.',
                        'document_id': document.id,
                        'summary': document.summary
                    }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

