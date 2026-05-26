from datetime import date

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from django.http import FileResponse, HttpResponse
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.files.storage import default_storage

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
    GenerationCardSerializer,
    CarDataProtocolSerializer,
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
    CreateUserSerializer,
    UpdateUserSerializer,
)
from .services.test_docx import generate_protocol_docx
from .word_utils import create_car_word_doc


# =========================================================
# --- HELPERS ---
# =========================================================

def notify_protocol_status_changed(protocol):
    channel_layer = get_channel_layer()

    locked_by_full_name = None

    if protocol.locked_by:
        locked_by_full_name = (
            f"{protocol.locked_by.last_name} {protocol.locked_by.first_name}"
            .strip()
        )

        if not locked_by_full_name:
            locked_by_full_name = protocol.locked_by.username

    cancelled_by_full_name = None

    if protocol.cancelled_by:
        cancelled_by_full_name = (
            f"{protocol.cancelled_by.last_name} {protocol.cancelled_by.first_name}"
            .strip()
        )

        if not cancelled_by_full_name:
            cancelled_by_full_name = protocol.cancelled_by.username

    async_to_sync(channel_layer.group_send)(
        "protocols",
        {
            "type": "protocol_status_changed",
            "protocol": {
                "id": protocol.id,
                "status": protocol.status,

                "locked_by": protocol.locked_by_id,
                "locked_by_id": protocol.locked_by_id,
                "locked_by_username": (
                    protocol.locked_by.username
                    if protocol.locked_by
                    else None
                ),
                "locked_by_full_name": locked_by_full_name,

                "returned_for_revision": protocol.returned_for_revision,
                "revision_comment": protocol.revision_comment,
                "cancelled_at": (
                    protocol.cancelled_at.isoformat()
                    if protocol.cancelled_at
                    else None
                ),
                "cancelled_by": protocol.cancelled_by_id,
                "cancelled_by_id": protocol.cancelled_by_id,
                "cancelled_by_username": (
                    protocol.cancelled_by.username
                    if protocol.cancelled_by
                    else None
                ),
                "cancelled_by_full_name": cancelled_by_full_name,
            },
        },
    )


def is_superuser_request(request):
    return bool(
        request.user
        and request.user.is_authenticated
        and request.user.is_superuser
    )


def user_has_role(user, role_name):
    if not user or not user.is_authenticated:
        return False

    return user.groups.filter(name=role_name).exists()


def is_manager_or_superuser_request(request):
    return bool(
        request.user
        and request.user.is_authenticated
        and (
                request.user.is_superuser
                or user_has_role(request.user, 'manager')
        )
    )


def is_executive_director_or_superuser_request(request):
    return bool(
        request.user
        and request.user.is_authenticated
        and (
                request.user.is_superuser
                or user_has_role(request.user, 'executive_director')
        )
    )

def is_protocol_reviewer_or_superuser_request(request):
    return bool(
        request.user
        and request.user.is_authenticated
        and (
            request.user.is_superuser
            or user_has_role(request.user, 'manager')
            or user_has_role(request.user, 'executive_director')
        )
    )

def normalize_region_name(region):
    if not region:
        return 'Не указано'

    mapping = {
        'japan': 'Япония',
        'china': 'Китай',
        'south-korea': 'Южная Корея',
    }

    return mapping.get(region, region)


def normalize_bool_param(value):
    if value is None or value == '':
        return None

    value = str(value).lower().strip()

    if value in ['true', '1', 'yes', 'да']:
        return True

    if value in ['false', '0', 'no', 'нет']:
        return False

    return None


def normalize_body_mark(value):
    if not value:
        return None

    value = str(value).strip()

    if '-' in value:
        return value.split('-')[-1].strip()

    return value


def extract_year_from_drom_date(value):
    if not value:
        return None

    value = str(value).strip()

    if value in ['н.в.', 'н.в', 'present', 'now', '-']:
        return None

    parts = value.split('.')

    if len(parts) == 2 and parts[1].isdigit():
        return int(parts[1])

    if value.isdigit() and len(value) == 4:
        return int(value)

    return None


