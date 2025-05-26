from rest_framework import viewsets, permissions, filters
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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'genre']
    search_fields = ['title', 'author__name']
    def get_permissions(self):
        # list/retrieve(GET) 은 누구나, 나머지(POST/PUT/PATCH/DELETE)는 인증된 사용자
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

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

# ────────────────────────────────────────────────────────────────────────────────
#                       리뷰 전용 커스텀 퍼미션
# ────────────────────────────────────────────────────────────────────────────────
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    SAFE_METHODS(GET, HEAD, OPTIONS)은 모두 허용,
    POST/PUT/PATCH/DELETE 등 수정 요청은 작성자(user) 본인만 허용.
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 요청이면 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 쓰기/수정/삭제 요청일 때, 작성자 본인이어야 허용
        return obj.user == request.user

class ReviewViewSet(viewsets.ModelViewSet):
    """
    리뷰 CRUD (읽기: 모두, 쓰기/수정/삭제: 인증 사용자)
    """
    queryset         = Review.objects.select_related('book','user').all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

    def perform_create(self, serializer):
        # user 필드에 로그인한 사용자(request.user) 할당
        serializer.save(user=self.request.user)


class MusicViewSet(viewsets.ModelViewSet):
    """
    자동생성 음악 기록의 CRUD
    """
    queryset = Music.objects.select_related('book').all()
    serializer_class   = MusicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]