# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Notificacao, NotificacaoDestinatario, NotificacaoEnviada
from core.mixins import ExcludeAuditFieldsAdminForm


class DestinariosInline(admin.StackedInline):
	model = NotificacaoDestinatario
	extra = 1


@admin.register(Notificacao)
class NotificacaoAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'mensagem', 'criado_por', 'criado_em']
	list_display_links = ['mensagem']
	inlines = [DestinariosInline]

	def get_queryset(self, request):
		return super(NotificacaoAdmin, self) \
			.get_queryset(request=request) \
			.select_related('criado_por', 'modificado_por')


@admin.register(NotificacaoDestinatario)
class NotificacaoDestinatarioAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'notificacao', 'is_empresa', 'is_curso', 'is_usuario', 'criado_em']
	list_display_links = ['notificacao']

	def get_queryset(self, request):
		return super(NotificacaoDestinatarioAdmin, self) \
			.get_queryset(request=request) \
			.select_related('notificacao', 'curso', 'empresa', 'destinario')


@admin.register(NotificacaoEnviada)
class NotificacaoEnviadaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
	list_display = ['id', 'lida', 'lida_em', 'criado_em']

	def get_queryset(self, request):
		return super(NotificacaoEnviadaAdmin, self) \
			.get_queryset(request=request) \
			.select_related('notificacao_destinario')
