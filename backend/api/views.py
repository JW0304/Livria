from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Book, Profile, Review, EmotionTag
from .serializers import (
    BookSerializer,
    ProfileSerializer, ProfileUpdateSerializer,
    ReviewSerializer
)

# --- 인증(Signup/Login) ViewSet ---
class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, request):
        username = request.data['username']
        password = request.data['password']
        # User 생성
        user = User.objects.create_user(username=username, password=password)
        # Profile 생성
        profile = Profile.objects.create(
            user=user,
            nickname=request.data.get('nickname', ''),
            age=request.data.get('age', None)
        )
        # 태그 추가
        for name in request.data.get('tags', []):
            tag, _ = EmotionTag.objects.get_or_create(name=name)
            profile.emotion_tags.add(tag)
        # 토큰 생성·반환
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        # DRF의 ObtainAuthToken 사용
        return ObtainAuthToken().post(request)

# --- 도서 관련 ViewSet ---
class BookViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, url_path='best-sellers')
    def best_sellers(self, request):
        qs = Book.objects.order_by('-global_recommend_count')[:10]
        return Response(BookSerializer(qs, many=True).data)

    @action(detail=False, url_path='recommendations')
    def recommendations(self, request):
        qs = Book.objects.order_by('?')[:5]
        return Response(BookSerializer(qs, many=True).data)

    @action(detail=False, url_path='list')
    def list_all(self, request):
        page = int(request.query_params.get('page', 1))
        per  = 12
        qs   = Book.objects.all()
        total= qs.count()
        data = qs[(page-1)*per: page*per]
        return Response({'total': total, 'books': BookSerializer(data, many=True).data})

    @action(detail=False, url_path='category/(?P<cat>[^/.]+)')
    def by_category(self, request, cat=None):
        page = int(request.query_params.get('page', 1))
        per  = 12
        qs   = Book.objects.filter(category__name=cat)
        total= qs.count()
        data = qs[(page-1)*per: page*per]
        return Response({'total': total, 'books': BookSerializer(data, many=True).data})

    @action(detail=False, url_path='search')
    def search(self, request):
        q    = request.query_params.get('q', '')
        page = int(request.query_params.get('page', 1))
        per  = 12
        qs   = (Book.objects.filter(title__icontains=q) |
                Book.objects.filter(author__name__icontains=q))
        total= qs.count()
        data = qs[(page-1)*per: page*per]
        return Response({'total': total, 'books': BookSerializer(data, many=True).data})

    @action(detail=True, url_path='detail')
    def detail(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        return Response(BookSerializer(book).data)

# --- 프로필 관련 ViewSet ---
class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, url_path='me')
    def retrieve_me(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        data = serializer.data
        data['favorites']  = data['favorites'][:3]
        data['read_books'] = data['read_books'][:3]
        return Response(data)

    @action(detail=False, methods=['patch'], url_path='me')
    def update_me(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'profile updated'})

    @action(detail=False, url_path='favorites-full')
    def favorites_full(self, request):
        profile = Profile.objects.get(user=request.user)
        return Response(BookSerializer(profile.favorites.all(), many=True).data)

    @action(detail=False, url_path='read-history')
    def read_history(self, request):
        profile = Profile.objects.get(user=request.user)
        return Response(BookSerializer(profile.read_books.all(), many=True).data)

    @action(detail=False, methods=['post'], url_path='password-change')
    def password_change(self, request):
        profile = Profile.objects.get(user=request.user)
        user    = profile.user
        old     = request.data.get('old_password')
        new     = request.data.get('new_password')
        if not user.check_password(old):
            return Response({'error': 'incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new)
        user.save()
        return Response({'status': 'password changed'})

# --- 리뷰 관련 ViewSet ---
class ReviewViewSet(viewsets.ModelViewSet):
    queryset         = Review.objects.select_related('user','book').all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
