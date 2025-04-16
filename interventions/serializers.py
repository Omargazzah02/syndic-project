from rest_framework import serializers
from .models import Intervention

class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervention
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'status']
