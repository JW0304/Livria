# backend/accounts/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import EmotionTag, DEFAULT_AVATAR_CHOICES
from api.serializers import BookSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    avatar_url     = serializers.SerializerMethodField()
    default_avatar = serializers.CharField(read_only=True)
    emotion_tags   = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=EmotionTag.objects.all()
    )
    favorites  = BookSerializer(many=True, read_only=True)
    read_books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'nickname', 'age', 'status_message',
            'avatar_url', 'default_avatar',
            'emotion_tags', 'favorites', 'read_books'
        ]
        read_only_fields = ['username', 'email']

    def get_avatar_url(self, obj):
        return obj.get_avatar_url()

class UserUpdateSerializer(serializers.ModelSerializer):
    emotion_tags   = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    default_avatar = serializers.ChoiceField(
        choices=[c[0] for c in DEFAULT_AVATAR_CHOICES],
        required=False, allow_blank=True
    )
    avatar         = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'nickname', 'age', 'status_message',
            'avatar', 'default_avatar', 'emotion_tags'
        ]

    def update(self, instance, validated_data):
        tags = validated_data.pop('emotion_tags', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if tags is not None:
            instance.emotion_tags.clear()
            for name in tags:
                tag, _ = EmotionTag.objects.get_or_create(name=name)
                instance.emotion_tags.add(tag)
        return instance
