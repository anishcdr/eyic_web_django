# myapp/serializers.py

from rest_framework import serializers

class SoilDataSerializer(serializers.Serializer):
    grid_section = serializers.CharField()
    nitrogen = serializers.FloatField()
    phosphorus = serializers.FloatField()
    potassium = serializers.FloatField()
    moisture_level = serializers.FloatField()
