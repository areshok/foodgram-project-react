from rest_framework import serializers
from django.forms import ValidationError

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
        user = User.objects.get(email=email)

        print('test password')
        print(user.check_password(password))
        if user.check_password(password):
            return data
        else:
            raise ValueError('ошибка валидатора')

        
