from django.shortcuts import render

from rest_framework.decorators import action, api_view,  permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from user.models import User

from rest_framework import views

from .serializers import TokenSerializers, UserSerializers, PasswordChangeSerialize

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



class TokenDestroy(views.APIView):
    #permission_classes = AllowAny
    http_method_names = ['post']
    # нужна проверка на неавторизованого юзера, сделать сериализатор и там проверять user, тут только удалить токет
    def post(self, request):
        print(request)
        user = request.user
        print(user.username)
        if Token.objects.filter(user=user).exists():
            Token.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AllowAny, )

    @action(detail=False,
        methods=('post',),
        url_path='set_password',
        permission_classes=(IsAuthenticated, ),
        serializer_class=PasswordChangeSerialize,
    )
    def set_password(self, request):
        #print('hello')
        
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        check_password = user.check_password(serializer.data.get('current_password'))
        #print(check_password)
        #print(serializer.data.get('current_password'))
        if check_password:
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # прописать ошибку валидации старого пароля

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(IsAuthenticated, ),
        serializer_class=UserSerializers
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

