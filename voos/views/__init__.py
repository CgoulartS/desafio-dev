from .home import HomeView
from .aviao import AviaoListView, AviaoCreateView, AviaoUpdateView, AviaoDeleteView
from .voo import VooListView, VooDetailView, VooCreateView, VooUpdateView, VooDeleteView, VooAssentosView
from .cliente import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView
from .reserva import ReservaListView, ReservaCreateView, ReservaUpdateView, ReservaDeleteView

__all__ = [
    'HomeView',
    'AviaoListView', 'AviaoCreateView', 'AviaoUpdateView', 'AviaoDeleteView',
    'VooListView', 'VooDetailView', 'VooCreateView', 'VooUpdateView', 'VooDeleteView', 'VooAssentosView',
    'ClienteListView', 'ClienteCreateView', 'ClienteUpdateView', 'ClienteDeleteView',
    'ReservaListView', 'ReservaCreateView', 'ReservaUpdateView', 'ReservaDeleteView',
]
