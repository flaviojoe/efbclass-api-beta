from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Timestamps, AuditModel
from core.utils import avataresIniciais, get_imagem_default
from cursos.models import Curso
from empresas.models import Departamento, Setor, Equipe, Regional, Empresa


def set_avatar_padrao():
	avatar = avataresIniciais()[2]
	return get_imagem_default(avatar)


class Aluno(Timestamps, AuditModel):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_aluno')
	nome = models.CharField(max_length=150)
	dta_nasc = models.DateField(null=True, blank=True)
	cpf = models.CharField(max_length=11, null=True, blank=True)
	foto_perfil = models.ImageField(upload_to='avatar', null=True, blank=True)
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, related_name='empresa_aluno')
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True,
									 related_name='departamento_aluno')
	setor = models.ForeignKey(Setor, on_delete=models.CASCADE, null=True, blank=True, related_name='setor_aluno')
	equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, null=True, blank=True, related_name='equipe_aluno')
	regional = models.ForeignKey(Regional, on_delete=models.CASCADE, null=True, blank=True,
								 related_name='regional_aluno')
	modo_escuro = models.BooleanField(default=False, verbose_name='ativar modo escuro')

	def __str__(self):
		return self.nome


# @receiver(post_save, sender=User)
# def gerar_vinculo_usuario_aluno(sender, **kwargs):
# 	if kwargs.get('created', False):
# 		if not settings.DEBUG:
# 			print('Criando Pré Vinculo entre Usuário e Aluno')
# 			usuario = kwargs.get('instance')
# 			Aluno.objects.create(
# 				nome=usuario.get_full_name() if usuario.first_name else usuario.username,
# 				usuario=usuario,
# 				criado_por=usuario,
# 				modificado_por=usuario
# 			)

@receiver(pre_save, sender=Aluno)
def setar_avatar_padrao(sender, instance, **kwargs):
	if not instance.foto_perfil:
		instance.foto_perfil = set_avatar_padrao()
