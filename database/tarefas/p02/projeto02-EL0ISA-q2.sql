-- Issue: #55
-- Função 2: Retorna TRUE se aluno está dentro do limite, senão FALSE
CREATE OR REPLACE FUNCTION verificar_limite_aulas(cpf_aluno VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    aulas_frequentadas INTEGER;
    limite_aulas INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO aulas_frequentadas
    FROM aula_aluno aa
    JOIN aula a ON aa.aula_codigo = a.codigo
    WHERE aa.aluno_cpf = cpf_aluno
      AND a.frequencia = TRUE;

    SELECT p.qtd_aulas
    INTO limite_aulas
    FROM aluno al
    JOIN plano p ON al.plano_codigo = p.codigo
    WHERE al.cpf = cpf_aluno;

    RETURN aulas_frequentadas < limite_aulas;
END;
$$ LANGUAGE plpgsql;
