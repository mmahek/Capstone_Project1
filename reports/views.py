from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import SymptomReport
from .serializers import SymptomReportSerializer

class SymptomReportViewSet(viewsets.ModelViewSet):
    queryset = SymptomReport.objects.all().order_by('-timestamp')
    serializer_class = SymptomReportSerializer

# Create your views here.
