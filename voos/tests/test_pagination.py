from voos.models import Aviao
from .base import BaseTestCase


class PaginationTest(BaseTestCase):
    def test_paginacao_avioes(self):
        for i in range(15):
            Aviao.objects.create(modelo=f'M{i}', fabricante='F', max_passageiros=100)
        self.assertEqual(len(self.client.get('/avioes/').context['avioes']), 10)
        self.assertEqual(len(self.client.get('/avioes/?page=2').context['avioes']), 5)
