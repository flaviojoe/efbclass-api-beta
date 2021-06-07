# -*- coding: utf-8 -*-
from rest_framework import serializers

from contas.api.serializers import UsuarioNameSerializers
from core.mixins import AuditFieldsSerializersMixin
from ..models import Notificacao, NotificacaoDestinatario


class NotificacaoSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    imagem = serializers.ImageField(use_url=True)
    criado_por = UsuarioNameSerializers(many=False)

    class Meta:
        model = Notificacao
        fields = ['id', 'mensagem', 'imagem', 'criado_por']


class NotificacaoDestinatarioSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    notificacao = NotificacaoSerializers(many=False)

    class Meta:
        model = NotificacaoDestinatario
        fields = ['id', 'notificacao', 'is_empresa', 'is_curso', 'is_usuario', 'criado_em']


class NotificacoesDoUsuarioSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    mensagem = serializers.CharField()
    criado_por_nome = serializers.CharField(max_length=50)
    is_empresa = serializers.BooleanField()
    is_curso = serializers.BooleanField()
    is_usuario = serializers.BooleanField()
    criado_em = serializers.DateTimeField()
    possui_imagem = serializers.BooleanField()