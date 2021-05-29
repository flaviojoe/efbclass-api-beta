# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import TipoMaterial, Material
from core.mixins import ExcludeAuditFieldsAdminForm


@admin.register(TipoMaterial)
class TipoMaterialAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'nome', 'criado_por', 'criado_em',
					'modificado_por', 'modificado_em']
	list_display_links = ['nome']

	def get_queryset(self, request):
		return super(
			TipoMaterialAdmin, self).get_queryset(
			request=request).select_related(
			'criado_por', 'modificado_por')


@admin.register(Material)
class MaterialAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'nome', 'tipo', 'criado_por', 'criado_em']
	list_display_links = ['nome']

	def get_queryset(self, request):
		return super(
			MaterialAdmin, self).get_queryset(
			request=request).select_related('curso', 'tipo',
											'criado_por', 'modificado_por')

