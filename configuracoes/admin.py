# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Configuracao, Preferencia
from core.mixins import ExcludeAuditFieldsAdminForm


@admin.register(Configuracao)
class ConfiguracaoAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'empresa', 'qtd_tentativas_provas']
    list_display_links = ['empresa']

    def get_queryset(self, request):
        return super(ConfiguracaoAdmin, self).get_queryset(request=request).select_related('empresa')


@admin.register(Preferencia)
class PreferenciaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'criado_por', 'modo_escuro']
    list_display_links = ['criado_por']

    def get_queryset(self, request):
        return super(PreferenciaAdmin, self).get_queryset(request=request).select_related('criado_por')