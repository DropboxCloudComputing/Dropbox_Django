from django.contrib import admin
from django.urls import path, include

from django.views.generic.base import TemplateView

urlpatterns = [
    path('api/v1/files/', include('files.urls')),
    path('api/v1/users/', include('user_app.urls')),
    path('admin/', admin.site.urls),
]