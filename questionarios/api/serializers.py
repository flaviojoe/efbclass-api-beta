# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.mixins import AuditFieldsSerializersMixin
from ..models import Questionario, QuestionarioXPergunta, Prova, Pergunta, Resposta, Avaliacao
from cursos.api.serializers.curso import CursoSimpleSerializers, MatriculaListProvasSerializers


class AvaliacaoSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = [
            'id', 'questionario_aluno', 'pergunta', 'resposta', 'criado_em', 'modificado_em', 'criado_por',
            'modificado_por'
        ]


class PerguntaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    class Meta:
        model = Pergunta
        fields = '__all__'


class RespostaSimpleSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = Resposta
        fields = ['id', 'label', 'value']

    def get_label(self, obj):
        return obj.resposta

    def get_value(self, obj):
        return '{0}:{1}:{2}'.format(obj.pergunta.id, obj.id, obj.resposta)


class PerguntaSimpleSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    respostas = RespostaSimpleSerializers(source='respostas_pergunta', many=True)

    class Meta:
        model = Pergunta
        fields = ['id', 'texto', 'respostas']


class RespostaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    pergunta_resposta = serializers.SerializerMethodField()

    class Meta:
        model = Resposta
        fields = ['id', 'pergunta', 'resposta', 'pergunta_resposta']

    def get_pergunta_resposta(self, obj):
        return '{0}:{1}'.format(obj.pergunta.id, obj.id)


class QuestionarioSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    curso = CursoSimpleSerializers(many=False)

    class Meta:
        model = Questionario
        fields = ['id', 'curso', 'observacao', 'criado_em', 'modificado_em']


class QuestionarioProvaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    class Meta:
        model = Questionario
        fields = ['id', 'observacao']


class QuestionarioSimpleSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    curso = CursoSimpleSerializers(many=False)

    class Meta:
        model = Questionario
        fields = ['id', 'curso']


class QuestionarioXPerguntaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    pergunta = PerguntaSimpleSerializers(many=False)
    questionario = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = QuestionarioXPergunta
        fields = ['id', 'questionario', 'pergunta', 'criado_em', 'modificado_em']


class QuestionarioXPerguntaSimpleSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    questionario = QuestionarioSerializers(many=False)

    class Meta:
        model = QuestionarioXPergunta
        fields = ['id', 'questionario', 'criado_em', 'modificado_em']


class QuestionarioDetailsSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    questionario_perguntas = QuestionarioXPerguntaSerializers(source='questionarios_mapeados', many=True)
    curso = serializers.StringRelatedField()

    class Meta:
        model = Questionario
        fields = ['id', 'curso', 'observacao', 'questionario_perguntas', 'criado_em', 'modificado_em']


class ProvaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    questionario = QuestionarioSimpleSerializers(many=False)
    matricula = MatriculaListProvasSerializers(many=False)
    qtd_perguntas = serializers.SerializerMethodField()
    qtd_respostas_certas = serializers.SerializerMethodField()

    class Meta:
        model = Prova
        fields = ['id', 'matricula', 'questionario', 'finalizado', 'criado_em', 'modificado_em', 'qtd_perguntas',
                  'qtd_respostas_certas']

    def get_qtd_perguntas(self, obj):
        return obj.prova_aluno.count()

    def get_qtd_respostas_certas(self, obj):
        return obj.prova_aluno.filter(e_correta=True).count()


class ProvaDetailsSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    qtd_perguntas = serializers.SerializerMethodField()
    qtd_respostas_certas = serializers.SerializerMethodField()

    class Meta:
        model = Prova
        fields = ['id', 'matricula', 'questionario', 'finalizado', 'criado_em', 'modificado_em', 'qtd_perguntas',
                  'qtd_respostas_certas']

    def get_qtd_perguntas(self, obj):
        return obj.prova_aluno.count()

    def get_qtd_respostas_certas(self, obj):
        return obj.prova_aluno.filter(e_correta=True).count()
