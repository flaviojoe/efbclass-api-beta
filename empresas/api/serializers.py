# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.mixins import AuditFieldsSerializersMixin
from ..models import Empresa


class EmpresaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nome', 'criado_por', 'modificado_por']
