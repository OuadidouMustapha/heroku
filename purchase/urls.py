from django.urls import path
from purchase.dashs import purchase_dash

from . import views

app_name = 'purchase'
urlpatterns = [
    path('purchase', views.Purchase.as_view(),
        name='purchase'),
]

