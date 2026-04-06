from datetime import date
from django.db.models import Count
from voos.models import Aviao, Voo, Cliente, Reserva


class DashboardService:

    @staticmethod
    def obter_metricas():
        total_avioes = Aviao.objects.count()
        total_voos = Voo.objects.count()
        total_clientes = Cliente.objects.count()
        total_reservas = Reserva.objects.count()

        voos_com_dados = Voo.objects.annotate(
            num_reservas=Count('reservas')
        ).select_related('aviao')

        total_res = sum(v.num_reservas for v in voos_com_dados)
        total_cap = sum(v.aviao.max_passageiros for v in voos_com_dados)
        taxa_ocupacao = round((total_res / total_cap * 100), 1) if total_cap > 0 else 0

        proximos_voos = Voo.objects.filter(
            data__gte=date.today()
        ).select_related('aviao').order_by('data', 'horario')[:5]

        return {
            'total_avioes': total_avioes,
            'total_voos': total_voos,
            'total_clientes': total_clientes,
            'total_reservas': total_reservas,
            'taxa_ocupacao': taxa_ocupacao,
            'proximos_voos': proximos_voos,
        }
