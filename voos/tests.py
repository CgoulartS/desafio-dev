from datetime import date, time

from django.contrib.auth.models import User
from django.test import TestCase, Client as TestClient

from voos.models import Aviao, Voo, Cliente, Reserva


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.client.login(username='admin', password='admin123')


class RegularUserTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='regular', password='pass123', is_staff=False)
        self.client.login(username='regular', password='pass123')


# === Aviao ===

class AviaoModelTest(TestCase):
    def test_criar_aviao_com_uuid(self):
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.assertEqual(str(aviao), 'Boeing 737')
        self.assertEqual(len(str(aviao.pk)), 36)

    def test_rejeitar_max_passageiros_zero(self):
        from voos.forms import AviaoForm
        form = AviaoForm(data={'modelo': '737', 'fabricante': 'Boeing', 'max_passageiros': 0})
        self.assertFalse(form.is_valid())


class AviaoViewTest(BaseTestCase):
    def test_listar_avioes(self):
        self.assertEqual(self.client.get('/avioes/').status_code, 200)

    def test_criar_aviao_post(self):
        r = self.client.post('/avioes/novo/', {'modelo': 'A320', 'fabricante': 'Airbus', 'max_passageiros': 150})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Aviao.objects.count(), 1)

    def test_requer_autenticacao(self):
        self.client.logout()
        self.assertEqual(self.client.get('/avioes/').status_code, 302)


class AviaoRBACTest(RegularUserTestCase):
    def test_nao_staff_nao_cria(self):
        self.assertEqual(self.client.get('/avioes/novo/').status_code, 403)

    def test_nao_staff_nao_deleta(self):
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.assertEqual(self.client.post(f'/avioes/{aviao.pk}/excluir/').status_code, 403)


# === Voo ===

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


# === Cliente ===

class ClienteModelTest(TestCase):
    def test_criar_cliente_com_uuid(self):
        c = Cliente.objects.create(nome='Joao', email='joao@t.com', cpf='12345678901', telefone='11999')
        self.assertEqual(len(str(c.pk)), 36)

    def test_email_unico(self):
        from django.db import IntegrityError
        Cliente.objects.create(nome='Joao', email='joao@t.com', cpf='12345678901', telefone='11999')
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nome='Maria', email='joao@t.com', cpf='98765432100', telefone='11888')

    def test_cpf_unico(self):
        from django.db import IntegrityError
        Cliente.objects.create(nome='Joao', email='joao@t.com', cpf='12345678901', telefone='11999')
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nome='Maria', email='maria@t.com', cpf='12345678901', telefone='11888')


class ClienteViewTest(BaseTestCase):
    def test_listar_clientes(self):
        self.assertEqual(self.client.get('/clientes/').status_code, 200)

    def test_buscar_por_nome(self):
        Cliente.objects.create(nome='Joao', email='joao@t.com', cpf='12345678901', telefone='11999')
        Cliente.objects.create(nome='Maria', email='maria@t.com', cpf='98765432100', telefone='11888')
        r = self.client.get('/clientes/?q=Joao')
        self.assertEqual(len(r.context['clientes']), 1)


# === Reserva ===

class ReservaTestBase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=3)
        self.voo = Voo.objects.create(aviao=self.aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        self.cliente1 = Cliente.objects.create(nome='Joao', email='joao@t.com', cpf='12345678901', telefone='11999')
        self.cliente2 = Cliente.objects.create(nome='Maria', email='maria@t.com', cpf='98765432100', telefone='11888')


class ReservaModelTest(ReservaTestBase):
    def test_criar_reserva_com_uuid(self):
        r = Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        self.assertEqual(len(str(r.pk)), 36)

    def test_assento_duplicado(self):
        from django.db import IntegrityError
        Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        with self.assertRaises(IntegrityError):
            Reserva.objects.create(cliente=self.cliente2, voo=self.voo, numero_assento=1)

    def test_cliente_duplicado_no_voo(self):
        from django.db import IntegrityError
        Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        with self.assertRaises(IntegrityError):
            Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=2)


class ReservaFormTest(ReservaTestBase):
    def test_assento_excede_capacidade(self):
        from voos.forms import ReservaForm
        form = ReservaForm(data={'cliente': self.cliente1.pk, 'voo': self.voo.pk, 'numero_assento': 10})
        self.assertFalse(form.is_valid())

    def test_voo_lotado(self):
        from voos.forms import ReservaForm
        c3 = Cliente.objects.create(nome='Pedro', email='pedro@t.com', cpf='11122233344', telefone='11777')
        Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        Reserva.objects.create(cliente=self.cliente2, voo=self.voo, numero_assento=2)
        Reserva.objects.create(cliente=c3, voo=self.voo, numero_assento=3)
        c4 = Cliente.objects.create(nome='Ana', email='ana@t.com', cpf='55566677788', telefone='11666')
        form = ReservaForm(data={'cliente': c4.pk, 'voo': self.voo.pk, 'numero_assento': 1})
        self.assertFalse(form.is_valid())


class ReservaViewTest(ReservaTestBase):
    def test_listar_reservas(self):
        self.assertEqual(self.client.get('/reservas/').status_code, 200)

    def test_criar_reserva_post(self):
        r = self.client.post('/reservas/nova/', {'cliente': self.cliente1.pk, 'voo': self.voo.pk, 'numero_assento': 1})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Reserva.objects.count(), 1)


class ReservaPrivacidadeTest(RegularUserTestCase):
    def test_usuario_comum_ve_apenas_suas_reservas(self):
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=10)
        voo = Voo.objects.create(aviao=aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        meu = Cliente.objects.create(nome='Eu', email='eu@t.com', cpf='11111111111', telefone='1', usuario=self.user)
        outro = Cliente.objects.create(nome='Outro', email='outro@t.com', cpf='22222222222', telefone='2')
        Reserva.objects.create(cliente=meu, voo=voo, numero_assento=1)
        Reserva.objects.create(cliente=outro, voo=voo, numero_assento=2)
        r = self.client.get('/reservas/')
        self.assertEqual(len(r.context['reservas']), 1)


# === Dashboard ===

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


# === Paginacao ===

class PaginationTest(BaseTestCase):
    def test_paginacao_avioes(self):
        for i in range(15):
            Aviao.objects.create(modelo=f'M{i}', fabricante='F', max_passageiros=100)
        self.assertEqual(len(self.client.get('/avioes/').context['avioes']), 10)
        self.assertEqual(len(self.client.get('/avioes/?page=2').context['avioes']), 5)


# === Assentos Endpoint ===

class VooAssentosTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=5)
        self.voo = Voo.objects.create(aviao=self.aviao, origem='GRU', destino='GIG', data=date(2026, 6, 1), horario=time(10, 0))
        self.cliente = Cliente.objects.create(nome='Joao', email='j@t.com', cpf='12345678901', telefone='11999')
        Reserva.objects.create(cliente=self.cliente, voo=self.voo, numero_assento=2)

    def test_endpoint_retorna_json(self):
        r = self.client.get(f'/voos/{self.voo.pk}/assentos/')
        data = r.json()
        self.assertEqual(data['max_passageiros'], 5)
        self.assertEqual(data['assentos_ocupados'], [2])

    def test_endpoint_requer_autenticacao(self):
        self.client.logout()
        self.assertEqual(self.client.get(f'/voos/{self.voo.pk}/assentos/').status_code, 302)
