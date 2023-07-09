from rest_framework import serializers
from login import models
class GoodsSerializer(serializers.ModelSerializer):
    """
    protein Serializer
    """
    class Meta:
        model = models.Proteins
        fields = '__all__'
