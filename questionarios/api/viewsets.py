# -*- coding: utf-8 -*-
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination

from alunos.models import Aluno
from core.mixins import AssociandoUserRequestMixin
from core.utils import respostaErro
from .mixins import QuestionarioViewsetMixin, AvaliacaoViewSetMixin
from .serializers import QuestionarioSerializers, ProvaSerializers, \
    AvaliacaoSerializers, RelatorioProvasAlunosSerializers, ProvaDetailsSerializers
from ..models import Prova, Questionario, Avaliacao
from ..queries import get_provas_alunos


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000


class QuestionarioViewset(AssociandoUserRequestMixin, QuestionarioViewsetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = QuestionarioSerializers
    queryset = Questionario.objects.select_related('curso', 'curso__criado_por').all()


class ProvaViewset(AssociandoUserRequestMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = ProvaSerializers
    queryset = Prova.objects.select_related('matricula', 'questionario').all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('questionario__curso__nome',)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'partial_update', 'update']:
            return ProvaDetailsSerializers
        return ProvaSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = Prova.objects.select_related('matricula', 'questionario') \
            .extra(select={
            'qtd_perguntas': 'select count(id) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id'}) \
            .extra(select={
            'qtd_respostas_certas': 'select sum(case when e_correta then 1 else 0 end) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id'}) \
            .get(id=self.kwargs['pk'])

        serializer = ProvaDetailsSerializers(instance)
        return Response(serializer.data)

    def get_queryset(self):
        usuario = self.request.user

        queryset = Prova.objects.select_related('matricula', 'questionario', 'questionario__curso',
                                                'questionario__curso__criado_por') \
            .extra(select={
            'qtd_perguntas': 'select count(id) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 1'}) \
            .extra(select={
            'qtd_respostas_certas': 'select sum(case when e_correta then 1 else 0 end) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 1'}) \
            .extra(select={
            'qtd_perguntas_2': 'select count(id) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 2'}) \
            .extra(select={
            'qtd_respostas_certas_2': 'select sum(case when e_correta then 1 else 0 end) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 2'}) \
            .extra(select={
            'qtd_perguntas_3': 'select count(id) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 3'}) \
            .extra(select={
            'qtd_respostas_certas_3': 'select sum(case when e_correta then 1 else 0 end) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 3'}) \
 \
            .filter(matricula__usuario_id=usuario.pk)

        return queryset

 #    def list(self, request, *args, **kwargs):
 #        usuario = request.user
 #
 #        queryset = Prova.objects.select_related('matricula', 'questionario', 'questionario__curso',
 #                                                'questionario__curso__criado_por') \
 #            .extra(select={
 #            'qtd_perguntas': 'select count(id) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 1'}) \
 #            .extra(select={
 #            'qtd_respostas_certas': 'select sum(case when e_correta then 1 else 0 end) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 1'}) \
 #            .extra(select={
 #            'qtd_perguntas_2': 'select count(id) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 2'}) \
 #            .extra(select={
 #            'qtd_respostas_certas_2': 'select sum(case when e_correta then 1 else 0 end) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 2'}) \
 #            .extra(select={
 #            'qtd_perguntas_3': 'select count(id) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 3'}) \
 #            .extra(select={
 #            'qtd_respostas_certas_3': 'select sum(case when e_correta then 1 else 0 end) qtd_perguntas from questionarios_avaliacao where prova_id = questionarios_prova.id and tentativa = 3'}) \
 # \
 #            .filter(matricula__usuario_id=usuario.pk)
 #
 #        page = self.paginate_queryset(queryset)
 #        if page is not None:
 #            serializer = self.get_serializer(page, many=True)
 #            return self.get_paginated_response(serializer.data)
 #
 #        serializer = self.get_serializer(queryset, many=True)
 #        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def provas_alunos(self, request, pk=None):
        try:
            queryset = Aluno.objects.raw(get_provas_alunos())
            serializer = RelatorioProvasAlunosSerializers(queryset, many=True)
            return Response(serializer.data)
        except Exception as ex:
            print(ex)
            return Response(respostaErro([], 'Erro ao gerar relatório'))


class AvaliacaoViewset(AssociandoUserRequestMixin, AvaliacaoViewSetMixin, CreateModelMixin, ListModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = AvaliacaoSerializers
    queryset = Avaliacao.objects.select_related('curso', 'prova', 'pergunta', 'resposta', 'criado_por',
                                                'modificado_por').all()
