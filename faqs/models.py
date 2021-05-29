from django.contrib.auth.models import User
from django.db import models

from core.models import Timestamps, AuditModel


class FAQ(Timestamps, AuditModel):
    pergunta = models.CharField(max_length=200)
    resposta = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'FAQ - Fale Conosco'
        verbose_name_plural = 'FAQs - Fale Conosco'

    def __str__(self):
        return self.pergunta
