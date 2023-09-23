from django.urls import path

from main.apps import MainConfig
from main.views import MainView  # MainView,

app_name = MainConfig.name

urlpatterns = [
    path('', MainView.as_view(), name='main'),
]
