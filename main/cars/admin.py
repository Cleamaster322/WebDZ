from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Generation)
admin.site.register(Configuration)
admin.site.register(CarData)
admin.site.register(Protocol)