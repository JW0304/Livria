# backend/accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'',  AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='users')
# router.register(r'auth/users', AuthViewSet, basename='auth-user')
# router.register(r'auth', AuthViewSet, basename='auth')           # ✅ signup/login은 여기
# router.register(r'users', UserViewSet, basename='users')         # ✅ me (GET/PATCH)는 여기

urlpatterns = [
    path('', include(router.urls)),
    path('me/favorites', UserViewSet.as_view({'get': 'get_favorites'}), name='get_user_favorites'),
]
