from datetime import date, time
from django.db import IntegrityError
from django.test import TestCase
from voos.models import Aviao, Voo, Cliente, Reserva
from voos.forms import ReservaForm
from .base import BaseTestCase, RegularUserTestCase


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
        Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        with self.assertRaises(IntegrityError):
            Reserva.objects.create(cliente=self.cliente2, voo=self.voo, numero_assento=1)

    def test_cliente_duplicado_no_voo(self):
        Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=1)
        with self.assertRaises(IntegrityError):
            Reserva.objects.create(cliente=self.cliente1, voo=self.voo, numero_assento=2)


class ReservaFormTest(ReservaTestBase):
    def test_assento_excede_capacidade(self):
        form = ReservaForm(data={'cliente': self.cliente1.pk, 'voo': self.voo.pk, 'numero_assento': 10})
        self.assertFalse(form.is_valid())

    def test_voo_lotado(self):
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
