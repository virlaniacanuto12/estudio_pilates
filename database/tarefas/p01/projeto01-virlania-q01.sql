--Mostra quantidade de aulas ministradas por funcionário

WITH aulas_ministradas AS (
    SELECT 
        a.instrutor_cpf AS cpf,
        COUNT(*) AS num_aulas_ministradas
    FROM agendamento a
    GROUP BY a.instrutor_cpf
)
SELECT 
    p.nome,
    p.cpf,
    am.num_aulas_ministradas
FROM aulas_ministradas am
JOIN pessoa p ON am.cpf = p.cpf
ORDER BY am.num_aulas_ministradas DESC;




