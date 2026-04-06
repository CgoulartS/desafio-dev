from django.db import models
from core.models import BaseModel


class Aviao(BaseModel):
    modelo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    max_passageiros = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Aviões'
        ordering = ['fabricante', 'modelo']

    def __str__(self):
        return f'{self.fabricante} {self.modelo}'
