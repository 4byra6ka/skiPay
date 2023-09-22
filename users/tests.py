from django.contrib.auth import authenticate
from django.test import TestCase

from users.models import User


class SigninTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(phone='+79876543210', first_name='user', last_name='test')
        self.user.set_password('Qwerty12#')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(phone='+79876543210', password='Qwerty12#')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='user_nonexistent', password='Qwerty12#')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(phone='+79876543210', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_login_web(self):
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)
        response = self.client.get("/users/")
        self.assertTrue(response.status_code == 200)
        response = self.client.post('/users/', {'id_phone': '+79876543210', 'id_password': 'Qwerty12#'})
        self.assertTrue(response.status_code == 200)
