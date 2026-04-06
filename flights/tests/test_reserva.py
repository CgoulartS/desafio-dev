from datetime import date, time
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase, Client as TestClient
from accounts.models import Cliente
from flights.models import Aviao, Voo, Reserva
from flights.forms import ReservaForm


class StaffTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.client.login(username='admin', password='admin123')
        self.aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=3)
        self.voo = Voo.objects.create(aviao=self.aviao, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        self.c1 = Cliente.objects.create(nome='João', email='joao@t.com', cpf='12345678901', telefone='11999')
        self.c2 = Cliente.objects.create(nome='Maria', email='maria@t.com', cpf='98765432100', telefone='11888')


class ReservaModelTest(StaffTestCase):
    def test_criar_com_uuid(self):
        r = Reserva.objects.create(cliente=self.c1, voo=self.voo, numero_assento=1)
        self.assertEqual(len(str(r.pk)), 36)

    def test_assento_duplicado(self):
        Reserva.objects.create(cliente=self.c1, voo=self.voo, numero_assento=1)
        with self.assertRaises(IntegrityError):
            Reserva.objects.create(cliente=self.c2, voo=self.voo, numero_assento=1)

    def test_cliente_duplicado(self):
        Reserva.objects.create(cliente=self.c1, voo=self.voo, numero_assento=1)
        with self.assertRaises(IntegrityError):
            Reserva.objects.create(cliente=self.c1, voo=self.voo, numero_assento=2)


class ReservaFormTest(StaffTestCase):
    def test_assento_excede(self):
        form = ReservaForm(data={'cliente': self.c1.pk, 'voo': self.voo.pk, 'numero_assento': 10})
        self.assertFalse(form.is_valid())

    def test_voo_lotado(self):
        c3 = Cliente.objects.create(nome='Pedro', email='pedro@t.com', cpf='11122233344', telefone='11777')
        Reserva.objects.create(cliente=self.c1, voo=self.voo, numero_assento=1)
        Reserva.objects.create(cliente=self.c2, voo=self.voo, numero_assento=2)
        Reserva.objects.create(cliente=c3, voo=self.voo, numero_assento=3)
        c4 = Cliente.objects.create(nome='Ana', email='ana@t.com', cpf='55566677788', telefone='11666')
        form = ReservaForm(data={'cliente': c4.pk, 'voo': self.voo.pk, 'numero_assento': 1})
        self.assertFalse(form.is_valid())


class ReservaViewTest(StaffTestCase):
    def test_listar(self):
        self.assertEqual(self.client.get('/reservas/').status_code, 200)

    def test_criar_post(self):
        r = self.client.post('/reservas/nova/', {'cliente': self.c1.pk, 'voo': self.voo.pk, 'numero_assento': 1})
        self.assertEqual(r.status_code, 302)


class ReservaPrivacidadeTest(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='regular', password='pass123', is_staff=False)
        self.client.login(username='regular', password='pass123')

    def test_ve_apenas_suas(self):
        a = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=10)
        v = Voo.objects.create(aviao=a, origem='GRU', destino='GIG', data=date(2026, 5, 1), horario=time(10, 0))
        meu = Cliente.objects.create(nome='Eu', email='eu@t.com', cpf='11111111111', telefone='1', usuario=self.user)
        outro = Cliente.objects.create(nome='Outro', email='outro@t.com', cpf='22222222222', telefone='2')
        Reserva.objects.create(cliente=meu, voo=v, numero_assento=1)
        Reserva.objects.create(cliente=outro, voo=v, numero_assento=2)
        r = self.client.get('/reservas/')
        self.assertEqual(len(r.context['reservas']), 1)
