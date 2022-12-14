from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import BlogCommentSerializer, BlogSerializer, VoteSerializer
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
        return Response({"msg": "There was nothing to update"}, status=status.HTTP_400_BAD_REQUEST)

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
    """
    This function adds new comments in the database.

    sample json object:
    {
        "content": "blog comment",
        "user": 1,
        "blog": 1
    }

    user and blog are integers that represent 
    the id of the user and blog
    """
    serializer = BlogCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    instance = get_object_or_404(BlogComment, id=comment_id)
    if instance:
        instance.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    """
    This function updates a comment

    sample json object:
    {
        "content":"Updated comment",
        "user":1,
        "blog":1
    }
    
    user and blog are integers that represent
    the id of the user and the id of the blog
    """
    instance = get_object_or_404(BlogComment, id=comment_id)
    if instance.content == request.data["content"]:
        return Response({"msg": "There was nothing to update"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = BlogCommentSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_vote(request, blog_id):
    """
    This function will add new votes to the database.
    Sample json object:
    {
        "user": 1,
        "blog": 1
    }
    """
    instance = get_object_or_404(Blog, id=blog_id)
    check_if_already_voted = Vote.objects.filter(user=request.user.id, blog=blog_id)
    if not check_if_already_voted:
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance.votes = instance.votes + 1
            instance.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Cannot vote the blog"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"msg": "You've already voted the blog"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_vote(request, blog_id):
    instance = get_object_or_404(Blog, id=blog_id)
    vote_instance = get_object_or_404(Vote, blog=instance.id)
    if instance and vote_instance:
        instance.votes = instance.votes - 1
        vote_instance.delete()
        instance.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
