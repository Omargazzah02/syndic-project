from rest_framework import serializers
from .models import Residence

class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields = ['id', 'residence_name', 'city', 'zip_code', 'country',  'floor_count' ,  'has_parking',  'created_at' , 'updated_at']
