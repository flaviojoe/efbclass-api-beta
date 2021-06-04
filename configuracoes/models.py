from django.db import models

from core.models import Timestamps, AuditModel
from empresas.models import Empresa


class Configuracao(Timestamps, AuditModel):
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='configuracao_empresa')
	qtd_tentativas_provas = models.IntegerField('Número de tentativas',
												help_text='Informe quantas vezes o aluno poderá fazer a mesma prova.',
												default=1)

	class Meta:
		verbose_name = 'Configuração'
		verbose_name_plural = 'Configurações'


class Preferencia(Timestamps, AuditModel):
	modo_escuro = models.BooleanField(default=False, verbose_name='ativar modo escuro')