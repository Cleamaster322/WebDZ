from django.db import models
from django.contrib.auth.models import User


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
        ('draft', 'draft'),
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('approved', 'approved'),
        ('cancelled', 'cancelled'),
    ]

    OWNER_TYPE_CHOICES = [
        ('individual', 'individual'),
        ('company', 'company'),
    ]

    id = models.BigAutoField(primary_key=True)
    protocol_number = models.CharField(max_length=100)
    protocol_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    car = models.ForeignKey(CarData, on_delete=models.DO_NOTHING, db_column='car_data_id')

    owner_type = models.CharField(max_length=20, choices=OWNER_TYPE_CHOICES, default='individual')
    owner_name = models.CharField(max_length=255)
    owner_address = models.CharField(max_length=500, null=True, blank=True)
    owner_document = models.CharField(max_length=255, null=True, blank=True)
    owner_phone = models.CharField(max_length=50, null=True, blank=True)

    vin = models.CharField(max_length=50, null=True, blank=True)
    chassis_number = models.CharField(max_length=100, null=True, blank=True)
    body_number = models.CharField(max_length=100, null=True, blank=True)
    engine_number = models.CharField(max_length=100, null=True, blank=True)
    registration_number = models.CharField(max_length=50, null=True, blank=True)

    manufacture_year = models.PositiveSmallIntegerField(null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    inspection_place = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'protocols'

    def __str__(self):
        return self.protocol_number

# =========================
# Расширенные замеры протокола
# =========================

class ProtocolMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    protocol = models.OneToOneField(
        Protocol,
        on_delete=models.CASCADE,
        db_column='protocol_id',
        related_name='measurement_data'
    )

    tire_depth_fl_mm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    tire_depth_fr_mm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    tire_depth_rl_mm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    tire_depth_rr_mm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    bumper_to_body_distance_mm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    protruding_elements_doors_mm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    protruding_elements_other_mm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    glass_transparency_left_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    glass_transparency_right_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    glass_transparency_windshield_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    sun_strip_width_mm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    steering_backlash_deg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    speed_by_speedometer_kmh = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_speed_kmh = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    exhaust_noise_db = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    co_min_pct = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    co_max_pct = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    light_absorption_1 = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    light_absorption_2 = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    light_absorption_3 = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    light_absorption_4 = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    light_absorption_5 = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    light_absorption_6 = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)

    vehicle_length_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vehicle_width_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vehicle_height_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vehicle_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    axle1_load_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    axle2_load_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stand_axle1_load_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stand_axle2_load_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    extra_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'protocol_measurements'

    def __str__(self):
        return f"Measurements for protocol #{self.protocol_id}"


class ProtocolBrake(models.Model):
    id = models.BigAutoField(primary_key=True)
    protocol = models.OneToOneField(
        Protocol,
        on_delete=models.CASCADE,
        db_column='protocol_id',
        related_name='brake_data'
    )

    service_brake_front_left_kn = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    service_brake_front_right_kn = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    service_brake_rear_left_kn = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    service_brake_rear_right_kn = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    parking_brake_left_kn = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    parking_brake_right_kn = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    axle_2_brake_difference_pct = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'protocol_brakes'

    def __str__(self):
        return f"Brakes for protocol #{self.protocol_id}"


class ProtocolLight(models.Model):
    HEADLIGHT_TYPE_CHOICES = [
        ('halogen', 'Halogen'),
        ('xenon', 'Xenon'),
        ('led', 'LED'),
        ('other', 'Other'),
    ]

    id = models.BigAutoField(primary_key=True)
    protocol = models.OneToOneField(
        Protocol,
        on_delete=models.CASCADE,
        db_column='protocol_id',
        related_name='light_data'
    )

    low_beam_count = models.PositiveSmallIntegerField(null=True, blank=True)
    high_beam_count = models.PositiveSmallIntegerField(null=True, blank=True)
    front_fog_count = models.PositiveSmallIntegerField(null=True, blank=True)
    reverse_light_count = models.PositiveSmallIntegerField(null=True, blank=True)
    turn_signal_count = models.PositiveSmallIntegerField(null=True, blank=True)
    front_position_light_count = models.PositiveSmallIntegerField(null=True, blank=True)
    rear_position_light_count = models.PositiveSmallIntegerField(null=True, blank=True)
    main_brake_signal_count = models.PositiveSmallIntegerField(null=True, blank=True)
    additional_brake_signal_count = models.PositiveSmallIntegerField(null=True, blank=True)
    rear_fog_count = models.PositiveSmallIntegerField(null=True, blank=True)
    plate_light_count = models.PositiveSmallIntegerField(null=True, blank=True)
    daytime_running_light_count = models.PositiveSmallIntegerField(null=True, blank=True)
    parking_light_count = models.PositiveSmallIntegerField(null=True, blank=True)

    headlight_type = models.CharField(
        max_length=20,
        choices=HEADLIGHT_TYPE_CHOICES,
        null=True,
        blank=True
    )
    headlight_type_other = models.CharField(max_length=100, null=True, blank=True)

    low_beam_upper_point_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    low_beam_lower_point_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    fog_light_upper_point_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fog_light_lower_point_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fog_light_left_distance_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fog_light_right_distance_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    brake_signal_upper_point_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    brake_signal_lower_point_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    brake_signal_left_distance_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    brake_signal_right_distance_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    additional_brake_signal_from_glass_edge_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    additional_brake_signal_from_support_surface_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    additional_brake_signal_optical_center_shift_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    rear_fog_upper_point_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rear_fog_lower_point_mm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    headlight_washer_present = models.BooleanField(null=True, blank=True)

    left_34v_cd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    left_52h_cd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    left_high_beam_cd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    right_34v_cd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    right_52h_cd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    right_high_beam_cd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    turn_signal_frequency_per_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    turn_signal_frequency_hz = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'protocol_lights'

    def __str__(self):
        return f"Lights for protocol #{self.protocol_id}"