-- Issue: #56
-- Função 1: Calcula o valor total de um plano multiplicando qtd_aulas pelo valor_aula.
CREATE OR REPLACE FUNCTION fn_calcular_valor_cheio_plano(p_plano_codigo INT)
RETURNS NUMERIC AS
$$
DECLARE
    v_valor_total NUMERIC;
BEGIN
    SELECT sp.qtd_aulas * sp.valor_aula
      INTO v_valor_total
      FROM studio_plano AS sp
     WHERE sp.codigo = p_plano_codigo;

    RETURN v_valor_total;
END;
$$ LANGUAGE plpgsql;

