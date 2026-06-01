from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer, UserProfileSerializer

class SignupView(generics.CreateAPIView):
    """
    회원가입 API

    username, email, nickname, password, password_confirm을 받아
    새 사용자를 생성하고 JWT 토큰(access, refresh)을 반환합니다.
    비밀번호 불일치 시 400 에러를 반환합니다.
    """
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

class MyProfileView(generics.RetrieveUpdateAPIView):
    """
    내 프로필 조회/수정 API

    - GET: 현재 로그인한 사용자의 프로필 정보를 반환
    - PUT/PATCH: 프로필 정보 수정 (email, nickname 변경 가능)

    인증 필요: JWT 토큰
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    """
    로그아웃 API

    refresh 토큰을 받아 블랙리스트에 등록하여 무효화합니다.
    성공 시 205 Reset Content를 반환합니다.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
