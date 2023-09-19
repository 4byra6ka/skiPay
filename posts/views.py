from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from posts.forms import AddPostMyForm, UpdatePostMyForm
# from skysend.forms import MailingSettingsForm, MailingClientForm, MailingMessageForm
from posts.models import Posts

from datetime import datetime
from django.utils import timezone

# from skysend.services import datetime_send_next, cron_send_mail, one_send_mail


class PostListView(ListView):
    """Список публичных публикаций"""
    model = Posts
    template_name = 'posts/posts_list.html'
    extra_context = {
        'title': 'Публикации'
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = Posts.objects.filter(is_published=True)
        return context


class PostFreeDetailView(DetailView):
    """Детали бесплатной публичной публикации"""
    model = Posts
    template_name = 'posts/posts_detail.html'

    def get_context_data(self, *args, **kwargs):
        if self.object.paid_published:
            raise PermissionDenied()
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        posts = Posts.objects.get(pk=self.object.pk)
        posts.count_views += 1
        posts.save()
        return context


class PostPayDetailView(LoginRequiredMixin, DetailView):
    """Детали платной публичной публикации"""
    model = Posts
    template_name = 'posts/posts_detail.html'

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        posts = Posts.objects.get(pk=self.object.pk)
        posts.count_views += 1
        posts.save()
        return context


class PostMyListView(PermissionRequiredMixin, ListView):
    """Список моих публикаций"""
    model = Posts
    template_name = 'posts/posts_my_list.html'
    extra_context = {
        'title': 'Мои публикации'
    }
    permission_required = ['posts.view_posts']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = Posts.objects.filter(owner=self.request.user)
        return context


class PostMyDetailView(PermissionRequiredMixin, DetailView):
    """Детали публикаций"""
    model = Posts
    template_name = 'posts/posts_my_detail.html'
    permission_required = ['posts.view_posts']

    def get_context_data(self, *args, **kwargs):
        if self.request.user == self.object.owner:
            context = super().get_context_data(*args, **kwargs)
            context['title'] = context['object']
        else:
            raise PermissionDenied()
        posts = Posts.objects.get(pk=self.object.pk)
        posts.count_views += 1
        posts.save()
        return context


class PostMyCreateView(PermissionRequiredMixin, CreateView):
    """Создание моей публикаций"""
    model = Posts
    template_name = 'posts/posts_my_form.html'
    permission_required = ['posts.add_posts']
    extra_context = {
        'title': 'Добавить публикацию'
    }
    form_class = AddPostMyForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:my_posts_detail', kwargs={'pk': self.object.pk})


class PostMyUpdateView(PermissionRequiredMixin, UpdateView):
    """Обновление контента моей публикаций"""
    model = Posts
    template_name = 'posts/posts_my_form.html'
    permission_required = ['posts.change_posts']
    form_class = UpdatePostMyForm

    def get_context_data(self, *args, **kwargs):
        if self.request.user == self.object.owner:
            context = super().get_context_data(*args, **kwargs)
            context['title'] = context['object']
        else:
            raise PermissionDenied()
        return context

    def get_success_url(self):
        return reverse_lazy('posts:my_posts_detail', kwargs={'pk': self.object.pk})


class PostMyDeleteView(PermissionRequiredMixin, DeleteView):
    """Удаление моей публикаций"""
    model = Posts
    template_name = 'posts/posts_my_confirm_delete.html'
    permission_required = ['posts.delete_posts']
    success_url = reverse_lazy('posts:my_posts')

    def get_context_data(self, *args, **kwargs):
        if self.request.user == self.object.owner:
            context = super().get_context_data(*args, **kwargs)
            context['title'] = context['object']
        else:
            raise PermissionDenied()
        return context
