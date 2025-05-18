from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .models import Brand
from .serializers import BrandSerializer

class TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("123get", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        return Response(data['message'], status=status.HTTP_200_OK)

# Добавить пагинацию, фильтрацию, сортровку
class BrandListAPIView(APIView):
    permission_classes = [IsAdminUser]
    # get all brands
    def get(self, request, *args, **kwargs):
        brands = Brand.objects.all()
        serializer_class = BrandSerializer(brands, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    # create new brand
    def post(self, request, *args, **kwargs):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# brand by id
class BrandDetailAPIView(APIView):

    # get brand by id
    def get(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            serializer_class = BrandSerializer(brand, many=False)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            serializer = BrandSerializer(brand, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update not full data brand by id
    def patch(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            serializer = BrandSerializer(brand, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # delete brand by id
    def delete (self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


