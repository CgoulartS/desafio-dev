from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from flights.services import DashboardService


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'flights/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(DashboardService.obter_metricas())
        return context
