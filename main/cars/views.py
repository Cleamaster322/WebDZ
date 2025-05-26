from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.middleware.csrf import get_token
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .word_utils import create_car_word_doc


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
    name = request.data.get('name', 'default value')
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


# --- CAR-DATA FUNCTIONS ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_car_data(request):
    try:
        car_data = CarData.objects.filter()

        # фильтрация по configuration_id
        configuration_id = request.GET.get('configuration_id')
        if configuration_id:
            car_data = car_data.filter(configuration_id=configuration_id)

        ordering = request.GET.get('ordering')
        if ordering:
            car_data = car_data.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(car_data, request)
        serializer = CarDataSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_car_data(request, pk):
    try:
        car_data = CarData.objects.get(pk=pk)
        serializer = CarDataSerializer(car_data)
        return Response(serializer.data)
    except CarData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_car_data(request):
    serializer = CarDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_car_data(request, pk):
    try:
        car_data = CarData.objects.get(pk=pk)
    except CarData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CarDataSerializer(car_data, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_car_data(request, pk):
    try:
        car_data = CarData.objects.get(pk=pk)
        car_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CarData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# --- Protocol FUNCTIONS ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_protocol(request):
    try:
        protocol_data = Protocol.objects.filter()

        # фильтрация по configuration_id
        user_id = request.GET.get('user_id')
        if user_id:
            protocol_data = protocol_data.filter(user_id=user_id)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(protocol_data, request)
        serializer = ProtocolSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol(request, pk):
    try:
        protocol_data = Protocol.objects.get(pk=pk)
        serializer = ProtocolSerializer(protocol_data)
        return Response(serializer.data)
    except CarData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol(request):
    data = request.data.copy()
    data['user'] = request.user.id  # подставляем ID текущего пользователя

    serializer = ProtocolSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- USER FUNCTIONS ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_word(request):
    """
    Принимает JSON с данными автомобиля, создает Word-файл и возвращает для скачивания.
    """
    try:
        data = request.data  # данные из POST-запроса

        # Создаем Word-документ в памяти
        word_file = create_car_word_doc(data)
        # --- Отправка уведомления в WebSocket группу ---
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "reports",
            {
                "type": "send_report_notification",
                "data": {
                    "user": request.user.username,
                    "date": word_file.created_at.isoformat() if hasattr(word_file, 'created_at') else "",
                    # если есть дата
                    "message": f"Отчёт создан пользователем {request.user.username}"
                }
            }
        )
        # ---------------------------------------------
        # Формируем ответ с вложением для скачивания
        response = HttpResponse(
            word_file.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        filename = f"{data.get('brand', 'car')}_{data.get('model', '')}.docx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except Exception as e:
        return Response({"error": str(e)}, status=500)
