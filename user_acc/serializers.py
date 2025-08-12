from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({'message':'Parollar mos emas', 'status':status.HTTP_400_BAD_REQUEST})
        username = data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError({'message':'Bu username orqali royxatdan otilgan', 'status':status.HTTP_400_BAD_REQUEST})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            age = validated_data['age'],
            address = validated_data['address'],
        )
        token = Token.objects.create(user=user)
        user.set_password(validated_data['password'])
        user.token = token.key
        user.save()

        return user



class LoginSerilizer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=120)
    password = serializers.CharField(max_length=120)
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def validate(self, data):
        if not data['username'] or not data['password']:
            raise ValidationError({'error':'Login yoki parol notogri', 'status':status.HTTP_400_BAD_REQUEST})
        try:
            authenticate(username=data['username'], password=data['password'])
            user = CustomUser.objects.get(username=data['username'])
            token , created = Token.objects.get_or_create(user = user)
        except Exception as e:
            raise ValidationError({'error':'Login yoki parol notogri', 'status':status.HTTP_400_BAD_REQUEST})
        data['token'] = token.key
        return data

