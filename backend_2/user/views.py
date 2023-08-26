from django.shortcuts import render
from .serializers import TokenSerializers
from rest_framework.decorators import action, api_view,  permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import User

@permission_classes([AllowAny])
@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, email=serializer.validated_data['email'])
    Token.objects.get_or_create(user=user)
    token = Token.objects.get(user=user).key
    message = {
        "auth_token": token
    }
    return Response(message, status=status.HTTP_201_CREATED)










