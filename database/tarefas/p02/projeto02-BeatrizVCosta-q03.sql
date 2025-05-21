-- Issue: #54
-- Procediemento 1: Cria um procedimento que ajusta a data de vencimento para um dia útil
CREATE OR REPLACE PROCEDURE ajustar_vencimento_para_dia_util(conta_codigo INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    venc DATE;
BEGIN
    SELECT vencimento INTO venc FROM conta_receber WHERE codigo = conta_codigo;

    IF venc IS NULL THEN
        RAISE EXCEPTION 'Conta_receber com código % não encontrada.', conta_codigo;
    END IF;

    -- Ajusta para o próximo dia útil se cair no fim de semana
    IF EXTRACT(DOW FROM venc) = 6 THEN  -- sábado
        venc := venc + 2;
    ELSIF EXTRACT(DOW FROM venc) = 0 THEN  -- domingo
        venc := venc + 1;
    END IF;

    UPDATE conta_receber
    SET vencimento = venc
    WHERE codigo = conta_codigo;

    RAISE NOTICE 'Data de vencimento ajustada para %', venc;
END;
$$;
