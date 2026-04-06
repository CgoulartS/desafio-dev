from django.db import IntegrityError
from django.test import TestCase
from voos.models import Cliente
from .base import BaseTestCase


class ClienteModelTest(TestCase):
    def test_criar_cliente_com_uuid(self):
        c = Cliente.objects.create(nome='Joao', email='joao@t.com', cpf='12345678901', telefone='11999')
        self.assertEqual(len(str(c.pk)), 36)

    def test_email_unico(self):
        Cliente.objects.create(nome='Joao', email='joao@t.com', cpf='12345678901', telefone='11999')
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nome='Maria', email='joao@t.com', cpf='98765432100', telefone='11888')

    def test_cpf_unico(self):
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
