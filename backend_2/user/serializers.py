from django.contrib.auth import authenticate
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

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
        request = self.context.get('request', None)
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


class SubscriptionSerializers(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()

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

    def get_recipes(self, obj):
        request = self.context.get('request')
        pass
