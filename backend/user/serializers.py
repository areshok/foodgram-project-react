from rest_framework import serializers

from .models import User



class TokenSerializers(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        #return super().validate(attrs)
        
