--Localizar alunos por bairro 

SELECT e.bairro,
       COUNT(*) AS alunos_bairro
FROM endereco e
JOIN pessoa p ON p.endereco_id = e.id
GROUP BY e.bairro

