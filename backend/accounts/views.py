# backend/accounts/views.py

from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import EmotionTag
from .serializers import UserSerializer, UserUpdateSerializer

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    """
    signup/login 만 AllowAny
    """

    @action(
        detail=False,
        methods=['post'],
        url_path='signup',
        permission_classes=[permissions.AllowAny]
    )
    def signup(self, request):
        try:
            user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                email=request.data.get('email', ''),
                nickname=request.data.get('nickname'),
                age=request.data.get('age')
            )
        except IntegrityError:
            return Response(
                {'error': 'username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 감정 태그 추가
        for name in request.data.get('tags', []):
            tag, _ = EmotionTag.objects.get_or_create(name=name)
            user.emotion_tags.add(tag)

        token, _ = Token.objects.get_or_create(user=user)
        serialized_user = UserSerializer(user)

        return Response({
            'token': token.key,
            'user': serialized_user.data
        })

    @action(
        detail=False,
        methods=['post'],
        url_path='login',
        permission_classes=[permissions.AllowAny]
    )
    def login(self, request):
        """
        POST /api/auth/login
        { "username":"...", "password":"..." }
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request=request._request,
            username=username,
            password=password
        )
        if user is None:
            return Response(
                {'error': 'invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)
        serialized_user = UserSerializer(user)

        return Response({
            'token': token.key,
            'user': serialized_user.data
        })


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        """
        GET  /api/auth/users/me   → 현재 사용자 정보 반환
        PATCH /api/auth/users/me   → 사용자 정보 업데이트
        """
        if request.method == 'GET':
            # UserSerializer 호출 시 context={'request': request} 추가
            serializer = UserSerializer(
                request.user,
                context={'request': request}
            )
            return Response(serializer.data)

        # PATCH 처리
        update_serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()

        # 업데이트 후에도 context 포함해서 전체 필드 응답
        serializer = UserSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data)