# -*- coding: utf-8 -*-
from rest_framework import serializers

from contas.api.serializers import UsuarioAlunoSerializers
from core.mixins import AuditFieldsSerializersMixin
from ..models import Aluno


class AlunoSerializers(serializers.ModelSerializer):
    empresa = serializers.StringRelatedField(many=False)
    departamento = serializers.StringRelatedField(many=False)
    setor = serializers.StringRelatedField(many=False)
    regional = serializers.StringRelatedField(many=False)
    usuario = UsuarioAlunoSerializers(many=False)
    equipe = serializers.StringRelatedField(many=False)
    foto_perfil = serializers.SerializerMethodField(method_name='get_imagem')

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'dta_nasc', 'foto_perfil',
                  'empresa', 'departamento', 'setor', 'regional', 'equipe', 'criado_em', 'modificado_em', 'usuario']

    def get_imagem(self, obj):
        if obj.foto_perfil:
            request = self.context.get('request')
            imagem_url = obj.foto_perfil.url
            return request.build_absolute_uri(imagem_url)
        return None


class AlunoCreateSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'usuario', 'criado_por', 'modificado_por']


class AlunoUpdateSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    nome = serializers.CharField(required=True)
    dta_nasc = serializers.DateField(required=True)

    class Meta:
        model = Aluno
        fields = ['nome', 'dta_nasc', 'criado_por', 'modificado_por']


class FotoPerfilSerializers(AuditFieldsSerializersMixin, serializers.ModelSerializer):
    foto_perfil = serializers.ImageField(required=True)

    class Meta:
        model = Aluno
        fields = ['foto_perfil', 'criado_por', 'modificado_por']
