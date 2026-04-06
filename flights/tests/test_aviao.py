from django.contrib.auth.models import User
from django.test import TestCase, Client as TestClient
from flights.models import Aviao
from flights.forms import AviaoForm


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


class AviaoModelTest(TestCase):
    def test_criar_com_uuid_e_timestamps(self):
        a = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.assertEqual(len(str(a.pk)), 36)
        self.assertIsNotNone(a.created_at)
        self.assertIsNotNone(a.updated_at)

    def test_rejeitar_max_passageiros_zero(self):
        form = AviaoForm(data={'modelo': '737', 'fabricante': 'Boeing', 'max_passageiros': 0})
        self.assertFalse(form.is_valid())


class AviaoViewTest(StaffTestCase):
    def test_listar(self):
        self.assertEqual(self.client.get('/avioes/').status_code, 200)

    def test_criar_post(self):
        r = self.client.post('/avioes/novo/', {'modelo': 'A320', 'fabricante': 'Airbus', 'max_passageiros': 150})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Aviao.objects.count(), 1)


class AviaoRBACTest(RegularUserTestCase):
    def test_nao_staff_nao_cria(self):
        self.assertEqual(self.client.get('/avioes/novo/').status_code, 403)

    def test_nao_staff_nao_deleta(self):
        a = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.assertEqual(self.client.post(f'/avioes/{a.pk}/excluir/').status_code, 403)
