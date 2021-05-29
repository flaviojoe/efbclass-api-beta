# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.mixins import AuditFieldsSerializersMixin
from ..models import FAQ


class FAQSerializers(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'pergunta', 'resposta']


class FAQCreateSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['pergunta', 'criado_por', 'modificado_por']
