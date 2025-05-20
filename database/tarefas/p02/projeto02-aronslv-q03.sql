-- Issue: #53
-- Procedimento 1: Desativa todos os alunos com planos vencidos
CREATE OR REPLACE PROCEDURE sp_desativar_alunos_com_plano_vencido()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE studio_aluno
    SET plano_ativo = FALSE
    WHERE data_vencimento_plano < current_date
      AND plano_ativo = TRUE;
END;
$$;
