from django.contrib import admin
from django.urls import path, include
# from user_app.views import SignInView, SignOutView


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    # path('admin/', admin.site.urls),
    path('login/', views.login_view),
    path('logout/', views.logout)

    # 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Token Obtain by email and pw
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # obtain new access token by refresh
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # check token is valid or not
]