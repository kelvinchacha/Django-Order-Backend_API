from rest_framework import serializers
from .models import Oda

class OdaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oda
        fields = '__all__' 
