# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.mixins import AuditFieldsSerializersMixin
from ...models import Aula, HistoricoAula


class HistoricoAulaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    class Meta:
        model = HistoricoAula
        fields = ['usuario', 'aula', 'finalizada']
        validators = [
            UniqueTogetherValidator(
                queryset=HistoricoAula.objects.all(),
                fields=['usuario', 'aula'],
                message="Aula já finalizada!"
            )
        ]


class VideoAulaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    video = serializers.FileField(required=True)

    class Meta:
        model = Aula
        fields = ['video']
