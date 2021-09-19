from re import I
from django.db.models import fields
from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializing a single blog post"""

    content = serializers.CharField(required=False)
    author = serializers.CharField(required=False)

    class Meta:
        model = BlogPost
        fields = "__all__"


class PostLikeSerializer(serializers.Serializer):
    """Serrializer for the like requests"""

    like = serializers.CharField()
