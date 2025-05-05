--Consultar pagamentos realizados por aluno, com status e valores

SELECT 
    p.nome,
    a.cpf,
    cr.codigo AS conta_receber_codigo,
    cr.valor AS valor_total,
    cr.vencimento,
    cr.status AS status_conta,
    pg.data AS data_pagamento,
    pg.metodo,
    pg.valor AS valor_pago,
    pg.status AS status_pagamento
FROM 
    ALUNO a
JOIN 
    PESSOA p ON a.cpf = p.cpf
JOIN 
    CONTA_RECEBER cr ON cr.aluno_cpf = a.cpf
LEFT JOIN 
    PAGAMENTO pg ON pg.conta_receber_codigo = cr.codigo
ORDER BY 
    p.nome, cr.vencimento DESC;
