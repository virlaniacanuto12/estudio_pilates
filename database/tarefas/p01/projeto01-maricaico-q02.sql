Listar os alunos e o quantidade de aulas que eles participaram.

WITH aulas_por_aluno AS (
    SELECT 
        aluno_cpf,
        COUNT(aula_codigo) AS qtd_aulas
    FROM aula_aluno
    GROUP BY aluno_cpf
)

SELECT 
    p.nome AS nome_aluno,
    COALESCE(apa.qtd_aulas, 0) AS quantidade_aulas
FROM aluno a
INNER JOIN pessoa p ON a.cpf = p.cpf
LEFT JOIN aulas_por_aluno apa ON a.cpf = apa.aluno_cpf
ORDER BY quantidade_aulas DESC;
