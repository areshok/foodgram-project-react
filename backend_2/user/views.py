from django.shortcuts import render

from rest_framework.decorators import action, api_view,  permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from user.models import User, Subscription

from rest_framework import views

from .serializers import TokenSerializers, UserSerializers, PasswordChangeSerialize, SubscriptionSerializers, SubscriptionSerializers_1

# классы и функции

# -----------------------------------------------------------------------------------------------------
class TokenViewSet(viewsets.ViewSet):

    @action(
        detail=False,
        methods=['post',],
        url_path='login',
        )
    def login(self, request):
        serializer = TokenSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data['email'])
        Token.objects.get_or_create(user=user)
        token = Token.objects.get(user=user).key
        message = {
            "auth_token": token
        }
        return Response(message, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['post',],
        url_path='logout')
    def logout(self, request):
        user = request.user
        if Token.objects.filter(user=user).exists():
            Token.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# -----------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AllowAny, )
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
        check_password = user.check_password(serializer.data.get('current_password'))
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
        methods=('get', 'post', 'del'),
        url_path='subscriptions',
        permission_classes=(IsAuthenticated, ),
        #serializer_class=SubscriptionSerializers,
    )
    def subscriptions(self, request):
        if request.method == 'GET':
            queryset = Subscription.objects.filter(user=request.user)


            '''
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = SubscriptionSerializers_1(page, many=True)
                custom_data = serializer.data
                return Response(custom_data)

            #serializer = SubscriptionSerializers_1(page, many=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            #pass
            '''
            return Response(queryset)
# -----------------------------------------------------------------------------------------------------

class FollowViewSet(viewsets.ModelViewSet):
    #serializer_class = UserSerializers
    permission_classes = (IsAuthenticated,)
    #pagination_class = LimitOffsetPagination
    #filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    #filterset_fields = ('user', 'following')
    #search_fields = ('subscription__username',)

    def get_queryset(self):
        #user = self.request.user
        #print(user)
        #user_2 = User.objects.get(id=2)
        #print(user_2)
        #print(user.followers.all().values('author'))
        #return self.request.user.followers.all().prefetch_related('authors')
        #return Subscription.objects.all().prefetch_related('author')
        #return User.objects.all().prefetch_related('author')
        #return User.objects.select_related('')
        
        queryset = User.objects.filter(authors__user=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
                serializer = UserSerializers(page, many=True)
                custom_data = serializer.data
                return Response(custom_data)
        
        #return UserSerializers(User.objects.get(id=1), many=True)
        #User.objects.filter(followers_user=self.request.user)
        #serialize = UserSerializers(User.objects.filter(authors__user=self.request.user), many=True)
        #return UserSerializers(user.followers.all().values('author'), many=True)
        #return Response(serialize.data)

    # User.objects.filter(authors__user=user)
