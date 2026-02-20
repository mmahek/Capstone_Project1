from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SymptomReportViewSet

router = DefaultRouter()
router.register(r'reports', SymptomReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
