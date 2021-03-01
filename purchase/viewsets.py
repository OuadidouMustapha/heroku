
from .models import Product
# from .serializers import
# from rest_framework import generics, views
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django_pandas.io import read_frame
from stock.models import Product, ProductCategory
from purchase.models import OrderDetail, ReceiptDetail
from rest_framework.response import Response
import numpy as np
from .serializers import OrderDetailSerializer, ReceiptDetailSerializer
from .filtersets import OrderDetailFilter, ReceiptDetailFilter
import json
import pandas as pd


def add_column_in_full_date(row, receiptdetail_df):
    '''
    cumul_receipted_quantity & cumul_ordered_quantity should be created first
    '''
    var = receiptdetail_df[(
        (receiptdetail_df['order__id'] == row['order__id']) &
        (receiptdetail_df['product'] == row['product']) &
        (receiptdetail_df['cumul_receipted_quantity']
         >= row['cumul_ordered_quantity'])
    )].sort_values(['cumul_receipted_quantity'], ascending=True).head(1)['receipt__receipt_at']

    if len(var) != 0:
        row['in_full_date'] = var.iloc[0]
    else:
        row['in_full_date'] = None
    return row


def add_column_delay_days(row):
    '''
    in_full_date should be created first
    '''
    if row['desired_at'] != None and row['in_full_date'] != None:
        row['delay_days'] = row['desired_at'] - row['in_full_date']
        row['delay_days'] = row['delay_days'].days
    else:
        row['delay_days'] = None

    return row


def add_column_otif_status(row):
    '''
    delay_days should be created first
    '''
    if row['delay_days'] != None:
        # TODO add 'partialy delivered' (IF-OT+)
        if row['delay_days'] >= 0:
            row['otif_status'] = 'IF+OT+'
        else:
            row['otif_status'] = 'IF+OT-'
    else:
        row['otif_status'] = 'Not delivered'

    return row


def add_columns_rest(row, receiptdetail_df, orderdetail_df):

    max_reciption = 0
    max_ordred = 0
    max_by_order_product_order = orderdetail_df[(orderdetail_df['order__id'] == row['order__id']) & (
        orderdetail_df['product'] == row['product'])].sort_values(['cumul_ordered_quantity'], ascending=False).head(1)['cumul_ordered_quantity']
    max_by_order_product_reciption = receiptdetail_df[(receiptdetail_df['order__id'] == row['order__id']) & (
        receiptdetail_df['product'] == row['product'])].sort_values(['cumul_receipted_quantity'], ascending=False).head(1)['cumul_receipted_quantity']
    if len(max_by_order_product_reciption) != 0:
        max_reciption = max_by_order_product_reciption.iloc[0]
    if len(max_by_order_product_order) != 0:
        max_ordred = max_by_order_product_order.iloc[0]
    row['rest_totle'] = max_reciption-max_ordred

    # Remaining rest
    if row['cumul_ordered_quantity'] <= max_reciption:
        row['rest'] = 0
    else:
        row['rest'] = max_reciption - row['cumul_ordered_quantity']

        # Remaining rest no all
    if row['cumul_ordered_quantity'] <= max_reciption:
        row['rest_no_all'] = 0
    else:
        if abs(max_reciption - row['cumul_ordered_quantity']) > row['ordered_quantity']:
            row['rest_no_all'] = - row['ordered_quantity']
        elif max_reciption == 0:
            row['rest_no_all'] = - row['ordered_quantity']
        else:
            row['rest_no_all'] = max_reciption - row['cumul_ordered_quantity']
    return row


def prepare_orderdetail_df(orderdetail_json, receiptdetail_json):
    # Get the orderedDict and convert to dataframe
    orderdetail_json = json.loads(orderdetail_json)
    orderdetail_df = pd.json_normalize(orderdetail_json, sep='__')
    # print(orderdetail_df.head())
    orderdetail_df['desired_at'] = orderdetail_df['desired_at'].astype(
        'datetime64[ns]')
    # Compute cumulative quantity by {order, product}
    orderdetail_df['cumul_ordered_quantity'] = orderdetail_df.sort_values(
        ['desired_at'], ascending=True).groupby(['order__id', 'product'])['ordered_quantity'].cumsum()

    # Get the orderedDict and convert to dataframe
    receiptdetail_json = json.loads(receiptdetail_json)
    receiptdetail_df = pd.json_normalize(receiptdetail_json, sep='__')
    # print(receiptdetail_df.head())
    receiptdetail_df['receipt__receipt_at'] = receiptdetail_df['receipt__receipt_at'].astype(
        'datetime64[ns]')
    # print(receiptdetail_df.dtypes)
    # Compute cumulative quantity by {order, receipt, product}
    receiptdetail_df['cumul_receipted_quantity'] = receiptdetail_df.sort_values(
        ['receipt__receipt_at'], ascending=True).groupby(['order__id', 'receipt__id', 'product'])['receipted_quantity'].cumsum()

    # Add calculated columns
    orderdetail_df = orderdetail_df.apply(
        lambda row: add_column_in_full_date(row, receiptdetail_df), axis=1)
    # print(orderdetail_df.head())
    orderdetail_df = orderdetail_df.apply(
        lambda row: add_column_delay_days(row), axis=1)
    orderdetail_df = orderdetail_df.apply(
        lambda row: add_column_otif_status(row), axis=1)
    orderdetail_df = orderdetail_df.apply(
        lambda row: add_columns_rest(row, receiptdetail_df, orderdetail_df), axis=1)

    # Convert NaN to None
    orderdetail_df = orderdetail_df.replace({np.nan: None})

    return orderdetail_df


class OrderDetailList(ListAPIView):
    queryset = OrderDetail.objects.select_related('order')
    serializer_class = OrderDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderDetailFilter


class ReceiptDetailList(ListAPIView):
    queryset = ReceiptDetail.objects.select_related('order', 'receipt')
    serializer_class = ReceiptDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReceiptDetailFilter


class OrderDetailDelay(APIView):
    """
    """
    # serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ProductFilter

    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        """
        # Get filtered queries from other viewsets
        orderdetail_json = json.dumps(
            OrderDetailList.as_view()(request=request._request).data)
        receiptdetail_json = json.dumps(
            ReceiptDetailList.as_view()(request=request._request).data)

        # Do data transformation
        orderdetail_df = prepare_orderdetail_df(
            orderdetail_json, receiptdetail_json)
        context = orderdetail_df.to_dict('records')
        return Response(context)


''' Examples from the doc'''
# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """

#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """

#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
