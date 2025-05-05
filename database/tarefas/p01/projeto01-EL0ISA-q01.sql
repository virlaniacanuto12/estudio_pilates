-- Consulta: As contas que vencer no mes atual que ainda não foram pagas ou que estão atrasadas
SELECT cr.codigo, cr.aluno_cpf, cr.valor, cr.vencimento
FROM conta_receber cr
LEFT JOIN pagamento p ON cr.codigo = p.conta_receber_codigo AND p.status = TRUE
WHERE 
  (
    (cr.vencimento >= date_trunc('month', current_date) 
     AND cr.vencimento < date_trunc('month', current_date) + interval '1 month')
    AND p.conta_receber_codigo IS NULL
  )
  OR
  (
    (cr.vencimento < current_date)
    AND p.conta_receber_codigo IS NULL
  );