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


class ProtocolBrakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolBrake
        fields = '__all__'


class ProtocolLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolLight
        fields = '__all__'


# =========================
# Пользователь
# =========================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'