-- Issue: #52
-- Procedimento 1: Registra um novo pagamento e atualiza o status da conta a receber
CREATE OR REPLACE PROCEDURE registrar_pagamento(
  cod_conta INTEGER,
  valor_pago NUMERIC,
  metodo TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO pagamento (conta_receber_codigo, data, metodo, valor, status)
  VALUES (cod_conta, CURRENT_TIMESTAMP, metodo, valor_pago, TRUE);

  UPDATE conta_receber
  SET status = TRUE
  WHERE codigo = cod_conta;
END;
$$;
