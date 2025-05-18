-- Issue: #56
-- Função 2: Retorna a data de vencimento do plano de um aluno específico, dado seu CPF.
CREATE OR REPLACE FUNCTION fn_calcular_proximo_vencimento_plano(p_aluno_cpf VARCHAR)
RETURNS DATE AS
$$
DECLARE
    v_data_vencimento DATE;
BEGIN
    SELECT sa.data_vencimento_plano
      INTO v_data_vencimento
      FROM studio_aluno AS sa
     WHERE sa.cpf = p_aluno_cpf;

    IF v_data_vencimento IS NULL THEN
        RAISE EXCEPTION 'CPF % não encontrado ou aluno sem plano vigente.', p_aluno_cpf;
    END IF;

    RETURN v_data_vencimento;
END;
$$ LANGUAGE plpgsql;