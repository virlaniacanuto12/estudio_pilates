-- Issue: #54
-- Função 2: Cria uma função que exibe os instrutores que ministraram mais aulas no mês
DROP FUNCTION IF EXISTS top_professores_mes_atual();

CREATE OR REPLACE FUNCTION top_professores_mes_atual()
RETURNS TABLE (
    nome_professor VARCHAR(100),
    total_aulas INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.nome,
        COUNT(a.codigo)::INTEGER AS total_aulas
    FROM aula a
    JOIN agendamento ag ON a.agendamento_codigo = ag.codigo
    JOIN funcionario f ON ag.instrutor_cpf = f.cpf
    JOIN pessoa p ON f.cpf = p.cpf
    WHERE date_trunc('month', a.data) = date_trunc('month', CURRENT_DATE)
    GROUP BY p.nome
    ORDER BY total_aulas DESC
    LIMIT 3;
END;
$$ LANGUAGE plpgsql;
