-- Issue: #53
-- Função 2: Verifica se um aluno está inadimplente (tem conta vencida e não paga)
CREATE OR REPLACE FUNCTION fn_aluno_inadimplente(p_cpf VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    v_inadimplente BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM studio_contareceber cr
        JOIN studio_aluno sa ON sa.id = cr.aluno_id
        WHERE sa.cpf = p_cpf
          AND cr.status != 'pago'
          AND cr.vencimento < current_date
    ) INTO v_inadimplente;

    RETURN v_inadimplente;
END;
$$ LANGUAGE plpgsql;