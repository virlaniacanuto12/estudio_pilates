-- Issue: #55
-- Função 1: Retorna todos os pagamentos de um aluno
CREATE OR REPLACE FUNCTION obter_historico_pagamentos_aluno(p_cpf VARCHAR)
RETURNS TABLE (
    nome_aluno VARCHAR,
    data_pagamento TIMESTAMP,
    valor_pagamento DECIMAL(10,2),
    metodo_pagamento VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        pe.nome,
        pg.data,
        pg.valor,
        pg.metodo
    FROM pagamento pg
    INNER JOIN conta_receber cr ON pg.conta_receber_codigo = cr.codigo
    INNER JOIN aluno al ON cr.aluno_cpf = al.cpf
    INNER JOIN pessoa pe ON al.cpf = pe.cpf
    WHERE al.cpf = p_cpf
    ORDER BY pg.data DESC;
END;
$$ LANGUAGE plpgsql;
