from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user.models import Subscription, User

from .serializers import (PasswordChangeSerialize, TokenSerializers,
                          UserSerializers, SubscriptionSerializers)


class TokenViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    @action(
        detail=False,
        methods=['post', ],
        url_path='login',
        )
    def login(self, request):
        serializer = TokenSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            email=serializer.validated_data['email']
        )
        Token.objects.get_or_create(user=user)
        token = Token.objects.get(user=user).key
        message = {
            "auth_token": token
        }
        return Response(message, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['post', ],
        url_path='logout')
    def logout(self, request):
        user = request.user
        if Token.objects.filter(user=user).exists():
            Token.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (IsAuthenticated, )
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=('post',),
        url_path='set_password',
        permission_classes=(IsAuthenticated, ),
        serializer_class=PasswordChangeSerialize,
    )
    def set_password(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        check_password = user.check_password(
            serializer.data.get('current_password')
        )
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

    @action(
        detail=False,
        methods=('get',),
        url_path='subscriptions',
        permission_classes=(IsAuthenticated, ),
        #serializer_class=SubscriptionSerializers,
    )
    def subscriptions(self, request):
        if request.method == 'GET':
            user = request.user
            queryset = user.followers.all()
            #queryset = User.objects.filter(authors__user=self.request.user)
            page = self.paginate_queryset(queryset)
            print('serialize')
            serializer = SubscriptionSerializers(
                page,
                many=True,
                context={'user': user}
            )
            print('return')
            return self.get_paginated_response(serializer.data)

            '''
            queryset = User.objects.filter(authors__user=self.request.user)
            print('terst')
            page = self.paginate_queryset(queryset)

            if page is not None:
                print('fsdfsdfsdfsdf')
                serializer = SubscriptionSerializers(page, many=True)
                print('test 2')
                return self.get_paginated_response(serializer.data)
            print('test 3')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            '''
    @action(
        detail=True,
        methods=('post', 'delete')
    )
    def subscribe(self, request, pk):
        author = User.objects.get(id=pk)
        if request.method == 'POST':
            Subscription.objects.create(user=request.user, author=author)
        if request.method == 'DELETE':
            Subscription.objects.get(user=request.user, author=author).delete()
        return Response()
