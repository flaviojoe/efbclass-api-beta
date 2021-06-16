# -*- coding: utf-8 -*-
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from knox.auth import TokenAuthentication
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.mixins import AssociandoUserRequestMixin
from .mixins import MatriculaViewSetMixin, HistoricoAulaViewSetMixin, VideoAulaUpdateViewMixin, CategoriaViewSetMixin
from .serializers.aulas import HistoricoAulaSerializers
from .serializers.categorias import CategoriaSimpleSerializers
from .serializers.curso import CursoSerializers, MatriculaSerializers, CursoGradeCurricularAulasSerializers, \
    CursoTopicosAulasSerializers, CursosPorCategoriaDetailsSerializers, CursosDoAlunoSerializers, \
    CursoDetailsSerializers
from .serializers.topicos import TopicoSerializers
from ..models import Categoria, Curso, HistoricoAula, Matricula, Topico


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoriaViewSet(AssociandoUserRequestMixin, CategoriaViewSetMixin, ListAPIView, GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = CategoriaSimpleSerializers
    queryset = Categoria.objects.select_related('criado_por', 'modificado_por').all()


class TopicosViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = TopicoSerializers
    queryset = Topico.objects.select_related('criado_por').all()


class MeusCursosViewSet(AssociandoUserRequestMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = CursosDoAlunoSerializers
    queryset = Curso.objects.select_related('categoria').all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('nome',)
    ordering_fields = ('nome', 'criado_em')
    pagination_class = StandardResultsSetPagination

    def get_matricula_curso_usuario(self, usuario):
        return Matricula.objects.filter(usuario_id=usuario.pk)

    def get_matriculas_usuario(self, queryset):
        prefetch_curso_usuario = Prefetch('curso_usuario', queryset=queryset)
        return prefetch_curso_usuario

    def get_queryset(self):
        usuario = self.request.user

        queryset_curso_usuario = self.get_matricula_curso_usuario(usuario)
        prefetch_curso_usuario = self.get_matriculas_usuario(queryset_curso_usuario)

        queryset = Curso.objects \
            .select_related('categoria', 'criado_por') \
            .prefetch_related(prefetch_curso_usuario) \
            .filter(curso_usuario__usuario_id=usuario.pk) \
            .all()

        return queryset


class CategoriaCursoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')
    categoria = django_filters.CharFilter(lookup_expr='iexact', field_name='categoria__nome')

    class Meta:
        model = Curso
        fields = ['nome', 'categoria']


class CursoViewSet(AssociandoUserRequestMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = CursoSerializers
    queryset = Curso.objects.select_related('categoria').all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    # filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = CategoriaCursoFilter
    # search_fields = ('nome',)
    ordering_fields = ('nome', 'criado_em')
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.action == 'list':
            aluno = self.request.user.usuario_aluno
            queryset = Curso.objects.filter(empresa_id=aluno.empresa_id).select_related('categoria')
            return queryset
        return super(CursoViewSet, self).get_queryset()

    def get_matricula_curso_usuario(self, usuario):
        return Matricula.objects.filter(usuario_id=usuario.pk)

    def get_matriculas_usuario(self, queryset):
        prefetch_curso_usuario = Prefetch('curso_usuario', queryset=queryset)
        return prefetch_curso_usuario

    # def list(self, request, *args, **kwargs):
    #     aluno = request.user.usuario_aluno
    #
    #     filtros = dict(request.GET.lists())
    #
    #     print(filtros)
    #
    #     queryset = Curso.objects.filter(empresa_id=aluno.empresa_id).select_related('categoria')
    #
    #     if filtros and filtros.get('categoria__nome'):
    #         categoria = str(filtros.get('categoria__nome')[0]).lower()
    #         print(categoria)
    #         queryset.filter(categoria__nome__iexact=categoria).all()
    #
    #     # queryset = self.filter_queryset(qs.all())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def cursos_por_categoria(self, request, pk=None):
        aluno = request.user.usuario_aluno
        queryset = Curso.objects.select_related('criado_por', 'categoria').filter(empresa_id=aluno.empresa_id,
                                                                                  categoria_id=pk)
        serializer = CursosPorCategoriaDetailsSerializers(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        curso_id = kwargs.get('pk')
        usuario = request.user

        queryset_curso_usuario = Matricula.objects.filter(usuario_id=usuario.pk, curso_id=curso_id)
        prefetch_curso_usuario = Prefetch('curso_usuario', queryset=queryset_curso_usuario)

        queryset = Curso.objects \
            .select_related('categoria', 'criado_por') \
            .prefetch_related(
            'topicos_curso', 'topicos_curso__topico_aula', prefetch_curso_usuario) \
            .get(pk=curso_id)

        serializer = CursoGradeCurricularAulasSerializers(queryset, many=False, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def topicos_por_curso(self, request, pk=None):
        curso = self.get_object()
        topicos = Topico.objects.filter(curso_id=curso.pk).select_related('criado_por').all()
        serializer = TopicoSerializers(topicos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def aulas_do_curso(self, request, pk=None):
        usuario = request.user

        serializer = None
        queryset_historico_aula_matricula = HistoricoAula.objects.filter(
            criado_por=usuario)
        prefetch_historico_aula_matricula = Prefetch('topicos_curso__topico_aula__historico',
                                                     queryset=queryset_historico_aula_matricula)

        queryset = Curso.objects.select_related('categoria', 'criado_por').prefetch_related(
            'topicos_curso', 'topicos_curso__topico_aula', prefetch_historico_aula_matricula).get(pk=pk)

        serializer = CursoTopicosAulasSerializers(queryset, many=False, context={"request": request})
        return Response(serializer.data)


class MatriculaCursoViewSet(AssociandoUserRequestMixin, MatriculaViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    serializer_class = MatriculaSerializers
    queryset = Matricula.objects.select_related('usuario', 'curso', 'criado_por',
                                                'modificado_por').all()


class HistoricoAulaViewset(AssociandoUserRequestMixin, HistoricoAulaViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = HistoricoAulaSerializers
    queryset = HistoricoAula.objects.select_related('usuario', 'aula').all()


class VideoAulaUpdateView(AssociandoUserRequestMixin, VideoAulaUpdateViewMixin, APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    parser_classes = [MultiPartParser, ]
