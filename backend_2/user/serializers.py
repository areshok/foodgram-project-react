from rest_framework import serializers
from django.forms import ValidationError
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


from .models import User


#user_1 = User.objects.get(username='admin')
#print(user_1.check_password('Areshok1980'))
class TokenSerializers(serializers.ModelSerializer):
    #email = serializers.CharField(required=True)
    #password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('email', 'password')


    def validate(self, data):
        #return super().validate(attrs)
        email = data.get('email')
        password = data.get('password')
        print(email)
        print(password)
        user = get_object_or_404(User, email=email)
        user_auth = authenticate(username=user.username, password=password)
        print('user_auth')
        print(user_auth)
        print('serialis')
        if user_auth is not None:
            return data
        else:
            raise ValidationError("invalid_credentials")

       
        #print('test password')
        #print(user.check_password(password))



    '''
    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")
        user = User.objects
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")
    ''' 

        
