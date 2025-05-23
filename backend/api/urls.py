from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet,
    AuthorViewSet,
    CategoryViewSet,
    EmotionTagViewSet,
    ReviewViewSet,
)

router = DefaultRouter()
router.register(r'books',      BookViewSet)
router.register(r'authors',    AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'emotion-tags', EmotionTagViewSet)
router.register(r'reviews',    ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
