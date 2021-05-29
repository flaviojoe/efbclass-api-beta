# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from core.models import Timestamps, AuditModel
from cursos.models import Curso
from empresas.models import Empresa


class Notificacao(Timestamps, AuditModel):
    mensagem = models.TextField()
    imagem = models.ImageField(upload_to='notificacoes', null=True, blank=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return self.mensagem


class NotificacaoDestinatario(Timestamps):
    notificacao = models.ForeignKey(Notificacao, on_delete=models.CASCADE, related_name='notificacoes_destinario')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='notificacoes_empresa', null=True,
                                blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='notificacoes_curso', null=True, blank=True)
    destinario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='destinário',
                                   related_name='notificacoes_destinarios')
    is_empresa = models.BooleanField(default=False, verbose_name='Para Empresa?')
    is_curso = models.BooleanField(default=False, verbose_name='Para Curso?')
    is_usuario = models.BooleanField(default=False, verbose_name='Para Usuário?')

    class Meta:
        verbose_name = 'Destinatário Notificação'
        verbose_name_plural = 'Destinatários Notificações'


class NotificacaoEnviada(Timestamps):
    notificacao_destinario = models.ForeignKey(NotificacaoDestinatario, on_delete=models.CASCADE,
                                               related_name='notificacoes_enviadas')
    lida = models.BooleanField(default=False, verbose_name='Foi lida?')
    lida_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Notificação Enviada'
        verbose_name_plural = 'Notificações Enviadas'
