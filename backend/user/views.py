from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import ReceiptPagination
from user.models import Subscription, User
from .serializers import (PasswordChangeSerialize, SubscriptionSerializers,
                          TokenSerializers, UserSerializers)


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
        Token.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = ReceiptPagination

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
            serializer.validated_data.get('current_password')
        )
        if check_password:
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(IsAuthenticated, ),
        serializer_class=UserSerializers,
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
    )
    def subscriptions(self, request):
        user = request.user
        print(request.query_params.get('recipes_limit'))
        queryset = user.followers.all()
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializers(
            page,
            many=True,
            context={'user': user}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, pk):
        message = {
            'post': {'errors': 'Вы уже подписались на этого пользователя'},
            'del': {'errors': 'Вы не подписанны на этого пользователя'},
        }
        user = request.user
        author = User.objects.get(id=pk)
        check = Subscription.objects.filter(
            user=request.user,
            author=author
        ).exists()

        if request.method == 'POST':
            if check:
                return Response(
                    message['post'],
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = Subscription.objects.create(
                user=request.user,
                author=author
            )
            serialize = SubscriptionSerializers(
                queryset,
                context={'user': user}
            )
            return Response(serialize.data)
        if check:
            Subscription.objects.get(
                user=request.user,
                author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            message['del'],
            status=status.HTTP_400_BAD_REQUEST
        )
