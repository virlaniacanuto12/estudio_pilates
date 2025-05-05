Listar os nomes dos alunos e nomes dos seus planos.

SELECT 
    p.nome AS nome_aluno,
    COALESCE(pl.nome, 'Sem Plano') AS nome_plano
FROM aluno a
INNER JOIN pessoa p ON a.cpf = p.cpf
LEFT JOIN plano pl ON a.plano_codigo = pl.codigo;
