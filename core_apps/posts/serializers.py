# blog/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post
from core_apps.accounts.serializers import UserSerializer
from core_apps.comments.serializers import CommentSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']



class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    created_at_formatted = serializers.SerializerMethodField()
    updated_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'author_name',
            'created_at', 'updated_at', 'created_at_formatted', 'updated_at_formatted',
            'total_likes', 'total_comments', 'is_liked', 'comments'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%B %d, %Y at %I:%M %p')

    def get_updated_at_formatted(self, obj):
        return obj.updated_at.strftime('%B %d, %Y at %I:%M %p')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.SerializerMethodField()
    total_likes = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()
    content_preview = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content_preview', 'author_name', 'author_full_name',
            'created_at', 'created_at_formatted', 'total_likes', 'total_comments', 'is_liked'
        ]

    def get_author_full_name(self, obj):
        if obj.author.first_name or obj.author.last_name:
            return f"{obj.author.first_name} {obj.author.last_name}".strip()
        return obj.author.username

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%B %d, %Y')

    def get_content_preview(self, obj):
        words = obj.content.split()
        if len(words) > 30:
            return ' '.join(words[:30]) + '...'
        return obj.content