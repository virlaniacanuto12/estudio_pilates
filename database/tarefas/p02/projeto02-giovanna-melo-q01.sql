-- Issue: #52
-- Função 1: Cria uma função que retorna a soma de todos os pagamentos de um plano específico
CREATE OR REPLACE FUNCTION calcula_receita_plano(plano_id INTEGER)
RETURNS NUMERIC AS $$
DECLARE
  total NUMERIC;
BEGIN
  SELECT COALESCE(SUM(pg.valor), 0)
  INTO total
  FROM pagamento pg
  JOIN conta_receber cr ON pg.conta_receber_codigo = cr.codigo
  JOIN aluno a ON cr.aluno_cpf = a.cpf
  WHERE a.plano_codigo = plano_id;

  RETURN total;
END;
$$ LANGUAGE plpgsql;
