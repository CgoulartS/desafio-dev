import uuid
from django.db import models


class Aviao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    modelo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    max_passageiros = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Avioes'
        ordering = ['fabricante', 'modelo']

    def __str__(self):
        return f'{self.fabricante} {self.modelo}'
