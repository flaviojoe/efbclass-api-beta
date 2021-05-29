# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Prefetch
from rest_framework.response import Response

from core.utils import respostaSucesso, respostaErro
from .serializers import QuestionarioDetailsSerializers, QuestionarioSerializers, ProvaDetailsSerializers, \
    ProvaSerializers
from ..models import Questionario, QuestionarioXPergunta, Prova, Resposta, Avaliacao, Pergunta


class QuestionarioViewsetMixin(object):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionarioDetailsSerializers
        return QuestionarioSerializers

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        qxp = QuestionarioXPergunta.objects \
            .select_related('pergunta') \
            .prefetch_related('pergunta__respostas_pergunta') \
            .filter(questionario_id=pk)
        pf_qxp = Prefetch('questionarios_mapeados', queryset=qxp)

        queryset = Questionario.objects \
            .select_related('curso') \
            .prefetch_related(
                pf_qxp) \
            .get(pk=pk)

        serializer = QuestionarioDetailsSerializers(queryset)
        return Response(serializer.data)


class ProvaViewsetMixin(object):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProvaDetailsSerializers
        return ProvaSerializers

    def get_queryset(self):
        if self.action == 'retrieve':
            return Prova.objects \
                .select_related('matricula', 'questionario__curso') \
                .prefetch_related('questionario__questionarios_mapeados') \
                .all()
        return super(ProvaViewsetMixin, self).get_queryset()

    def list(self, request, *args, **kwargs):
        usuario = request.user

        queryset = Prova.objects \
            .select_related('matricula', 'questionario') \
            .prefetch_related('questionario__curso', 'questionario__curso__criado_por') \
            .filter(matricula__usuario=usuario) \
            .all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AvaliacaoViewSetMixin(object):
    def create(self, request, *args, **kwargs):
        try:
            dados = request.data.copy()
            usuario = request.user
            prova = Prova.objects.get(pk=dados[0].get('questionario_aluno_id'))
            alvos = []
            for d in dados:
                r = Resposta.objects.get(id=d.get('resposta_id'))
                alvos.append(
                    Avaliacao(
                        prova=prova,
                        pergunta=Pergunta.objects.get(id=d.get('pergunta_id')),
                        resposta=r,
                        e_correta=r.e_correta,
                        criado_por=usuario,
                        modificado_por=usuario,
                        curso=prova.curso
                    )
                )
            Avaliacao.objects.bulk_create(alvos)
            prova.finalizado = True
            prova.save()
            return Response(respostaSucesso([], 'Prova recebida com sucesso!'))
        except Prova.DoesNotExist as ex:
            return Response(respostaErro([], 'Prova não encontrada!'))
        except ValueError as ex:
            print(ex)
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
        except ValidationError as ex:
            print(ex.messages)
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
        except IntegrityError as ex:
            print(ex)
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
        except Exception as ex:
            print(type(ex))
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
