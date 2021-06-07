# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alunos.api.serializers import AlunoCreateSerializers
from core.utils import respostaSucesso, respostaErro
from .serializers import UsuarioSerializers, RegistroSerializers, ChangePasswordSerializer, \
    ChangeEmailSerializer


class UsuarioAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UsuarioSerializers

    def get_object(self):
        return self.request.user


class RegistroAPIView(generics.GenericAPIView):
    serializer_class = RegistroSerializers
    queryset = User.objects.prefetch_related('aluno', 'groups').all()

    def post(self, request, *args, **kwargs):
        serializer = None
        try:
            dados = request.data.copy()
            serializer = self.get_serializer(data=dados)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            grupoPadrao = Group.objects.get(name='Aluno')
            user.groups.add(grupoPadrao)
            user.is_active = False
            user.save()

            dados['usuario'] = user.pk
            dados['nome'] = user.get_full_name()

            serializer = AlunoCreateSerializers(data=dados)
            serializer.is_valid(raise_exception=True)
            aluno = serializer.save()

            return Response(respostaSucesso([], 'Registrado com sucesso! Aguarde sua aprovação.'))
        except ValidationError as e:
            return Response(respostaErro(e.detail, 'Dado(s) inválido(s)!'))
        except Exception as e:
            print(type(e))
            return Response(respostaErro(serializer.errors, 'Erro ao atualizar foto de perfil!'))


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        usuario = User.objects.prefetch_related('usuario_aluno', 'groups').get(id=request.user.id)
        # preferencia =
        data["user"] = UsuarioSerializers(
            usuario,
            context=self.get_context()
        ).data
        return data


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(respostaSucesso([], 'Senha alterada com sucesso!'))
        except ValidationError as ex:
            return Response(respostaErro(serializer.errors, 'Erro ao alterar a senha!'))


class ChangeEmailView(generics.UpdateAPIView):
    serializer_class = ChangeEmailSerializer
    model = User
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(respostaSucesso([], 'E-mail alterado com sucesso!'))
        except ValidationError as ex:
            return Response(respostaErro(serializer.errors, 'Erro ao alterar o e-mail'))
