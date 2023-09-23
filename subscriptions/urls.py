from django.urls import path

from subscriptions.apps import SubscriptionsConfig
from subscriptions.views import SubscriptionsListView

app_name = SubscriptionsConfig.name

urlpatterns = [
    path("", SubscriptionsListView.as_view(), name="list"),
]
