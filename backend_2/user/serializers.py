from rest_framework import serializers
from django.forms import ValidationError
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import AnonymousUser 
from .models import User, Subscription

import datetime as dt


# классы

# ТОКЕН  ГОТОВ
# -----------------------------------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------------------------------

# USER 
# -----------------------------------------------------------------------------------------------------
class UserSerializers(serializers.ModelSerializer):
    #is_subscribed = serializers.SerializerMethodField(required=False, read_only=True,)
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
         
    def get_is_subscribed(self, obj):
        pass
        
        request = self.context.get('request', None)
        if str(request.user) == 'AnonymousUser':
            return False
        else:
            check_fol = Subscription.objects.filter(user=request.user, author=obj).exists()
            if check_fol:
                return True
            else:
                return False
        
# -----------------------------------------------------------------------------------------------------

# Пароль
# -----------------------------------------------------------------------------------------------------
class PasswordChangeSerialize(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()
# -----------------------------------------------------------------------------------------------------

# Подписки
# -----------------------------------------------------------------------------------------------------
class SubscriptionSerializers(serializers.ModelSerializer):
    #author = serializers.StringRelatedField(many=True, read_only=True)
    #author = UserSerializers()
    class Meta:
        model = Subscription
        fields = '__all__'
# -----------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------
class SubscriptionSerializers_1(serializers.Serializer):
    author = UserSerializers()
# -----------------------------------------------------------------------------------------------------

class UserSuSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('authors',)  

