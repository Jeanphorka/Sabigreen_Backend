from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField()  # ให้แสดงชื่อแทน id

    class Meta:
        model = Product
        fields = '__all__'
