from datetime import date

from channels.layers import get_channel_layer
from django.http import FileResponse, HttpResponse
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (
    Brand,
    Model,
    Generation,
    Configuration,
    CarData,
    Protocol,
    ProtocolMeasurement,
    ProtocolBrake,
    ProtocolLight,
    ProtocolPhoto,
    ProtocolTestCondition,
    ProtocolRoadCondition,
    ProtocolPowerSupply,
)
from .pagination import Pagination
from .serializers import (
    BrandSerializer,
    ModelSerializer,
    GenerationSerializer,
    ConfigurationSerializer,
    CarDataSerializer,
    ProtocolSerializer,
    ProtocolCreateSerializer,
    ProtocolMeasurementSerializer,
    ProtocolBrakeSerializer,
    ProtocolLightSerializer,
    ProtocolPhotoSerializer,
    ProtocolFullSerializer,
    ProtocolTestConditionSerializer,
    ProtocolRoadConditionSerializer,
    ProtocolPowerSupplySerializer,
    UserSerializer,
)
from .services.test_docx import generate_protocol_docx
from .word_utils import create_car_word_doc
from django.contrib.auth.models import User


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
    return Response({'test': 123321})


# =========================================================
# --- BRAND FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_brands(request):
    try:
        queryset = Brand.objects.all()

        name = request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        ordering = request.GET.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(queryset, request)
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

        serializer = BrandSerializer(
            brand,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
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


# =========================================================
# --- MODEL FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_models(request):
    try:
        queryset = Model.objects.all()

        name = request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        brand_id = request.GET.get('brand_id')
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        ordering = request.GET.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(queryset, request)
        serializer = ModelSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model(request, pk):
    try:
        obj = Model.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ModelSerializer(obj)
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
        obj = Model.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ModelSerializer(
            obj,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
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
        obj = Model.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- GENERATION FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_generations(request):
    try:
        queryset = Generation.objects.all()

        model_id = request.GET.get('model_id')
        if model_id:
            queryset = queryset.filter(model_id=model_id)

        ordering = request.GET.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(queryset, request)
        serializer = GenerationSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_generation(request, pk):
    try:
        obj = Generation.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GenerationSerializer(obj)
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
        obj = Generation.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GenerationSerializer(
            obj,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
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
        obj = Generation.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- CONFIGURATION FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_configurations(request):
    try:
        queryset = Configuration.objects.all()

        generation_id = request.GET.get('generation_id')
        if generation_id:
            queryset = queryset.filter(generation_id=generation_id)

        ordering = request.GET.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(queryset, request)
        serializer = ConfigurationSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_configuration(request, pk):
    try:
        obj = Configuration.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ConfigurationSerializer(obj)
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
        obj = Configuration.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ConfigurationSerializer(
            obj,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
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
        obj = Configuration.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- CAR-DATA FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_car_data(request):
    try:
        queryset = CarData.objects.all()

        configuration_id = request.GET.get('configuration_id')
        if configuration_id:
            queryset = queryset.filter(configuration_id=configuration_id)

        ordering = request.GET.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(queryset, request)
        serializer = CarDataSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_car_data(request, pk):
    try:
        obj = CarData.objects.get(pk=pk)
        serializer = CarDataSerializer(obj)
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


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_car_data(request, pk):
    try:
        obj = CarData.objects.get(pk=pk)
    except CarData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CarDataSerializer(
        obj,
        data=request.data,
        partial=(request.method == 'PATCH')
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_car_data(request, pk):
    try:
        obj = CarData.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CarData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# =========================================================
# --- PROTOCOL FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_protocols(request):
    try:
        queryset = Protocol.objects.all().order_by('-created_at')

        user_id = request.GET.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        status_value = request.GET.get('status')
        if status_value:
            queryset = queryset.filter(status=status_value)

        car_id = request.GET.get('car_id')
        if car_id:
            queryset = queryset.filter(car_id=car_id)

        paginator = Pagination()
        paginated = paginator.paginate_queryset(queryset, request)
        serializer = ProtocolSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol(request, pk):
    try:
        protocol = Protocol.objects.filter(pk=pk).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolSerializer(protocol)
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

        serializer = ProtocolCreateSerializer(data=data)
        if serializer.is_valid():
            protocol = serializer.save()
            return Response(
                ProtocolSerializer(protocol).data,
                status=status.HTTP_201_CREATED
            )

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
        data['user'] = protocol.user_id

        partial = request.method == 'PATCH'
        serializer = ProtocolSerializer(protocol, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_protocol(request, pk):
    try:
        protocol = Protocol.objects.filter(pk=pk).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        protocol.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- PROTOCOL-MEASUREMENT FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol_measurement(request, protocol_id):
    try:
        obj = ProtocolMeasurement.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolMeasurementSerializer(obj)
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
        obj = ProtocolMeasurement.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolMeasurementSerializer(
            obj,
            data=data,
            partial=(request.method == 'PATCH')
        )
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
        obj = ProtocolBrake.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolBrakeSerializer(obj)
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
        obj = ProtocolBrake.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolBrakeSerializer(
            obj,
            data=data,
            partial=(request.method == 'PATCH')
        )
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
        obj = ProtocolLight.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolLightSerializer(obj)
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
        obj = ProtocolLight.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolLightSerializer(
            obj,
            data=data,
            partial=(request.method == 'PATCH')
        )
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

        queryset = ProtocolPhoto.objects.filter(protocol_id=protocol_id).order_by('sort_order', 'id')
        serializer = ProtocolPhotoSerializer(queryset, many=True)
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


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol_photo(request, photo_id):
    try:
        obj = ProtocolPhoto.objects.filter(pk=photo_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = obj.protocol_id

        serializer = ProtocolPhotoSerializer(
            obj,
            data=data,
            partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_protocol_photo(request, photo_id):
    try:
        obj = ProtocolPhoto.objects.filter(pk=photo_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- PROTOCOL-TEST-CONDITIONS FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol_test_conditions(request, protocol_id):
    try:
        obj = ProtocolTestCondition.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolTestConditionSerializer(obj)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol_test_conditions(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        existing = ProtocolTestCondition.objects.filter(protocol_id=protocol_id).first()
        if existing:
            return Response(
                {'error': 'Test conditions already exist for this protocol'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolTestConditionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol_test_conditions(request, protocol_id):
    try:
        obj = ProtocolTestCondition.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolTestConditionSerializer(
            obj,
            data=data,
            partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- PROTOCOL-ROAD-CONDITIONS FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol_road_conditions(request, protocol_id):
    try:
        obj = ProtocolRoadCondition.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolRoadConditionSerializer(obj)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol_road_conditions(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        existing = ProtocolRoadCondition.objects.filter(protocol_id=protocol_id).first()
        if existing:
            return Response(
                {'error': 'Road conditions already exist for this protocol'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolRoadConditionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol_road_conditions(request, protocol_id):
    try:
        obj = ProtocolRoadCondition.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolRoadConditionSerializer(
            obj,
            data=data,
            partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =========================================================
# --- PROTOCOL-POWER-SUPPLY FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protocol_power_supply(request, protocol_id):
    try:
        obj = ProtocolPowerSupply.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProtocolPowerSupplySerializer(obj)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_protocol_power_supply(request, protocol_id):
    try:
        protocol = Protocol.objects.filter(pk=protocol_id).first()
        if not protocol:
            return Response(status=status.HTTP_404_NOT_FOUND)

        existing = ProtocolPowerSupply.objects.filter(protocol_id=protocol_id).first()
        if existing:
            return Response(
                {'error': 'Power supply already exists for this protocol'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolPowerSupplySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol_power_supply(request, protocol_id):
    try:
        obj = ProtocolPowerSupply.objects.filter(protocol_id=protocol_id).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['protocol'] = protocol_id

        serializer = ProtocolPowerSupplySerializer(
            obj,
            data=data,
            partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


# =========================================================
# --- USER FUNCTIONS ---
# =========================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    try:
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# =========================================================
# --- WORD FUNCTIONS ---
# =========================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_word(request):
    try:
        data = request.data
        word_file = create_car_word_doc(data)

        # если потом понадобится websocket-уведомление — слой уже доступен
        _channel_layer = get_channel_layer()

        response = HttpResponse(
            word_file.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        filename = f"{data.get('brand', 'car')}_{data.get('model', '')}.docx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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