-- Consulta alunos que nunca participaram de uma aula desde que contrataram o plano(Aluno fantasma);
SELECT p.nome AS aluno, a.data_inicio_plano
FROM aluno a
JOIN pessoa p ON a.cpf = p.cpf
LEFT JOIN aula_aluno aa ON a.cpf = aa.aluno_cpf
WHERE aa.aluno_cpf IS NULL;
