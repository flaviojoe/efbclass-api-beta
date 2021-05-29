# -*- coding: utf-8 -*-

from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from core.mixins import ExcludeAuditFieldsAdminForm
from .models import Categoria, Curso, Topico, Aula, HistoricoAula, Matricula


@admin.register(Categoria)
class CategoriaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'nome', 'criado_por', 'criado_em', 'modificado_por', 'modificado_em']
	list_display_links = ['nome']

	def get_queryset(self, request):
		return super(CategoriaAdmin, self).get_queryset(request=request).select_related('criado_por', 'modificado_por')


class AulaCursoInline(ExcludeAuditFieldsAdminForm, NestedTabularInline):
	model = Aula
	extra = 1
	fields = ['titulo', 'numero', 'url']


class TopicoCursoInline(NestedStackedInline):
	model = Topico
	extra = 1
	exclude = ['sessao', 'criado_por', 'modificado_por']
	inlines = [
		AulaCursoInline
	]


@admin.register(Curso)
class CursoAdmin(ExcludeAuditFieldsAdminForm, NestedModelAdmin):
	list_display = ['id', 'nome', 'categoria', 'nivel', 'criado_por', 'criado_em',
					'modificado_por', 'modificado_em']
	list_display_links = ['nome']
	inlines = [
		TopicoCursoInline
	]

	def get_queryset(self, request):
		return super(
			CursoAdmin, self).get_queryset(
			request=request).select_related(
			'categoria', 'criado_por', 'modificado_por')


class AulaTopicoInline(ExcludeAuditFieldsAdminForm, NestedStackedInline):
	model = Aula
	extra = 1


@admin.register(Topico)
class TopicoAdmin(ExcludeAuditFieldsAdminForm, NestedModelAdmin):
	list_display = ['id', 'nome', 'curso', 'criado_por', 'criado_em',
					'modificado_por', 'modificado_em']
	list_display_links = ['nome']
	inlines = [
		AulaTopicoInline
	]

	def get_queryset(self, request):
		return super(TopicoAdmin, self).get_queryset(request=request).select_related('curso', 'criado_por',
																					 'modificado_por')


@admin.register(Matricula)
class MatriculaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'usuario', 'curso', 'criado_em', 'modificado_em']
	list_display_links = ['usuario', 'curso']

	def get_queryset(self, request):
		return super(MatriculaAdmin, self).get_queryset(request=request).select_related('usuario', 'curso',
																						'criado_por',
																						'modificado_por')


@admin.register(Aula)
class AulaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'topico', 'titulo', 'numero', 'criado_por', 'criado_em',
					'modificado_por', 'modificado_em']
	list_display_links = ['titulo']
	ordering = ['topico', 'numero']

	def get_queryset(self, request):
		return super(
			AulaAdmin, self).get_queryset(
			request=request).select_related(
			'topico', 'criado_por', 'modificado_por')


@admin.register(HistoricoAula)
class HistoricoAulaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'usuario', 'aula', 'finalizada', 'criado_em']
	list_display_links = ['aula']

	def get_queryset(self, request):
		return super(HistoricoAulaAdmin, self).get_queryset(request).select_related('usuario', 'aula')
