from django.shortcuts import render

from rest_framework import viewsets

from .serializers import UserSerializer, TokenSerializer
from .models import User, Follow
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



@permission_classes([AllowAny])
@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = get_object_or_404(User, password=password, email=email)
    refresh = RefreshToken.for_user(user)
    token = {'token': str(refresh.access_token), }
    message = (
        f"'refresh': {(refresh)} \n"
        f"'access': {refresh.access_token}")
    return Response(token, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)