from .models import *
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            'content',
            "user",
            "votes",
        ]
        read_only_fields = ["date"]


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = [
            "id",
            "content",
            "user",
            "blog"
        ]
        read_only_fields = ["date"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["user", "blog"]