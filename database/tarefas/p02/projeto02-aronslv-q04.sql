-- Issue: #53
-- Procedimento 2: Atualiza status de contas para "pago" com base nos pagamentos existentes
CREATE OR REPLACE PROCEDURE sp_sincronizar_pagamentos()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE studio_contareceber cr
    SET status = 'pago'
    FROM studio_pagamento pg
    WHERE pg.conta_id = cr.id;
END;
$$;
