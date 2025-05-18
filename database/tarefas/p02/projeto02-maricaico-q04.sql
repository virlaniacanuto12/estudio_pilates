-- Issue: #56
-- Procedimento 2: Altera a função e o salário de um funcionário específico.
CREATE OR REPLACE PROCEDURE sp_alterar_funcao_e_salario_funcionario(
    p_funcionario_cpf VARCHAR(14),
    p_nova_funcao VARCHAR(100),
    p_novo_salario DECIMAL(10,4)
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE studio_funcionario
    SET
        funcao = p_nova_funcao,
        salario = p_novo_salario
    WHERE
        cpf = p_funcionario_cpf;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Funcionário com CPF % não encontrado.', p_funcionario_cpf;
    END IF;
END;
$$;