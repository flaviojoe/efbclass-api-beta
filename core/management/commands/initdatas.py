from django.core.management import BaseCommand

from core.utils import imagensIniciais, get_imagem_default, imagensCategorias
from cursos.models import Curso, Categoria, Topico, Aula, Matricula
from empresas.models import Regional, Departamento, Setor, Equipe
from materiais.models import TipoMaterial, Material
from questionarios.models import Questionario, Pergunta, Resposta, QuestionarioXPergunta, Prova


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.imagensIniciais = imagensIniciais()
        self.imagensCategorias = imagensCategorias()

    def handle(self, *args, **options):
        try:
            print('Iniciando carga inicial de dados...')
            print('Verificando regionais...')
            if Regional.objects.count() == 0:
                Regional.objects.bulk_create([
                    Regional(nome='Centro', criado_por_id=1,
                             modificado_por_id=1),
                    Regional(nome='Leste', criado_por_id=1, modificado_por_id=1),
                    Regional(nome='Noroeste', criado_por_id=1,
                             modificado_por_id=1),
                    Regional(nome='Nordeste', criado_por_id=1,
                             modificado_por_id=1),
                    Regional(nome='Norte', criado_por_id=1, modificado_por_id=1),
                    Regional(nome='Oeste', criado_por_id=1, modificado_por_id=1),
                    Regional(nome='Sul', criado_por_id=1, modificado_por_id=1),
                    Regional(nome='Sede', criado_por_id=1,
                             modificado_por_id=1),
                ])
                print('Pronto! Regionais criadas.')
            print('Verificando categorias...')
            if Categoria.objects.count() == 0:
                Categoria.objects.bulk_create([
                    Categoria(nome='Atendimento', imagem=get_imagem_default(self.imagensCategorias[0]), criado_por_id=1, modificado_por_id=1),
                    Categoria(nome='Leitura', imagem=get_imagem_default(self.imagensCategorias[3]), criado_por_id=1, modificado_por_id=1),
                    Categoria(nome='Negociação', imagem=get_imagem_default(self.imagensCategorias[4]), criado_por_id=1, modificado_por_id=1),
                    Categoria(nome='Cadastro', imagem=get_imagem_default(self.imagensCategorias[1]), criado_por_id=1, modificado_por_id=1),
                    Categoria(nome='Desenvolvimento', imagem=get_imagem_default(self.imagensCategorias[2]), criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! Categorias criadas.')
            print('Verificando departamentos...')
            if Departamento.objects.count() == 0:
                Departamento.objects.bulk_create([
                    Departamento(nome='Cobrança', criado_por_id=1, modificado_por_id=1),
                    Departamento(nome='Relacionamento', criado_por_id=1, modificado_por_id=1),
                    Departamento(nome='Leitura', criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! Departamentos criados.')
            print('Verificando setores...')
            if Setor.objects.count() == 0:
                Setor.objects.bulk_create([
                    Setor(nome='Corporativo', criado_por_id=1, modificado_por_id=1),
                    Setor(nome='Distribuidora', criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! Setores criados.')
            print('Verificando equipes...')
            if Equipe.objects.count() == 0:
                Equipe.objects.bulk_create([
                    Equipe(nome='Sem Equipe', criado_por_id=1, modificado_por_id=1),
                    Equipe(nome='COB00001', criado_por_id=1, modificado_por_id=1),
                    Equipe(nome='COB00002', criado_por_id=1, modificado_por_id=1),
                    Equipe(nome='COB00003', criado_por_id=1, modificado_por_id=1),
                    Equipe(nome='COB00004', criado_por_id=1, modificado_por_id=1),
                    Equipe(nome='COB00005', criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! Equipes criados.')
            print('Verificando tipos de material...')
            if TipoMaterial.objects.count() == 0:
                TipoMaterial.objects.bulk_create([
                    TipoMaterial(nome='Apostila', criado_por_id=1, modificado_por_id=1),
                    TipoMaterial(nome='Livro', criado_por_id=1, modificado_por_id=1),
                    TipoMaterial(nome='Áudio', criado_por_id=1, modificado_por_id=1),
                    TipoMaterial(nome='Apresentação', criado_por_id=1, modificado_por_id=1),
                    TipoMaterial(nome='Vídeo', criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! Tipos de material criadas.')
            print('Verificando cursos...')
            if Curso.objects.count() == 0:
                Curso.objects.bulk_create([
                    Curso(
                        empresa_id=1,
                        categoria_id=1, nome='Jujutsu Kaisen OP',
                        descricao='Kaikai Kitan / Eve - Guitar Cover',
                        imagem=get_imagem_default(self.imagensIniciais[0]),
                        url='https://www.youtube.com/watch?v=Sqa7HeEAFzQ', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1, nome='MAGIC! - No Way No',
                        descricao='(Official Music Video)',
                        imagem=get_imagem_default(self.imagensIniciais[1]),
                        url='https://www.youtube.com/watch?v=HdobynnfKQE', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1, nome='Daily Exercises App',
                        descricao='Flutter UI - Speed Code',
                        imagem=get_imagem_default(self.imagensIniciais[2]),
                        url='https://www.youtube.com/watch?v=qQ75cxc5q8o', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1,
                        nome='Create a Twitter Clone with Vue.js, Quasar & Firebase',
                        descricao='Learn how to create a beautiful, responsive, cross-platform Twitter app from SCRATCH and get it running and working on 5 different platforms',
                        imagem=get_imagem_default(self.imagensIniciais[3]),
                        url='https://www.youtube.com/watch?v=la-0ulfn0_M', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1, nome='Quasar Framework 10 - Geolocalização',
                        descricao='Como integrar de maneira simples a web API de geolocalização em nosso projeto com quasar framework.',
                        imagem=get_imagem_default(self.imagensIniciais[4]),
                        url='https://www.youtube.com/watch?v=Tcl07a_HQP4', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1,
                        nome='Vuejs - Quasar Framework UI Design, Admin Dashboard',
                        descricao='In this tutorial well learn How to design a Modern Admin  Dashboard Upload file application ( web design ) using Quasar Framework and  vuejs 2 , material design icons, Font Awsome icons.',
                        imagem=get_imagem_default(self.imagensIniciais[5]),
                        url='https://www.youtube.com/watch?v=le4f8qblaW8', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1,
                        nome='Create an Instagram Clone with Vue JS, Quasar & Firebase',
                        descricao='in 4 HOURS! 6 aulas',
                        imagem=get_imagem_default(self.imagensIniciais[6]),
                        url='https://www.youtube.com/watch?v=9tyFBchdb00&list=PLAiDzIdBfy8h6HgfQg3namagsCUT0Y2Bs',
                        criado_por_id=1, modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1, nome='Plant App', descricao='Flutter UI - Speed Code',
                        imagem=get_imagem_default(self.imagensIniciais[7]),
                        url='https://www.youtube.com/watch?v=LN668OAUrK4&t=22s', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1, nome='Chat/Messaging App Light and Dark Theme',
                        descricao='Flutter UI - Speed Code',
                        imagem=get_imagem_default(self.imagensIniciais[8]),
                        url='https://www.youtube.com/watch?v=uiJF-ShOLyo&t=1s', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=1, nome='Quiz App',
                        descricao='Flutter Complete App - Speed Code',
                        imagem=get_imagem_default(self.imagensIniciais[9]),
                        url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1,
                        modificado_por_id=1),
                    Curso(
                        empresa_id=1,
                        categoria_id=5,
                        nome='Quasar Framework Cross-Platform Vue JS Vuex & Firebase Apps',
                        descricao='''In this course I’ll show you how to use Quasar Framework (along with Vue JS 2, Vuex & Firebase) to create real-world, cross-platforms apps using a single Vue JS codebase; and get these apps production-ready and deployed to all the major platforms - Web, iOS, Android, Mac & Windows.

Throughout this course we'll create a real-world app called Awesome Todo. In this app we can add, edit or delete tasks and mark them as completed. 

We can also sort tasks by name or date and search through tasks using a search bar.

It's also going to have a Settings page, with 2 real settings which change the way the app works - and which persist when app is closed and restarted (or the browser reloaded on the web version). It will also have a help page, a "visit our website" link and an "email us" link.

The app will have its own back-end created using a Firebase Realtime Database. Users can register, log in and see their data sync in realtime across all of their devices.

We'll get the app production ready for all the different platforms - web, iOS, Android, Mac & Windows.

You'll learn all of the basics of Quasar Framework, including the Quasar CLI, Quasar Components, Quasar Plugins, Quasar Directives, Platform Detection, Layouts, Theming & various Quasar Utilities.

I'll also show you all of the basics of Vue.js, including Data Binding, Events, Computed Properties, Components, Directives, Filters, Lists & Lifecycle Hooks.

You'll learn how to manage the state of your app using Vuex, where I'll cover State, Mutations, Actions & Setters.

I'll cover all of the basics of Firebase, including Authentication, Reading data, Writing data & protecting your data with Database Rules.

By the end of this course, you will be able to create your own real-world apps, with real back-ends which work on all the different platforms.''',
                        imagem=get_imagem_default(self.imagensIniciais[10]),
                        url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1,
                        modificado_por_id=1), ])
                print('Pronto! cursos criados.')
            print('Verificando materiais...')
            if Material.objects.count() == 0:
                Material.objects.bulk_create([
                    Material(empresa_id=1, curso_id=1, tipo_id=2, nome='Todo Esse Tempo', informativo=True,
                             conteudo='https://drive.google.com/viewerng/viewer?url=http://ler-agora.jegueajato.com/Rachael+Lippincott/Todo+Esse+Tempo+(312)/Todo+Esse+Tempo+-+Rachael+Lippincott?chave%3D1677cfea7cb1b4e721f78316a481fd9c&dsl=',
                             criado_por_id=1, modificado_por_id=1),
                    Material(empresa_id=1, curso_id=2, tipo_id=2, nome='O Garoto do Fundo da Sala', informativo=True,
                             conteudo='https://drive.google.com/viewerng/viewer?url=http://ler-agora.jegueajato.com/Onjali+Q+Rauf/O+Garoto+do+Fundo+da+Sala+(303)/O+Garoto+do+Fundo+da+Sala+-+Onjali+Q+Rauf?chave%3D1677cfea7cb1b4e721f78316a48',
                             criado_por_id=1, modificado_por_id=1),
                    Material(empresa_id=1, curso_id=3, tipo_id=2, nome='Como Evitar um Desastre Climático – Bill Gates', informativo=True,
                             conteudo='https://drive.google.com/viewerng/viewer?url=http://ler-agora.jegueajato.com/Bill+Gates/Como+Evitar+Um+Desastre+Climatico+(304)/Como+Evitar+Um+Desastre+Climati+-+Bill+Gates?chave%3D1677cfea7cb1b4e721f',
                             criado_por_id=1, modificado_por_id=1),
                    Material(empresa_id=1, curso_id=4, tipo_id=2, nome='Ideias Para Adiar o Fim do Mundo – Ailton Krenak', informativo=True,
                             conteudo='https://drive.google.com/viewerng/viewer?url=http://ler-agora.jegueajato.com/Ailton+Krenak/Ideias+para+adiar+o+fim+do+mundo+(118)/Ideias+para+adiar+o+fim+do+mund+-+Ailton+Krenak?chave%3D1677cfea7cb1b4',
                             criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! Material criados.')

            print('Verificando tópicos...')
            if Topico.objects.count() == 0:
                Topico.objects.bulk_create([
                    Topico(nome='Introduction', numero=1, curso_id=11, criado_por_id=1, modificado_por_id=1),
                    Topico(nome='Getting started', numero=2, curso_id=11, criado_por_id=1, modificado_por_id=1),
                    Topico(nome='Vue.js Basics', numero=3, curso_id=11, criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! tópicos criados.')

            print('Verificando aulas...')
            if Aula.objects.count() == 0:
                Aula.objects.bulk_create([
                    Aula(topico_id=1, numero=1, titulo='Introduction & Course App Awesome Todo',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=1, numero=2, titulo='What is Quasar',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=1, numero=3, titulo='What is Vue.js',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=1, titulo='Module Introduction',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=2, titulo='Install Node.js and Quasar CLI',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=3, titulo='Create & launch a new Quasar Project in the Browser',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=4, titulo='Auto-import Components & Directives',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=5, titulo='Folder structure - Layouts, Pages, Routes & more',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=3, numero=1, titulo='Module Introduction',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=2, titulo='Anatomy of a Vue Single File Component',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=3, titulo='Binding Data to the View',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=4, titulo='Two-way Data Binding with v-model',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=5, titulo='Events & Methods - Click',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=6, titulo='Events - Keyboard & more',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=7, titulo='Showing and Hiding Elements - v-show',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=8, titulo='Conditional Rendering - v-if & v-else',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=9, titulo='Computed Properties',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=10, titulo='Filters', url='https://www.youtube.com/watch?v=Nhy0VWAMsFU',
                         criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=11, titulo='Directives', url='https://www.youtube.com/watch?v=Nhy0VWAMsFU',
                         criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=12, titulo='Binding to Attributes & CSS',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=13, titulo='Lifecycle Hooks - Introduction',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=14, titulo='Lifecycle Hooks - In Action',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=15, titulo='Refs', url='https://www.youtube.com/watch?v=Nhy0VWAMsFU',
                         criado_por_id=1, modificado_por_id=1),
                    Aula(topico_id=2, numero=16, titulo='Practise Vue.js Basics',
                         url='https://www.youtube.com/watch?v=Nhy0VWAMsFU', criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! aulas criados.')

            print('Verificando Matriculas...')
            if Matricula.objects.count() == 0:
                curso = Curso.objects.get(pk=11)
                Matricula.objects.bulk_create([
                    Matricula(usuario_id=1, curso_id=11, criado_por_id=1, modificado_por_id=1, descricao=curso.nome),
                    Matricula(usuario_id=2, curso_id=11, criado_por_id=2, modificado_por_id=1, descricao=curso.nome),
                    Matricula(usuario_id=3, curso_id=11, criado_por_id=3, modificado_por_id=1, descricao=curso.nome),
                    Matricula(usuario_id=4, curso_id=11, criado_por_id=4, modificado_por_id=1, descricao=curso.nome),
                ])
                print('Pronto! matriculas criadas.')

            print('Verificando Questionário...')
            if Questionario.objects.count() == 0:
                Questionario.objects.bulk_create([
                    Questionario(curso_id=11, criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! Questionário criados.')

            print('Verificando Perguntas...')
            if Pergunta.objects.count() == 0:
                Pergunta.objects.bulk_create([
                    Pergunta(texto='O que é Quasar?', criado_por_id=1, modificado_por_id=1),
                    Pergunta(texto='O Quasar é baseado em?', criado_por_id=1, modificado_por_id=1),
                    Pergunta(texto='Consigo utilizar o Quasar para desenvolver Apps para Android/IOS?', criado_por_id=1,
                             modificado_por_id=1),
                    Pergunta(texto='Consigo utilizar o Quasar para desenvolver sistemas Desktop?', criado_por_id=1,
                             modificado_por_id=1),
                ])
                print('Pronto! perguntas criadas.')

            print('Verificando Respostas...')
            if Resposta.objects.count() == 0:
                Resposta.objects.bulk_create([
                    Resposta(pergunta_id=1, resposta='Perfume', criado_por_id=1, modificado_por_id=1),
                    Resposta(pergunta_id=1, resposta='Desodorante', criado_por_id=1, modificado_por_id=1),
                    Resposta(pergunta_id=1, resposta='Marca de Roupa', criado_por_id=1, modificado_por_id=1),
                    Resposta(pergunta_id=1, resposta='Framework', e_correta=True, criado_por_id=1, modificado_por_id=1),

                    Resposta(pergunta_id=2, resposta='Java', criado_por_id=1, modificado_por_id=1),
                    Resposta(pergunta_id=2, resposta='Angular', criado_por_id=1, modificado_por_id=1),
                    Resposta(pergunta_id=2, resposta='Goland', criado_por_id=1, modificado_por_id=1),
                    Resposta(pergunta_id=2, resposta='Vue.js', e_correta=True, criado_por_id=1, modificado_por_id=1),

                    Resposta(pergunta_id=3, resposta='Sim', e_correta=True, criado_por_id=1, modificado_por_id=1),
                    Resposta(pergunta_id=3, resposta='Nao', criado_por_id=1, modificado_por_id=1),

                    Resposta(pergunta_id=4, resposta='Nao', criado_por_id=1, modificado_por_id=1),
                    Resposta(pergunta_id=4, resposta='Sim', e_correta=True, criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! respostas criadas.')

            print('Verificando Mapeamento de perguntas do questionário...')
            if QuestionarioXPergunta.objects.count() == 0:
                QuestionarioXPergunta.objects.bulk_create([
                    QuestionarioXPergunta(questionario_id=1, pergunta_id=1, criado_por_id=1, modificado_por_id=1),
                    QuestionarioXPergunta(questionario_id=1, pergunta_id=2, criado_por_id=1, modificado_por_id=1),
                    QuestionarioXPergunta(questionario_id=1, pergunta_id=3, criado_por_id=1, modificado_por_id=1),
                    QuestionarioXPergunta(questionario_id=1, pergunta_id=4, criado_por_id=1, modificado_por_id=1),
                ])
                print('Pronto! Mapeamento de perguntas do questionário criados.')

            print('Verificando Provas...')
            if Prova.objects.count() == 0:
                Prova.objects.bulk_create([
                    Prova(matricula_id=1, questionario_id=1, criado_por_id=1, modificado_por_id=1, curso_id=11),
                    Prova(matricula_id=2, questionario_id=1, criado_por_id=2, modificado_por_id=1, curso_id=11),
                    Prova(matricula_id=3, questionario_id=1, criado_por_id=3, modificado_por_id=1, curso_id=11),
                    Prova(matricula_id=4, questionario_id=1, criado_por_id=4, modificado_por_id=1, curso_id=11),
                ])
                print('Pronto! Provas criadas.')

        except Exception as ex:
            print('Erro! Ao carregar de dados iniciais.')
            print(ex)
