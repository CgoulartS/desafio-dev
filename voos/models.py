from django.db import models
from django.db.models import UniqueConstraint


class Aviao(models.Model):
    modelo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    max_passageiros = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Avioes'

    def __str__(self):
        return f'{self.fabricante} {self.modelo}'


class Voo(models.Model):
    aviao = models.ForeignKey(Aviao, on_delete=models.CASCADE, related_name='voos')
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    data = models.DateField()
    horario = models.TimeField()

    class Meta:
        verbose_name_plural = 'Voos'

    def __str__(self):
        return f'{self.origem} -> {self.destino} ({self.data})'


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    voo = models.ForeignKey(Voo, on_delete=models.CASCADE, related_name='reservas')
    numero_assento = models.PositiveIntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['voo', 'numero_assento'], name='unique_assento_por_voo'),
            UniqueConstraint(fields=['voo', 'cliente'], name='unique_cliente_por_voo'),
        ]

    def __str__(self):
        return f'{self.cliente.nome} - Voo {self.voo} - Assento {self.numero_assento}'
