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
from pdf2image import convert_from_bytes
import pytesseract
import logging







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
    




# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the summarizer pipeline
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    logger.error(f"Failed to load summarization model: {e}")
    summarizer = None

def extract_text_from_pdf(pdf_file, language='fra'):
    try:
        # Read file content
        content = pdf_file.read()
        pdf_file.seek(0)  # Reset pointer for Django file field
        
        # Try to extract text directly from PDF
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        
        full_text = ''
        has_extractable_text = False
        
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text and len(page_text.strip()) > 50:
                has_extractable_text = True
                full_text += page_text + "\n"
        
        if not has_extractable_text:
            ocr_text = extract_text_with_ocr(content, language)
            if ocr_text:
                full_text = ocr_text
        
        cleaned_text = ' '.join(full_text.split())  # Normalize whitespace
        return cleaned_text
    
    except Exception as e:
        logger.error(f"PDF text extraction failed: {str(e)}")
        return ""

def extract_text_with_ocr(content, language='fra'):

    try:
        images = convert_from_bytes(
            content,
            dpi=300,  
            fmt='jpeg',
            grayscale=False,
            size=(1700, None),
            poppler_path=r"C:\poppler\poppler-24.08.0\Library\bin"
        )
        
        if not images:
            logger.error("Failed to convert PDF to images")
            return ""
        
        text = ""
        for image in images:
            enhanced_image = enhance_image_for_ocr(image)
            ocr_text = pytesseract.image_to_string(enhanced_image, lang=language, config='--psm 1')
            if ocr_text:
                text += ocr_text + "\n"
        
        return text
    
    except Exception as e:
        logger.error(f"OCR processing failed: {str(e)}")
        return ""

def enhance_image_for_ocr(image):

    try:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        logger.error(f"Image enhancement failed: {str(e)}")
        return image

def generate_summary(text, fallback_summary):

    if text and len(text.strip()) > 100:
        try:
            if summarizer:
                text_for_summary = text[:10000]  # Limit to first 10000 chars to be safe
                summary = summarizer(text_for_summary, max_length=150, min_length=50, do_sample=False)
                return summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
        
        # Fallback to basic summarization (first 3 sentences)
        sentences = text.split('.')[:3]
        return '. '.join(sentences) + '.'
    
    logger.info(f"Using fallback summary: {fallback_summary}")
    return fallback_summary

class DocumentUploadView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, residence_id):
        try:
            residence = Residence.objects.get(id=residence_id)
        except Residence.DoesNotExist:
            return Response({"error": "Cette résidence n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

        pdf_file = request.FILES.get('pdf_file')
        title = request.data.get('title')
        category = request.data.get('category')
        
        if not pdf_file or not title or not category:
            return Response({"error": "Le fichier, le titre et la catégorie sont requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        language = request.data.get('language', 'fra')
        fallback_summary = f"Document {title} ({category})"
        
        extracted_text = extract_text_from_pdf(pdf_file, language)
        summary = generate_summary(extracted_text, fallback_summary)
        
        data = {
            'title': title,
            'category': category,
            'pdf_file': pdf_file,
            'summary': summary
        }
        
        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            document = serializer.save(residence=residence)
            return Response({
                'message': 'Document uploaded and processed successfully.',
                'document_id': document.id,
                'summary': document.summary,
                'text_extracted': bool(extracted_text),
                'text_length': len(extracted_text) if extracted_text else 0
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
