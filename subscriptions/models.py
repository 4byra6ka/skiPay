from django.conf import settings
from django.db import models
from django.urls import reverse

from users.models import NULLABLE


class Subscriptions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    post = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, verbose_name='id сессии stripe')
    url_pay = models.TextField(verbose_name='Ссылка оплаты')
    payment_status = models.CharField(max_length=100, verbose_name='Статус оплаты')
    status_pay = models.BooleanField(verbose_name='Статус')

    def __str__(self):
        return f'{self.user}:{self.post}'

    # def get_absolute_url(self):
    #     return reverse('blog:blog', args=[str(self.id)])

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-create_date']

