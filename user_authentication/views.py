from django.shortcuts import get_object_or_404
from .models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    instance = User.objects.filter(email=request.data["email"])
    if serializer.is_valid() and not instance:
        serializer.save()
        return Response({"msg": "Account created"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"msg": "Username or email is already in the database."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    instance = get_object_or_404(User, id=user_id)
    instance.delete()
    return Response({"msg": "User has been deleted to the database"}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    instance = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response({"msg": "User information updated"}, status=status.HTTP_200_OK)
