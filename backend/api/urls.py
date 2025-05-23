from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AuthViewSet, BookViewSet, ProfileViewSet, ReviewViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'auth',    AuthViewSet,    basename='auth')
router.register(r'books',   BookViewSet,    basename='books')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'reviews', ReviewViewSet,  basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
