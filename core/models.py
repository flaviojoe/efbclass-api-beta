# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

from middleware.current_user import CurrentUserMiddleware


class Timestamps(models.Model):
	criado_em = models.DateTimeField(auto_now_add=True)
	modificado_em = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class TimestampsNoAutoNow(models.Model):
	criado_em = models.DateTimeField()
	modificado_em = models.DateTimeField()

	class Meta:
		abstract = True


class AuditModel(models.Model):
	criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_criadopor',
								   on_delete=models.CASCADE, null=True, blank=True)
	modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_modificadopor',
									   on_delete=models.CASCADE, null=True, blank=True)

	@staticmethod
	def get_current_user():
		return CurrentUserMiddleware.get_current_user()

	def set_user_fields(self, user):
		if user and user.pk:
			if not self.pk:
				self.criado_por = user
			self.modificado_por = user

	def save(self, *args, **kwargs):
		current_user = self.get_current_user()
		self.set_user_fields(current_user)
		super().save(*args, **kwargs)

	class Meta:
		abstract = True


class Rank(models.Model):
	id = models.BigIntegerField(primary_key=True)
	empresa = models.CharField(max_length=50)
	usuario = models.CharField(max_length=25)
	nome = models.CharField(max_length=100)
	avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
	qtd_acertos = models.BigIntegerField()
	qtd_perguntas = models.BigIntegerField()
	data_ultima_prova = models.DateTimeField()
	pontuacao = models.FloatField()
	posicao = models.BigIntegerField()

	class Meta:
		managed = False
		db_table = 'core_ranks'


class RankCurso(models.Model):
	id = models.BigIntegerField(primary_key=True)
	empresa = models.CharField(max_length=50)
	nome_curso = models.CharField(max_length=100)
	usuario = models.CharField(max_length=25)
	nome = models.CharField(max_length=100)
	avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
	qtd_acertos = models.BigIntegerField()
	qtd_perguntas = models.BigIntegerField()
	data_ultima_prova = models.DateTimeField()
	pontuacao = models.FloatField()
	posicao = models.BigIntegerField()

	class Meta:
		managed = False
		db_table = 'core_ranks_curso'
