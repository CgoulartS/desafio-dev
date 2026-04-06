from django.db import models
from core.models import BaseModel
from .aviao import Aviao


class Voo(BaseModel):
    aviao = models.ForeignKey(Aviao, on_delete=models.CASCADE, related_name='voos')
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    data = models.DateField()
    horario = models.TimeField()

    class Meta:
        verbose_name_plural = 'Voos'
        ordering = ['data', 'horario']

    def __str__(self):
        return f'{self.origem} → {self.destino} ({self.data})'

    @property
    def assentos_disponiveis(self):
        return self.aviao.max_passageiros - self.reservas.count()

    @property
    def esta_lotado(self):
        return self.reservas.count() >= self.aviao.max_passageiros
