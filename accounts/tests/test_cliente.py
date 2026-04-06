from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase, Client as TestClient
from accounts.models import Cliente


class StaffTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.client.login(username='admin', password='admin123')


class RegularUserTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = User.objects.create_user(username='regular', password='pass123', is_staff=False)
        self.client.login(username='regular', password='pass123')


class ClienteModelTest(TestCase):
    def test_criar_com_uuid(self):
        c = Cliente.objects.create(nome='João', email='joao@t.com', cpf='12345678901', telefone='11999')
        self.assertEqual(len(str(c.pk)), 36)

    def test_tem_timestamps(self):
        c = Cliente.objects.create(nome='João', email='joao@t.com', cpf='12345678901', telefone='11999')
        self.assertIsNotNone(c.created_at)
        self.assertIsNotNone(c.updated_at)

    def test_email_unico(self):
        Cliente.objects.create(nome='João', email='joao@t.com', cpf='12345678901', telefone='11999')
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nome='Maria', email='joao@t.com', cpf='98765432100', telefone='11888')

    def test_cpf_unico(self):
        Cliente.objects.create(nome='João', email='joao@t.com', cpf='12345678901', telefone='11999')
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nome='Maria', email='maria@t.com', cpf='12345678901', telefone='11888')


class ClienteViewStaffTest(StaffTestCase):
    def test_listar_clientes(self):
        self.assertEqual(self.client.get('/clientes/').status_code, 200)

    def test_buscar_por_nome(self):
        Cliente.objects.create(nome='João', email='joao@t.com', cpf='12345678901', telefone='11999')
        Cliente.objects.create(nome='Maria', email='maria@t.com', cpf='98765432100', telefone='11888')
        r = self.client.get('/clientes/?q=João')
        self.assertEqual(len(r.context['clientes']), 1)


class ClienteLGPDTest(RegularUserTestCase):
    def test_usuario_comum_nao_ve_lista_clientes(self):
        self.assertEqual(self.client.get('/clientes/').status_code, 403)

    def test_usuario_comum_nao_cria_cliente(self):
        self.assertEqual(self.client.get('/clientes/novo/').status_code, 403)
