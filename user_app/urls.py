from django.contrib import admin
from django.urls import path, include
# from user_app.views import SignInView, SignOutView
from user_app import views
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

# router = routers.DefaultRouter()
# router.register(r'login', views.UserLoginAPI)
# router.register(r'logout', views.logout)

urlpatterns = [
    # path('login/', views.UserLoginAPI.as_view()),
    path('login/', views.login_view),
    path('logout/', views.logout),
    # path('', include(router.urls)),

    # 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]