# -*- coding: utf-8 -*-
import mimetypes

from rest_framework import serializers

from core.mixins import AuditFieldsSerializersMixin
from ..models import Material


class MaterialSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    curso = serializers.StringRelatedField(many=False)
    tipo = serializers.StringRelatedField(many=False)
    mimetype = serializers.SerializerMethodField(method_name='get_mimetype')

    class Meta:
        model = Material
        fields = ['id', 'nome', 'curso', 'tipo', 'conteudo', 'informativo', 'arquivo', 'criado_em', 'mimetype']

    def get_mimetype(self, obj):
        print(obj.arquivo.name)
        return mimetypes.guess_type(obj.arquivo.name)[0] if obj.arquivo else ''


class MaterialSimpleSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    tipo = serializers.StringRelatedField(many=False)

    class Meta:
        model = Material
        fields = ['id', 'nome', 'tipo', 'conteudo', 'informativo', 'arquivo', 'criado_em', 'modificado_em']
