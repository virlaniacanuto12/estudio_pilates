-- Issue: #14
-- Consulta 1.1: Lista de alunos vinculados aos planos

SELECT
  p.nome AS nome_aluno,
  pl.nome AS nome_plano,
  a.data_inicio_plano
FROM
  aluno a
  INNER JOIN plano pl ON a.plano_codigo = pl.codigo
  INNER JOIN pessoa p ON a.cpf = p.cpf
WHERE
  a.plano_codigo IS NOT NULL
ORDER BY
  p.nome;