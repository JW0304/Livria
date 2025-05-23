from rest_framework import serializers
from .models import Book, Author, Category, EmotionTag, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'image_url', 'summary', 'works']


class BookSerializer(serializers.ModelSerializer):
    author   = AuthorSerializer()
    category = CategorySerializer()

    class Meta:
        model  = Book
        fields = [
            'id',
            'isbn',
            'title',
            'publisher',
            'cover_url',
            'description',
            'pub_date',
            'category',
            'global_recommend_count',
            'author',
        ]


class EmotionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EmotionTag
        fields = ['name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ['id', 'book', 'user', 'content', 'created_at']
