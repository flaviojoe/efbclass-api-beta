# -*- coding: utf-8 -*-

from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from core.mixins import AssociandoUserRequestMixin
from .mixins import AlunoFotoPerfilUpdateViewMixin, AlunoViewSetMixin
from .serializers import AlunoSerializers
from ..models import Aluno


class AlunoFotoPerfilUpdateView(AssociandoUserRequestMixin, AlunoFotoPerfilUpdateViewMixin, UpdateAPIView, APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    parser_classes = [MultiPartParser, ]


class AlunoViewSet(AssociandoUserRequestMixin, AlunoViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    serializer_class = AlunoSerializers
    queryset = Aluno.objects.select_related('usuario', 'empresa', 'departamento', 'setor', 'equipe').all()
