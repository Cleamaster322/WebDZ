from rest_framework import serializers
from .models import Brand, Model, Generation, Configuration,CarData

# simple serializers
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def validate_name(self, name):
        if Brand.objects.filter(name=name).exists():
            raise serializers.ValidationError('Brand name already exists')
        return name

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

    def validate_name(self, name):
        if Model.objects.filter(name=name).exists():
            raise serializers.ValidationError('Model name already exists')
        return name

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
