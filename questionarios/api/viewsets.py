# -*- coding: utf-8 -*-
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response

from core.mixins import AssociandoUserRequestMixin
from core.utils import respostaErro
from .mixins import QuestionarioViewsetMixin, ProvaViewsetMixin, AvaliacaoViewSetMixin
from .serializers import QuestionarioSerializers, ProvaSerializers, \
    AvaliacaoSerializers, RelatorioProvasAlunosSerializers
from ..models import Prova, Questionario, Avaliacao
from alunos.models import Aluno
from rest_framework.decorators import action


class QuestionarioViewset(AssociandoUserRequestMixin, QuestionarioViewsetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = QuestionarioSerializers
    queryset = Questionario.objects.select_related('curso').all()


class ProvaViewset(AssociandoUserRequestMixin, ProvaViewsetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = ProvaSerializers
    queryset = Prova.objects \
        .select_related('matricula', 'questionario') \
        .prefetch_related('questionario__curso', 'questionario__curso__criado_por') \
        .all()

    @action(detail=False, methods=['get'])
    def provas_alunos(self, request, pk=None):
        try:
            queryset = Aluno.objects.raw('''
                SELECT a.id,
                c.id as id_prova,
                b.username as login,
                a.nome,
                c.finalizado,
                c.curso_id,
                d.nome as curso,
                a.empresa_id,
                f.nome as empresa_nome,
                sum(CASE e_correta WHEN true THEN 1	ELSE 0 END) acertos
                
                FROM public.alunos_aluno a
                left join auth_user b on a.usuario_id=b.id
                left join questionarios_prova c on a.usuario_id=c.criado_por_id
                left join cursos_curso d on c.curso_id=d.id
                left join questionarios_avaliacao e on a.usuario_id=e.criado_por_id and c.curso_id=e.curso_id
                left join empresas_empresa f on a.empresa_id = f.id
                
                where a.id > 6
                
                group by a.id,
                c.id,
                username, a.nome,
                c.finalizado,
                c.curso_id,
                d.nome,
                a.empresa_id,
                f.nome
            ''')
            serializer = RelatorioProvasAlunosSerializers(queryset, many=True)
            return Response(serializer.data)
        except Exception as ex:
            print(ex)
            return Response(respostaErro([], 'Erro ao gerar relatório'))


class AvaliacaoViewset(AssociandoUserRequestMixin, AvaliacaoViewSetMixin, CreateModelMixin, ListModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = AvaliacaoSerializers
    queryset = Avaliacao.objects.select_related('questionario_aluno', 'pergunta', 'resposta', 'criado_por',
                                                'modificado_por').all()
