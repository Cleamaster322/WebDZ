from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class TestAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response("123get", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(data['message'], status=status.HTTP_200_OK)
