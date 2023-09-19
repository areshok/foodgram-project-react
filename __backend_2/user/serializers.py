from django.contrib.auth import authenticate
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Subscription, User
from receipt.models import Receipt

class TokenSerializers(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = get_object_or_404(User, email=email)
        user_auth = authenticate(username=user.username, password=password)
        if user_auth is not None:
            return data
        else:
            raise ValidationError("invalid_credentials")


class UserSerializers(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        print(f'asdasdasd {request}')
        if str(request.user) == 'AnonymousUser':
            return False
        else:
            return (
                Subscription.objects.filter(
                    user=request.user, author=obj
                ).exists())


class PasswordChangeSerialize(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()



class ReceiptSubscribeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

class SubscriptionSerializers(serializers.ModelSerializer):
    #recipes = serializers.SerializerMethodField()

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.r_user.count')
    is_subscribed = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('user')
        return Subscription.objects.filter(
            author=obj.author,
            user=user
        ).exists()

    def get_recipes(self, obj):
        receipts = obj.author.r_user.all()
        serializer = ReceiptSubscribeSerializers(receipts, many=True)
        return serializer.data