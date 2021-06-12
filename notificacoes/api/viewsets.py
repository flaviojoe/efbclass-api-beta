# -*- coding: utf-8 -*-

from knox.auth import TokenAuthentication
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from core.mixins import AssociandoUserRequestMixin
from .mixins import NotificacaoUsuarioViewSetMixin
from .serializers import NotificacaoSerializers, NotificacoesDoUsuarioSerializers
from ..models import Notificacao
from ..queries import get_notificacoes, get_notificacoes_filter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class NotificacaoUsuarioViewSet(AssociandoUserRequestMixin, NotificacaoUsuarioViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = NotificacaoSerializers
    queryset = Notificacao.objects.select_related('criado_por').all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('mensagem')
    pagination_class = StandardResultsSetPagination

    def notifacacoes_do_usuario(self, request, filter):
        usuario = request.user
        if filter:
            print('Filter => ', filter)
            queryset = Notificacao.objects.raw(get_notificacoes_filter(), [usuario.pk, usuario.pk, usuario.pk, '%' + filter.lower() + '%'])
            return queryset
        queryset = Notificacao.objects.raw(get_notificacoes(), [usuario.pk, usuario.pk, usuario.pk])
        return queryset

    def list(self, request, *args, **kwargs):
        filtro = request.GET.get('filter')
        queryset = self.notifacacoes_do_usuario(request, filtro)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NotificacoesDoUsuarioSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # return self.notifacacoes_do_usuario(request)
