from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .models import Product



class ProductSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'reference', 'unit_price', 'category')


class ProductDropdownSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'reference')
