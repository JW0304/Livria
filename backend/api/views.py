# backend/api/views.py

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Book, Review
from .serializers import BookSerializer, BookDetailSerializer, ReviewSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    • list        GET /api/books/
    • retrieve    GET /api/books/{pk}/          → BookDetailSerializer
    • best-sellers GET /api/books/best-sellers/
    • new-items   GET /api/books/new-items/
    • category    GET /api/books/category/{cat}/?page=X
    • search      GET /api/books/search/?q=…&page=X
    """
    queryset = Book.objects.all().order_by("-pub_date")
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer

    @action(detail=False, methods=["get"], url_path="best-sellers")
    def best_sellers(self, request):
        qs = self.queryset.filter(category__name="베스트셀러")[:10]
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"], url_path="new-items")
    def new_items(self, request):
        qs = self.queryset.filter(category__name="신간")[:12]
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"], url_path="category/(?P<cat>[^/.]+)")
    def by_category(self, request, cat=None):
        page = int(request.query_params.get("page", 1))
        per  = 12
        qs   = self.queryset.filter(category__name=cat)
        start, end = (page-1)*per, page*per
        return Response({
            "total": qs.count(),
            "books": BookSerializer(qs[start:end], many=True).data
        })

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        q    = request.query_params.get("q", "")
        page = int(request.query_params.get("page", 1))
        per  = 12
        qs   = Book.objects.filter(title__icontains=q) | Book.objects.filter(author__name__icontains=q)
        start, end = (page-1)*per, page*per
        return Response({
            "total": qs.count(),
            "books": BookSerializer(qs[start:end], many=True).data
        })

class ReviewViewSet(viewsets.ModelViewSet):
    """
    • CRUD /api/reviews/
    """
    queryset = Review.objects.select_related("user", "book").all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
