
from django.urls import path
from .views import ( RegisterUser, VerifyOTP, LoginUser, UpdateUserProfile, ChangePassword, RequestPasswordReset,
 ConfirmPasswordReset, DeleteAccount,Logout, ViewLoginActivity)
from django.shortcuts import render
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

def register_page(request):
    return render(request, 'register.html')
def login_page(request):
    return render(request, 'login.html')
def verify_page(request):
    return render(request, 'verifyAccount.html')
urlpatterns = [
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    #user interface
     path('register/', register_page, name='register_page'),
     path('login/', login_page, name='login_page'),
     path('verify-otp/', verify_page, name='verify_page'),
       # api route
    path('api/register/', RegisterUser.as_view(), name='register_api'),
    path('api/verify-otp/', VerifyOTP.as_view(), name='verify-api'),
    path('api/login/', LoginUser.as_view(), name='login'),
    path('api/logout/', Logout.as_view(), name='logout'),
    path('api/update-profile/', UpdateUserProfile.as_view(), name='update-profile'),
    path('api/change-password/', ChangePassword.as_view(), name='change-password'),
    path('api/reset-password-request/', RequestPasswordReset.as_view(), name='reset-password-request'),
    path('api/reset-password-confirm/', ConfirmPasswordReset.as_view(), name='reset-password-confirm'),
    path('api/view-login-activity/', ViewLoginActivity.as_view(), name='view-login-activity'),
    path('api/deleteAccount/', DeleteAccount.as_view(), name='Delete-Account')
    
]