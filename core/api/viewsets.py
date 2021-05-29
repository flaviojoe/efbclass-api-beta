# -*- coding: utf-8 -*-
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.mixins import AssociandoUserRequestMixin
from core.models import Rank, RankCurso
from core.utils import respostaErro
from cursos.models import Curso
from alunos.models import Aluno
from questionarios.models import Avaliacao
from .serializers import RankSerializers, RankPorCursoSerializers


class RankViewSet(AssociandoUserRequestMixin, ListAPIView, GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = RankSerializers
    queryset = Avaliacao.objects.all()

    def list(self, request, *args, **kwargs):
        usuario = request.user
        aluno = Aluno.objects.select_related('empresa').get(usuario=usuario)

        queryset = Rank.objects.filter(empresa=aluno.empresa.nome).all()[:10]

        serializer = RankSerializers(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def rank_por_curso(self, request, pk=None):
        try:
            curso = Curso.objects.get(pk=pk)
        except Curso.DoesNotExist as ex:
            return Response(respostaErro([], 'Curso não encontrado!'))

        queryset = Rank.objects.filter(nome_curso=curso.nome).all()

        serializer = RankPorCursoSerializers(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def rank_usuario_por_curso(self, request, pk=None):
        try:
            curso = Curso.objects.get(pk=pk)
            usuario = request.user
            queryset = RankCurso.objects.filter(nome_curso=curso.nome, usuario=usuario.username).first()

            serializer = RankPorCursoSerializers(queryset, many=False, context={"request": request})
            return Response(serializer.data)

        except Curso.DoesNotExist as ex:
            return Response(respostaErro([], 'Curso não encontrado!'))
        except IndexError as ex:
            return Response(respostaErro([], 'Sem ranks encontrados!'))
