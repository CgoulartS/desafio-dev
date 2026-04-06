from datetime import date
from django.core.cache import cache
from django.db.models import Count
from accounts.models import Cliente
from flights.models import Aviao, Voo, Reserva


class DashboardService:

    CACHE_KEY = 'dashboard_metricas'
    CACHE_TTL = 60  # segundos

    @staticmethod
    def obter_metricas():
        cached = cache.get(DashboardService.CACHE_KEY)
        if cached:
            return cached
        metricas = DashboardService._calcular_metricas()
        cache.set(DashboardService.CACHE_KEY, metricas, DashboardService.CACHE_TTL)
        return metricas

    @staticmethod
    def invalidar_cache():
        cache.delete(DashboardService.CACHE_KEY)

    @staticmethod
    def _calcular_metricas():
        voos_dados = Voo.objects.annotate(num_reservas=Count('reservas')).select_related('aviao')
        total_res = sum(v.num_reservas for v in voos_dados)
        total_cap = sum(v.aviao.max_passageiros for v in voos_dados)
        taxa = round((total_res / total_cap * 100), 1) if total_cap > 0 else 0

        return {
            'total_avioes': Aviao.objects.count(),
            'total_voos': Voo.objects.count(),
            'total_clientes': Cliente.objects.count(),
            'total_reservas': Reserva.objects.count(),
            'taxa_ocupacao': taxa,
            'proximos_voos': Voo.objects.filter(
                data__gte=date.today()
            ).select_related('aviao').order_by('data', 'horario')[:5],
        }
