# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.utils import respostaErro, respostaSucesso
from .serializers.aulas import VideoAulaSerializers
from .serializers.curso import MatriculaSerializers, MatriculaCreateSerializers
from ..models import HistoricoAula, Aula, Categoria


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


class CategoriaViewSetMixin(object):
    def categorias_empresa_usuario(self, request):
        aluno = request.user.usuario_aluno

        return Categoria.objects.prefetch_related('cursos_categoria').filter(
            cursos_categoria__isnull=False, cursos_categoria__empresa_id=aluno.empresa_id).distinct().all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.categorias_empresa_usuario(request), many=True)
        return Response(serializer.data)
