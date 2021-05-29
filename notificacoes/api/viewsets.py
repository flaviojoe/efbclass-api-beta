# -*- coding: utf-8 -*-

from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.mixins import AssociandoUserRequestMixin
from .mixins import NotificacaoUsuarioViewSetMixin
from .serializers import NotificacaoSerializers
from ..models import Notificacao


class NotificacaoUsuarioViewSet(AssociandoUserRequestMixin, NotificacaoUsuarioViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = NotificacaoSerializers
    queryset = Notificacao.objects.select_related('criado_por').all()
