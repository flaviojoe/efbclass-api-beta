# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from core.models import Timestamps, AuditModel
from efbclass.storage import fields
from efbclass.storage.storage_vimeo import VimeoFileStorage
from empresas.models import Empresa
from .lists import NIVEIS_CHOICES


# from s3upload.fields import S3UploadField


class Categoria(Timestamps, AuditModel):
    nome = models.CharField('categoria', max_length=50, unique=True)
    imagem = models.ImageField(upload_to='categoria', null=True, blank=True)

    def __str__(self):
        return self.nome

    @property
    def qtd_cursos(self):
        return self.cursos_categoria.count()


class Curso(Timestamps, AuditModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='cursos_empresa')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='cursos_categoria')
    nome = models.CharField(max_length=60)
    descricao = models.TextField(blank=True)
    nivel = models.IntegerField(choices=NIVEIS_CHOICES, default=1)
    imagem = models.ImageField('Imagem de apresentação', upload_to='curso_apresentacao', null=True, blank=True)
    url = models.URLField('Vídeo de apresentação', blank=True)

    def __str__(self):
        return self.nome

    @property
    def e_matriculado(self):
        return self.curso_usuario.exists()


class Topico(Timestamps, AuditModel):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='topicos_curso')
    nome = models.CharField(max_length=255)
    numero = models.IntegerField()

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['curso_id', 'numero']

    def __str__(self):
        return self.nome


class Aula(Timestamps, AuditModel):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='topico_aula')
    titulo = models.CharField(max_length=100)
    url = models.URLField('Link do vídeo', blank=True, help_text='O link pode ser do Youtube ou Vimeo')
    numero = models.IntegerField()
    video = fields.VimeoField(blank=True, null=True, storage=VimeoFileStorage, help_text='Enviar para o Vimeo - Teste')
    arquivo_video = models.FileField(upload_to='aulas_video', blank=True, null=True,
                                     help_text='Enviar para o Storage padrão')

    # arquivovideos3 = S3UploadField(dest='aulas_video', blank=True, null=True,
    # 								 help_text='Enviar para o Storage S3')

    class Meta:
        unique_together = ['topico', 'titulo']
        ordering = ['numero']

    def __str__(self):
        return self.titulo


class Matricula(Timestamps, AuditModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matricula_usuario')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='curso_usuario')
    descricao = models.CharField(max_length=150, help_text='Campo atribuído automaticamente.')

    class Meta:
        unique_together = ['usuario', 'curso']

    def __str__(self):
        return self.descricao


class HistoricoAula(Timestamps, AuditModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico_aula_usuario')
    # matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='historico_aula_matricula')
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='historico')
    finalizada = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Histórico de Aula'
        verbose_name_plural = 'Histórico de Aulas'
        unique_together = ['usuario', 'aula']


# unique_together = ['matricula', 'aula']


# Signals

@receiver(pre_save, sender=Matricula)
def atribuicoes_prova(sender, instance, **kwargs):
    print('Atribuindo descrição para Matricula')
    atrib = '{0}: {1}'.format(instance.usuario, instance.curso)
    print('Atribuição => ', atrib)
    instance.descricao = atrib


@receiver(post_save, sender=Matricula)
def gerar_avaliacao_matricula(sender, **kwargs):
    from questionarios.models import Prova, Questionario

    if kwargs.get('created', False):
        print('Mapeando provas para essa matricula.')
        matricula = kwargs.get('instance')
        questionarios_curso = Questionario.objects.filter(curso_id=matricula.curso.pk).all()

        print('Verificando se existe provas cadastradas para o curso.')
        if questionarios_curso.count():
            alvos = (Prova(matricula_id=matricula.pk, questionario_id=q.pk, criado_por=matricula.criado_por,
                           modificado_por=matricula.modificado_por, curso=matricula.curso
                           ) for q in questionarios_curso)
            Prova.objects.bulk_create(alvos)
            print('Provas mapeadas para essa matricula.')
        print('Sem provas cadastradas para o curso!')
