from datetime import date, time
from voos.models import Aviao, Voo, Cliente, Reserva
from .base import BaseTestCase


class DashboardTest(BaseTestCase):
    def test_metricas_vazias(self):
        r = self.client.get('/')
        self.assertEqual(r.context['total_avioes'], 0)
        self.assertEqual(r.context['taxa_ocupacao'], 0)

    def test_metricas_com_dados(self):
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=10)
        voo = Voo.objects.create(aviao=aviao, origem='GRU', destino='GIG', data=date(2026, 6, 1), horario=time(10, 0))
        cliente = Cliente.objects.create(nome='J', email='j@t.com', cpf='12345678901', telefone='1')
        Reserva.objects.create(cliente=cliente, voo=voo, numero_assento=1)
        r = self.client.get('/')
        self.assertEqual(r.context['total_reservas'], 1)
        self.assertEqual(r.context['taxa_ocupacao'], 10.0)
