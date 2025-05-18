-- Issue: #52
-- Função 2: Retorna o número de alunos vinculados a um plano
CREATE OR REPLACE FUNCTION quantidade_alunos_plano(plano_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
  qtd INTEGER;
BEGIN
  SELECT COUNT(*)
  INTO qtd
  FROM aluno
  WHERE plano_codigo = plano_id;

  RETURN qtd;
END;
$$ LANGUAGE plpgsql;
