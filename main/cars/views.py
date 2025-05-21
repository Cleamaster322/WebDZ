from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_csrf_token(request):
    token = get_token(request)
    return Response({'csrf_token': token})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def test(request):
    return Response({'test': 123321})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def test1(request):
    name = request.data.get('name','default value')
    return Response({'name': name})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test2(request):
    print(request.user)
    return Response({'test': 123321})


class Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

# Добавить пагинацию, фильтрацию, сортровку
class BrandListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            brands = Brand.objects.all()

            # filter by name
            name = request.GET.get('name')
            if name:
                brands = brands.filter(name__icontains=name)

            # sort
            ordering = request.GET.get('ordering')
            if ordering:
                brands = brands.order_by(ordering)

            paginator = Pagination()
            paginated_brands = paginator.paginate_queryset(brands, request)
            serializer = BrandSerializer(paginated_brands, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = BrandSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BrandDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            serializer_class = BrandSerializer(brand, many=False)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            serializer = BrandSerializer(brand, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            brand = Brand.objects.get(pk=kwargs['pk'])
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModelListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            models_car = Model.objects.all()

            # filter by name
            name = request.GET.get('name')
            if name:
                models_car = models_car.filter(name__icontains=name)

            # filter by brand_id
            brand_id = request.GET.get('brand_id')
            if brand_id:
                models_car = models_car.filter(brand_id=brand_id)

            # sort
            ordering = request.GET.get('ordering')
            if ordering:
                models_car = models_car.order_by(ordering)

            paginator = Pagination()
            paginated_models = paginator.paginate_queryset(models_car, request)
            serializer = ModelSerializer(paginated_models, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = ModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModelDetailAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            model = Model.objects.get(pk=kwargs['pk'])
            serializer = ModelSerializer(model, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            model = Model.objects.get(pk=kwargs['pk'])
            serializer = ModelSerializer(model, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            model = Model.objects.get(pk=kwargs['pk'])
            serializer = ModelSerializer(model, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            model = Model.objects.get(pk=kwargs['pk'])
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            generations = Generation.objects.all()

            # фильтрация по model_id
            model_id = request.GET.get('model_id')
            if model_id:
                generations = generations.filter(model_id=model_id)

            # сортировка
            ordering = request.GET.get('ordering')
            if ordering:
                generations = generations.order_by(ordering)

            paginator = Pagination()
            paginated_generations = paginator.paginate_queryset(generations, request)
            serializer = GenerationSerializer(paginated_generations, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = GenerationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerationDetailAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            generation = Generation.objects.get(pk=kwargs['pk'])
            serializer = GenerationSerializer(generation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Generation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            generation = Generation.objects.get(pk=kwargs['pk'])
            serializer = GenerationSerializer(generation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Generation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            generation = Generation.objects.get(pk=kwargs['pk'])
            serializer = GenerationSerializer(generation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Generation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            generation = Generation.objects.get(pk=kwargs['pk'])
            generation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Generation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)