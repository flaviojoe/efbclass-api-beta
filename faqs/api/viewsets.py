# -*- coding: utf-8 -*-
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.mixins import AssociandoUserRequestMixin
from core.utils import respostaSucesso, respostaErro
from .serializers import FAQSerializers, FAQCreateSerializers
from ..models import FAQ


class FAQViewSet(AssociandoUserRequestMixin, ModelViewSet):
	permission_classes = [IsAuthenticated]
	authentication_classes = (TokenAuthentication, SessionAuthentication,)
	serializer_class = FAQSerializers
	queryset = FAQ.objects.select_related('criado_por', 'modificado_por').all()

	def get_serializer_class(self):
		if self.action == 'create':
			return FAQCreateSerializers
		return FAQSerializers

	def create(self, request, *args, **kwargs):
		serializer = None
		try:
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer)
			headers = self.get_success_headers(serializer.data)
			return Response(respostaSucesso(serializer.data, 'Pergunta recebida com sucesso!', status.HTTP_201_CREATED),
							headers=headers)
		except ValidationError as e:
			print(type(e))
			return Response(respostaErro(serializer.errors, 'Erro ao criar a pergunta!'))
