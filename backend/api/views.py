from rest_framework import viewsets, permissions
from .models     import Book, Author, Category, EmotionTag, Review
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    EmotionTagSerializer,
    ReviewSerializer,
)

class BookViewSet(viewsets.ModelViewSet):
    queryset         = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class EmotionTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = EmotionTag.objects.all()
    serializer_class = EmotionTagSerializer
    permission_classes = [permissions.AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset         = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
