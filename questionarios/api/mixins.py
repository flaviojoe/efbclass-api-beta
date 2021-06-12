# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Prefetch
from rest_framework.response import Response

from core.utils import respostaSucesso, respostaErro
from .serializers import QuestionarioDetailsSerializers, QuestionarioSerializers
from ..models import Questionario, QuestionarioXPergunta, Prova, Resposta, Avaliacao, Pergunta


class QuestionarioViewsetMixin(object):
    def get_serializer_class(self):
        if self.action in ['retrieve', 'partial_update', 'update']:
            return QuestionarioDetailsSerializers
        return QuestionarioSerializers

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        qxp = QuestionarioXPergunta.objects \
            .select_related('pergunta', 'questionario') \
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


class AvaliacaoViewSetMixin(object):
    def create(self, request, *args, **kwargs):
        try:
            dados = request.data.copy()
            usuario = request.user
            prova = Prova.objects.get(pk=dados[0].get('prova_id'))
            curso_id = dados[0].get('curso_id')
            alvos = []

            ultima_tentativa = Avaliacao.objects.filter(criado_por_id=usuario.pk, prova_id=prova.pk,
                                                        curso_id=curso_id).order_by(
                '-tentativa').first()

            tentativa = ultima_tentativa.tentativa if ultima_tentativa else 0
            nova_tentativa = tentativa + 1

            if tentativa < 3:
                for d in dados:
                    r = Resposta.objects.get(id=d.get('resposta_id'))
                    p_id = d.get('pergunta_id')
                    alvos.append(
                        Avaliacao(
                            prova_id=prova.pk,
                            pergunta_id=p_id,
                            resposta_id=r.pk,
                            e_correta=r.e_correta,
                            criado_por_id=usuario.pk,
                            curso_id=curso_id,
                            tentativa=nova_tentativa
                        )
                    )
                Avaliacao.objects.bulk_create(alvos)

                if nova_tentativa >= 3:
                    prova.finalizado = True

                prova.save()
                return Response(respostaSucesso([], 'Prova recebida com sucesso!'))

            return Response(respostaErro([], 'Já utilizou todas as tentativas disponíveis!'))

        except Prova.DoesNotExist as ex:
            return Response(respostaErro([], 'Prova não encontrada!'))
        except ValueError as ex:
            print('ValueError => ', ex)
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
        except ValidationError as ex:
            print('ValidationError => ', ex.messages)
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
        except IntegrityError as ex:
            print('IntegrityError => ', ex)
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
        except AttributeError as ex:
            print('AttributeError => ', ex)
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
        except Exception as ex:
            print('Exception => ', type(ex))
            return Response(respostaErro([], 'Erro ao processar sua prova!'))
