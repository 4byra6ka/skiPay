from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from subscriptions.models import Subscriptions


class SubscriptionsListView(LoginRequiredMixin, ListView):
    """Список купленных подписок и оплата"""
    model = Subscriptions
    template_name = 'subscriptions/subscriptions_list.html'
    extra_context = {
        'title': 'Купленные подписки и оплаты'
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = Subscriptions.objects.filter(user=self.request.user)
        return context
