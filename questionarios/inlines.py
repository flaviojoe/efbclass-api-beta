# -*- coding: utf-8 -*-
from nested_inline.admin import NestedTabularInline, NestedStackedInline

from core.mixins import ExcludeAuditFieldsAdminForm
from .models import Pergunta, Resposta, QuestionarioXPergunta


class RespostaInline(NestedTabularInline):
    extra = 2
    fk_name = 'pergunta'
    model = Resposta
    verbose_name_plural = 'Opções de respostas para a pergunta'
    exclude = ['criado_por', 'modificado_por']


class PerguntaInline(ExcludeAuditFieldsAdminForm, NestedTabularInline):
    extra = 1
    model = Pergunta
    fk_name = 'pergunta'
    inlines = [RespostaInline]


class QuestionarioXPerguntaInline(ExcludeAuditFieldsAdminForm, NestedStackedInline):
    extra = 1
    model = QuestionarioXPergunta
    fk_name = 'questionario'
