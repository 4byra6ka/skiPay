from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from posts.models import Posts
from users.models import User


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(phone='+79876543210', first_name='user', last_name='test')
        self.user.set_password('Qwerty12#')
        self.user.save()
        self.client.post('/users/', {'id_phone': '+79876543210', 'id_password': 'Qwerty12#'})
        self.client.login(phone='+79876543210', password='Qwerty12#')

    def test_crud_post(self):
        self.client.login(phone='+79876543210', password='Qwerty12#')
        self.assertTrue(self.client.get(reverse('posts:posts')).status_code == 200)
        # Добавление поста
        self.user.user_permissions.add(Permission.objects.get(codename='view_posts'))
        response = self.client.get(reverse('posts:my_posts'))
        self.assertTrue(response.status_code == 200)
        # Изменение поста
        self.user.user_permissions.add(Permission.objects.get(codename='add_posts'))
        self.post1 = Posts.objects.create(
            owner=self.user,
            title="test free",
            content='test free',
            is_published=True
        )
        response = self.client.get(reverse('posts:my_posts_detail', kwargs={'pk': self.post1.pk}))
        self.assertTrue(response.status_code == 200)
        # Изменение поста
        self.user.user_permissions.add(Permission.objects.get(codename='change_posts'))
        response = self.client.post(reverse('posts:my_posts_update', kwargs={'pk': self.post1.pk}),
                                    {'id_title': 'testpay', 'id_content': 'testpay'})
        self.assertTrue(response.status_code == 200)
        # Удаление поста
        self.user.user_permissions.add(Permission.objects.get(codename='delete_posts'))
        response = self.client.get(reverse('posts:my_posts_delete', kwargs={'pk': self.post1.pk}), {})
        self.assertTrue(response.status_code == 200)
