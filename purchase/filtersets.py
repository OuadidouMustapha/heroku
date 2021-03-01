from django_filters import rest_framework as filters
from .models import OrderDetail, ReceiptDetail


# class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
#     pass


# class CharInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass


class OrderDetailFilter(filters.FilterSet):
    # id__in = NumberInFilter(field_name='id', lookup_expr='in')
    # reference__in = filters.BaseInFilter(
    #     field_name='reference', lookup_expr='in')

    class Meta:
        model = OrderDetail
        fields = {
            'id': ['exact'],
            'product': ['exact', 'in'],
            'warehouse': ['exact', 'in'],
            'order__supplier': ['exact', 'in'],
            'desired_at': ['gte', 'lte', 'exact', 'gt', 'lt', 'range'],
        }
        # fields = ['order', 'ordered_quantity', 'unit_price',
        #           'desired_at', 'order__reference', 'order__ordered_at']


class ReceiptDetailFilter(filters.FilterSet):
    # id__in = NumberInFilter(field_name='id', lookup_expr='in')
    # reference__in = filters.BaseInFilter(
    #     field_name='reference', lookup_expr='in')

    class Meta:
        model = ReceiptDetail
        fields = ['order', 'order_detail', 'receipt', 'warehouse', 'product', 'receipted_quantity', 'unit_cost',
                  'status', 'receipt_at', 'receipt__order', 'receipt__reference', 'receipt__receipt_at', 'receipt__supplier']
