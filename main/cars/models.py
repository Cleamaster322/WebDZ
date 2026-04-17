from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


# =========================
# Автомобильный справочник
# =========================

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=255)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, db_column='brand_id')
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=255)

    class Meta:
        db_table = 'models'

    def __str__(self):
        return self.name


class Generation(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, db_column='model_id')
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    body_code = models.CharField(max_length=100, null=True, blank=True)
    body_type = models.CharField(max_length=100, null=True, blank=True)
    is_hybrid = models.BooleanField(default=False)
    generation_num = models.IntegerField()
    restyling_num = models.IntegerField()
    date_start = models.CharField(max_length=11)
    date_end = models.CharField(max_length=11)

    class Meta:
        db_table = 'generations'

    def __str__(self):
        return self.name


class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    generation = models.ForeignKey(Generation, on_delete=models.DO_NOTHING, db_column='generation_id')
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    engine_name = models.CharField(max_length=100, null=True, blank=True)
    date_start = models.CharField(max_length=11)
    date_end = models.CharField(max_length=11)

    class Meta:
        db_table = 'configurations'

    def __str__(self):
        return self.name


class CarData(models.Model):
    id = models.AutoField(primary_key=True)
    configuration = models.ForeignKey(Configuration, on_delete=models.DO_NOTHING, db_column='configuration_id')
    front_tires = models.CharField(max_length=50)
    rear_tires = models.CharField(max_length=50)
    engine_capacity = models.FloatField()
    engine_power_hp = models.IntegerField()
    engine_power_kw = models.IntegerField()
    consumption = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    drive_type = models.CharField(max_length=50)
    seats_count = models.IntegerField()
    doors_count = models.IntegerField()
    clearance = models.IntegerField()
    trunk_volume = models.IntegerField()

    class Meta:
        db_table = 'car_data'
        verbose_name = 'Car Data'
        verbose_name_plural = 'Car Data'

    def __str__(self):
        return f"{self.configuration.name} - {self.fuel_type}"


# =========================
# Протокол
# =========================

class Protocol(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершён'),
        ('approved', 'Утверждён'),
        ('cancelled', 'Отменён'),
    ]

    OWNER_TYPE_CHOICES = [
        ('individual', 'Физическое лицо'),
        ('company', 'Компания'),
    ]

    protocol_number = models.CharField(max_length=100, unique=True)
    protocol_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='protocols'
    )
    car = models.ForeignKey(
        'CarData',
        on_delete=models.RESTRICT,
        related_name='protocols'
    )

    owner_type = models.CharField(max_length=20, choices=OWNER_TYPE_CHOICES, default='individual')
    owner_name = models.CharField(max_length=255)
    owner_address = models.CharField(max_length=500, blank=True, null=True)
    owner_document = models.CharField(max_length=255, blank=True, null=True)
    owner_phone = models.CharField(max_length=50, blank=True, null=True)

    appendix_number = models.CharField(max_length=100, blank=True, null=True)
    commercial_name = models.CharField(max_length=150, blank=True, null=True)

    vin = models.CharField(max_length=50, blank=True, null=True)
    chassis_number = models.CharField(max_length=50, blank=True, null=True)
    body_number = models.CharField(max_length=50, blank=True, null=True)
    engine_number = models.CharField(max_length=50, blank=True, null=True)
    registration_number = models.CharField(max_length=50, blank=True, null=True)

    manufacture_year = models.SmallIntegerField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    inspection_place = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'protocols'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.protocol_number}'

# =========================
# ProtocolMeasurement
# =========================

class ProtocolMeasurement(models.Model):
    WHEEL_FORMULA_CHOICES = [
        ('4x2_front', '4x2 передний'),
        ('4x2_rear', '4x2 задний'),
        ('4x4', '4x4'),
    ]

    ENGINE_LAYOUT_CHOICES = [
        ('transverse', 'Поперечное'),
        ('longitudinal', 'Продольное'),
    ]

    CYLINDER_LAYOUT_CHOICES = [
        ('inline', 'Рядное'),
        ('opposed', 'Оппозитное'),
        ('v_shape', 'V-образное'),
    ]

    FUEL_TYPE_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('hybrid', 'Гибрид'),
        ('electric', 'Электро'),
        ('other', 'Другое'),
    ]

    TRANSMISSION_TYPE_CHOICES = [
        ('automatic', 'Автомат'),
        ('cvt', 'CVT'),
        ('manual', 'Механика'),
        ('robot', 'Робот'),
        ('reducer', 'Редуктор'),
        ('other', 'Другое'),
    ]

    protocol = models.OneToOneField(
        Protocol,
        on_delete=models.CASCADE,
        related_name='measurement'
    )

    wheel_formula = models.CharField(max_length=20, choices=WHEEL_FORMULA_CHOICES, blank=True, null=True)
    mufflers_count = models.PositiveSmallIntegerField(blank=True, null=True)
    seats_count = models.PositiveSmallIntegerField(blank=True, null=True)
    suspension_present = models.BooleanField(blank=True, null=True)

    engine_layout = models.CharField(max_length=20, choices=ENGINE_LAYOUT_CHOICES, blank=True, null=True)
    cylinder_layout = models.CharField(max_length=20, choices=CYLINDER_LAYOUT_CHOICES, blank=True, null=True)
    cylinders_count = models.PositiveSmallIntegerField(blank=True, null=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, blank=True, null=True)
    turbo_present = models.BooleanField(blank=True, null=True)
    transmission_type = models.CharField(max_length=20, choices=TRANSMISSION_TYPE_CHOICES, blank=True, null=True)

    tire_depth_fl_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tire_depth_fr_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tire_depth_rl_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tire_depth_rr_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    bumper_to_body_distance_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    protruding_elements_doors_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    protruding_elements_other_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    glass_transparency_left_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    glass_transparency_right_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    glass_transparency_windshield_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    sun_strip_width_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    steering_backlash_deg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    speed_by_speedometer_kmh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    actual_speed_kmh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    exhaust_noise_db = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    co_min_pct = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    co_max_pct = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)

    light_absorption_1 = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    light_absorption_2 = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    light_absorption_3 = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    light_absorption_4 = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    light_absorption_5 = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    light_absorption_6 = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)

    vehicle_length_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vehicle_width_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vehicle_height_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vehicle_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    axle1_load_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    axle2_load_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stand_axle1_load_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stand_axle2_load_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'protocol_measurements'

