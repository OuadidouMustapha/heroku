from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'reference', 'unit_price', 'category')


class ProductDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'reference')
