from django.db import models
from django.db.models import (CharField, FloatField, DecimalField, IntegerField, DateTimeField, Value,
                              ExpressionWrapper, F, Q, Count, Sum, Avg, Subquery, OuterRef, Case, When, Window)
from django.db.models.functions import Concat

from common import utils as common_utils  # TODO : Manage classes and functions # TODO : Manage classes and functions
# from . import models
import datetime
from django.apps import apps

class OrderQuerySet(models.QuerySet):

    def get_all_orders(self):
        '''
        return list of unique/distinct productscategory
        '''
        return self.annotate(label=F('reference'), value=F('id')).values('label', 'value').distinct()

    def get_all_order_type_of_orders(self):
        '''
        return list of unique/distinct order_type
        '''
        return self.annotate(label=F('order_type'), value=F('order_type')).values('label', 'value').order_by('order_type').distinct('order_type')
    def get_all_incoterm_of_orders(self):
        '''
        return list of unique/distinct incoterm
        '''
        return self.annotate(label=F('incoterm'), value=F('incoterm')).values('label', 'value').order_by('incoterm').distinct('incoterm')