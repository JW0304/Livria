from rest_framework import serializers
from .models import Book, Review, Author, Category, Genre, EmotionTag, Music

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='book-detail'
    )
    class Meta:
        model  = Author
        fields = ['url','id','name','summary','books']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='book-detail'
    )
    class Meta:
        model  = Category
        fields = ['url', 'id', 'name', 'books']

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='book-detail'
    )
    class Meta:
        model  = Genre
        fields = ['url', 'id', 'name', 'books']

class EmotionTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = EmotionTag
        fields = ['url','id','name']

class BookSerializer(serializers.HyperlinkedModelSerializer):
    author   = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='author-detail'
    )
    category = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='category-detail'
    )
    genre    = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='genre-detail'
    )
    class Meta:
        model  = Book
        fields = [
            'url','id','isbn','title','publisher','cover_url',
            'description','pub_date','category','genre',
            'global_recommend_count','author'
        ]


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    book = serializers.HyperlinkedRelatedField(read_only=True, view_name='book-detail')
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    class Meta:
        model  = Review
        fields = ['url','id','book','user','content','created_at']
    def create(self, validated_data):
        # 작성자는 요청한 user로 설정
        request = self.context.get('request')
        return Review.objects.create(user=request.user, **validated_data)
    
class MusicSerializer(serializers.HyperlinkedModelSerializer):
    book = serializers.HyperlinkedRelatedField(read_only=True, view_name='book-detail')
    class Meta:
        model  = Music
        fields = ['url','id','book','tag','audio_file','created_at']