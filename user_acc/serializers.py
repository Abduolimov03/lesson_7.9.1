from rest_framework import serializers
from .models import CustomUser
from django.core.validators import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token

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
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)

        return user

    # def create(self, validated_data):
    #     validated_data.pop['cinfirm_password']
    #     user = CustomUser.objects.create_user(**validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()