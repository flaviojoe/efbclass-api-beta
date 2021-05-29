from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand, call_command

from alunos.models import Aluno
from core.utils import geradorCPF, usuariosIniciais, avataresIniciais, get_imagem_default
from empresas.models import Empresa


class Command(BaseCommand):

	def __init__(self):
		super(Command, self).__init__()
		self.avataresIniciais = avataresIniciais()

	def criarAluno(self, dados):
		if 'empresa' in dados:
			return Aluno.objects.create(
				nome=dados.get('nome'),
				cpf=dados.get('cpf'),
				usuario=dados.get('usuario'),
				foto_perfil=dados.get('foto_perfil'),
				criado_por=dados.get('usuario'),
				modificado_por=dados.get('usuario'),
				empresa=dados.get('empresa')
			)
		return Aluno.objects.create(
			nome=dados.get('nome'),
			cpf=dados.get('cpf'),
			usuario=dados.get('usuario'),
			foto_perfil=dados.get('foto_perfil'),
			criado_por=dados.get('usuario'),
			modificado_por=dados.get('usuario'),
		)

	def procedimentoCriarUsuario(self, usuario, index):
		if not User.objects.filter(username=usuario.get('username')).exists():
			username = usuario.get('username')
			email = usuario.get('email')
			password = usuario.get('password')
			print('Criando super usuário: {} {}'.format(username, email))
			admin = User.objects.create_superuser(email=email, username=username, password=password)
			admin.is_active = usuario.get('is_active')
			admin.is_admin = usuario.get('is_admin')
			admin.first_name = usuario.get('first_name')
			admin.last_name = usuario.get('last_name')
			admin.save()

			grupo = usuario.get('group')
			if grupo == 'Todos':
				admin.groups.set(Group.objects.all().values_list('id', flat=True))
			else:
				admin.groups.set(Group.objects.all().filter(name=grupo).values_list('id', flat=True))

			aluno = {
				'nome': admin.get_full_name(),
				'cpf': geradorCPF(com_pontuacao=False),  # Gerador de CPF
				'usuario': admin,
				'foto_perfil': get_imagem_default(self.avataresIniciais[usuario.get('avatar_index')]),
				'criado_por': admin,
				'modificado_por': admin
			}

			if index > 0:
				empresa = Empresa.objects.get(pk=1)
				aluno['empresa'] = empresa
				self.criarAluno(dados=aluno)
			else:
				self.criarAluno(dados=aluno)

			print('Usuário admin {}, criado com sucesso!'.format(username))
		else:
			print('Usuário já existe!')

	def criarGrupos(self):
		print('Verificando grupos...')
		if Group.objects.count() == 0:
			Group.objects.bulk_create([
				Group(name='Aluno'),
				Group(name='Instrutor'),
				Group(name='Administrativo'),
			])
			print('Pronto! Grupos criados.')

	def criarEmpresas(self):
		print('Verificando empresas...')
		if Empresa.objects.count() == 0:
			Empresa.objects.bulk_create([
				Empresa(nome='Equatorial',
						criado_por_id=1, modificado_por_id=1),
				Empresa(nome='CGB',
						criado_por_id=1, modificado_por_id=1),
				Empresa(nome='55 Soluções',
						criado_por_id=1, modificado_por_id=1),
				Empresa(nome='Equatorial Pará',
						criado_por_id=1, modificado_por_id=1),
				Empresa(nome='Equatorial Maranhão',
						criado_por_id=1, modificado_por_id=1),
				Empresa(nome='Equatorial Piauí',
						criado_por_id=1, modificado_por_id=1),
				Empresa(nome='Equatorial Alagoas',
						criado_por_id=1, modificado_por_id=1),
			])
			print('Pronto! Empresas criadas.')

	def handle(self, *args, **options):
		call_command('migrate')
		try:
			self.criarGrupos()
			usuarios = usuariosIniciais()
			for index, usuario in enumerate(usuarios):
				if index == 1:
					self.criarEmpresas()
					aluno_anterior = Aluno.objects.get(pk=1)
					aluno_anterior.empresa_id = 1
					aluno_anterior.save()
				self.procedimentoCriarUsuario(usuario, index)

			call_command('initdatas')
		except Exception as ex:
			print(ex)
