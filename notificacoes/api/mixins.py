# -*- coding: utf-8 -*-

import datetime

from django.core.cache import cache
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response

from cursos.models import Matricula
from .serializers import NotificacaoDestinatarioSerializers
from ..models import NotificacaoDestinatario


class NotificacaoUsuarioViewSetMixin(object):
    # @method_decorator(cache_page(60 * 15))
    # @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        # Por padrão as notificações que serão mostradas serão dos últimos 1 meses
        data_inicial = datetime.date.today() - datetime.timedelta(days=30)
        usuario = request.user
        aluno = usuario.usuario_aluno
        cursos_matriculados = Matricula.objects.filter(usuario_id=aluno.usuario_id).values('curso_id')
        # chave = 'notificacoes_{0}'.format(usuario.username)

        # serializer = cache.get(chave)

        # if not serializer:
        queryset = NotificacaoDestinatario \
                .objects \
                .filter(criado_em__gte=data_inicial) \
                .filter(Q(destinario_id=aluno.usuario_id) | Q(empresa_id=aluno.empresa_id) | Q(curso_id__in=cursos_matriculados)).all()

        serializer = NotificacaoDestinatarioSerializers(queryset, many=True, context={"request": request})
            # cache.set(chave, serializer, 30)
            # print(cache.get(chave))

        return Response(serializer.data)
