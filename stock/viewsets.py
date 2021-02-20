from .models import Product
from .serializers import ProductSerializer, ProductDropdownSerializer
from rest_framework import generics, views
from rest_framework.permissions import AllowAny
from django.db.models import F

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filtersets import ProductFilter


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ordering_fields = ['id', 'reference']
    search_fields = ['id', 'reference']
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', 'reference', 'category']
    filterset_class = ProductFilter
    # filter_backends = [DjangoFilterBackend,
    #                    filters.OrderingFilter, filters.SearchFilter]

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     id_list = self.request.GET.getlist("id")
    #     test = self.request.query_params.getlist('id')

    #     print('test ', test)

    #     qs = Product.objects.all()
    #     # list_id = self.request.query_params.get('id', None)
    #     if id_list is not None:
    #         print('id_list ', id_list)
    #         qs = qs.filter(id__in=id_list)
    #     return qs


class ProductDropdown(generics.ListAPIView):
    queryset = Product.objects.values('reference', 'id').distinct()
    serializer_class = ProductDropdownSerializer
    # FIXME permission used in demo mode
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return Product.objects.annotate(label=F('reference'), value=F('id')).values('label', 'value').distinct()


# class CategoryChart(views.APIView):
