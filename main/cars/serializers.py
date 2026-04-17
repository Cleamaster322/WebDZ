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
    ProtocolLight, ProtocolPhoto,
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
        exclude = ['id', 'protocol']


class ProtocolBrakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolBrake
        exclude = ['id', 'protocol']


class ProtocolLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolLight
        exclude = ['id', 'protocol']


class ProtocolPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolPhoto
        exclude = ['protocol']

class ProtocolDetailSerializer(serializers.ModelSerializer):
    measurement = ProtocolMeasurementSerializer(read_only=True)
    brake = ProtocolBrakeSerializer(read_only=True)
    light = ProtocolLightSerializer(read_only=True)
    photos = ProtocolPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Protocol
        fields = '__all__'

class ProtocolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = [
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
            'vin',
            'chassis_number',
            'body_number',
            'engine_number',
            'registration_number',
            'manufacture_year',
            'color',
            'inspection_place',
            'comment',
        ]

    def create(self, validated_data):
        protocol = Protocol.objects.create(**validated_data)
        ProtocolMeasurement.objects.create(protocol=protocol)
        ProtocolBrake.objects.create(protocol=protocol)
        ProtocolLight.objects.create(protocol=protocol)
        return protocol

class ProtocolFullSerializer(serializers.ModelSerializer):
    measurement = ProtocolMeasurementSerializer(read_only=True)
    brake = ProtocolBrakeSerializer(read_only=True)
    light = ProtocolLightSerializer(read_only=True)
    photos = ProtocolPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Protocol
        fields = '__all__'
# =========================
# Пользователь
# =========================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'