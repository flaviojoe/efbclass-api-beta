# -*- coding: utf-8 -*-
from rest_framework import serializers

from .fields import UsuarioField
from ...models import Aula, Topico, HistoricoAula


class AulaCursoDetailsSerializers(serializers.ModelSerializer):
	class AulaFinalizadaSerializers(serializers.ModelSerializer):
		class Meta:
			model = HistoricoAula
			fields = ['finalizada']

	historico = AulaFinalizadaSerializers(many=True)

	class Meta:
		model = Aula
		fields = ['id', 'numero', 'titulo', 'url', 'video', 'arquivo_video', 'historico']


class AulaCursoGradeSerializers(serializers.ModelSerializer):
	class Meta:
		model = Aula
		fields = ['id', 'numero', 'titulo']


class TopicoCursoDetailsSerializers(serializers.ModelSerializer):
	aulas = AulaCursoDetailsSerializers(source='topico_aula', many=True)

	class Meta:
		model = Topico
		fields = ['id', 'numero', 'nome', 'aulas']


class TopicoCursoGradeSerializers(serializers.ModelSerializer):
	aulas = AulaCursoGradeSerializers(source='topico_aula', many=True)

	class Meta:
		model = Topico
		fields = ['id', 'numero', 'nome', 'aulas']


class AulasTopicoSerializers(serializers.ModelSerializer):
	class Meta:
		model = Aula
		fields = ['id', 'numero', 'titulo', 'url', 'video', 'arquivo_video']


class TopicoSerializers(serializers.ModelSerializer):
	criado_por = UsuarioField(many=False, read_only=True)

	class Meta:
		model = Topico
		fields = ['id', 'nome', 'numero', 'criado_por']


class TopicoDetailsSerializers(serializers.ModelSerializer):
	criado_por = serializers.StringRelatedField()
	aulas = AulaCursoDetailsSerializers(source='topico_aula', many=True)
	# aulas = AulasTopicoSerializers(source='topico_aula', many=True)

	class Meta:
		model = Topico
		fields = ['id', 'nome', 'numero', 'criado_por', 'aulas']
