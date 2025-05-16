from django.db import models

# Create Brand models
class Brand(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=255)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name

# Create Model models
class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING,db_column='brand_id')
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=255)

    class Meta:
        db_table = 'models'

    def __str__(self):
        return self.name

# Create Generation models
class Generation(models.Model):
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING,db_column='model_id')
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
# Create Configuration models
class Configuration(models.Model):
    generation = models.ForeignKey(Generation, on_delete=models.DO_NOTHING,db_column='generation_id')
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    engine_name = models.CharField(max_length=100, null=True, blank=True)
    date_start = models.CharField(max_length=11)
    date_end = models.CharField(max_length=11)

    class Meta:
        db_table = 'configurations'

    def __str__(self):
        return self.name

# Create CarData models
class CarData(models.Model):
    configuration = models.ForeignKey(Configuration, on_delete=models.DO_NOTHING,db_column='configuration_id')
    front_tires = models.CharField(max_length=50)
    rear_tires = models.CharField(max_length=50)
    engine_capacity = models.FloatField()
    engine_power_hp = models.IntegerField()
    engine_power_kw = models.IntegerField()
    consumption = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    driver_type = models.CharField(max_length=50)
    seats_count = models.IntegerField()
    doors_count = models.IntegerField()
    clearance = models.IntegerField()
    trunk_volume = models.IntegerField()

    class Meta:
        db_table = 'car_data'

    def __str__(self):
        return f"{self.configuration.name} - {self.fuel_type}"