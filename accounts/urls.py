from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/novo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<uuid:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('clientes/<uuid:pk>/excluir/', views.ClienteDeleteView.as_view(), name='cliente-delete'),
]
