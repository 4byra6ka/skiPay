import random

from django.views.generic import TemplateView

from posts.models import Posts


class MainView(TemplateView):
    """Главная страница"""
    template_name = 'main/main.html'
    extra_context = {
        'title': 'skiPay: Главная страница'
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        count_post = len(Posts.objects.filter(is_published=True))
        if count_post > 0:
            blog_3_post = random.sample(list(Posts.objects.filter(is_published=True)),
                                        count_post if count_post < 6 else 6)
            context['blogs'] = blog_3_post
            return context
