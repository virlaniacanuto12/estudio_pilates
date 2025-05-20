-- Issue: #54
-- Procedimento 2: Cria um procedimento que reativa plano de aluno após efetivado o pagamento
CREATE OR REPLACE PROCEDURE reativar_plano_aluno_quitacao()
LANGUAGE plpgsql
AS $$
DECLARE
    aluno_cpf_var VARCHAR(11);
BEGIN
    -- Percorre os alunos com plano inativo
    FOR aluno_cpf_var IN
        SELECT a.cpf
        FROM aluno a
        WHERE a.plano_ativo = FALSE
          AND NOT EXISTS (
              SELECT 1
              FROM conta_receber cr
              WHERE cr.aluno_cpf = a.cpf
                AND cr.status = FALSE  -- ainda não paga
          )
    LOOP
        -- Ativa o plano do aluno
        UPDATE aluno
        SET plano_ativo = TRUE
        WHERE cpf = aluno_cpf_var;

        RAISE NOTICE 'Plano reativado para o aluno: %', aluno_cpf_var;
    END LOOP;
END;
$$;
