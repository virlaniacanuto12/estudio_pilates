-- Issue: #14
-- Consulta 1.2: Receita gerada pelos planos

WITH receita_por_plano AS (
  SELECT
    al.plano_codigo,
    SUM(pg.valor) AS receita_total
  FROM
    pagamento pg
    INNER JOIN conta_receber cr ON pg.conta_receber_codigo = cr.codigo
    INNER JOIN aluno al ON cr.aluno_cpf = al.cpf
  GROUP BY
    al.plano_codigo
)
SELECT
  pl.nome AS nome_plano,
  COALESCE(rpp.receita_total, 0) AS receita_gerada
FROM
  plano pl
  LEFT JOIN receita_por_plano rpp ON pl.codigo = rpp.plano_codigo
ORDER BY
  receita_gerada DESC;