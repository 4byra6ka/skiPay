from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, RedirectView

from posts.forms import AddPostMyForm, UpdatePostMyForm
from posts.models import Posts

from subscriptions.models import Subscriptions
from subscriptions.services import create_session, retrieve_session


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
        if self.request.user.is_authenticated:
            context['sub_read_list'] = Posts.objects.filter(is_published=True, subscriptions__user=self.request.user,
                                                            subscriptions__pay_status='complete')
            context['sub_pay_list'] = Posts.objects.filter(is_published=True, paid_published=True).exclude(
                subscriptions__user=self.request.user)
            context['sub_pay_open_list'] = Posts.objects.filter(is_published=True, paid_published=True,
                                                                subscriptions__user=self.request.user,
                                                                subscriptions__pay_status='open')
        return context


class PostDetailView(DetailView):
    """Детали бесплатной публичной публикации"""
    model = Posts
    template_name = 'posts/posts_detail.html'

    def get_context_data(self, *args, **kwargs):
        post = Posts.objects.get(pk=self.object.pk)
        if not self.object.paid_published:
            context = super().get_context_data(*args, **kwargs)
            context['title'] = context['object']
            post.count_views += 1
            post.save()
            return context
        if Subscriptions.objects.filter(user=self.request.user, post=post,
                                        pay_status='complete') or self.object.owner == self.request.user:
            context = super().get_context_data(*args, **kwargs)
            context['title'] = context['object']
            post.count_views += 1
            post.save()
            return context
        if self.object.paid_published:
            raise PermissionDenied()


class PostPayRedirectView(LoginRequiredMixin, RedirectView):
    """Детали платной публичной публикации"""

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Posts, pk=kwargs['pk'])
        subscription = Subscriptions.objects.filter(user=self.request.user)
        if subscription.filter(post=post, pay_status='complete'):
            return reverse_lazy("posts:posts_detail", kwargs={'pk': post.pk})
        elif subscription.filter(post=post, pay_status='open'):
            sub_retrieve_session = retrieve_session(subscription.get(post=post, pay_status='open').session_id)
            if sub_retrieve_session['status'] == 'complete':
                subscription_post = subscription.get(post=post, pay_status='open')
                subscription_post.payment_status = sub_retrieve_session['payment_status']
                subscription_post.pay_status = sub_retrieve_session['status']
                subscription_post.post.count_pay = subscription_post.post.count_pay + 1
                subscription_post.post.save()
                subscription_post.save()
                # task_retrieve_session.delay()
                return reverse_lazy("posts:posts_detail", kwargs={'pk': post.pk})
            return subscription.get(post=post, pay_status='open').url_pay
        if post.paid_published:
            success_url = f'http://{get_current_site(self.request)}{reverse_lazy("subscriptions:list")}'
            pay_session = create_session(success_url, f'Публикация: {post.title}', post.cost * 100)
            Subscriptions.objects.create(
                user=self.request.user,
                post=post,
                session_id=pay_session['id'],
                url_pay=pay_session['url'],
                payment_status=pay_session['payment_status'],
                pay_status=pay_session['status'],
            )
            return pay_session['url']
        return reverse_lazy("posts:posts")


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
