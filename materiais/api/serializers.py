# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.mixins import AuditFieldsSerializersMixin
from ..models import Material


class MaterialSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    curso = serializers.StringRelatedField(many=False)
    tipo = serializers.StringRelatedField(many=False)

    class Meta:
        model = Material
        fields = ['id', 'nome', 'curso', 'tipo', 'conteudo', 'informativo', 'arquivo', 'criado_em']


class MaterialSimpleSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    tipo = serializers.StringRelatedField(many=False)

    class Meta:
        model = Material
        fields = ['id', 'nome', 'tipo', 'conteudo', 'informativo', 'arquivo', 'criado_em', 'modificado_em']
