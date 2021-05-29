from django.contrib import messages
from django.utils.translation import ngettext


class AcoesProvaAdmin(object):
	def marcar_como_finalizada(self, request, queryset):
		atualizacao = queryset.update(finalizado=True)
		self.message_user(request, ngettext(
			'%d prova foi marcada como finalizada com sucesso.',
			'%d provas foram marcadas como finalizadas com sucesso.',
			atualizacao
		) % atualizacao, messages.SUCCESS)

	marcar_como_finalizada.short_description = 'Marcar como finalizada'

	def marcar_como_ativa(self, request, queryset):
		atualizacao = queryset.update(finalizado=False)
		self.message_user(request, ngettext(
			'%d prova foi marcada como ativa com sucesso.',
			'%d provas foram marcadas como ativas com sucesso.',
			atualizacao
		) % atualizacao, messages.SUCCESS)

	marcar_como_ativa.short_description = 'Marcar como ativa'
