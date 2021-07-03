# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.mixins import AuditFieldsSerializersMixin
from cursos.api.serializers.curso import CursoSimpleSerializers, MatriculaListProvasSerializers
from ..models import Questionario, QuestionarioXPergunta, Prova, Pergunta, Resposta, Avaliacao


class AvaliacaoSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    prova = serializers.PrimaryKeyRelatedField(read_only=True)
    pergunta = serializers.PrimaryKeyRelatedField(read_only=True)
    resposta = serializers.PrimaryKeyRelatedField(read_only=True)
    curso = serializers.StringRelatedField()
    criado_por = serializers.PrimaryKeyRelatedField(read_only=True)
    modificado_por = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Avaliacao
        fields = [
            'id', 'curso', 'prova', 'pergunta', 'resposta', 'criado_em', 'modificado_em', 'criado_por',
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
    curso_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Questionario
        fields = ['id', 'curso', 'curso_id', 'observacao', 'questionario_perguntas', 'criado_em', 'modificado_em']


class ProvaSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    questionario_id = serializers.PrimaryKeyRelatedField(read_only=True)
    curso_id = serializers.SerializerMethodField(method_name='get_curso_id')
    curso_nome = serializers.SerializerMethodField(method_name='get_curso_nome')
    curso_imagem = serializers.SerializerMethodField(method_name='get_curso_imagem')
    curso_criado_por = serializers.SerializerMethodField(method_name='get_curso_criado_por')
    matriculado_em = serializers.SerializerMethodField(method_name='get_matriculado_em')
    qtd_perguntas = serializers.IntegerField()
    qtd_respostas_certas = serializers.IntegerField(default=0)
    qtd_perguntas_2 = serializers.IntegerField()
    qtd_respostas_certas_2 = serializers.IntegerField(default=0)
    qtd_perguntas_3 = serializers.IntegerField()
    qtd_respostas_certas_3 = serializers.IntegerField(default=0)
    acertos = serializers.SerializerMethodField(method_name='get_acertos')
    acertos_2 = serializers.SerializerMethodField(method_name='get_acertos_2')
    acertos_3 = serializers.SerializerMethodField(method_name='get_acertos_3')

    class Meta:
        model = Prova
        fields = ['id', 'matriculado_em', 'questionario_id', 'curso_id', 'curso_nome', 'curso_imagem',
                  'curso_criado_por', 'finalizado', 'qtd_perguntas',
                  'qtd_respostas_certas', 'qtd_perguntas_2', 'qtd_respostas_certas_2', 'qtd_perguntas_3',
                  'qtd_respostas_certas_3', 'acertos', 'acertos_2', 'acertos_3']

    def get_curso_id(self, obj):
        return obj.questionario.curso_id

    def get_curso_nome(self, obj):
        return obj.questionario.curso.nome

    def get_curso_imagem(self, obj):
        return obj.questionario.curso.imagem.url

    def get_curso_criado_por(self, obj):
        return '{0} {1}'.format(obj.questionario.curso.criado_por.first_name,
                                obj.questionario.curso.criado_por.last_name)

    def get_matriculado_em(self, obj):
        return obj.matricula.criado_em.strftime("%m/%d/%Y %H:%M:%S")

    def get_acertos(self, obj):
        return round(obj.qtd_respostas_certas / obj.qtd_perguntas * 100, 1) if obj.qtd_perguntas > 0 else 0

    def get_acertos_2(self, obj):
        return round(obj.qtd_respostas_certas_2 / obj.qtd_perguntas_2 * 100, 1) if obj.qtd_perguntas_2 > 0 else 0

    def get_acertos_3(self, obj):
        return round(obj.qtd_respostas_certas_3 / obj.qtd_perguntas_3 * 100, 1) if obj.qtd_perguntas_3 > 0 else 0


class ProvaDetailsSerializers(AuditFieldsSerializersMixin, serializers.Serializer):
    id = serializers.IntegerField()
    matricula = serializers.SerializerMethodField()
    questionario = serializers.SerializerMethodField()
    finalizado = serializers.BooleanField()
    criado_em = serializers.DateTimeField()
    modificado_em = serializers.DateTimeField()
    qtd_perguntas = serializers.IntegerField()
    qtd_respostas_certas = serializers.IntegerField()

    class Meta:
        fields = ['id', 'matricula', 'questionario', 'finalizado', 'criado_em', 'modificado_em', 'qtd_perguntas',
                  'qtd_respostas_certas']

    def get_matricula(self, obj):
        return obj.matricula_id

    def get_questionario(self, obj):
        return obj.questionario_id


class RelatorioProvasAlunosSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    id_prova = serializers.IntegerField()
    login = serializers.CharField(max_length=50)
    nome = serializers.CharField(max_length=60, allow_null=True)
    finalizado = serializers.BooleanField()
    curso_id = serializers.IntegerField()
    curso = serializers.CharField(max_length=150, allow_null=True)
    empresa_id = serializers.IntegerField()
    empresa_nome = serializers.CharField(max_length=100, allow_null=True)
    acertos = serializers.IntegerField()
