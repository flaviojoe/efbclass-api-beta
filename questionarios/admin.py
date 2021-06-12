# -*- coding: utf-8 -*-

from django.contrib import admin
from nested_inline.admin import NestedModelAdmin

from core.mixins import ExcludeAuditFieldsAdminForm
from .actions import AcoesProvaAdmin
from .inlines import QuestionarioXPerguntaInline, RespostaInline
from .models import Pergunta, Questionario, Resposta, QuestionarioXPergunta, Prova, Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['tentativa', 'criado_por', 'id', 'curso', 'e_correta', 'pergunta', 'resposta']

    def get_queryset(self, request):
        return super(AvaliacaoAdmin, self).get_queryset(request=request).select_related(
            'prova__matricula', 'prova__questionario', 'pergunta', 'resposta', 'criado_por', 'curso')


@admin.register(Questionario)
class QuestionarioAdmin(ExcludeAuditFieldsAdminForm, NestedModelAdmin):
    list_display = ['id', 'curso', 'qtd_perguntas', 'criado_em',
                    'modificado_em']
    list_display_links = ['curso']
    inlines = [QuestionarioXPerguntaInline]

    def get_queryset(self, request):
        return super(QuestionarioAdmin, self).get_queryset(
            request=request).select_related(
            'curso', 'criado_por', 'modificado_por').prefetch_related('questionarios_mapeados')

    def qtd_perguntas(self, obj):
        return obj.questionarios_mapeados.count()

    qtd_perguntas.short_description = 'Qtd Perguntas'
    qtd_perguntas.admin_order_field = 'qtd_perguntas'


@admin.register(QuestionarioXPergunta)
class QuestionarioXPerguntaAdmin(ExcludeAuditFieldsAdminForm, NestedModelAdmin):
    list_display = ['id', 'questionario', 'pergunta']
    list_display_links = ['questionario', 'pergunta']

    def get_queryset(self, request):
        return super(QuestionarioXPerguntaAdmin, self).get_queryset(request=request).select_related(
            'questionario', 'questionario__curso', 'pergunta'
        )


@admin.register(Pergunta)
class PerguntaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'texto', 'criado_em', 'modificado_em']
    list_display_links = ['texto']
    inlines = [RespostaInline]

    def get_queryset(self, request):
        return super(PerguntaAdmin, self).get_queryset(request).select_related('criado_por', 'modificado_por')


@admin.register(Resposta)
class RespostaAdmin(ExcludeAuditFieldsAdminForm, admin.ModelAdmin):
    list_display = ['id', 'resposta', 'e_correta', 'criado_em', 'pergunta', 'modificado_em']
    list_display_links = ['pergunta']

    def get_queryset(self, request):
        return super(RespostaAdmin, self).get_queryset(request).select_related(
            'pergunta', 'criado_por', 'modificado_por'
        )


@admin.register(Prova)
class ProvaAdmin(ExcludeAuditFieldsAdminForm, AcoesProvaAdmin, admin.ModelAdmin):
    list_display = ['id', 'finalizado', 'criado_por', 'curso']
    list_display_links = ['criado_por']
    actions = ['marcar_como_finalizada', 'marcar_como_ativa']
    list_filter = ['finalizado']

    def get_queryset(self, request):
        return Prova.objects.select_related('criado_por', 'curso', 'questionario', 'matricula')
