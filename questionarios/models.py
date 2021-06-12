# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from alunos.models import Aluno
from core.models import Timestamps, AuditModel
from cursos.models import Curso, Topico, Matricula


class Pergunta(Timestamps, AuditModel):
    texto = models.TextField('Pergunta', unique=True, help_text='Digite a pergunta.')

    def __str__(self):
        return self.texto


class Resposta(Timestamps, AuditModel):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='respostas_pergunta')
    resposta = models.CharField(max_length=200, help_text='Digite as opções de resposta das perguntas.')
    e_correta = models.BooleanField(
        default=False, help_text='Marque esse campo, somente se essa opção for a resposta certa da pergunta.')

    def __str__(self):
        return self.resposta


class Questionario(Timestamps, AuditModel):
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, related_name='questionarios_curso',
        help_text='Selecione o curso do qual deseja criar o questionário'
    )
    observacao = models.CharField('Observação', max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Questionário'
        verbose_name_plural = 'Questionários'

    def __str__(self):
        return self.curso.nome


class QuestionarioXPergunta(Timestamps, AuditModel):
    questionario = models.ForeignKey(
        Questionario, on_delete=models.CASCADE, related_name='questionarios_mapeados',
        verbose_name='Questionário do curso',
        help_text='Para adicionar uma pergunta a um Questionário existente, selecione pelo nome do curso. Caso queira montar um novo questionário, cliqueo no botão + ao lado.'
    )
    pergunta = models.ForeignKey(
        Pergunta, on_delete=models.CASCADE, related_name='perguntas_mapeadas',
        help_text='Selecione uma das perguntas cadastradas em nosso banco de dados, ou clique no + ao lado para adiconar uma nova pergunta.'
    )

    class Meta:
        unique_together = ['questionario', 'pergunta']
        verbose_name = 'Mapeamento de Questionário e Perguntas'
        verbose_name_plural = 'Mapeamento de Questionários e Perguntas'


class Prova(Timestamps, AuditModel):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='questionarios_matricula')
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE, related_name='questionarios_prova')
    data_limite = models.DateField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, related_name='questionario_curso',
        help_text='Informação atribuída automaticamente.')


class Avaliacao(Timestamps, AuditModel):
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE, related_name='prova_aluno')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='prova_perguntas')
    resposta = models.ForeignKey(Resposta, on_delete=models.CASCADE, related_name='prova_respostas')
    e_correta = models.BooleanField(default=False)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='prova_curso')
    tentativa = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'


@receiver(pre_save, sender=Prova)
def atribuicoes_prova(sender, instance, **kwargs):
    print('Atribuindo curso do questionário em prova!')
    q = Questionario.objects.get(pk=instance.questionario.pk)
    instance.curso = q.curso
