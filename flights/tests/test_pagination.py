from django.contrib.auth.models import User
from django.test import TestCase, Client as TestClient
from flights.models import Aviao


class PaginationTest(TestCase):
    def setUp(self):
        self.client = TestClient()
        User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.client.login(username='admin', password='admin123')

    def test_paginacao_avioes(self):
        for i in range(15):
            Aviao.objects.create(modelo=f'M{i}', fabricante='F', max_passageiros=100)
        self.assertEqual(len(self.client.get('/avioes/').context['avioes']), 10)
        self.assertEqual(len(self.client.get('/avioes/?page=2').context['avioes']), 5)
