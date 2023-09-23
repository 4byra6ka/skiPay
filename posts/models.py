from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from users.models import NULLABLE


class Posts(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Cодержимое')
    image = models.ImageField(upload_to='posts/', verbose_name='Изображение', **NULLABLE)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    last_change_date = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)
    is_published = models.BooleanField(verbose_name='Признак публикации')
    paid_published = models.BooleanField(verbose_name='Платная публикация', default=False)
    cost = models.IntegerField(verbose_name='Цена подписки', default=100)
    count_views = models.IntegerField(verbose_name='Количество просмотров', default=0)
    count_pay = models.IntegerField(verbose_name='Количество покупок', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:posts', args=[str(self.id)])

    def clean(self) -> None:
        super().clean()
        if self.cost < 100:
            raise ValidationError({'cost': 'Цена публикации не может быть ниже 100 рублей.'})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-create_date']
