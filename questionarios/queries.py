def get_provas_alunos():
    return '''
                SELECT a.id, c.id as id_prova, b.username as login, a.nome, c.finalizado, c.curso_id, d.nome as curso,
                a.empresa_id, f.nome as empresa_nome, sum(CASE e_correta WHEN true THEN 1	ELSE 0 END) acertos
                
                FROM alunos_aluno a
                left join auth_user b on a.usuario_id=b.id
                left join questionarios_prova c on a.usuario_id=c.criado_por_id
                left join cursos_curso d on c.curso_id=d.id
                left join questionarios_avaliacao e on a.usuario_id=e.criado_por_id and c.curso_id=e.curso_id
                left join empresas_empresa f on a.empresa_id = f.id
                
                -- where a.id > 6
                
                group by a.id, c.id, b.username, a.nome, c.finalizado, c.curso_id, d.nome, a.empresa_id, f.nome
            '''
