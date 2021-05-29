# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Configuracao
from core.mixins import ExcludeAuditFieldsAdminForm


@admin.register(Configuracao)
class ConfiguracaoAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'empresa', 'qtd_tentativas_provas']
    list_display_links = ['empresa']

    def get_queryset(self, request):
        return super(ConfiguracaoAdmin, self).get_queryset(request=request).select_related('empresa')