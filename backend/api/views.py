from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models      import Book, Author, Category, Genre, EmotionTag, Review, Music
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    GenreSerializer,
    EmotionTagSerializer,
    ReviewSerializer,
    MusicSerializer
)

class BookViewSet(viewsets.ModelViewSet):
    """
    도서 CRUD (읽기: 모두, 쓰기/수정/삭제: 인증 사용자)
    """
    queryset         = Book.objects.select_related('author','category','genre').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre']

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('books').all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.prefetch_related('books').all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

class EmotionTagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    감정 태그 읽기
    """
    queryset         = EmotionTag.objects.all()
    serializer_class = EmotionTagSerializer
    permission_classes = [permissions.AllowAny]

class ReviewViewSet(viewsets.ModelViewSet):
    """
    리뷰 CRUD (읽기: 모두, 쓰기/수정/삭제: 인증 사용자)
    """
    queryset         = Review.objects.select_related('book','user').all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MusicViewSet(viewsets.ModelViewSet):
    """
    자동생성 음악 기록의 CRUD
    """
    queryset = Music.objects.select_related('book').all()
    serializer_class   = MusicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]