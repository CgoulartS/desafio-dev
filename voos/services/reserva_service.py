from django.core.exceptions import ValidationError
from voos.models import Reserva


class ReservaService:

    @staticmethod
    def validar_assento(voo, numero_assento, excluir_reserva_pk=None):
        max_pass = voo.aviao.max_passageiros

        if numero_assento > max_pass or numero_assento < 1:
            raise ValidationError(
                f'Assento {numero_assento} invalido. '
                f'O aviao comporta assentos de 1 a {max_pass}.'
            )

        qs = Reserva.objects.filter(voo=voo, numero_assento=numero_assento)
        if excluir_reserva_pk:
            qs = qs.exclude(pk=excluir_reserva_pk)
        if qs.exists():
            raise ValidationError(
                f'Assento {numero_assento} ja esta ocupado neste voo.'
            )

    @staticmethod
    def validar_capacidade(voo, excluir_reserva_pk=None):
        reservas_count = voo.reservas.count()
        if excluir_reserva_pk:
            reservas_count -= 1
        if reservas_count >= voo.aviao.max_passageiros:
            raise ValidationError('Este voo ja esta com capacidade maxima.')

    @staticmethod
    def validar_cliente_unico(voo, cliente, excluir_reserva_pk=None):
        qs = Reserva.objects.filter(voo=voo, cliente=cliente)
        if excluir_reserva_pk:
            qs = qs.exclude(pk=excluir_reserva_pk)
        if qs.exists():
            raise ValidationError('Este cliente ja possui reserva neste voo.')

    @staticmethod
    def obter_assentos_ocupados(voo):
        return list(voo.reservas.values_list('numero_assento', flat=True))
