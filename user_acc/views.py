from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import render
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'status':status.HTTP_201_CREATED})
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':serializer.errors})