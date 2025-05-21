-- Issue: #55
-- Procedimento 2: Atualiza o campo is_admin para TRUE de um funcionario
CREATE OR REPLACE PROCEDURE tornar_funcionario_admin(p_cpf VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM funcionario WHERE cpf = p_cpf) THEN
        RAISE EXCEPTION 'Funcionário com CPF % não encontrado.', p_cpf;
    END IF;

    UPDATE funcionario
    SET is_admin = TRUE
    WHERE cpf = p_cpf;

    RAISE NOTICE 'Funcionário com CPF % agora é administrador.', p_cpf;
END;
$$;