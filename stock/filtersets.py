from django_filters import rest_framework as filters
from .models import Product


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


# class CharInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass


class ProductFilter(filters.FilterSet):
    id__in = NumberInFilter(field_name='id', lookup_expr='in')
    reference__in = filters.BaseInFilter(
        field_name='reference', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['id', 'reference', 'category']
