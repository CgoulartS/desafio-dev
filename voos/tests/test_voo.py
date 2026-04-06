from datetime import date, time
from django.test import TestCase
from voos.models import Aviao, Voo, Cliente, Reserva
from .base import BaseTestCase


class VooModelTest(TestCase):
    def test_criar_voo_com_uuid(self):
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        voo = Voo.objects.create(aviao=aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        self.assertIn('GRU', str(voo))
        self.assertEqual(len(str(voo.pk)), 36)

    def test_assentos_disponiveis(self):
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=3)
        voo = Voo.objects.create(aviao=aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        self.assertEqual(voo.assentos_disponiveis, 3)


class VooViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.voo = Voo.objects.create(aviao=self.aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))

    def test_listar_voos(self):
        self.assertEqual(self.client.get('/voos/').status_code, 200)

    def test_detail_voo(self):
        self.assertEqual(self.client.get(f'/voos/{self.voo.pk}/').status_code, 200)

    def test_buscar_por_origem(self):
        Voo.objects.create(aviao=self.aviao, origem='CNF', destino='SSA', data=date(2026, 7, 1), horario=time(14, 0))
        r = self.client.get('/voos/?q=GRU')
        self.assertEqual(len(r.context['voos']), 1)


class VooAssentosTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=5)
        self.voo = Voo.objects.create(aviao=self.aviao, origem='GRU', destino='GIG', data=date(2026, 6, 1), horario=time(10, 0))
        cliente = Cliente.objects.create(nome='Joao', email='j@t.com', cpf='12345678901', telefone='11999')
        Reserva.objects.create(cliente=cliente, voo=self.voo, numero_assento=2)

    def test_endpoint_retorna_json(self):
        r = self.client.get(f'/voos/{self.voo.pk}/assentos/')
        data = r.json()
        self.assertEqual(data['max_passageiros'], 5)
        self.assertEqual(data['assentos_ocupados'], [2])

    def test_endpoint_requer_autenticacao(self):
        self.client.logout()
        self.assertEqual(self.client.get(f'/voos/{self.voo.pk}/assentos/').status_code, 302)
