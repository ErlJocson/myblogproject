from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import  BlogCommentSerializer, BlogSerializer, VoteSerializer
from .models import Blog, BlogComment, Vote


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_blog(request, blog_id):
    instance = get_object_or_404(Blog, id=blog_id)
    serializer = BlogSerializer(instance)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_blogs(request):
    instance = Blog.objects.all().order_by('date')
    if instance:
        data = BlogSerializer(instance, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    return Response({"msg": "There are no blogs"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_blog(request):
    """
    This function will add new blog to the database.

        Sample json object:
        {
            "title": "blog title",
            "content": "blog content",
            "user": 1
        }
    """
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"msg": "Saving new blog failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_blog(request, blog_id):
    instance = get_object_or_404(Blog, id=blog_id)
    instance.delete()
    return Response({"msg": "Blog deleted"}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_blog(request, blog_id):
    """
    This function will update a blog.

        Sample json object:
        {
            "title": "updated title",
            "content": "updated blog",
            "user": 1
        }
    """
    instance = get_object_or_404(Blog, id=blog_id)

    if instance.title == request.data["title"] and instance.content == request.data["content"]:
        return Response({"msg":"There was nothing to update"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = BlogSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_comments(request, blog_id):
    instance = BlogComment.objects.filter(blog_id=blog_id).order_by("date")
    if instance:
        data = BlogCommentSerializer(instance, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    return Response({"msg": "There are no comments"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_comment(request, comment_id):
    instance = get_object_or_404(BlogComment, id=comment_id)
    serializer = BlogCommentSerializer(instance)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_comment(request):
    serializer = BlogCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    instance = get_object_or_404(BlogComment, id=comment_id)
    instance.delete()
    return Response(status=status.HTTP_201_CREATED)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    instance = get_object_or_404(BlogComment, id=comment_id)
    if instance.comment == request.data["comment"]:
        return Response({"msg": "There was nothing to update"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = BlogCommentSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_vote(request, blog_id):
    instance = get_object_or_404(Blog, id=blog_id)
    serializer = VoteSerializer(user=request.user, blog=instance)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_vote(request, blog_id):
    instance = get_object_or_404(Blog, id=blog_id)
    vote_instance = get_object_or_404(Vote, blog_id=instance.id)
    vote_instance.delete()
    return Response(status=status.HTTP_200_OK)
    