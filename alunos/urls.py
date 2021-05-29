from django.urls import path
from .api.viewsets import AlunoFotoPerfilUpdateView

urlpatterns = [
    path('', AlunoFotoPerfilUpdateView.as_view())
]
