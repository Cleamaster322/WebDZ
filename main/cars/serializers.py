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


class GenerationCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generation
        fields = [
            'id',
            'model',
            'name',
            'link',
            'body_code',
            'region',
            'body_type',
            'is_hybrid',
            'generation_num',
            'restyling_num',
            'date_start',
            'date_end',
            'image_path',
        ]


class ConfigurationSerializer(serializers.ModelSerializer):
    drive_type = serializers.SerializerMethodField()
    fuel_type = serializers.SerializerMethodField()
    engine_model = serializers.SerializerMethodField()
    transmission = serializers.SerializerMethodField()
    seats_count = serializers.SerializerMethodField()
    engine_power_kw = serializers.SerializerMethodField()
    engine_power_hp = serializers.SerializerMethodField()
    turbo_present = serializers.SerializerMethodField()
    front_tires = serializers.SerializerMethodField()
    rear_tires = serializers.SerializerMethodField()
    body_type = serializers.SerializerMethodField()
    manufacture_year = serializers.SerializerMethodField()

    class Meta:
        model = Configuration
        fields = [
            'id',
            'generation',
            'name',
            'link',
            'engine_name',
            'date_start',
            'date_end',

            # данные из car_data для отображения и выбора комплектации
            'drive_type',
            'fuel_type',
            'engine_model',
            'transmission',
            'seats_count',
            'engine_power_kw',
            'engine_power_hp',
            'turbo_present',
            'front_tires',
            'rear_tires',
            'body_type',
            'manufacture_year',
        ]

    def get_car_data(self, obj):
        return CarData.objects.filter(configuration_id=obj.id).first()

    def get_drive_type(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.drive_type if car_data else None

    def get_fuel_type(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.fuel_type if car_data else None

    def get_engine_model(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.engine_model if car_data else None

    def get_transmission(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.transmission if car_data else None

    def get_seats_count(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.seats_count if car_data else None

    def get_engine_power_kw(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.engine_power_kw if car_data else None

    def get_engine_power_hp(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.engine_power_hp if car_data else None

    def get_turbo_present(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.turbo_present if car_data else None

    def get_front_tires(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.front_tires if car_data else None

    def get_rear_tires(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.rear_tires if car_data else None

    def get_body_type(self, obj):
        car_data = self.get_car_data(obj)
        if car_data and car_data.body_type:
            return car_data.body_type

        if obj.generation and obj.generation.body_type:
            return obj.generation.body_type

        return None

    def get_manufacture_year(self, obj):
        car_data = self.get_car_data(obj)
        return car_data.manufacture_year if car_data else None


class CarDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarData
        fields = '__all__'


class CarDataProtocolSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(
        source='configuration.generation.model.brand.name',
        read_only=True
    )
    model_name = serializers.CharField(
        source='configuration.generation.model.name',
        read_only=True
    )
    generation_id = serializers.IntegerField(
        source='configuration.generation.id',
        read_only=True
    )
    generation_name = serializers.CharField(
        source='configuration.generation.name',
        read_only=True
    )
    configuration_id = serializers.IntegerField(
        source='configuration.id',
        read_only=True
    )

    class Meta:
        model = CarData
        fields = [
            'id',
            'configuration_id',
            'brand_name',
            'model_name',
            'generation_id',
            'generation_name',

            'configuration_name',
            'manufacture_year',
            'body_type',

            'front_tires',
            'rear_tires',

            'fuel_type',
            'transmission',
            'drive_type',
            'seats_count',
            'clearance',

            'vehicle_weight_kg',

            'engine_model',
            'engine_capacity',
            'engine_power_hp',
            'engine_power_kw',
            'cylinder_layout',
            'cylinders_count',
            'turbo_present',

            'front_brakes',
            'rear_brakes',

            'vehicle_length_mm',
            'vehicle_width_mm',
            'vehicle_height_mm',
        ]


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
    configuration_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Protocol
        fields = [
            'id',
            'configuration_id',

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

    def normalize_fuel_type(self, value):
        if not value:
            return None

        value = str(value).lower()

        if 'бенз' in value or 'petrol' in value or 'gasoline' in value:
            return 'petrol'
        if 'диз' in value or 'diesel' in value:
            return 'diesel'
        if 'гибрид' in value or 'hybrid' in value:
            return 'hybrid'
        if 'элект' in value or 'electric' in value:
            return 'electric'

        return None

    def normalize_transmission(self, value):
        if not value:
            return None

        value = str(value).lower()

        if 'вариатор' in value or 'cvt' in value:
            return 'variator'
        if 'механ' in value or 'мкпп' in value or 'manual' in value:
            return 'manual'
        if 'робот' in value or 'robot' in value:
            return 'robot'
        if 'редуктор' in value or 'reductor' in value:
            return 'reductor'
        if 'автомат' in value or 'акпп' in value or 'automatic' in value:
            return 'automatic'

        return None

    def normalize_wheel_formula(self, value):
        if not value:
            return None

        value = str(value).lower()

        if 'перед' in value or 'front' in value:
            return '4x2_front'
        if 'зад' in value or 'rear' in value:
            return '4x2_rear'
        if 'полн' in value or '4wd' in value or 'awd' in value or '4x4' in value:
            return '4x4'

        return None

    def normalize_cylinder_layout(self, value):
        if not value:
            return None

        value = str(value).lower()

        if 'ряд' in value or 'inline' in value:
            return 'inline'
        if 'оппозит' in value or 'opposed' in value:
            return 'opposed'
        if 'v' in value or 'v-' in value or 'v образ' in value:
            return 'v_shape'

        return None

    def normalize_service_brake_type(self, front_brakes, rear_brakes):
        front = str(front_brakes or '').lower()
        rear = str(rear_brakes or '').lower()

        front_is_disc = 'диск' in front or 'disc' in front
        rear_is_disc = 'диск' in rear or 'disc' in rear
        rear_is_drum = 'барабан' in rear or 'drum' in rear

        if front_is_disc and rear_is_disc:
            return 'disc_disc'

        if front_is_disc and rear_is_drum:
            return 'disc_drum'

        return None

    def get_default_light_values(self):
        """
        Дефолтные значения под актуальный шаблон протокола.
        Пользователь потом может изменить их на странице осмотра.
        """
        return {
            # Ближний свет: в шаблоне подсказка "всегда 2"
            'low_beam_count': 2,
            'low_beam_color': 'белый',

            # Дальний свет обычно 2, но оставляем редактируемым
            'high_beam_count': 2,
            'high_beam_color': 'белый',

            # Передние указатели поворота: "всегда 2"
            'turn_signal_count': 2,
            'turn_signal_color': 'автожелтый',

            # Передние габаритные огни: "всегда 2"
            'front_position_light_count': 2,
            'front_position_light_color': 'белый',

            # Задние габаритные огни: "красный + 2"
            'rear_position_light_count': 2,
            'rear_position_light_color': 'красный',

            # Основной сигнал торможения: "красный + 2"
            'main_brake_signal_count': 2,
            'main_brake_signal_color': 'красный',

            # Задние стояночные огни: "нет или всегда 2"
            # По умолчанию лучше оставить пустым, чтобы пользователь выбрал.
            'rear_parking_light_count': None,
            'rear_parking_light_color': 'красный',

            # Передние стояночные огни — тоже оставляем на выбор.
            'parking_light_count': None,
            'parking_light_color': 'белый',

            # Остальные приборы зависят от конкретного ТС.
            'front_fog_count': None,
            'front_fog_color': 'белый',

            'reverse_light_count': None,
            'reverse_light_color': 'белый',

            'additional_brake_signal_count': None,
            'additional_brake_signal_color': 'красный',

            'rear_fog_count': None,
            'rear_fog_color': 'красный',

            'plate_light_count': None,
            'plate_light_color': 'белый',

            'daytime_running_light_count': None,
            'daytime_running_light_color': 'белый',

            'adaptive_front_lighting_count': None,
            'adaptive_front_lighting_color': 'белый',
        }

    def create(self, validated_data):
        configuration_id = validated_data.pop('configuration_id', None)

        car_data = None
        configuration = None

        if configuration_id:
            car_data = (
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

            if not car_data:
                raise serializers.ValidationError({
                    'configuration_id': 'Для выбранной комплектации не найдены данные car_data'
                })

            configuration = car_data.configuration
            generation = configuration.generation
            model = generation.model
            brand = model.brand

            validated_data['car'] = car_data

            if not validated_data.get('brand_name'):
                validated_data['brand_name'] = brand.name

            if not validated_data.get('commercial_name'):
                validated_data['commercial_name'] = model.name

            if not validated_data.get('body_type'):
                validated_data['body_type'] = car_data.body_type or generation.body_type

            if not validated_data.get('wheel_marking_front'):
                validated_data['wheel_marking_front'] = car_data.front_tires

            if not validated_data.get('wheel_marking_rear'):
                validated_data['wheel_marking_rear'] = car_data.rear_tires

            if not validated_data.get('manufacture_year'):
                validated_data['manufacture_year'] = car_data.manufacture_year

        protocol = Protocol.objects.create(**validated_data)

        measurement_defaults = {}

        if car_data:
            measurement_defaults = {
                'wheel_formula': self.normalize_wheel_formula(car_data.drive_type),
                'seats_count': car_data.seats_count,

                'engine_model': car_data.engine_model or configuration.engine_name,
                'engine_power_kw': car_data.engine_power_kw,
                'fuel_type': self.normalize_fuel_type(car_data.fuel_type),
                'cylinder_layout': self.normalize_cylinder_layout(car_data.cylinder_layout),
                'cylinders_count': car_data.cylinders_count,
                'turbo_present': car_data.turbo_present,

                'transmission_type': self.normalize_transmission(car_data.transmission),

                'vehicle_length_mm': car_data.vehicle_length_mm,
                'vehicle_width_mm': car_data.vehicle_width_mm,
                'vehicle_height_mm': car_data.vehicle_height_mm,
                'vehicle_weight_kg': car_data.vehicle_weight_kg,
            }

        ProtocolMeasurement.objects.create(
            protocol=protocol,
            **measurement_defaults
        )

        brake_defaults = {}

        if car_data:
            service_brake_type = self.normalize_service_brake_type(
                car_data.front_brakes,
                car_data.rear_brakes
            )

            if service_brake_type:
                brake_defaults['service_brake_type'] = service_brake_type

        ProtocolBrake.objects.create(
            protocol=protocol,
            **brake_defaults
        )

        ProtocolLight.objects.create(
            protocol=protocol,
            **self.get_default_light_values()
        )

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
