from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterAPIView, LoginAPIView, UserProfileAPIView, ChangePasswordAPIView, UserProfileUpdateAPIView

urlpatterns = [
    #http://127.0.0.1:8000/api/register/
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # POST http://127.0.0.1:8000/api/login/
    #{
   # "email": "usha@gmail.com",
    #"password": "Nepal@456"
    #}
    path("login/", LoginAPIView.as_view(), name="login"),

    # GET http://127.0.0.1:8000/api/profile/
    path("profile/", UserProfileAPIView.as_view(), name="profile"),

    
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    
    # PATCH http://127.0.0.1:8000/api/student-profile/update/
    path("updated-profile/", UserProfileUpdateAPIView.as_view(), name="updated-profile"),

            
    
]