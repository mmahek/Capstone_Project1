from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import signup

urlpatterns = [

    # Admin panel
    path('admin/', admin.site.urls),

    # Signup
    path('accounts/signup/', signup, name='signup'),

    # Django built-in authentication (login, logout, password reset)
    path('auth/', include('django.contrib.auth.urls')),

    # Custom user pages (profile, edit, logout, login override)
    path('accounts/', include('accounts.urls')),

    # Reports API
    path('api/', include('reports.urls')),

    # Main App (Dashboard, Chat, Alerts, History, Health Records)
    path('', include('chatbot.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
