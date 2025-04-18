from rest_framework import serializers
from .models import Document
class DocumentSerializer(serializers.ModelSerializer):
      # Format personnalisé de la date
    date_creation = serializers.DateTimeField(format="%d/%m/%Y : %H:%M")

    class Meta:
        model = Document
        fields = ['id', 'title', 'pdf_file', 'date_creation']