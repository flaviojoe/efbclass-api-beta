from django.urls import path
from .views import MeusTreinamentosView

urlpatterns = [
    path('meus_treinamentos', MeusTreinamentosView.as_view(), name='meus_treinamentos'),
]
