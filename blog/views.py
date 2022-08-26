from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import *


@api_view(["GET"])
def get_blog(request, id):
    data = {}
    instance = get_object_or_404(Blog, id=id)
    data = BlogSerializer(instance).data
    return Response(data)


@api_view(["GET"])
def get_blogs(request):
    data = {}
    instance = Blog.objects.all().order_by('date')
    if instance:
        data = BlogSerializer(instance, many=True).data
    return Response(data)


@api_view(["POST"])
def add_blog(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_blog(request, id):
    instance = get_object_or_404(Blog, id=id)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
def update_blog(request, id):
    instance = get_object_or_404(Blog, id=id)
    serializer = BlogSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# comments
@api_view(["GET"])
def get_comments(request, blog_id):
    data = {}
    instance = BlogComment.objects.filter(blog_id=blog_id).order_by("date")
    if instance:
        data = BlogSerializer(instance, many=True)
    return Response(data)


@api_view(["DELETE"])
def delete_comment(request, id):
    instance = get_object_or_404(BlogComment, id=id)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
def update_comment(request, id):
    instance = get_object_or_404(BlogComment, id=id)
    serializer = BlogCommentSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
