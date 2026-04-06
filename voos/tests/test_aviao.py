from django.test import TestCase
from voos.models import Aviao
from voos.forms import AviaoForm
from .base import BaseTestCase, RegularUserTestCase


class AviaoModelTest(TestCase):
    def test_criar_aviao_com_uuid(self):
        aviao = Aviao.objects.create(modelo='737', fabricante='Boeing', max_passageiros=180)
        self.assertEqual(str(aviao), 'Boeing 737')
        self.assertEqual(len(str(aviao.pk)), 36)

    def test_rejeitar_max_passageiros_zero(self):
        form = AviaoForm(data={'modelo': '737', 'fabricante': 'Boeing', 'max_passageiros': 0})
        self.assertFalse(form.is_valid())
        self.assertIn('max_passageiros', form.errors)


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
