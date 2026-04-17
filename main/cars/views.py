from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .word_utils import create_car_word_doc
from datetime import date

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Protocol,
    ProtocolMeasurement,
    ProtocolBrake,
    ProtocolLight,
    ProtocolPhoto,
)
from .serializers import (
    ProtocolSerializer,
    ProtocolMeasurementSerializer,
    ProtocolBrakeSerializer,
    ProtocolLightSerializer,
    ProtocolPhotoSerializer,
)
from .pagination import Pagination
from .models import Protocol
from .services.test_docx import generate_protocol_docx
from django.http import FileResponse

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


# =========================================================
# --- PROTOCOL FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_protocol(request):
    try:
        protocol_data = Protocol.objects.all().order_by('-created_at')

        user_id = request.GET.get('user_id')
        if user_id:
            protocol_data = protocol_data.filter(user_id=user_id)

        status_value = request.GET.get('status')
        if status_value:
            protocol_data = protocol_data.filter(status=status_value)

        car_id = request.GET.get('car_id')
        if car_id:
            protocol_data = protocol_data.filter(car_id=car_id)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(protocol_data, request)
        serializer = ProtocolSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol(request, pk):
    try:
        protocol_data = Protocol.objects.filter(pk=pk).first()
        if not protocol_data:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolSerializer(protocol_data)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol(request):
    try:
        data = request.data.copy()
        data['user'] = request.user.id

        if not data.get('protocol_number'):
            data['protocol_number'] = f"TMP-{request.user.id}-{date.today().strftime('%Y%m%d')}"

        if not data.get('protocol_date'):
            data['protocol_date'] = str(date.today())

        if not data.get('owner_name'):
            data['owner_name'] = 'Не указано'

        if not data.get('owner_type'):
            data['owner_type'] = 'individual'

        if not data.get('status'):
            data['status'] = 'draft'

        serializer = ProtocolSerializer(data=data)
        if serializer.is_valid():
            protocol = serializer.save()

            ProtocolMeasurement.objects.create(protocol=protocol)
            ProtocolBrake.objects.create(protocol=protocol)
            ProtocolLight.objects.create(protocol=protocol)

            return Response(ProtocolSerializer(protocol).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol(request, pk):
    try:
        protocol = Protocol.objects.filter(pk=pk).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        if 'user' not in data:
            data['user'] = protocol.user_id

        partial = request.method == 'PATCH'
        serializer = ProtocolSerializer(protocol, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- PROTOCOL-MEASUREMENT FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol_measurement(request, protocol_id):
    try:
        measurement = ProtocolMeasurement.objects.filter(protocol_id=protocol_id).first()
        if not measurement:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolMeasurementSerializer(measurement)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol_measurement(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        existing = ProtocolMeasurement.objects.filter(protocol_id=protocol_id).first()
        if existing:
            return Response(
                {'error': 'Measurement already exists for this protocol'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolMeasurementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol_measurement(request, protocol_id):
    try:
        measurement = ProtocolMeasurement.objects.filter(protocol_id=protocol_id).first()
        if not measurement:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        partial = request.method == 'PATCH'
        serializer = ProtocolMeasurementSerializer(measurement, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- PROTOCOL-BRAKE FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol_brake(request, protocol_id):
    try:
        brake = ProtocolBrake.objects.filter(protocol_id=protocol_id).first()
        if not brake:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolBrakeSerializer(brake)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol_brake(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        existing = ProtocolBrake.objects.filter(protocol_id=protocol_id).first()
        if existing:
            return Response(
                {'error': 'Brake already exists for this protocol'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolBrakeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol_brake(request, protocol_id):
    try:
        brake = ProtocolBrake.objects.filter(protocol_id=protocol_id).first()
        if not brake:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        partial = request.method == 'PATCH'
        serializer = ProtocolBrakeSerializer(brake, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- PROTOCOL-LIGHT FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol_light(request, protocol_id):
    try:
        light = ProtocolLight.objects.filter(protocol_id=protocol_id).first()
        if not light:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolLightSerializer(light)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol_light(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        existing = ProtocolLight.objects.filter(protocol_id=protocol_id).first()
        if existing:
            return Response(
                {'error': 'Light already exists for this protocol'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolLightSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol_light(request, protocol_id):
    try:
        light = ProtocolLight.objects.filter(protocol_id=protocol_id).first()
        if not light:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        partial = request.method == 'PATCH'
        serializer = ProtocolLightSerializer(light, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- PROTOCOL-PHOTO FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol_photos(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        photos = ProtocolPhoto.objects.filter(protocol_id=protocol_id).order_by('sort_order', 'id')
        serializer = ProtocolPhotoSerializer(photos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol_photo(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolPhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_protocol_photo(request, photo_id):
    try:
        photo = ProtocolPhoto.objects.filter(pk=photo_id).first()
        if not photo:
            return Response(status=status.HTTP_404_NOT_FOUND)

        photo.delete()
        return Response({'message': 'Photo deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- FULL PROTOCOL FUNCTION ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_full_protocol(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolFullSerializer(protocol)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


# =========================================================
# --- PROTOCOL-DOCX FUNCTIONS ---
# =========================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_protocol_docx_file(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(
                {'error': 'Protocol not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        file_path = generate_protocol_docx(protocol)

        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=f'protocol_{protocol.id}.docx',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )