from django.contrib.auth import authenticate
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from receipt.models import Receipt
from .models import Subscription, User


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
        raise ValidationError("Неверные данные")


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
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
            'is_subscribed',
            'password'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return (
                Subscription.objects.filter(
                    user=request.user, author=obj
                ).exists())
        return False

    def create(self, validate_data):
        return User.objects.create_user(
            username=validate_data['username'],
            email=validate_data['email'],
            first_name=validate_data['first_name'],
            last_name=validate_data['last_name'],
            password=validate_data['password'],
        )


class PasswordChangeSerialize(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=150,
    )
    current_password = serializers.CharField(
        max_length=150,
    )


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
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='author.receipt_user.count'
    )
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
        recipes_limit = self.context.get('recipes_limit')
        receipts = obj.author.receipt_user.all()[0:recipes_limit]
        serializer = ReceiptSubscribeSerializers(receipts, many=True)
        return serializer.data
