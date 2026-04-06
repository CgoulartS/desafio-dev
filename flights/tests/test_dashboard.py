from datetime import date, time
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, Client as TestClient
from accounts.models import Cliente
from flights.models import Aviao, Voo, Reserva


class DashboardTest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = TestClient()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.client.login(username='admin', password='admin123')

    def test_metricas_vazias(self):
        r = self.client.get('/')
        self.assertEqual(r.context['total_avioes'], 0)
        self.assertEqual(r.context['taxa_ocupacao'], 0)

    def test_metricas_com_dados(self):
        a = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=10)
        v = Voo.objects.create(aviao=a, origem='GRU', destino='GIG', data=date(2026, 6, 1), horario=time(10, 0))
        c = Cliente.objects.create(nome='J', email='j@t.com', cpf='12345678901', telefone='1')
        Reserva.objects.create(cliente=c, voo=v, numero_assento=1)
        r = self.client.get('/')
        self.assertEqual(r.context['total_reservas'], 1)
        self.assertEqual(r.context['taxa_ocupacao'], 10.0)
