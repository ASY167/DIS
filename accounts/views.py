from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import CustomUser, Profile, ActivityLog
from .serializers import (
    RegisterSerializer, UpdateUserProfileSerializer, UserProfileSerializer, ChangePasswordSerializer,
    ResetPasswordRequestSerializer,VerifyOTPSerializer, SetNewPasswordSerializer, LoginSerializer,
    LogoutSerializer, LoginActivitySerializer, AuditLogSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import pyotp
from django.utils.timezone import now
import pyotp
from django.contrib.auth.hashers import check_password
import datetime
# USER MANAGEMENT VIEWS
class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = pyotp.TOTP(user.totp_secret).now()
            send_mail(
                "Email Verification OTP",
                f"Your OTP is: {otp}",
                "noreply@example.com",
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Registration successful. Check your email for OTP."})
        return Response(serializer.errors, status=400)
class VerifyOTP(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get("username")
        otp = request.data.get("otp")
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        # Verify the OTP
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(otp,valid_window=1):
            user.is_email_verified = True
            user.save()
            return Response({"message": "OTP verified successfully!"})
        else:
            # Regenerate OTP if expired
            new_otp = totp.now()
            send_mail(
                "Your New OTP Code",
                f"Your new OTP code is: {new_otp}",
                "noreply@example.com",
                [user.email],
                fail_silently=False,
            )
            return Response({"error": "Invalid OTP. A new OTP has been sent."}, status=401)

# Helper function to get JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(username=username, password=password)

            if not user:
                return Response({"error": "Invalid username or password"}, status=401)

            if not user.is_email_verified:
                return Response({"error": "Email not verified. Please verify your email first."}, status=403)

            ActivityLog.objects.create(
                user=user,
                action='login activity',
                ip_address=self.get_client_ip(request),
                timestamp=datetime.datetime.now(),
                was_successful=True,
            )

            tokens = get_tokens_for_user(user)
            return Response({"message": "User login successful.", "tokens": tokens})

        return Response(serializer.errors, status=400)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class UpdateUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateUserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!"})
        return Response(serializer.errors, status=400)

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not check_password(serializer.validated_data['old_password'], request.user.password):
                return Response({"error": "Incorrect old password"}, status=400)
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Password changed successfully!"})
        return Response(serializer.errors, status=400)
class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(email=serializer.validated_data['email'])
                otp = pyotp.TOTP(user.totp_secret).now()
                send_mail(
                    "Password Reset OTP",
                    f"Your OTP is: {otp}",
                    "noreply@example.com",
                    [user.email],
                    fail_silently=False,
                )
                return Response({"message": "Password reset OTP sent to your email."})
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=404)
        return Response(serializer.errors, status=400)

class CheckEmailAndSendOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
            otp = pyotp.TOTP(user.totp_secret).now()

            send_mail(
                "Your Password Reset OTP",
                f"Your OTP is: {otp}",
                "noreply@example.com",
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent successfully."})
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=404)
class VerifyResetOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(email=serializer.validated_data['email'])
                totp = pyotp.TOTP(user.totp_secret)
                if totp.verify(serializer.validated_data['otp'], valid_window=1):
                    return Response({"message": "OTP verified successfully"})
                return Response({"error": "Invalid or expired OTP"}, status=400)
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=404)
        return Response(serializer.errors, status=400)

# views.py
class SetNewPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(email=serializer.validated_data['email'])
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"message": "Password reset successfully!"})
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=404)
        return Response(serializer.errors, status=400)

class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response({"message": "Account deleted successfully!"})
# User Management Endpoints
class Logout(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = RefreshToken(serializer.validated_data['refresh'])
                token.blacklist()  # Requires Blacklist app from simplejwt
                return Response({"message": "Successfully logged out."})
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        return Response(serializer.errors, status=400)
class ViewLoginActivity(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = ActivityLog.objects.filter(user=request.user)
        serializer = LoginActivitySerializer(activities, many=True)
        return Response(serializer.data)
