from datetime import date, time
from django.contrib.auth.models import User
from django.test import TestCase, Client as TestClient
from accounts.models import Cliente
from flights.models import Aviao, Voo, Reserva


class StaffTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.client.login(username='admin', password='admin123')


class VooModelTest(TestCase):
    def test_criar_com_uuid(self):
        a = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        v = Voo.objects.create(aviao=a, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        self.assertEqual(len(str(v.pk)), 36)
        self.assertIn('GRU', str(v))

    def test_assentos_disponiveis(self):
        a = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=3)
        v = Voo.objects.create(aviao=a, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        self.assertEqual(v.assentos_disponiveis, 3)


class VooViewTest(StaffTestCase):
    def setUp(self):
        super().setUp()
        self.aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.voo = Voo.objects.create(aviao=self.aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))

    def test_listar(self):
        self.assertEqual(self.client.get('/voos/').status_code, 200)

    def test_detail(self):
        self.assertEqual(self.client.get(f'/voos/{self.voo.pk}/').status_code, 200)

    def test_buscar_por_origem(self):
        Voo.objects.create(aviao=self.aviao, origem='CNF', destino='SSA', data=date(2026, 7, 1), horario=time(14, 0))
        r = self.client.get('/voos/?q=GRU')
        self.assertEqual(len(r.context['voos']), 1)


class VooAssentosTest(StaffTestCase):
    def setUp(self):
        super().setUp()
        a = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=5)
        self.voo = Voo.objects.create(aviao=a, origem='GRU', destino='GIG', data=date(2026, 6, 1), horario=time(10, 0))
        c = Cliente.objects.create(nome='João', email='j@t.com', cpf='12345678901', telefone='11999')
        Reserva.objects.create(cliente=c, voo=self.voo, numero_assento=2)

    def test_endpoint_json(self):
        r = self.client.get(f'/voos/{self.voo.pk}/assentos/')
        data = r.json()
        self.assertEqual(data['max_passageiros'], 5)
        self.assertEqual(data['assentos_ocupados'], [2])

    def test_requer_auth(self):
        self.client.logout()
        self.assertEqual(self.client.get(f'/voos/{self.voo.pk}/assentos/').status_code, 302)
