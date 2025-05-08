from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    tea_type = serializers.StringRelatedField()  # ให้แสดงชื่อแทน id

    class Meta:
        model = Product
        fields = '__all__'
