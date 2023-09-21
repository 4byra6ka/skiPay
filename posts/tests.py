from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Posts
from users.models import User


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(phone='+79876543210', first_name='user', last_name='test')
        self.user.set_password('Qwerty12#')
        self.user.save()
        self.client.post('/users/', {'id_phone': '+79876543210', 'id_password': 'Qwerty12#'})
        self.client.login(phone='+79876543210',password='Qwerty12#')



    def test_crud_post(self):
        self.client.login(phone='+79876543210', password='Qwerty12#')
        self.assertTrue(self.client.get(reverse('posts:posts')).status_code == 200)
        self.user.user_permissions.add(Permission.objects.get(codename='view_posts'))
        response = self.client.get(reverse('posts:my_posts'))
        self.assertTrue(response.status_code == 200)
        self.user.user_permissions.add(Permission.objects.get(codename='add_posts'))
        print(self.client.post(reverse('posts:my_posts_create'), {'id_title': 'testfree', 'id_content': 'testfree'}))
        response = self.client.get(reverse('posts:my_posts_detail'))
        # self.client.post(
        #     reverse('posts:my_posts_create', kwargs={'pk': self.test_bookinstance1.pk, }
        #
        #             )
        # self.test_post1 = Posts.objects.create(book=test_book, imprint='Unlikely Imprint, 2016',
        #                                        due_back=return_date, borrower=test_user1, status='o')
        # reverse('posts:my_posts_create', kwargs={'pk':self.test_bookinstance1.pk,}
    # def test_correct(self):
    #     user = authenticate(phone='+79876543210', password='Qwerty12#')
    #     self.assertTrue((user is not None) and user.is_authenticated)
    # def test_wrong_username(self):
    #     user = authenticate(username='user_nonexistent', password='Qwerty12#')
    #     self.assertFalse(user is not None and user.is_authenticated)
    # def test_wrong_pssword(self):
    #     user = authenticate(phone='+79876543210', password='wrong')
    #     self.assertFalse(user is not None and user.is_authenticated)
    #
    # def test_login_web(self):
    #     c = Client()
    #     response = c.get("/")
    #     print(response.status_code)
    #     response = c.get("/users/")
    #     print(response.status_code)
    #     # response = c.post('/users/', {'phone': '+79876543210', 'password': 'Qwerty12#'})
    #     response = self.client.post('/users/', {'id_phone': '+79876543210', 'id_password': 'Qwerty12#'})
    #     print(response.status_code)
    #     self.assertTrue(response.status_code == 200)

