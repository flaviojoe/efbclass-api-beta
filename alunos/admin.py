# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Aluno
from core.mixins import ExcludeAuditFieldsAdminForm


@admin.register(Aluno)
class AlunoAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'nome', 'usuario', 'empresa',
                    'criado_em',
                    'modificado_em']
    list_display_links = ['nome']

    def get_queryset(self, request):
        return super(
            AlunoAdmin, self).get_queryset(
            request=request).select_related(
            'empresa', 'departamento', 'setor', 'regional', 'usuario', 'criado_por', 'modificado_por')
