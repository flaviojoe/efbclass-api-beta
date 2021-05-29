import os
import random

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status


def respostaSucesso(serializer_data, mensagem, code_status=status.HTTP_200_OK):
    return {
        'status': 'success',
        'code': code_status,
        'message': mensagem,
        'data': serializer_data
    }


def respostaErro(serializer_data, mensagem, code_status=status.HTTP_400_BAD_REQUEST):
    return {
        'status': 'error',
        'code': code_status,
        'message': mensagem,
        'data': serializer_data
    }


def geradorCPF(com_pontuacao=True):
    def calcula_digito(digs):
        s = 0
        qtd = len(digs)
        for i in range(qtd):
            s += n[i] * (1 + qtd - i)
        res = 11 - s % 11
        if res >= 10: return 0
        return res

    n = [random.randrange(10) for i in range(9)]
    n.append(calcula_digito(n))
    n.append(calcula_digito(n))
    if com_pontuacao:
        return "%d%d%d.%d%d%d.%d%d%d-%d%d" % tuple(n)
    return ("%d%d%d.%d%d%d.%d%d%d-%d%d" % tuple(n)).replace('.', '').replace('-', '')


def usuariosIniciais():
    usuarios = []
    usuarios.append({
        'username': 'diego',
        'email': 'diego@gmail.com',
        'password': '123456789',
        'first_name': 'Diego',
        'last_name': 'Adm',
        'is_active': True,
        'is_admin': True,
        'group': 'Todos',
        'avatar_index': 0
    })
    usuarios.append({
        'username': 'bruno',
        'email': 'bruno@gmail.com',
        'password': '123456789',
        'first_name': 'Bruno',
        'last_name': 'Adm',
        'is_active': True,
        'is_admin': True,
        'group': 'Todos',
        'avatar_index': 1
    })
    usuarios.append({
        'username': 'flavio',
        'email': 'flavio@gmail.com',
        'password': '123456789',
        'first_name': 'Flávio',
        'last_name': 'Adm',
        'is_active': True,
        'is_admin': True,
        'group': 'Todos',
        'avatar_index': 2
    })
    usuarios.append({
        'username': 'aluno',
        'email': 'aluno@gmail.com',
        'password': '123456789',
        'first_name': 'Aluno',
        'last_name': 'Teste',
        'is_active': True,
        'group': 'Aluno',
        'avatar_index': 3
    })
    usuarios.append({
        'username': 'professor',
        'email': 'professor@gmail.com',
        'password': '123456789',
        'first_name': 'Professor',
        'last_name': 'Teste',
        'is_active': True,
        'group': 'Instrutor',
        'avatar_index': 4
    })
    usuarios.append({
        'username': 'administrativo',
        'email': 'administrativo@gmail.com',
        'password': '123456789',
        'first_name': 'Administrativo',
        'last_name': 'Teste',
        'is_active': True,
        'group': 'Administrativo',
        'avatar_index': 5
    })
    return usuarios


def avataresIniciais():
    imagens = []
    path = os.path.join(settings.BASE_DIR, "avatares")
    imagens.append({
        'name': 'avatar1.png',
        'content_path': os.path.join(path, 'avatar1.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'avatar2.png',
        'content_path': os.path.join(path, 'avatar2.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'avatar3.png',
        'content_path': os.path.join(path, 'avatar3.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'avatar4.png',
        'content_path': os.path.join(path, 'avatar4.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'avatar5.png',
        'content_path': os.path.join(path, 'avatar5.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'avatar6.png',
        'content_path': os.path.join(path, 'avatar6.png'),
        'content_type': 'image/png'
    })
    return imagens


def imagensIniciais():
    imagens = []
    path = os.path.join(settings.BASE_DIR, 'avatares')
    imagens.append({
        'name': 'jujutsu.png',
        'content_path': os.path.join(path, 'jujutsu.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'magic_no_way_no.png',
        'content_path': os.path.join(path, 'magic_no_way_no.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'Daily Exercises App.png',
        'content_path': os.path.join(path, 'Daily Exercises App.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'quasar_4.png',
        'content_path': os.path.join(path, 'quasar_4.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'quasar_1.png',
        'content_path': os.path.join(path, 'quasar_1.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'quasar_3.jpg',
        'content_path': os.path.join(path, 'quasar_3.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'quasar_2.jpg',
        'content_path': os.path.join(path, 'quasar_2.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'Plant App.png',
        'content_path': os.path.join(path, 'Plant App.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'ChatMessagingApp.png',
        'content_path': os.path.join(path, 'ChatMessagingApp.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'quizapp.png',
        'content_path': os.path.join(path, 'quizapp.png'),
        'content_type': 'image/png'
    })
    imagens.append({
        'name': 'quasar_5.png',
        'content_path': os.path.join(path, 'quasar_5.png'),
        'content_type': 'image/png'
    })
    return imagens


def imagensCategorias():
    imagens = []
    path = os.path.join(settings.BASE_DIR, 'avatares', 'categorias')
    arquivos = [
        'atendimento.jpg',
        'cadastro.jpg',
        'desenvolvimento.jpg',
        'leitura.jpg',
        'negociador.jpg'
    ]

    for arquivo in arquivos:
        imagens.append({
            'name': arquivo,
            'content_path': os.path.join(path, arquivo),
            'content_type': 'image/jpg'
        })

    return imagens


def get_imagem_default(alvo):
    return SimpleUploadedFile(
        name=alvo.get('name'),
        content=open(alvo.get('content_path'), 'rb').read(),
        content_type=alvo.get('content_type'))
