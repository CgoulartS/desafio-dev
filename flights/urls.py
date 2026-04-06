from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # Aviões
    path('avioes/', views.AviaoListView.as_view(), name='aviao-list'),
    path('avioes/novo/', views.AviaoCreateView.as_view(), name='aviao-create'),
    path('avioes/<uuid:pk>/editar/', views.AviaoUpdateView.as_view(), name='aviao-update'),
    path('avioes/<uuid:pk>/excluir/', views.AviaoDeleteView.as_view(), name='aviao-delete'),
    # Voos
    path('voos/', views.VooListView.as_view(), name='voo-list'),
    path('voos/novo/', views.VooCreateView.as_view(), name='voo-create'),
    path('voos/<uuid:pk>/', views.VooDetailView.as_view(), name='voo-detail'),
    path('voos/<uuid:pk>/editar/', views.VooUpdateView.as_view(), name='voo-update'),
    path('voos/<uuid:pk>/excluir/', views.VooDeleteView.as_view(), name='voo-delete'),
    path('voos/<uuid:pk>/assentos/', views.VooAssentosView.as_view(), name='voo-assentos'),
    # Reservas
    path('reservas/', views.ReservaListView.as_view(), name='reserva-list'),
    path('reservas/nova/', views.ReservaCreateView.as_view(), name='reserva-create'),
    path('reservas/<uuid:pk>/editar/', views.ReservaUpdateView.as_view(), name='reserva-update'),
    path('reservas/<uuid:pk>/excluir/', views.ReservaDeleteView.as_view(), name='reserva-delete'),
]
