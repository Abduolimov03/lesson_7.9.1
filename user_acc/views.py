from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import render
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerilizer
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.validated_data, 'status':status.HTTP_201_CREATED})
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':serializer.errors})


class LoginApi(APIView):
    def post(self, request):
        serializer = LoginSerilizer(data=request.data)
        if serializer.is_valid():
            return Response({'status':status.HTTP_200_OK, 'data':serializer.validated_data})
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})

class LogoutApi(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'msg':'Siz dasturdan chiqdingiz', 'status':status.HTTP_200_OK})
        except Exception as e:
            return Response({'error':e , 'status':status.HTTP_400_BAD_REQUEST})
