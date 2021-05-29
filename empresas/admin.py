# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Empresa, Regional, Departamento, Setor, Equipe
from core.mixins import ExcludeAuditFieldsAdminForm


@admin.register(Empresa)
class EmpresaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'nome', 'criado_por', 'criado_em',
                    'modificado_por', 'modificado_em']
    list_display_links = ['nome']

    def get_queryset(self, request):
        return super(EmpresaAdmin, self).get_queryset(request=request).select_related('criado_por', 'modificado_por')


@admin.register(Regional)
class RegionalAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'nome', 'criado_por', 'criado_em',
                    'modificado_por', 'modificado_em']
    list_display_links = ['nome']

    def get_queryset(self, request):
        return super(RegionalAdmin, self).get_queryset(request=request).select_related('criado_por', 'modificado_por')


@admin.register(Departamento)
class DepartamentoAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'nome', 'criado_por', 'criado_em',
                    'modificado_por', 'modificado_em']
    list_display_links = ['nome']

    def get_queryset(self, request):
        return super(
            DepartamentoAdmin, self).get_queryset(
            request=request).select_related(
            'criado_por', 'modificado_por')


@admin.register(Setor)
class SetorAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'nome', 'criado_por', 'criado_em',
                    'modificado_por', 'modificado_em']
    list_display_links = ['nome']

    def get_queryset(self, request):
        return super(
            SetorAdmin, self).get_queryset(
            request=request).select_related(
            'criado_por', 'modificado_por')


@admin.register(Equipe)
class EquipeAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'nome', 'criado_por', 'criado_em',
                    'modificado_por', 'modificado_em']
    list_display_links = ['nome']

    def get_queryset(self, request):
        return super(
            EquipeAdmin, self).get_queryset(
            request=request).select_related(
            'criado_por', 'modificado_por')
