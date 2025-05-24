from rest_framework import serializers
from .models import Book, Review, Author, Category, Genre, EmotionTag

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Author
        fields = ['name','image_url','summary','works']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Genre
        fields = ['name']

class EmotionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EmotionTag
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    author   = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    genre    = GenreSerializer(read_only=True)

    class Meta:
        model  = Book
        fields = [
            'isbn','title','publisher','cover_url','description',
            'pub_date','category','genre','global_recommend_count','author'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ['id','book','user','content','created_at']
        read_only_fields = ['id','created_at']
