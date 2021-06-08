def get_notificacoes():
    return '''
        select a.* from (
        select a.id,
        a.mensagem,
        (c.first_name || ' ' || c.last_name) criado_por_nome,
        b.is_empresa,
        b.is_curso,
        b.is_usuario,
        a.criado_em,
        case when a.imagem <> '' then true else false end possui_imagem
        from notificacoes_notificacao a
        inner join notificacoes_notificacaodestinatario b ON b.notificacao_id = a.id
        inner join auth_user c on a.criado_por_id = c.id
        where a.criado_em >= current_date - 30
        and (
            b.destinario_id = %s
            or b.curso_id in (
                select id from cursos_matricula cm where cm.usuario_id = %s
            )
            or b.empresa_id = (select empresa_id from alunos_aluno aa where aa.usuario_id = %s)
        )
        ) a
    '''

def get_notificacoes_filter():
    return '''
        select a.* from (
        select a.id,
        a.mensagem,
        (c.first_name || ' ' || c.last_name) criado_por_nome,
        b.is_empresa,
        b.is_curso,
        b.is_usuario,
        a.criado_em,
        case when a.imagem <> '' then true else false end possui_imagem
        from notificacoes_notificacao a
        inner join notificacoes_notificacaodestinatario b ON b.notificacao_id = a.id
        inner join auth_user c on a.criado_por_id = c.id
        where a.criado_em >= current_date - 30
        and (
            b.destinario_id = %s
            or b.curso_id in (
                select id from cursos_matricula cm where cm.usuario_id = %s
            )
            or b.empresa_id = (select empresa_id from alunos_aluno aa where aa.usuario_id = %s)
        )
        and lower(a.mensagem) like %s
        ) a
    '''