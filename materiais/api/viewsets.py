# -*- coding: utf-8 -*-

from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.mixins import AssociandoUserRequestMixin
from .serializers import MaterialSerializers
from ..models import Material


class MaterialViewSet(AssociandoUserRequestMixin, ModelViewSet):
	permission_classes = [IsAuthenticated]
	authentication_classes = (TokenAuthentication, SessionAuthentication)
	serializer_class = MaterialSerializers
	queryset = Material \
		.objects \
		.select_related('curso', 'tipo', 'criado_por') \
		.all()

	@action(detail=False, methods=['get'])
	def informativos(self, request, pk=None):
		aluno = request.user.usuario_aluno
		print('Empresa => ', aluno.empresa)
		queryset = Material \
			.objects \
			.select_related('empresa', 'tipo', 'criado_por') \
			.filter(empresa_id=aluno.empresa_id) \
			.filter(informativo__exact=True) \
			.all()
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	@action(detail=True, methods=['get'])
	def materiais_curso(self, request, pk=None):
		queryset = Material.objects.filter(curso_id=pk).select_related('empresa', 'tipo', 'criado_por')
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)
