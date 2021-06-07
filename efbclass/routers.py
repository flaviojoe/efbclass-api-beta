from rest_framework import routers

from alunos.api.viewsets import AlunoViewSet
from core.api.viewsets import RankViewSet
from cursos.api.viewsets import CursoViewSet, CategoriaViewSet, HistoricoAulaViewset, MatriculaCursoViewSet, \
    TopicosViewSet
from empresas.api.viewsets import EmpresaViewSet
from faqs.api.viewsets import FAQViewSet
from materiais.api.viewsets import MaterialViewSet
from notificacoes.api.viewsets import NotificacaoUsuarioViewSet
from questionarios.api.viewsets import QuestionarioViewset, ProvaViewset, AvaliacaoViewset

router = routers.DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresas')
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'cursos', CursoViewSet, basename='cursos')
router.register(r'historico_aula', HistoricoAulaViewset, basename='historico_aula')
router.register(r'materiais', MaterialViewSet, basename='materiais')
router.register(r'alunos', AlunoViewSet, basename='alunos')
router.register(r'matricula', MatriculaCursoViewSet, basename='matriculas')
router.register(r'faqs', FAQViewSet, basename='faqs')
router.register(r'questionarios', QuestionarioViewset, basename='questionarios')
router.register(r'provas', ProvaViewset, basename='provas')
router.register(r'entrega_provas', AvaliacaoViewset, basename='entrega_provas')
router.register(r'notificacoes', NotificacaoUsuarioViewSet, basename='notificacoes')
router.register(r'ranks', RankViewSet, basename='ranks')
router.register(r'topicos', TopicosViewSet, basename='topicos')

routerpatterns = router.urls
