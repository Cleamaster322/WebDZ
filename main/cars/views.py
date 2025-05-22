from django.middleware.csrf import get_token
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny

from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    token = get_token(request)
    return Response({'csrf_token': token})

@api_view(['GET'])
@permission_classes([AllowAny])
def test(request):
    return Response({'test': 123321})

@api_view(['POST'])
@permission_classes([AllowAny])
def test1(request):
    name = request.data.get('name','default value')
    return Response({'name': name})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test2(request):
    print(request.user)
    return Response({'test': 123321})


class Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

# --- BRAND FUNCTIONS ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_brands(request):
    try:
        brands = Brand.objects.filter()

        name = request.GET.get('name')
        if name:
            brands = brands.filter(name__icontains=name)

        ordering = request.GET.get('ordering')
        if ordering:
            brands = brands.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(brands, request)
        serializer = BrandSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brand(request, pk):
    try:
        brand = Brand.objects.filter(pk=pk).first()
        if not brand:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BrandSerializer(brand)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_brand(request):
    try:
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_brand(request, pk):
    try:
        brand = Brand.objects.filter(pk=pk).first()
        if not brand:
            return Response(status=status.HTTP_404_NOT_FOUND)

        partial = request.method == 'PATCH'
        serializer = BrandSerializer(brand, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_brand(request, pk):
    try:
        brand = Brand.objects.filter(pk=pk).first()
        if not brand:
            return Response(status=status.HTTP_404_NOT_FOUND)

        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# --- MODEL FUNCTIONS ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_models(request):
    try:
        models = Model.objects.filter()

        name = request.GET.get('name')
        if name:
            models = models.filter(name__icontains=name)

        brand_id = request.GET.get('brand_id')
        if brand_id:
            models = models.filter(brand_id=brand_id)

        ordering = request.GET.get('ordering')
        if ordering:
            models = models.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(models, request)
        serializer = ModelSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model(request, pk):
    try:
        model = Model.objects.filter(pk=pk).first()
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ModelSerializer(model)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_model(request):
    try:
        serializer = ModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_model(request, pk):
    try:
        model = Model.objects.filter(pk=pk).first()
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)

        partial = request.method == 'PATCH'
        serializer = ModelSerializer(model, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_model(request, pk):
    try:
        model = Model.objects.filter(pk=pk).first()
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)

        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# --- GENERATION FUNCTIONS ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_generations(request):
    try:
        generations = Generation.objects.filter()

        model_id = request.GET.get('model_id')
        if model_id:
            generations = generations.filter(model_id=model_id)

        ordering = request.GET.get('ordering')
        if ordering:
            generations = generations.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(generations, request)
        serializer = GenerationSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_generation(request, pk):
    try:
        generation = Generation.objects.filter(pk=pk).first()
        if not generation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GenerationSerializer(generation)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_generation(request):
    try:
        serializer = GenerationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_generation(request, pk):
    try:
        generation = Generation.objects.filter(pk=pk).first()
        if not generation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        partial = request.method == 'PATCH'
        serializer = GenerationSerializer(generation, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_generation(request, pk):
    try:
        generation = Generation.objects.filter(pk=pk).first()
        if not generation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        generation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- CONFIGURATION FUNCTIONS ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_configurations(request):
    try:
        configurations = Configuration.objects.filter()

        generation_id = request.GET.get('generation_id')
        if generation_id:
            configurations = configurations.filter(generation_id=generation_id)

        ordering = request.GET.get('ordering')
        if ordering:
            configurations = configurations.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(configurations, request)
        serializer = ConfigurationSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_configuration(request, pk):
    try:
        configuration = Configuration.objects.filter(pk=pk).first()
        if not configuration:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ConfigurationSerializer(configuration)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_configuration(request):
    try:
        serializer = ConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_configuration(request, pk):
    try:
        configuration = Configuration.objects.filter(pk=pk).first()
        if not configuration:
            return Response(status=status.HTTP_404_NOT_FOUND)

        partial = request.method == 'PATCH'
        serializer = ConfigurationSerializer(configuration, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_configuration(request, pk):
    try:
        configuration = Configuration.objects.filter(pk=pk).first()
        if not configuration:
            return Response(status=status.HTTP_404_NOT_FOUND)

        configuration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
