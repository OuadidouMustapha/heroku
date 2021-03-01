from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework import generics

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser






from .models import (ProductCategory, Product, Supplier, Customer, Supply, SupplyDetail,
                     Order, Delivery, DeliveryDetail, Warehouse, StockControl)


class ProductIndexView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "stock/product_index.html"
    context_object_name = 'product_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # NOTE : You can use super(ProductDescriptionView, self) to inherate from other classes
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['page_title'] = 'Product Dashboard'
        context['table_title'] = 'Product List'
        context['dash_title'] = 'Product Description'
        context['total_products'] = Product.get_total_products()
        context['total_categories'] = ProductCategory.get_total_categories()
        return context


class StockIndexView(LoginRequiredMixin, ListView):
    # permission_required = 'polls.add_choice'

    model = StockControl
    product_category_model = ProductCategory
    template_name = "stock/stock_index.html"
    context_object_name = 'stock_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['product_category_model'] = self.product_category_model
        context['product_category_list'] = ProductCategory.tree.all()
        context['page_elements'] = {}
        context['page_elements']['page_title'] = 'Stock Overview'
        context['page_elements']['table_title'] = 'Stock List'
        # context['page_elements']['dash_stock_value_title'] = 'Stock Value'
        # context['page_elements']['dash_stock_coverage_title'] = 'Stock DIO'
        return context


class StockValueView(LoginRequiredMixin, TemplateView):
    template_name = "stock/stock_value.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_elements'] = {}
        context['page_elements']['page_title'] = 'Stock Value'
        context['page_elements']['dash_title'] = 'Stock Value'
        return context

class StockDioView(LoginRequiredMixin, TemplateView):
    template_name = "stock/stock_dio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_elements'] = {}
        context['page_elements']['page_title'] = 'Stock DIO'
        context['page_elements']['dash_title'] = 'Stock DIO'
        return context


class StockParetoView(LoginRequiredMixin, TemplateView):
    template_name = "stock/stock_pareto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_elements'] = {}
        context['page_elements']['page_title'] = 'Pareto Distribution'
        context['page_elements']['dash_title'] = 'Pareto Distribution'
        return context



class DeliveryIndexView(LoginRequiredMixin, TemplateView):
    template_name = "stock/sale_index.html"


class PurchaseIndexView(LoginRequiredMixin, TemplateView):
    template_name = "stock/purchase_index.html"


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = "stock/index.html"

class ProductListApiView(APIView):
    
    def get(self, request):
        products=Product.objects.all()
        serializer=ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data,many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            print(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailApiView(APIView):
    """
    Retrieve, update or delete a Product instance.
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Product = self.get_object(pk)
        serializer = ProductSerializer(Product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Product = self.get_object(pk)
        serializer = ProductSerializer(Product, data=request.dataProduct,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Product = self.get_object(pk)
        Product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListTodo(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @csrf_exempt
    def snippet_list(request):
        """
        List all code snippets, or create a new snippet.
        """
        if request.method == 'GET':
            snippets = Product.objects.all()
            serializer = ProductSerializer(snippets, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        
# def get_product_category_tree(request):
#     return render(request, "stock/product_category_tree.html", {'product_category': ProductCategory.objects.all()})
