from django.contrib.auth.models import User
from django.test import TestCase, Client as TestClient


class BaseTestCase(TestCase):
    """Base com usuario staff autenticado."""

    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.client.login(username='admin', password='admin123')


class RegularUserTestCase(TestCase):
    """Base com usuario comum (nao-staff)."""

    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='regular', password='pass123', is_staff=False)
        self.client.login(username='regular', password='pass123')
