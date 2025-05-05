--Listar funcionários, suas funções, horários e permissões

SELECT 
    p.nome,
    f.cpf,
    f.funcao,
    f.salario,
    f.carga_horaria,
    f.is_admin,
    fh.horario,
    fp.permissao
FROM 
    FUNCIONARIO f
JOIN 
    PESSOA p ON f.cpf = p.cpf
LEFT JOIN 
    FUNCIONARIO_HORARIOS fh ON f.cpf = fh.funcionario_cpf
LEFT JOIN 
    FUNCIONARIO_PERMISSOES fp ON f.cpf = fp.funcionario_cpf
ORDER BY 
    p.nome;

