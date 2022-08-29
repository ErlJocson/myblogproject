from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import *
from .models import *


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
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_blog(request, blog_id):
    instance = get_object_or_404(Blog, id=blog_id)
    instance.delete()
    return Response({"msg": "Blog deleted"}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_blog(request, blog_id):
    instance = get_object_or_404(Blog, id=blog_id)
    if instance.title == request.data["title"] and instance.content == request.data["content"]:
        return Response({"msg": "There was nothing to update"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = BlogSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"msg": "There was an error"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_comments(request, blog_id):
    instance = BlogComment.objects.filter(blog_id=blog_id).order_by("date")
    if instance:
        data = BlogCommentSerializer(instance, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    return Response({"msg": "There are no comments"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_comment(request):
    serializer = BlogCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"msg": "There was an error"}, status=status.HTTP_400_BAD_REQUEST)


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
    return Response(status=status.HTTP_400_BAD_REQUEST)


# anonymous comments
# the following functions will allow anyone to comment on a blog
@api_view(["GET"])
def get_comments_anonymous(request):
    instances = AnonymousComment.objects.all().order_by("date")
    if instances:
        data = AnonymousCommentSerializer(instances, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    return Response({"msg": "There are no anonymous comments"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def add_comments_anonymous(request):
    serializer = AnonymousCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"msg": "There was an error"}, status=status.HTTP_400_BAD_REQUEST)
