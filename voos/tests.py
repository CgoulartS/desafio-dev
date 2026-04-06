from datetime import date, time

from django.contrib.auth.models import User
from django.test import TestCase, Client


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')


# --- Aviao Tests (Story 1.3) ---

class AviaoModelTest(TestCase):
    def test_criar_aviao_valido(self):
        from voos.models import Aviao
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.assertEqual(str(aviao), 'Boeing 737')
        self.assertEqual(aviao.max_passageiros, 180)

    def test_rejeitar_max_passageiros_zero(self):
        from voos.forms import AviaoForm
        form = AviaoForm(data={'modelo': '737', 'fabricante': 'Boeing', 'max_passageiros': 0})
        self.assertFalse(form.is_valid())
        self.assertIn('max_passageiros', form.errors)


class AviaoViewTest(BaseTestCase):
    def test_listar_avioes(self):
        response = self.client.get('/avioes/')
        self.assertEqual(response.status_code, 200)

    def test_criar_aviao_post(self):
        response = self.client.post('/avioes/novo/', {
            'modelo': 'A320', 'fabricante': 'Airbus', 'max_passageiros': 150
        })
        self.assertEqual(response.status_code, 302)
        from voos.models import Aviao
        self.assertEqual(Aviao.objects.count(), 1)

    def test_view_requer_autenticacao(self):
        self.client.logout()
        response = self.client.get('/avioes/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


# --- Voo Tests (Story 2.1) ---

class VooModelTest(TestCase):
    def test_criar_voo_valido(self):
        from voos.models import Aviao, Voo
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        voo = Voo.objects.create(aviao=aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        self.assertIn('GRU', str(voo))


class VooViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        from voos.models import Aviao, Voo
        self.aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.voo = Voo.objects.create(aviao=self.aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))

    def test_listar_voos(self):
        response = self.client.get('/voos/')
        self.assertEqual(response.status_code, 200)

    def test_detail_voo(self):
        response = self.client.get(f'/voos/{self.voo.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_requer_autenticacao(self):
        self.client.logout()
        response = self.client.get('/voos/')
        self.assertEqual(response.status_code, 302)


# --- Cliente Tests (Story 2.2) ---

class ClienteModelTest(TestCase):
    def test_criar_cliente_valido(self):
        from voos.models import Cliente
        cliente = Cliente.objects.create(nome='Joao Silva', email='joao@test.com', cpf='12345678901', telefone='11999999999')
        self.assertEqual(str(cliente), 'Joao Silva')

    def test_email_unico(self):
        from voos.models import Cliente
        from django.db import IntegrityError
        Cliente.objects.create(nome='Joao', email='joao@test.com', cpf='12345678901', telefone='11999999999')
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nome='Maria', email='joao@test.com', cpf='98765432100', telefone='11888888888')

    def test_cpf_unico(self):
        from voos.models import Cliente
        from django.db import IntegrityError
        Cliente.objects.create(nome='Joao', email='joao@test.com', cpf='12345678901', telefone='11999999999')
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nome='Maria', email='maria@test.com', cpf='12345678901', telefone='11888888888')


class ClienteViewTest(BaseTestCase):
    def test_listar_clientes(self):
        response = self.client.get('/clientes/')
        self.assertEqual(response.status_code, 200)

    def test_view_requer_autenticacao(self):
        self.client.logout()
        response = self.client.get('/clientes/')
        self.assertEqual(response.status_code, 302)


# --- Reserva Tests (Story 2.3) ---

class ReservaTestBase(BaseTestCase):
    def setUp(self):
        super().setUp()
        from voos.models import Aviao, Voo, Cliente
        self.aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=3)
        self.voo = Voo.objects.create(aviao=self.aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        self.cliente1 = Cliente.objects.create(nome='Joao', email='joao@test.com', cpf='12345678901', telefone='11999999999')
        self.cliente2 = Cliente.objects.create(nome='Maria', email='maria@test.com', cpf='98765432100', telefone='11888888888')


class ReservaModelTest(ReservaTestBase):
    def test_criar_reserva_valida(self):
        from voos.models import Reserva
        reserva = Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        self.assertIn('Joao', str(reserva))

    def test_assento_duplicado(self):
        from voos.models import Reserva
        from django.db import IntegrityError
        Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        with self.assertRaises(IntegrityError):
            Reserva.objects.create(cliente=self.cliente2, voo=self.voo, numero_assento=1)

    def test_cliente_duplicado_no_voo(self):
        from voos.models import Reserva
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
        from voos.models import Reserva
        from voos.forms import ReservaForm
        c3 = self.__class__.__mro__[0]  # dummy
        from voos.models import Cliente
        c3 = Cliente.objects.create(nome='Pedro', email='pedro@test.com', cpf='11122233344', telefone='11777777777')
        Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        Reserva.objects.create(cliente=self.cliente2, voo=self.voo, numero_assento=2)
        Reserva.objects.create(cliente=c3, voo=self.voo, numero_assento=3)
        c4 = Cliente.objects.create(nome='Ana', email='ana@test.com', cpf='55566677788', telefone='11666666666')
        form = ReservaForm(data={'cliente': c4.pk, 'voo': self.voo.pk, 'numero_assento': 1})
        self.assertFalse(form.is_valid())


class ReservaViewTest(ReservaTestBase):
    def test_listar_reservas(self):
        response = self.client.get('/reservas/')
        self.assertEqual(response.status_code, 200)

    def test_criar_reserva_post(self):
        response = self.client.post('/reservas/nova/', {
            'cliente': self.cliente1.pk, 'voo': self.voo.pk, 'numero_assento': 1
        })
        self.assertEqual(response.status_code, 302)
        from voos.models import Reserva
        self.assertEqual(Reserva.objects.count(), 1)

    def test_view_requer_autenticacao(self):
        self.client.logout()
        response = self.client.get('/reservas/')
        self.assertEqual(response.status_code, 302)
