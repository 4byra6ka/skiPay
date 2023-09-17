from django.shortcuts import render
from django.views.generic import TemplateView


class MainView(TemplateView):
    """Главная страница"""
    template_name = 'main/main.html'
    extra_context = {
        'title': 'skiPay: Главная страница'
    }
