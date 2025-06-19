
from django.urls import path
from .views import ( RegisterUser, VerifyOTP, LoginUser,GetUserProfile, UpdateUserProfile,
    SetNewPassword, ChangePassword, RequestPasswordReset, CheckEmailAndSendOTP,
  VerifyResetOTP, DeleteAccount,Logout, ViewLoginActivity)
from django.shortcuts import render
from rest_framework_simplejwt.views import (
  TokenRefreshView, TokenVerifyView,
)

def register_page(request):
    return render(request, 'register.html')
def login_page(request):
    return render(request, 'login.html')
def verify_page(request):
    return render(request, 'verifyAccount.html')
def dashboard_page(request):
    return render(request, 'dashboard.html')
def profile_page(request):
    return render(request, 'profile.html')
def editProfile_page(request):
    return render(request, 'edit_profile.html')
def viewLog_page(request):
    return render(request, 'view_log.html')
def ChangePassword_page(request):
    return render(request, 'change_password.html')
def forgotPassword_page(request):
    return render(request, 'forgot_password.html')
def verifyOtpPassword_page(request):
    return render(request, 'verifyOtp.html')
def setPassword_page(request):
    return render(request, 'set_new_password.html')
urlpatterns = [
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    #user interface
     path('register/', register_page, name='register_page'),
     path('login/', login_page, name='login_page'),
     path('verify-otp/', verify_page, name='verify_page'),
     path('dashboard/', dashboard_page, name='dashboard_page'),
     path('profile/',profile_page, name='profile_page'),
     path('edit-profille/', editProfile_page, name='editProfile_page'),
     path('view-log/', viewLog_page, name='viewLog_page'),
     path('change-password/', ChangePassword_page, name='ChangePassword_page'),
     path('forgot-password/', forgotPassword_page, name='forgotPassword_page'),
     path('verifyOtp-password/', verifyOtpPassword_page, name='verifyOtpPassword_page'),
     path('set-password/', setPassword_page, name='setPassword_page'),
     
       # api route
    path('api/register/', RegisterUser.as_view(), name='register_api'),
    path('api/verify-otp/', VerifyOTP.as_view(), name='verify-api'),
    path('api/login/', LoginUser.as_view(), name='login'),
    path('api/logout/', Logout.as_view(), name='logout'),
    path('api/get-profile/', GetUserProfile.as_view(), name='get-profile'),

    path('api/update-profile/', UpdateUserProfile.as_view(), name='update-profile'),
    path('api/change-password/', ChangePassword.as_view(), name='change-password'),
    path('api/reset-password/', RequestPasswordReset.as_view()),
    path('api/password-reset/check-email/', CheckEmailAndSendOTP.as_view(), name='check_email_and_send_otp'),
    path('api/verify-reset-otp/', VerifyResetOTP.as_view(), name='verify_otp_page'),
    path('api/set-new-password/', SetNewPassword.as_view(),  name='set-new-password'),
    path('api/view-login-activity/', ViewLoginActivity.as_view(), name='view-login-activity'),
    path('api/deleteAccount/', DeleteAccount.as_view(), name='Delete-Account')
    
]