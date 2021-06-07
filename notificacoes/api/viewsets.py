# -*- coding: utf-8 -*-

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.mixins import AssociandoUserRequestMixin
from .mixins import NotificacaoUsuarioViewSetMixin
from .serializers import NotificacaoSerializers, NotificacoesDoUsuarioSerializers
from ..models import Notificacao


class NotificacaoUsuarioViewSet(AssociandoUserRequestMixin, NotificacaoUsuarioViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = NotificacaoSerializers
    queryset = Notificacao.objects.select_related('criado_por').all()

    # @method_decorator(cache_page(60 * 15))
    # @method_decorator(vary_on_cookie)
    def notifacacoes_do_usuario(self, request):
        usuario = request.user
        queryset = Notificacao.objects.raw('''
        select a.id,
        a.mensagem,
        (c.first_name || ' ' || c.last_name) criado_por_nome,
        b.is_empresa,
        b.is_curso,
        b.is_usuario,
        a.criado_em,
        case when a.imagem <> '' then true else false end possui_imagem
        from notificacoes_notificacao a
        inner join notificacoes_notificacaodestinatario b ON b.notificacao_id = a.id
        inner join auth_user c on a.criado_por_id = c.id
        where a.criado_em >= current_date - 30
        and (
            b.destinario_id = %s
            or b.curso_id in (
                select id from cursos_matricula cm where cm.usuario_id = %s
            )
            or b.empresa_id = (select empresa_id from alunos_aluno aa where aa.usuario_id = %s)
        )
        ''', [usuario.pk, usuario.pk, usuario.pk])
        serializer = NotificacoesDoUsuarioSerializers(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return self.notifacacoes_do_usuario(request)
