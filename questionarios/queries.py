def get_provas_alunos():
    return '''
                SELECT a.id, c.id as id_prova, username as login, a.nome, c.finalizado, c.curso_id, d.nome as curso, 
                a.empresa_id, f.nome as empresa_nome, b.is_active as e_ativo, sum(CASE e_correta WHEN true THEN 1 ELSE 0 END) acertos 
                
                FROM public.alunos_aluno a 
                left join public.auth_user b on a.usuario_id=b.id 
                left join public.questionarios_prova c on a.usuario_id=c.criado_por_id
                left join public.cursos_curso d on c.curso_id=d.id
                left join public.questionarios_avaliacao e on a.usuario_id=e.criado_por_id and c.curso_id=e.curso_id
                left join public.empresas_empresa f on a.empresa_id = f.id

                WHERE a.id > 6
                and b.is_active=true
                
                GROUP BY a.id, c.id, username, a.nome, c.finalizado, c.curso_id, d.nome, a.empresa_id, f.nome, b.is_active
            '''
