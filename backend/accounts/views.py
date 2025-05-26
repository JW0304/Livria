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
from api.models import Book

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

class UserViewSet(viewsets.ModelViewSet):
    """
    사용자 정보 조회/수정 + 읽음/찜 토글
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'pk'

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        """
        GET  /api/auth/users/me     → 현재 사용자 정보 반환  
        PATCH /api/auth/users/me    → 사용자 정보 업데이트
        """
        if request.method == 'GET':
            serializer = UserSerializer(request.user, context={'request': request})
            return Response(serializer.data)

        # PATCH
        update_serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()

        # 변경된 정보 다시 반환
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'delete'], url_path=r'me/favorites/(?P<book_pk>[^/.]+)')
    def favorites(self, request, book_pk=None):
        """
        POST   /api/auth/users/me/favorites/{book_pk}   → 찜 추가  
        DELETE /api/auth/users/me/favorites/{book_pk}   → 찜 해제
        """
        user = request.user
        try:
            book = Book.objects.get(pk=book_pk)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            user.favorites.add(book)
            return Response({'detail': 'Added to favorites.'}, status=status.HTTP_201_CREATED)

        user.favorites.remove(book)
        return Response({'detail': 'Removed from favorites.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post', 'delete'], url_path=r'me/read_books/(?P<book_pk>[^/.]+)')
    def read_books(self, request, book_pk=None):
        """
        POST   /api/auth/users/me/read_books/{book_pk}   → 읽음 추가  
        DELETE /api/auth/users/me/read_books/{book_pk}   → 읽음 해제
        """
        user = request.user
        try:
            book = Book.objects.get(pk=book_pk)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            user.read_books.add(book)
            return Response({'detail': 'Marked as read.'}, status=status.HTTP_201_CREATED)

        user.read_books.remove(book)
        return Response({'detail': 'Unmarked as read.'}, status=status.HTTP_204_NO_CONTENT)