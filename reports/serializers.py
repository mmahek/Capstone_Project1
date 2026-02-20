from rest_framework import serializers
from .models import SymptomReport

class SymptomReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomReport
        fields = '__all__'
