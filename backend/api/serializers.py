from rest_framework import serializers
from .models import Book, Review

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "isbn",
            "title",
            "publisher",
            "cover_url",
            "description",
            "pub_date",
            "category",
            "global_recommend_count",
        ]


class BookDetailSerializer(BookSerializer):
    author_name    = serializers.CharField(source="author.name", read_only=True)
    author_image   = serializers.URLField(source="author.image_url", read_only=True)
    author_summary = serializers.CharField(source="author.summary", read_only=True)
    author_works   = serializers.ListField(source="author.works", read_only=True)

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + [
            "author_name",
            "author_image",
            "author_summary",
            "author_works",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "book",
            "content",
            "created_at",
        ]
