from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet,
    AuthorViewSet,
    CategoryViewSet,
    GenreViewSet,
    EmotionTagViewSet,
    MusicViewSet,
    ReviewViewSet,
    BookRecommendationView
)

router = DefaultRouter()
router.register(r'books',       BookViewSet)
router.register(r'authors',     AuthorViewSet)
router.register(r'categories',  CategoryViewSet)
router.register(r'genres',      GenreViewSet)
router.register(r'musics',        MusicViewSet)
router.register(r'emotion-tags',EmotionTagViewSet)
router.register(r'reviews',     ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:book_id>/recommendations/', BookRecommendationView.as_view(), name='book-recommendations'),
]  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
