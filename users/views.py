from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView, CreateView
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm
from users.models import User
from posts.models import Posts


class CustomLoginView(FormView):
    """Контроллер входа пользователя"""
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Войти'
    }

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('main:main')
        if form.is_valid():
            try:
                phone = form.cleaned_data['phone']
                password = form.cleaned_data['password']
                user = User.objects.get(phone=phone)
                if user.check_password(password):
                    login(self.request, user)
                    perm_post = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Posts))
                    user.user_permissions.add(perm_post.get(codename='add_posts'))
                    user.user_permissions.add(perm_post.get(codename='view_posts'))
                    user.user_permissions.add(perm_post.get(codename='change_posts'))
                    user.user_permissions.add(perm_post.get(codename='delete_posts'))
                    if self.request.GET.get('next', '') != '':
                        return HttpResponseRedirect(self.request.GET.get('next', ''))
                    return redirect('main:main')
                else:
                    messages.add_message(self.request, messages.WARNING, 'Неправильный номер телефона или пароль')
            except:
                messages.add_message(self.request, messages.WARNING, 'Неправильный номер телефона или пароль')
            else:
                message = 'Login failed!'
        return render(
            self.request, 'users/login.html', context={'form': form})


class RegisterView(CreateView):
    """Контроллер регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {
        'title': 'Регистрация'
    }

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = True
            self.object.save()
            return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO,
                             f'Пользователь с телефонным номером {self.object.phone} создан.')
        return reverse_lazy('users:login')


class ProfileView(UpdateView):
    """Обновление профиля"""
    model = User
    form_class = UserProfileForm
    extra_context = {
        'title': 'Данные профиля'
    }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Данные профиля изменены')
        return reverse_lazy('users:profile')
