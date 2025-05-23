from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Author, Book,
    EmotionTag, Profile, Review
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author   = AuthorSerializer()
    category = CategorySerializer()
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'cover_url',
            'description', 'isbn', 'pub_date', 'category'
        ]

class EmotionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionTag
        fields = ['id', 'name']

class ProfileSerializer(serializers.ModelSerializer):
    emotion_tags = EmotionTagSerializer(many=True)
    favorites    = BookSerializer(many=True)
    read_books   = BookSerializer(many=True)
    class Meta:
        model = Profile
        fields = [
            'nickname', 'age', 'avatar_url',
            'status_message', 'emotion_tags',
            'favorites', 'read_books'
        ]

class ProfileUpdateSerializer(serializers.ModelSerializer):
    # 감성 태그 이름 리스트로 받기
    emotion_tags = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    class Meta:
        model = Profile
        fields = [
            'nickname', 'age', 'avatar_url',
            'status_message', 'emotion_tags'
        ]

    def update(self, instance, validated_data):
        tags = validated_data.pop('emotion_tags', None)
        # 기본 필드 업데이트
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        # 태그 업데이트
        if tags is not None:
            instance.emotion_tags.clear()
            for name in tags:
                tag, _ = EmotionTag.objects.get_or_create(name=name)
                instance.emotion_tags.add(tag)
        return instance

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'content', 'created_at']
