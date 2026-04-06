from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # Avioes
    path('avioes/', views.AviaoListView.as_view(), name='aviao-list'),
    path('avioes/novo/', views.AviaoCreateView.as_view(), name='aviao-create'),
    path('avioes/<int:pk>/editar/', views.AviaoUpdateView.as_view(), name='aviao-update'),
    path('avioes/<int:pk>/excluir/', views.AviaoDeleteView.as_view(), name='aviao-delete'),
    # Voos
    path('voos/', views.VooListView.as_view(), name='voo-list'),
    path('voos/novo/', views.VooCreateView.as_view(), name='voo-create'),
    path('voos/<int:pk>/', views.VooDetailView.as_view(), name='voo-detail'),
    path('voos/<int:pk>/editar/', views.VooUpdateView.as_view(), name='voo-update'),
    path('voos/<int:pk>/excluir/', views.VooDeleteView.as_view(), name='voo-delete'),
    path('voos/<int:pk>/assentos/', views.VooAssentosView.as_view(), name='voo-assentos'),
    # Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/novo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('clientes/<int:pk>/excluir/', views.ClienteDeleteView.as_view(), name='cliente-delete'),
    # Reservas
    path('reservas/', views.ReservaListView.as_view(), name='reserva-list'),
    path('reservas/nova/', views.ReservaCreateView.as_view(), name='reserva-create'),
    path('reservas/<int:pk>/editar/', views.ReservaUpdateView.as_view(), name='reserva-update'),
    path('reservas/<int:pk>/excluir/', views.ReservaDeleteView.as_view(), name='reserva-delete'),
]
