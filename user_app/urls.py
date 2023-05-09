from django.contrib import admin
from django.urls import path, include
from user_app import views

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    # path('admin/', admin.site.urls),
    path('login', views.login_view),
    path('logout', views.logout)
]