# =========================
# ProtocolBrake
# =========================

class ProtocolBrake(models.Model):
    SERVICE_BRAKE_TYPE_CHOICES = [
        ('disc_disc', 'Диск/Диск'),
        ('disc_drum', 'Диск/Барабан'),
        ('other', 'Другое'),
    ]

    PARKING_BRAKE_TYPE_CHOICES = [
        ('mechanical_hand', 'Ручной'),
        ('mechanical_pedal', 'Педаль'),
        ('electric', 'Электрический'),
        ('other', 'Другое'),
    ]

    protocol = models.OneToOneField(
        Protocol,
        on_delete=models.CASCADE,
        related_name='brake'
    )

    service_brake_type = models.CharField(max_length=30, choices=SERVICE_BRAKE_TYPE_CHOICES, blank=True, null=True)
    parking_brake_type = models.CharField(max_length=30, choices=PARKING_BRAKE_TYPE_CHOICES, blank=True, null=True)

    service_brake_control_force_axle1_n = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    service_brake_control_force_axle2_n = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    parking_brake_control_force_n = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    axle_1_brake_difference_pct = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    axle_2_brake_difference_pct = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    service_brake_front_left_kn = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    service_brake_front_right_kn = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    service_brake_rear_left_kn = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    service_brake_rear_right_kn = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    parking_brake_left_kn = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    parking_brake_right_kn = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'protocol_brakes'

# =========================
# ProtocolLight
# =========================

class ProtocolLight(models.Model):
    HEADLIGHT_TYPE_CHOICES = [
        ('halogen', 'Галоген'),
        ('xenon', 'Ксенон'),
        ('led', 'LED'),
        ('other', 'Другое'),
    ]

    protocol = models.OneToOneField(
        Protocol,
        on_delete=models.CASCADE,
        related_name='light'
    )

    low_beam_count = models.PositiveSmallIntegerField(blank=True, null=True)
    high_beam_count = models.PositiveSmallIntegerField(blank=True, null=True)
    front_fog_count = models.PositiveSmallIntegerField(blank=True, null=True)
    reverse_light_count = models.PositiveSmallIntegerField(blank=True, null=True)
    turn_signal_count = models.PositiveSmallIntegerField(blank=True, null=True)
    front_position_light_count = models.PositiveSmallIntegerField(blank=True, null=True)
    rear_position_light_count = models.PositiveSmallIntegerField(blank=True, null=True)
    main_brake_signal_count = models.PositiveSmallIntegerField(blank=True, null=True)
    additional_brake_signal_count = models.PositiveSmallIntegerField(blank=True, null=True)
    rear_fog_count = models.PositiveSmallIntegerField(blank=True, null=True)
    plate_light_count = models.PositiveSmallIntegerField(blank=True, null=True)
    daytime_running_light_count = models.PositiveSmallIntegerField(blank=True, null=True)
    parking_light_count = models.PositiveSmallIntegerField(blank=True, null=True)

    headlight_type = models.CharField(max_length=20, choices=HEADLIGHT_TYPE_CHOICES, blank=True, null=True)

    low_beam_upper_point_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    low_beam_lower_point_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    fog_light_upper_point_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fog_light_lower_point_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fog_light_left_distance_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fog_light_right_distance_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    brake_signal_upper_point_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    brake_signal_lower_point_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    brake_signal_left_distance_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    brake_signal_right_distance_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    additional_brake_signal_from_glass_edge_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    additional_brake_signal_from_support_surface_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    additional_brake_signal_optical_center_shift_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    rear_fog_upper_point_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rear_fog_lower_point_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    headlight_washer_present = models.BooleanField(blank=True, null=True)

    left_34v_cd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    left_52h_cd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    left_high_beam_cd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    right_34v_cd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    right_52h_cd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    right_high_beam_cd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    turn_signal_frequency_per_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    turn_signal_frequency_hz = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'protocol_lights'

# =========================
# ProtocolPhoto
# =========================

class ProtocolPhoto(models.Model):
    PHOTO_TYPE_CHOICES = [
        ('front_view', 'Вид спереди'),
        ('rear_view', 'Вид сзади'),
        ('left_view', 'Вид слева'),
        ('right_view', 'Вид справа'),
        ('vin_plate', 'VIN табличка'),
        ('vin_body', 'VIN на кузове'),
        ('tire_marking', 'Маркировка шин'),
        ('odometer', 'Одометр'),
        ('test_process', 'Процесс испытаний'),
        ('exhaust_noise_test', 'Замер шума'),
        ('other', 'Другое'),
    ]

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo_type = models.CharField(max_length=50, choices=PHOTO_TYPE_CHOICES, default='other')
    file_path = models.CharField(max_length=500)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'protocol_photos'
        ordering = ['sort_order', 'id']

