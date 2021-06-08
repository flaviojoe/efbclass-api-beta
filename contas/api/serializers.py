# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from alunos.models import Aluno

User._meta.get_field('email')._unique = True


class RegistroSerializers(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User.objects.create_user(
			validated_data['username'],
			validated_data['email'],
			validated_data['password']
		)
		user.first_name = validated_data['first_name']
		user.last_name = validated_data['last_name']
		user.save()
		return user


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

	def validate(self, data):
		user = authenticate(**data)
		if user and user.is_active:
			return user
		raise serializers.ValidationError("Credenciais incorretas!")


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('name',)


class FotoPerfilSerializer(serializers.ModelSerializer):
	class Meta:
		model = Aluno
		fields = ['foto_perfil']


class UsuarioSerializers(serializers.ModelSerializer):
	nome = serializers.SerializerMethodField(method_name='get_nome')
	groups = GroupSerializer(many=True)
	foto_perfil = serializers.SerializerMethodField(method_name='get_avatar')
	modo_escuro = serializers.SerializerMethodField(method_name='get_modo_escuro')
	aluno_id = serializers.SerializerMethodField(method_name='get_aluno_id')

	class Meta:
		model = User
		fields = ('id', 'username', 'nome', 'email', 'groups', 'foto_perfil', 'modo_escuro', 'aluno_id')

	def get_nome(self, obj):
		return obj.get_full_name()

	def get_avatar(self, obj):
		request = self.context.get('request')
		imagem_url = obj.usuario_aluno.foto_perfil.url
		return request.build_absolute_uri(imagem_url)

	def get_modo_escuro(self, obj):
		return obj.usuario_aluno.modo_escuro

	def get_aluno_id(self, obj):
		return obj.usuario_aluno.pk


class UsuarioAlunoSerializers(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'email',)


class ChangePasswordSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)
	old_password = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('old_password', 'password', 'password2')

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"erro": "Os campos de senha não coincidem."})

		return attrs

	def validate_old_password(self, value):
		user = self.context['request'].user
		if not user.check_password(value):
			raise serializers.ValidationError({"erro": "A senha antiga não está correta"})
		return value

	def update(self, instance, validated_data):
		instance.set_password(validated_data['password'])
		instance.save()
		return instance


class ChangeEmailSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True)

	class Meta:
		model = User
		fields = ('email',)

	def validate_email(self, value):
		user = self.context['request'].user
		if User.objects.exclude(pk=user.pk).filter(email=value).exists():
			raise serializers.ValidationError({"email": "Esse e-mail já está em uso."})
		return value

	def update(self, instance, validated_data):
		instance.email = validated_data['email']
		instance.save()
		return instance


class UsuarioDetailsSimpleSerializers(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name')


class UsuarioNameSerializers(serializers.ModelSerializer):
	nome = serializers.SerializerMethodField(method_name='get_full_name')

	class Meta:
		model = User
		fields = ('id', 'nome')

	def get_full_name(self, obj):
		return obj.get_full_name()
