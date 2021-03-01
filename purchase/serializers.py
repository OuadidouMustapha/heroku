from rest_flex_fields import FlexFieldsModelSerializer

from rest_framework import serializers

from .models import Order, OrderDetail, Receipt, ReceiptDetail


class OrderSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'reference', 'ordered_at', 'supplier')


class ReceiptSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Receipt
        fields = ('id', 'order', 'reference', 'receipt_at', 'supplier')


class OrderDetailSerializer(FlexFieldsModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = OrderDetail
        fields = ('id', 'order', 'warehouse', 'product', 'ordered_quantity', 'unit_price',
                  'desired_at')


class ReceiptDetailSerializer(FlexFieldsModelSerializer):
    receipt = ReceiptSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = ReceiptDetail
        fields = ('id', 'order', 'order_detail', 'receipt', 'warehouse', 'product', 'receipted_quantity', 'unit_cost',
                  'status', 'receipt_at')
