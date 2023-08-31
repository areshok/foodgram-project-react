from rest_framework import serializers
from django.forms import ValidationError
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import AnonymousUser 
from .models import User, Follow

import datetime as dt

class FollowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(required=False, read_only=True,)
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
         
    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        print('request user')
        print(request.user)
        print(type(request.user))
        print(request.user is AnonymousUser)
        if str(request.user) == 'AnonymousUser':
            pass
        else:
            check_fol = Follow.objects.filter(user=request.user, following=obj).exists()
            if check_fol:
                return True
            else:
                return False
    
    


class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        #return super().validate(attrs)
        email = data.get('email')
        password = data.get('password')
        #print(email)
        #print(password)
        user = get_object_or_404(User, email=email)
        user_auth = authenticate(username=user.username, password=password)
        #print('user_auth')
        #print(user_auth)
        #print('serialis')
        if user_auth is not None:
            return data
        else:
            raise ValidationError("invalid_credentials")

  
class PasswordChangeSerialize(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()
