from rest_framework import serializers
from . models import Product,ProductCategory
from drf_dynamic_fields import DynamicFieldsMixin
from drf_queryfields import QueryFieldsMixin
from django_restql.mixins import DynamicFieldsMixin


class ProductCategorySerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
class ProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    category = ProductCategorySerializer()
    class Meta:
        model=Product
        fields = '__all__'
    def create(self, validated_data):
        productCategory = ProductCategory.objects.get(pk=validated_data.pop('event'))
        product = Product.objects.create(**validated_data)
        product.category = productCategory
        product.save()
        return product
    def to_representation(self, product):
        representation = super(ProductSerializer, self).to_representation(product)
        # representation['assigment'] = ProductCategorySerializer(product.assigment_set.all(), many=True).data
        return representation 
    