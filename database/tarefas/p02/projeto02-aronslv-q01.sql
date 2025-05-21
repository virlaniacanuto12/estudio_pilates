-- Issue: #53
-- Função 1: Retorna o nome do plano com maior número de alunos vinculados
CREATE OR REPLACE FUNCTION fn_plano_mais_popular()
RETURNS VARCHAR AS $$
DECLARE
    v_nome_plano VARCHAR;
BEGIN
    SELECT sp.nome
    INTO v_nome_plano
    FROM studio_plano sp
    JOIN studio_aluno sa ON sa.plano_id = sp.id 
    GROUP BY sp.id, sp.nome
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    RETURN v_nome_plano;
END;
$$ LANGUAGE plpgsql;
