# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework import serializers

from core.mixins import AuditFieldsSerializersMixin
from .fields import UsuarioField
from .topicos import TopicoCursoDetailsSerializers, TopicoCursoGradeSerializers
from ...models import Curso, Categoria, Matricula


class MatriculaListProvasSerializers(serializers.ModelSerializer):
	class Meta:
		model = Matricula
		fields = ['id', 'criado_em']


class MatriculaCreateSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
	class Meta:
		model = Matricula
		fields = ['usuario', 'curso', 'criado_por', 'modificado_por']


class CursoSimpleSerializers(serializers.ModelSerializer):
	# imagem = serializers.SerializerMethodField()
	criado_por = UsuarioField(many=False, read_only=True)

	class Meta:
		model = Curso
		fields = ['id', 'nome', 'imagem', 'criado_por']

	def get_imagem(self, obj):
		if settings.DEBUG:
			request = self.context.get('request')
			imagem_url = obj.imagem.url
			return request.build_absolute_uri(imagem_url)
		return obj.imagem.url


class MatriculaSerializers(serializers.ModelSerializer):
	curso = CursoSimpleSerializers(many=False)
	aluno = serializers.StringRelatedField(many=False)

	class Meta:
		model = Matricula
		fields = ['id', 'usuario', 'curso', 'criado_em', 'modificado_em']


class CursoSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
	categoria = serializers.StringRelatedField(many=False)

	class Meta:
		model = Curso
		fields = [
			'id', 'nome', 'categoria', 'descricao', 'nivel', 'url', 'imagem', 'criado_em',
			'modificado_em'
		]


class CursoDetailsSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
	categoria = serializers.StringRelatedField(many=False)
	e_matriculado = serializers.ReadOnlyField()

	class Meta:
		model = Curso
		fields = [
			'id', 'nome', 'categoria', 'descricao', 'nivel', 'url', 'imagem', 'criado_em', 'modificado_em',
			'e_matriculado'
		]


class CursosPorCategoriaDetailsSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
	criado_por = UsuarioField(many=False, read_only=True)
	categoria = serializers.StringRelatedField()

	class Meta:
		model = Curso
		fields = [
			'categoria', 'id', 'nome', 'descricao', 'url', 'imagem', 'criado_em', 'criado_por',
			'modificado_em'
		]


class CursosPorCategoriaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
	cursos = CursosPorCategoriaDetailsSerializers(source='cursos_categoria', many=True)

	class Meta:
		model = Categoria
		fields = ['id', 'nome', 'cursos']


class CursosDoAlunoSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
	categoria = serializers.StringRelatedField()
	criado_por = UsuarioField(many=False, read_only=True)
	imagem = serializers.SerializerMethodField()

	class Meta:
		model = Curso
		fields = [
			'id', 'nome', 'categoria', 'descricao', 'nivel', 'url', 'imagem', 'criado_por',
			'criado_em', 'modificado_em'
		]

	def get_imagem(self, obj):
		request = self.context.get('request')
		imagem_url = obj.imagem.url
		return request.build_absolute_uri(imagem_url)


class CursoTopicosAulasSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
	categoria = serializers.StringRelatedField()
	topicos = TopicoCursoDetailsSerializers(source='topicos_curso', many=True)
	criado_por = UsuarioField(many=False, read_only=True)

	class Meta:
		model = Curso
		fields = [
			'id', 'nome', 'categoria', 'descricao', 'nivel', 'url', 'imagem',
			'criado_por', 'criado_em', 'modificado_em', 'topicos'
		]


class CursoGradeCurricularAulasSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
	categoria = serializers.StringRelatedField()
	e_matriculado = serializers.ReadOnlyField()
	qtd_topicos = serializers.SerializerMethodField(method_name='get_qtd_topicos', source='topicos_curso')
	topicos = TopicoCursoGradeSerializers(source='topicos_curso', many=True)
	criado_por = UsuarioField(many=False, read_only=True)

	class Meta:
		model = Curso
		fields = [
			'id', 'nome', 'categoria', 'descricao', 'url', 'imagem', 'e_matriculado',
			'criado_por', 'criado_em', 'modificado_em', 'qtd_topicos', 'topicos'
		]

	def get_qtd_topicos(self, obj):
		return obj.topicos_curso.count()

class CursosPorCategoriaRAWSerializers(AuditFieldsSerializersMixin, serializers.Serializer):
	id = serializers.IntegerField()
	categoria = serializers.CharField()
	cursos = serializers.DictField(child=serializers.CharField())
