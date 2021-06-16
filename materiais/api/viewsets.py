# -*- coding: utf-8 -*-

from knox.auth import TokenAuthentication
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from core.mixins import AssociandoUserRequestMixin
from .serializers import MaterialSerializers
from ..models import Material


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000


class MaterialViewSet(AssociandoUserRequestMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = MaterialSerializers
    queryset = Material \
        .objects \
        .select_related('curso', 'tipo', 'criado_por') \
        .all()

    @action(detail=True, methods=['get'])
    def materiais_curso(self, request, pk=None):
        queryset = Material.objects.filter(curso_id=pk).select_related('empresa', 'tipo', 'criado_por')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InformativoViewSet(AssociandoUserRequestMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = MaterialSerializers
    queryset = Material.objects.filter(informativo__exact=True).select_related('curso', 'tipo', 'criado_por')
    pagination_class = StandardResultsSetPagination
    search_fields = ('nome',)

    def get_queryset(self):
        aluno_logado = self.request.user.usuario_aluno
        self.queryset = Material.objects.filter(informativo__exact=True).select_related('curso', 'tipo',
                                                                                        'criado_por').filter(
            empresa_id=aluno_logado.empresa_id)
        return super(InformativoViewSet, self).get_queryset()
