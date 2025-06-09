from rest_framework import serializers
from .models import Book, Review, Author, Category, Genre, EmotionTag, Music, MusicReaction

class SimilarBookSerializer(serializers.ModelSerializer):
    """
    추천 도서 4권에 대해 id, title, cover_url만 직렬화
    """
    class Meta:
        model = Book
        fields = ('id', 'title', 'cover_url')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='book-detail'
    )
    class Meta:
        model  = Author
        fields = ['url', 'id', 'name', 'summary', 'books']

class EmotionTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = EmotionTag
        fields = ['url', 'id', 'name']

class MusicSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = ["id", "tag", "audio_url"]

    def get_audio_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.audio_file.url)

class MusicReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicReaction
        fields = ['music', 'is_like']

class BookSerializer(serializers.HyperlinkedModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)
    similar_books = SimilarBookSerializer(many=True, read_only=True)

    url = serializers.HyperlinkedIdentityField(view_name="book-detail", read_only=True)
    author           = serializers.HyperlinkedRelatedField(read_only=True, view_name='author-detail')
    category         = serializers.HyperlinkedRelatedField(read_only=True, view_name='category-detail')
    genre            = serializers.HyperlinkedRelatedField(read_only=True, view_name='genre-detail')

    author_name      = serializers.CharField(source='author.name', read_only=True)
    author_summary   = serializers.CharField(source='author.summary', read_only=True)
    author_image_url = serializers.CharField(source='author.image_url', read_only=True)
    
    category_name    = serializers.CharField(source='category.name', read_only=True)
    genre_name       = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'url', 'id', 'isbn', 'title', 'publisher', 'cover_url',
            'description', 'pub_date',
            'category', 'category_name',
            'genre', 'genre_name',
            'author', 'author_name', 'author_summary', 'author_image_url',
            'global_recommend_count',
            'musics',
            'similar_books',  # 추가된 추천 도서 필드
        ]

class CategorySerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True, context={'request': None})
    class Meta:
        model  = Category
        fields = ['id', 'name', 'books']

class GenreSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True, context={'request': None})
    class Meta:
        model  = Genre
        fields = ['id', 'name', 'books']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_avatar = serializers.SerializerMethodField()
    book_cover_url = serializers.SerializerMethodField()
    book_id = serializers.IntegerField(source='book.id', read_only=True)

    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    def get_user_avatar(self, obj):
        request = self.context.get('request')
        url = obj.user.get_avatar_url()
        return request.build_absolute_uri(url) if url else None
    
    def get_book_cover_url(self, obj):
        return obj.book.cover_url

    class Meta:
        model  = Review
        fields = [
            'id', 'book_id', 'book_cover_url', 'book',
            'user', 'user_avatar', 'content', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'user_avatar']
