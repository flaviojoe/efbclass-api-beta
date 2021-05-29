# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.mixins import AuditFieldsSerializersMixin
from ...models import Categoria


class CategoriaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'criado_por', 'modificado_por']


class CategoriaSimpleSerializers(serializers.ModelSerializer):
    qtd_cursos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'imagem', 'qtd_cursos']

    def get_qtd_cursos(self, obj):
        return obj.qtd_cursos