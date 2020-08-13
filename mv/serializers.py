from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ModelMV


# chuyển dữ liệu từ model -> json chuyển đến client, chuyển dữ liệu từ json(client) -> object(model)

class Get_mv(serializers.ModelSerializer):
    class Meta:
        model = ModelMV
        fields = ('id', 'name_MV', 'singer_MV','img_MV', 'intro_MV', 'description_MV')
