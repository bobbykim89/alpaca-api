from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HelloSerializer

# Create your views here.


class HelloWorldView(APIView):
    def get(self, request):
        data = {"message": "Hello World"}
        serializer = HelloSerializer(data)
        return Response(serializer.data)


class HelloNameView(APIView):
    def get(self, request, name):
        message = f"Hello {name}!"
        serializer = HelloSerializer({'message': message})
        return Response(serializer.data)
