-- Consulta: Dados dos alunos que tem contas atrasadas
SELECT 
  cr.codigo AS codigo_conta,
  p.cpf AS cpf_aluno,
  p.nome AS nome_aluno,
  p.email,
  cr.valor,
  cr.vencimento
FROM conta_receber cr
full JOIN pagamento pag 
  ON cr.codigo = pag.conta_receber_codigo AND pag.status = TRUE
JOIN aluno a 
  ON cr.aluno_cpf = a.cpf
JOIN pessoa p 
  ON a.cpf = p.cpf
WHERE 
  cr.vencimento < CURRENT_DATE
  AND pag.conta_receber_codigo IS NULL
ORDER BY cr.vencimento;
