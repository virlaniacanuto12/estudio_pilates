-- Issue: #56
-- Procedimento 1: Registra um novo serviço (modalidade de aula) no estúdio.
CREATE OR REPLACE PROCEDURE sp_registrar_novo_servico(
    p_modalidade VARCHAR(50),
    p_dificuldade VARCHAR(30),
    p_descricao TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_niveis_permitidos VARCHAR(30)[] := ARRAY['Iniciante', 'Intermediário', 'Avançado'];
BEGIN
    IF NOT (p_dificuldade = ANY(v_niveis_permitidos)) THEN
        RAISE EXCEPTION 'Nível de dificuldade inválido: %. Valores permitidos são: %', 
                        p_dificuldade, array_to_string(v_niveis_permitidos, ', ');
    END IF;

    INSERT INTO studio_servico (modalidade, niveis_dificuldade, descricao)
    VALUES (p_modalidade, p_dificuldade, p_descricao);
END;
$$;