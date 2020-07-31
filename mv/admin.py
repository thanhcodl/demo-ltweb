from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ModelMV


# Register your models here.
class CustomModelMV(admin.ModelAdmin):
    list_display = ['name_MV', 'time_Post']


admin.site.register(ModelMV, CustomModelMV)
