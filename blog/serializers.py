from .models import *
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            'content',
            "user_id"
        ]
        read_only_fields = ["date"]


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = [
            "id",
            "comment",
            "user_id",
            "blog_id"
        ]
        read_only_fields = ["date"]
