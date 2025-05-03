from rest_framework import serializers
from .models import Charge

class ChargeSerializer  (serializers.ModelSerializer) : 
    date_creation = serializers.DateTimeField(format="%d/%m/%Y : %H:%M")

    class Meta : 
        model = Charge
        fields = ['id' , 'title' , 'category' ,  'price' ,'date_creation']