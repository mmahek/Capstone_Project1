from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatMessageViewSet,
    chat_page,
    dashboard,
    alerts_page,
    chat_history,
    health_records,
    chat_api
)

router = DefaultRouter()
router.register(r'chat', ChatMessageViewSet)

urlpatterns = [

    # Pages
    path("dashboard/", dashboard, name="dashboard"),
    path("chat/", chat_page, name="chat-page"),
    path("alerts/", alerts_page, name="alerts"),
    path("history/", chat_history, name="chat-history"),
    path("records/", health_records, name="health-records"),
    
    path("api/chat/", chat_api, name="chat_api"),

    # API
    path("api/", include(router.urls)),
    
]
