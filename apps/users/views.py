from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import (
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserSerializer,
    UserSignupSerializer,
)

User = get_user_model()


# Create your views here.
class RegisterView(CreateModelMixin, GenericAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_verification_email(user)
        return Response({"detail": "회원가입 완료. 이메일을 확인하세요."}, status=status.HTTP_201_CREATED)

    def send_verification_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = f"http://localhost:8000/activate/{uid}/{token}"
        send_mail(
            subject="이메일 인증",
            message=f"링크를 클릭하여 이메일을 인증하세요: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


class EmailVerificationView(GenericAPIView):
    serializer_class = EmailVerificationSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "유효하지 않은 UID입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"detail": "이미 활성화된 계정입니다."}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save()
        return Response({"detail": "계정이 활성화 되었습니다."}, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Response body에 토큰 포함
        response_data = {
            "message": "성공적으로 로그인했습니다.",
            "access": access_token,
            "refresh": str(refresh),
        }

        response = Response(response_data, status=status.HTTP_200_OK)

        # 쿠키에도 토큰 저장
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Strict",
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            samesite="Strict",
        )
        return response


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 추가
        except Exception:
            return Response({"message": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "성공적으로 로그아웃했습니다."}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "계정이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
