from rest_framework import viewsets, permissions
from .models      import Book, Author, Category, Genre, EmotionTag, Review
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    GenreSerializer,
    EmotionTagSerializer,
    ReviewSerializer
)

class BookViewSet(viewsets.ModelViewSet):
    """
    도서 CRUD (읽기: 모두, 쓰기/수정/삭제: 인증 사용자)
    """
    queryset         = Book.objects.select_related('author','category','genre').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    작가 목록/상세 (읽기만)
    """
    queryset         = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    카테고리(베스트셀러/신간/블로거 추천) 읽기
    """
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    장르(사용자 정의 7개) 읽기
    """
    queryset         = Genre.objects.all()
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
