from django.db import models

from core.models import Timestamps, AuditModel


class Empresa(Timestamps, AuditModel):
    nome = models.CharField('empresa', max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Regional(Timestamps, AuditModel):
    nome = models.CharField('regional', max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Regionais'

    def __str__(self):
        return self.nome


class Departamento(Timestamps, AuditModel):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Setor(Timestamps, AuditModel):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Setores'

    def __str__(self):
        return self.nome


class Equipe(Timestamps, AuditModel):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome
