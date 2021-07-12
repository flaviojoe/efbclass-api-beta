# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Curso
import django_filters
from django_filters.views import FilterView


class CursoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Curso
        fields = ['nome']

class MeusTreinamentosView(LoginRequiredMixin, FilterView):
    template_name = 'meus_treinamentos.html'
    model = Curso
    paginate_by = 2
    context_object_name = 'cursos_list'
    filterset_class = CursoFilter

    def get_queryset(self):
        return super(MeusTreinamentosView, self).get_queryset().select_related('categoria')
