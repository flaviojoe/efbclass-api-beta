from rest_framework import serializers


class RankSerializers(serializers.Serializer):
    empresa = serializers.CharField(max_length=50, allow_null=True)
    usuario = serializers.CharField(max_length=50, allow_null=True)
    nome = serializers.CharField(max_length=50, allow_null=True)
    avatar = serializers.ImageField(allow_null=True)
    qtd_acertos = serializers.IntegerField(default=0)
    qtd_perguntas = serializers.IntegerField(default=0)
    pontuacao = serializers.DecimalField(default=0.0, max_digits=19, decimal_places=1)
    posicao = serializers.IntegerField(default=0)


class RankPorCursoSerializers(serializers.Serializer):
    empresa = serializers.CharField(max_length=50, allow_null=True)
    nome_curso = serializers.CharField(allow_null=True)
    usuario = serializers.CharField(max_length=50, allow_null=True)
    nome = serializers.CharField(max_length=50, allow_null=True)
    avatar = serializers.ImageField(allow_null=True)
    qtd_acertos = serializers.IntegerField(default=0)
    qtd_perguntas = serializers.IntegerField(default=0)
    pontuacao = serializers.DecimalField(default=0.0, max_digits=19, decimal_places=1)
    posicao = serializers.IntegerField(default=0)
