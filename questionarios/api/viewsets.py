# -*- coding: utf-8 -*-
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.mixins import AssociandoUserRequestMixin
from .mixins import QuestionarioViewsetMixin, ProvaViewsetMixin, AvaliacaoViewSetMixin
from .serializers import QuestionarioSerializers, ProvaSerializers, \
    AvaliacaoSerializers
from ..models import Prova, Questionario, Avaliacao


class QuestionarioViewset(AssociandoUserRequestMixin, QuestionarioViewsetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = QuestionarioSerializers
    queryset = Questionario.objects.select_related('curso').all()


class ProvaViewset(AssociandoUserRequestMixin, ProvaViewsetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = ProvaSerializers
    queryset = Prova.objects \
        .select_related('matricula', 'questionario') \
        .prefetch_related('questionario__curso', 'questionario__curso__criado_por') \
        .all()


class AvaliacaoViewset(AssociandoUserRequestMixin, AvaliacaoViewSetMixin, CreateModelMixin, ListModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = AvaliacaoSerializers
    queryset = Avaliacao.objects.select_related('questionario_aluno', 'pergunta', 'resposta', 'criado_por',
                                                'modificado_por').all()
