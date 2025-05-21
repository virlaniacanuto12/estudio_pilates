-- Issue: #54
-- Função 1: Cria uma função que retorna o tempo restante do plano de um  aluno especifico
CREATE OR REPLACE FUNCTION tempo_restante_plano(cpf_aluno TEXT)
RETURNS INTEGER AS $$
DECLARE
    data_venc DATE;
    dias_restantes INTEGER;
BEGIN
    -- Buscar a data de vencimento do plano do aluno
    SELECT pl.limite_vigencia
    INTO data_venc
    FROM aluno al
    JOIN plano pl ON al.plano_codigo = pl.codigo
    WHERE al.cpf = cpf_aluno;

    -- Se o aluno não tiver plano registrado, retorna 0
    IF data_venc IS NULL THEN
        RETURN 0;
    END IF;

    -- Calcula dias restantes (impede valor negativo)
    dias_restantes := GREATEST(0, data_venc - CURRENT_DATE);

    RETURN dias_restantes;
END;
$$ LANGUAGE plpgsql;