def configuration_matches_year(configuration, year):
    if not year:
        return True

    try:
        year = int(year)
    except (TypeError, ValueError):
        return True

    start_year = extract_year_from_drom_date(configuration.date_start)
    end_year = extract_year_from_drom_date(configuration.date_end)

    if start_year and year < start_year:
        return False

    if end_year and year > end_year:
        return False

    return True


# =========================================================
# --- TEST / CSRF FUNCTIONS ---
# =========================================================

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
        serializer = GenerationCardSerializer(paginated, many=True)
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

        serializer = GenerationCardSerializer(obj)
        return Response(serializer.data)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model_filter_options(request):
    try:
        model_id = request.GET.get('model_id')

        if not model_id:
            return Response(
                {'error': 'model_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        generations = Generation.objects.filter(model_id=model_id)

        car_data = CarData.objects.filter(
            configuration__generation__model_id=model_id
        )

        regions = []
        for region in generations.values_list('region', flat=True).distinct():
            regions.append({
                'value': region,
                'label': normalize_region_name(region),
            })

        drive_types = list(
            car_data
            .exclude(drive_type__isnull=True)
            .exclude(drive_type='')
            .values_list('drive_type', flat=True)
            .distinct()
        )

        fuel_types = list(
            car_data
            .exclude(fuel_type__isnull=True)
            .exclude(fuel_type='')
            .values_list('fuel_type', flat=True)
            .distinct()
        )

        engine_models = list(
            car_data
            .exclude(engine_model__isnull=True)
            .exclude(engine_model='')
            .values_list('engine_model', flat=True)
            .distinct()
        )

        transmissions = list(
            car_data
            .exclude(transmission__isnull=True)
            .exclude(transmission='')
            .values_list('transmission', flat=True)
            .distinct()
        )

        seats_counts = list(
            car_data
            .exclude(seats_count__isnull=True)
            .exclude(seats_count='')
            .values_list('seats_count', flat=True)
            .distinct()
        )

        return Response({
            'regions': regions,
            'drive_types': drive_types,
            'fuel_types': fuel_types,
            'engine_models': engine_models,
            'transmissions': transmissions,
            'seats_counts': seats_counts,
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_filtered_generations(request):
    try:
        model_id = request.GET.get('model_id')

        if not model_id:
            return Response(
                {'error': 'model_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        region = request.GET.get('region')
        drive_type = request.GET.get('drive_type')
        fuel_type = request.GET.get('fuel_type')
        engine_model = request.GET.get('engine_model')
        transmission = request.GET.get('transmission')
        seats_count = request.GET.get('seats_count')

        queryset = Generation.objects.filter(model_id=model_id)

        if region:
            queryset = queryset.filter(region=region)

        car_filter = {}

        if drive_type:
            car_filter['configuration__cardata__drive_type'] = drive_type

        if fuel_type:
            car_filter['configuration__cardata__fuel_type'] = fuel_type

        if engine_model:
            car_filter['configuration__cardata__engine_model'] = engine_model

        if transmission:
            car_filter['configuration__cardata__transmission'] = transmission

        if seats_count:
            car_filter['configuration__cardata__seats_count'] = seats_count

        if car_filter:
            queryset = queryset.filter(**car_filter)

        queryset = queryset.distinct().order_by('-date_start', '-id')

        paginator = Pagination()
        paginated = paginator.paginate_queryset(queryset, request)
        serializer = GenerationCardSerializer(paginated, many=True)

        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_configuration_filter_options(request):
    try:
        generation_id = request.GET.get('generation_id')

        if not generation_id:
            return Response(
                {'error': 'generation_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        car_data = CarData.objects.filter(
            configuration__generation_id=generation_id
        )

        drive_types = list(
            car_data
            .exclude(drive_type__isnull=True)
            .exclude(drive_type='')
            .values_list('drive_type', flat=True)
            .distinct()
            .order_by('drive_type')
        )

        fuel_types = list(
            car_data
            .exclude(fuel_type__isnull=True)
            .exclude(fuel_type='')
            .values_list('fuel_type', flat=True)
            .distinct()
            .order_by('fuel_type')
        )

        engine_models = list(
            car_data
            .exclude(engine_model__isnull=True)
            .exclude(engine_model='')
            .values_list('engine_model', flat=True)
            .distinct()
            .order_by('engine_model')
        )

        transmissions = list(
            car_data
            .exclude(transmission__isnull=True)
            .exclude(transmission='')
            .values_list('transmission', flat=True)
            .distinct()
            .order_by('transmission')
        )

        seats_counts = list(
            car_data
            .exclude(seats_count__isnull=True)
            .exclude(seats_count='')
            .values_list('seats_count', flat=True)
            .distinct()
            .order_by('seats_count')
        )

        engine_powers_kw = list(
            car_data
            .exclude(engine_power_kw__isnull=True)
            .values_list('engine_power_kw', flat=True)
            .distinct()
            .order_by('engine_power_kw')
        )

        body_marks_raw = list(
            car_data
            .exclude(body_mark__isnull=True)
            .exclude(body_mark='')
            .values_list('body_mark', flat=True)
            .distinct()
        )

        body_marks = []

        for body_mark in body_marks_raw:
            normalized_body_mark = normalize_body_mark(body_mark)

            if normalized_body_mark and normalized_body_mark not in body_marks:
                body_marks.append(normalized_body_mark)

        body_marks = sorted(body_marks)

        turbo_values = list(
            car_data
            .exclude(turbo_present__isnull=True)
            .values_list('turbo_present', flat=True)
            .distinct()
        )

        return Response({
            'drive_types': drive_types,
            'fuel_types': fuel_types,
            'engine_models': engine_models,
            'transmissions': transmissions,
            'seats_counts': seats_counts,
            'engine_powers_kw': engine_powers_kw,
            'body_marks': body_marks,
            'turbo_values': turbo_values,
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_filtered_configurations(request):
    try:
        generation_id = request.GET.get('generation_id')

        if not generation_id:
            return Response(
                {'error': 'generation_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        name = request.GET.get('name')
        drive_type = request.GET.get('drive_type')
        fuel_type = request.GET.get('fuel_type')
        engine_model = request.GET.get('engine_model')
        transmission = request.GET.get('transmission')
        seats_count = request.GET.get('seats_count')

        manufacture_year = request.GET.get('manufacture_year')
        engine_power = request.GET.get('engine_power')
        body_code = request.GET.get('body_code')
        turbo_present = normalize_bool_param(request.GET.get('turbo_present'))

        queryset = (
            Configuration.objects
            .filter(generation_id=generation_id)
            .select_related('generation')
        )

        if name:
            queryset = queryset.filter(name__icontains=name)

        car_filter = {}

        if drive_type:
            car_filter['cardata__drive_type'] = drive_type

        if fuel_type:
            car_filter['cardata__fuel_type'] = fuel_type

        if engine_model:
            car_filter['cardata__engine_model'] = engine_model

        if transmission:
            car_filter['cardata__transmission'] = transmission

        if seats_count:
            car_filter['cardata__seats_count'] = seats_count

        if turbo_present is not None:
            car_filter['cardata__turbo_present'] = turbo_present

        if engine_power:
            car_filter['cardata__engine_power_kw'] = engine_power

        if car_filter:
            queryset = queryset.filter(**car_filter)

        queryset = queryset.distinct().order_by('name', 'date_start', 'id')

        if body_code:
            filtered_ids = []

            for configuration in queryset:
                car_data = CarData.objects.filter(configuration_id=configuration.id).first()

                if not car_data:
                    continue

                normalized_body_mark = normalize_body_mark(car_data.body_mark)

                if normalized_body_mark == body_code:
                    filtered_ids.append(configuration.id)

            queryset = Configuration.objects.filter(id__in=filtered_ids).order_by('name', 'date_start', 'id')

        if manufacture_year:
            filtered_ids = [
                configuration.id
                for configuration in queryset
                if configuration_matches_year(configuration, manufacture_year)
            ]

            queryset = Configuration.objects.filter(id__in=filtered_ids).order_by('name', 'date_start', 'id')

        paginator = Pagination()
        paginated = paginator.paginate_queryset(queryset, request)
        serializer = ConfigurationSerializer(paginated, many=True)

        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_car_data_by_configuration(request, configuration_id):
    try:
        obj = (
            CarData.objects
            .select_related(
                'configuration',
                'configuration__generation',
                'configuration__generation__model',
                'configuration__generation__model__brand',
            )
            .filter(configuration_id=configuration_id)
            .first()
        )

        if not obj:
            return Response(
                {'error': 'Car data not found for this configuration'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CarDataProtocolSerializer(obj)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

        # Номер протокола теперь формируется после создания,
        # потому что нужен id протокола.
        data.pop('protocol_number', None)

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

            protocol.protocol_number = str(protocol.id).zfill(5)
            protocol.save(update_fields=['protocol_number'])

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
            protocol = serializer.save()

            if protocol.status == 'completed':
                protocol.returned_for_revision = False
                protocol.revision_comment = None
                protocol.cancelled_by = None
                protocol.cancelled_at = None
                protocol.save(update_fields=[
                    'returned_for_revision',
                    'revision_comment',
                    'cancelled_by',
                    'cancelled_at',
                ])

            if protocol.status in ['draft', 'completed', 'approved', 'cancelled']:
                protocol.locked_by = None
                protocol.locked_at = None
                protocol.save(update_fields=['locked_by', 'locked_at'])

            notify_protocol_status_changed(protocol)

            return Response(ProtocolSerializer(protocol).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_protocol_editing(request, pk):
    try:
        with transaction.atomic():
            protocol = Protocol.objects.select_for_update().filter(pk=pk).first()

            if not protocol:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if protocol.status == 'completed':
                return Response(
                    {
                        'detail': 'Завершённый протокол нельзя занять для редактирования.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if protocol.status in ['approved', 'cancelled']:
                return Response(
                    {
                        'detail': 'Этот протокол нельзя занять для редактирования.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if (
                    protocol.status == 'in_progress'
                    and protocol.locked_by_id
                    and protocol.locked_by_id != request.user.id
            ):
                return Response(
                    {
                        'detail': 'Протокол уже редактируется другим пользователем.',
                        'locked_by_id': protocol.locked_by_id,
                        'locked_by_username': (
                            protocol.locked_by.username
                            if protocol.locked_by
                            else None
                        ),
                    },
                    status=423,
                )

            protocol.status = 'in_progress'
            protocol.locked_by = request.user
            protocol.locked_at = timezone.now()
            protocol.save(update_fields=['status', 'locked_by', 'locked_at'])

        notify_protocol_status_changed(protocol)

        return Response(ProtocolSerializer(protocol).data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_protocol_to_draft(request, pk):
    try:
        with transaction.atomic():
            protocol = Protocol.objects.select_for_update().filter(pk=pk).first()

            if not protocol:
                return Response(status=status.HTTP_404_NOT_FOUND)

            protocol.status = 'draft'
            protocol.locked_by = None
            protocol.locked_at = None
            protocol.save(update_fields=['status', 'locked_by', 'locked_at'])

        notify_protocol_status_changed(protocol)

        return Response(ProtocolSerializer(protocol).data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manager_release_protocol_lock(request, pk):
    try:
        if not is_protocol_reviewer_or_superuser_request(request):
            return Response(
                {'detail': 'Освободить занятый протокол может только руководитель или исполнительный директор.'},
                status=status.HTTP_403_FORBIDDEN
            )

        with transaction.atomic():
            protocol = Protocol.objects.select_for_update().filter(pk=pk).first()

            if not protocol:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if protocol.status != 'in_progress':
                return Response(
                    {
                        'detail': 'Освободить можно только протокол в статусе "В работе".'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            protocol.status = 'draft'
            protocol.locked_by = None
            protocol.locked_at = None
            protocol.save(update_fields=['status', 'locked_by', 'locked_at'])

        notify_protocol_status_changed(protocol)

        return Response(ProtocolSerializer(protocol).data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_protocol(request, pk):
    try:
        if not is_protocol_reviewer_or_superuser_request(request):
            return Response(
                {'detail': 'Утвердить протокол может только руководитель или исполнительный директор.'},
                status=status.HTTP_403_FORBIDDEN
            )

        with transaction.atomic():
            protocol = Protocol.objects.select_for_update().filter(pk=pk).first()

            if not protocol:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if protocol.status != 'completed':
                return Response(
                    {'detail': 'Утвердить можно только завершённый протокол.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            protocol.status = 'approved'
            protocol.returned_for_revision = False
            protocol.revision_comment = None
            protocol.cancelled_by = None
            protocol.cancelled_at = None
            protocol.locked_by = None
            protocol.locked_at = None

            protocol.save(update_fields=[
                'status',
                'returned_for_revision',
                'revision_comment',
                'cancelled_by',
                'cancelled_at',
                'locked_by',
                'locked_at',
            ])

        notify_protocol_status_changed(protocol)

        return Response(ProtocolSerializer(protocol).data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_protocol(request, pk):
    try:
        if not is_protocol_reviewer_or_superuser_request(request):
            return Response(
                {'detail': 'Вернуть протокол на доработку может только руководитель или исполнительный директор.'},
                status=status.HTTP_403_FORBIDDEN
            )

        with transaction.atomic():
            protocol = Protocol.objects.select_for_update().filter(pk=pk).first()

            if not protocol:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if protocol.status != 'completed':
                return Response(
                    {'detail': 'На доработку можно вернуть только завершённый протокол.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            revision_comment = str(
                request.data.get('revision_comment', '')
            ).strip()

            protocol.status = 'draft'
            protocol.returned_for_revision = True
            protocol.revision_comment = revision_comment
            protocol.cancelled_by = request.user
            protocol.cancelled_at = timezone.now()
            protocol.locked_by = None
            protocol.locked_at = None

            protocol.save(update_fields=[
                'status',
                'returned_for_revision',
                'revision_comment',
                'cancelled_by',
                'cancelled_at',
                'locked_by',
                'locked_at',
            ])

        notify_protocol_status_changed(protocol)

        return Response(ProtocolSerializer(protocol).data)

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


DOCX_PHOTO_TYPES = [
    'stand_test_photo',
    'gas_test_photo',
    'noise_test_photo',
]

ALLOWED_PHOTO_EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.webp',
]


def get_uploaded_photo_file(request):
    """
    Поддерживаем два варианта имени поля:
    - file
    - image

    На frontend лучше отправлять FormData с ключом file.
    """
    return request.FILES.get('file') or request.FILES.get('image')


def validate_photo_file(uploaded_file):
    if not uploaded_file:
        return 'Файл фото не передан'

    extension = Path(uploaded_file.name).suffix.lower()

    if extension not in ALLOWED_PHOTO_EXTENSIONS:
        return 'Разрешены только изображения: jpg, jpeg, png, webp'

    max_size = 10 * 1024 * 1024

    if uploaded_file.size > max_size:
        return 'Размер фото не должен превышать 10 МБ'

    return None


def build_protocol_photo_path(protocol_id, photo_type, uploaded_file):
    extension = Path(uploaded_file.name).suffix.lower()
    filename = f'{photo_type}_{uuid4().hex}{extension}'

    return f'protocol_photos/{protocol_id}/{filename}'


def delete_photo_file_if_exists(file_path):
    if not file_path:
        return

    try:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
    except Exception:
        pass


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

        queryset = (
            ProtocolPhoto.objects
            .filter(protocol_id=protocol_id)
            .order_by('sort_order', 'id')
        )

        serializer = ProtocolPhotoSerializer(
            queryset,
            many=True,
            context={'request': request}
        )

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

        uploaded_file = get_uploaded_photo_file(request)

        file_error = validate_photo_file(uploaded_file)
        if file_error:
            return Response(
                {'file': file_error},
                status=status.HTTP_400_BAD_REQUEST
            )

        photo_type = request.data.get('photo_type') or 'other'

        allowed_types = [choice[0] for choice in ProtocolPhoto.PHOTO_TYPE_CHOICES]
        if photo_type not in allowed_types:
            return Response(
                {'photo_type': 'Недопустимый тип фото'},
                status=status.HTTP_400_BAD_REQUEST
            )

        sort_order = request.data.get('sort_order') or 0

        # Для трёх фото, которые идут в DOCX,
        # храним только одно актуальное фото каждого типа.
        if photo_type in DOCX_PHOTO_TYPES:
            old_photos = ProtocolPhoto.objects.filter(
                protocol_id=protocol_id,
                photo_type=photo_type
            )

            for old_photo in old_photos:
                delete_photo_file_if_exists(old_photo.file_path)

            old_photos.delete()

        relative_path = build_protocol_photo_path(
            protocol_id=protocol_id,
            photo_type=photo_type,
            uploaded_file=uploaded_file
        )

        saved_path = default_storage.save(relative_path, uploaded_file)

        photo = ProtocolPhoto.objects.create(
            protocol=protocol,
            photo_type=photo_type,
            file_path=saved_path,
            sort_order=sort_order,
        )

        serializer = ProtocolPhotoSerializer(
            photo,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_protocol_photo(request, photo_id):
    try:
        photo = ProtocolPhoto.objects.filter(pk=photo_id).first()
        if not photo:
            return Response(status=status.HTTP_404_NOT_FOUND)

        uploaded_file = get_uploaded_photo_file(request)

        new_photo_type = request.data.get('photo_type', photo.photo_type)
        new_sort_order = request.data.get('sort_order', photo.sort_order)

        allowed_types = [choice[0] for choice in ProtocolPhoto.PHOTO_TYPE_CHOICES]
        if new_photo_type not in allowed_types:
            return Response(
                {'photo_type': 'Недопустимый тип фото'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Если фото переводят в один из трёх DOCX-типов,
        # удаляем другие фото этого же типа у этого протокола.
        if new_photo_type in DOCX_PHOTO_TYPES:
            duplicates = (
                ProtocolPhoto.objects
                .filter(
                    protocol_id=photo.protocol_id,
                    photo_type=new_photo_type
                )
                .exclude(pk=photo.pk)
            )

            for duplicate in duplicates:
                delete_photo_file_if_exists(duplicate.file_path)

            duplicates.delete()

        if uploaded_file:
            file_error = validate_photo_file(uploaded_file)
            if file_error:
                return Response(
                    {'file': file_error},
                    status=status.HTTP_400_BAD_REQUEST
                )

            delete_photo_file_if_exists(photo.file_path)

            relative_path = build_protocol_photo_path(
                protocol_id=photo.protocol_id,
                photo_type=new_photo_type,
                uploaded_file=uploaded_file
            )

            photo.file_path = default_storage.save(relative_path, uploaded_file)

        photo.photo_type = new_photo_type
        photo.sort_order = new_sort_order
        photo.save(update_fields=['photo_type', 'file_path', 'sort_order'])

        serializer = ProtocolPhotoSerializer(
            photo,
            context={'request': request}
        )

        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_protocol_photo(request, photo_id):
    try:
        photo = ProtocolPhoto.objects.filter(pk=photo_id).first()
        if not photo:
            return Response(status=status.HTTP_404_NOT_FOUND)

        delete_photo_file_if_exists(photo.file_path)

        photo.delete()

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

        serializer = ProtocolFullSerializer(
            protocol,
            context={'request': request}
        )

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
        if not is_executive_director_or_superuser_request(request):
            return Response(
                {'detail': 'Доступ разрешён только исполнительному директору.'},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = (
            User.objects
            .filter(is_superuser=False)
            .order_by('id')
        )

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_employee_user(request):
    try:
        if not is_executive_director_or_superuser_request(request):
            return Response(
                {'detail': 'Создавать сотрудников может только исполнительный директор.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_employee_user(request, user_id):
    try:
        if not is_executive_director_or_superuser_request(request):
            return Response(
                {'detail': 'Изменять сотрудников может только исполнительный директор.'},
                status=status.HTTP_403_FORBIDDEN
            )

        employee = User.objects.filter(pk=user_id).first()

        if not employee:
            return Response(
                {'detail': 'Пользователь не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if employee.is_superuser:
            return Response(
                {'detail': 'Нельзя изменять технический аккаунт суперпользователя.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UpdateUserSerializer(
            employee,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_employee_user(request, user_id):
    try:
        if not is_executive_director_or_superuser_request(request):
            return Response(
                {'detail': 'Удалять сотрудников может только исполнительный директор.'},
                status=status.HTTP_403_FORBIDDEN
            )

        employee = User.objects.filter(pk=user_id).first()

        if not employee:
            return Response(
                {'detail': 'Пользователь не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if employee.id == request.user.id:
            return Response(
                {'detail': 'Нельзя удалить собственный аккаунт.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if employee.is_superuser:
            return Response(
                {'detail': 'Нельзя удалить технический аккаунт суперпользователя.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        confirm_text = str(request.data.get('confirm_text', '')).strip().lower()

        if confirm_text != 'удалить':
            return Response(
                {'detail': 'Для удаления нужно ввести слово "Удалить".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
