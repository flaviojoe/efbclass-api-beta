# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.utils import respostaSucesso, respostaErro
from .serializers import AlunoSerializers, FotoPerfilSerializers, AlunoUpdateSerializers
from ..models import Aluno


class AlunoViewSetMixin(object):
    def get_serializer_class(self):
        if self.action == 'atualizar_dados_publicos':
            return AlunoUpdateSerializers
        return AlunoSerializers

    @action(detail=True, methods=['put'])
    def atualizar_dados_publicos(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(respostaSucesso(serializer.data, 'Dados públicos atualizados com sucesso!'))
        except ValidationError:
            return Response(respostaErro([], 'Erro ao atualizar dados públicos!'))

    @action(detail=False, methods=['get'])
    def detalhe_usuario(self, request, pk=None):
        usuario = request.user
        queryset = self.get_queryset().filter(usuario_id=usuario.id).first()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)


class AlunoFotoPerfilUpdateViewMixin(object):
    def put(self, request, pk):
        try:
            obj = Aluno.objects.get(id=pk)
            dados = request.data.copy()
            serializer = FotoPerfilSerializers(obj, data=dados)
            if serializer.is_valid():
                obj.foto_perfil.delete(save=False)
                serializer.save()
                return Response(respostaSucesso(serializer.data, 'Foto de perfil atualizada com sucesso!'))
            else:
                return Response(respostaErro(serializer.errors, 'Erro ao atualizar foto de perfil!'))
        except Aluno.DoesNotExist:
            return Response(respostaErro([], 'Aluno informado não existe!'))
