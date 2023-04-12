from django.contrib import admin
from django.urls import path, include
from user_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login_view),
    path('logout', views.logout)
]