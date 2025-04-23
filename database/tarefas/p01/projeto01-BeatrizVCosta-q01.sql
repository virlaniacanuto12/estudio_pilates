-- Consultar relatório de ocupação das aulas (quantidade de alunos por aula)

SELECT 
    a.codigo AS aula_codigo,
    ag.data,
    ag.horario,
    ag.local,
    COUNT(aa.aluno_cpf) AS total_alunos
FROM aula a
JOIN agendamento ag ON a.agendamento_codigo = ag.codigo
LEFT JOIN aula_aluno aa ON a.codigo = aa.aula_codigo
GROUP BY a.codigo, ag.data, ag.horario, ag.local;
