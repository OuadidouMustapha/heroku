from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Purchase(LoginRequiredMixin, TemplateView):
    template_name = "purchase/index.html"
