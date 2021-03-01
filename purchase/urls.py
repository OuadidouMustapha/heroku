from django.urls import path
from purchase.dashs import purchase_dash
from rest_framework.routers import DefaultRouter

from . import views
from . import viewsets

app_name = 'purchase'

# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'api/orderdetail_delay/', viewsets.OrderDetailDelay)

urlpatterns = [
    path('purchase', views.Purchase.as_view(),
         name='purchase'),

    path('api/orderdetail_delay/', viewsets.OrderDetailDelay.as_view(),
         name='orderdetail_delay'),
    path('api/orderdetail_list/', viewsets.OrderDetailList.as_view(),
         name='orderdetail_list'),
    #     # API
    #     path('', include(router.urls)),
]
