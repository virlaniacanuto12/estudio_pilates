-- Issue: #52
-- Procedimento 2: Desativa o plano de um aluno e limpa os dados de vínculo
CREATE OR REPLACE PROCEDURE desativa_plano_aluno(cpf_aluno VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE aluno
  SET plano_ativo = FALSE,
      plano_codigo = NULL,
      data_inicio_plano = NULL,
      data_vencimento_plano = NULL
  WHERE cpf = cpf_aluno;
END;
$$;
