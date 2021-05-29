# -*- coding: utf-8 -*-

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.mixins import AssociandoUserRequestMixin
from .serializers import EmpresaSerializers
from ..models import Empresa


class EmpresaViewSet(AssociandoUserRequestMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = EmpresaSerializers
    queryset = Empresa.objects.select_related('criado_por', 'modificado_por').all()
