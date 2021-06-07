# -*- coding: utf-8 -*-
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.utils import respostaErro, respostaSucesso
from .serializers.aulas import VideoAulaSerializers
from .serializers.curso import CursoDetailsSerializers, CursoSerializers, CursosDoAlunoSerializers, \
    MatriculaSerializers, MatriculaCreateSerializers
from ..models import HistoricoAula, Aula, Matricula, Curso, Categoria


class MatriculaViewSetMixin(object):
    def get_serializer_class(self):
        if self.action == 'create':
            return MatriculaCreateSerializers
        return MatriculaSerializers

    def create(self, request, *args, **kwargs):
        serializer = []
        try:
            usuario = request.user
            dados = request.data.copy()
            dados['usuario'] = usuario.pk
            serializer = self.get_serializer(data=dados)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(respostaSucesso(serializer.data, 'Matricula efetuada com sucesso!'), headers=headers)
        except ValidationError as e:
            print(e.detail)
            return Response(respostaErro(e.detail, 'Erro ao efetuar matricula'))
        except Exception as e:
            print(type(e))
            return Response(respostaErro(serializer.errors, 'Erro ao efetuar matricula'))


class HistoricoAulaViewSetMixin(object):
    def create(self, request, *args, **kwargs):
        dados = request.data.copy()
        usuario = request.user
        dados['usuario'] = usuario.pk

        if HistoricoAula.objects.filter(usuario_id=usuario.pk, aula_id=dados['aula']).exists():
            return Response(respostaSucesso([], 'Aula já finalizada!'))

        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VideoAulaUpdateViewMixin(object):
    def put(self, request, pk):
        try:
            obj = Aula.objects.get(id=pk)
            dados = request.data.copy()
            serializer = VideoAulaSerializers(obj, data=dados)
            if serializer.is_valid():
                obj.foto_perfil.delete(save=False)
                serializer.save()
                return Response(respostaSucesso(serializer.data, 'Vídeo carregado com sucesso!'))
            else:
                return Response(respostaErro(serializer.errors, 'Erro ao carregar vídeo!'))
        except Aula.DoesNotExist:
            return Response(respostaErro([], 'Aula informada não existe!'))


class CursoViewSetMixin(object):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CursoDetailsSerializers
        return CursoSerializers

    def get_matricula_curso_usuario(self, usuario, curso_id):
        return Matricula.objects.filter(usuario=usuario, curso_id=curso_id)

    def get_matriculas_usuario(self, queryset):
        prefetch_curso_usuario = Prefetch('curso_usuario', queryset=queryset)
        return prefetch_curso_usuario

    @action(detail=False, methods=['get'])
    def cursos_do_aluno(self, request, pk=None):
        usuario = request.user

        queryset_curso_usuario = self.get_matricula_curso_usuario(usuario, pk)
        prefetch_curso_usuario = self.get_matriculas_usuario(queryset_curso_usuario)

        queryset = Curso.objects \
            .select_related('categoria', 'criado_por') \
            .prefetch_related(prefetch_curso_usuario) \
            .filter(curso_usuario__usuario=usuario) \
            .all()

        serializer = CursosDoAlunoSerializers(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class CategoriaViewSetMixin(object):
    def categorias_empresa_usuario(self, request):
        aluno = request.user.usuario_aluno

        return Categoria.objects.prefetch_related('cursos_categoria').filter(
            cursos_categoria__isnull=False, cursos_categoria__empresa_id=aluno.empresa_id).distinct().all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.categorias_empresa_usuario(request), many=True)
        return Response(serializer.data)
