from rest_framework import serializers
from django.contrib.auth.models import User

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


# =========================
# Справочник автомобилей
# =========================

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class GenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generation
        fields = '__all__'


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'


class CarDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarData
        fields = '__all__'


# =========================
# Протокол
# =========================

class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = '__all__'


class ProtocolMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolMeasurement
        fields = '__all__'
        read_only_fields = ['id']


class ProtocolBrakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolBrake
        fields = '__all__'
        read_only_fields = ['id']


class ProtocolLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolLight
        fields = '__all__'
        read_only_fields = ['id']


class ProtocolPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolPhoto
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ProtocolTestConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolTestCondition
        fields = '__all__'
        read_only_fields = ['id']


class ProtocolRoadConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolRoadCondition
        fields = '__all__'
        read_only_fields = ['id']


class ProtocolPowerSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolPowerSupply
        fields = '__all__'
        read_only_fields = ['id']


# =========================
# Полный / детальный протокол
# =========================

class ProtocolDetailSerializer(serializers.ModelSerializer):
    measurement = ProtocolMeasurementSerializer(read_only=True)
    brake = ProtocolBrakeSerializer(read_only=True)
    light = ProtocolLightSerializer(read_only=True)
    test_conditions = ProtocolTestConditionSerializer(read_only=True)
    road_conditions = ProtocolRoadConditionSerializer(read_only=True)
    power_supply = ProtocolPowerSupplySerializer(read_only=True)
    photos = ProtocolPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Protocol
        fields = '__all__'


class ProtocolFullSerializer(serializers.ModelSerializer):
    measurement = ProtocolMeasurementSerializer(read_only=True)
    brake = ProtocolBrakeSerializer(read_only=True)
    light = ProtocolLightSerializer(read_only=True)
    test_conditions = ProtocolTestConditionSerializer(read_only=True)
    road_conditions = ProtocolRoadConditionSerializer(read_only=True)
    power_supply = ProtocolPowerSupplySerializer(read_only=True)
    photos = ProtocolPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Protocol
        fields = '__all__'


# =========================
# Создание протокола
# =========================

class ProtocolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = [
            'id',
            'protocol_number',
            'protocol_date',
            'status',
            'user',
            'car',

            'owner_type',
            'owner_name',
            'owner_address',
            'owner_document',
            'owner_phone',

            'appendix_number',
            'commercial_name',
            'brand_name',
            'vehicle_category',
            'body_type',

            'vin',
            'chassis_number',
            'body_number',
            'engine_number',
            'registration_number',

            'wheel_marking_front',
            'wheel_marking_rear',
            'tire_season',
            'has_spikes',

            'manufacture_year',
            'color',
            'inspection_place',
            'comment',

            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        protocol = Protocol.objects.create(**validated_data)

        ProtocolMeasurement.objects.create(protocol=protocol)
        ProtocolBrake.objects.create(protocol=protocol)
        ProtocolLight.objects.create(protocol=protocol)
        ProtocolTestCondition.objects.create(protocol=protocol)
        ProtocolRoadCondition.objects.create(protocol=protocol)
        ProtocolPowerSupply.objects.create(protocol=protocol)

        return protocol


# =========================
# Пользователь
# =========================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'