from django.db import models

from core.models import Timestamps, AuditModel
from cursos.models import Curso, Aula
from empresas.models import Empresa


class TipoMaterial(Timestamps, AuditModel):
    nome = models.CharField('tipo de material', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Tipo de Material'
        verbose_name_plural = 'Tipos de Material'

    def __str__(self):
        return self.nome


class Material(Timestamps, AuditModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='materiais_empresa', null=True,
                                blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materiais_curso', null=True, blank=True)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='materiais_aula', null=True, blank=True)
    tipo = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE, related_name='materiais_tipo')
    nome = models.CharField(max_length=120)
    conteudo = models.CharField(max_length=200, blank=True, help_text='Um resumo do material (Não é obrigatório)')
    arquivo = models.FileField(upload_to='material', null=True, blank=True)
    informativo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'

    def __str__(self):
        return self.nome
