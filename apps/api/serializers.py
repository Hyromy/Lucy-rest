from rest_framework import serializers
from . import models

class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guild
        fields = '__all__'
