-- Issue: #55
-- Procedimento 1: Ajustar a quantidade de vagas disponíveis de um agendamento
CREATE OR REPLACE PROCEDURE atualizar_vagas_disponiveis(
    p_agendamento_codigo INTEGER,
    p_delta INTEGER  -- valor positivo para aumentar vagas, negativo para diminuir
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE agendamento
    SET vagas_disponiveis = vagas_disponiveis + p_delta
    WHERE codigo = p_agendamento_codigo
      AND (vagas_disponiveis + p_delta) BETWEEN 0 AND vagas_totais;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Atualização inválida: vagas resultantes fora do limite permitido.';
    END IF;
END;
$$;
