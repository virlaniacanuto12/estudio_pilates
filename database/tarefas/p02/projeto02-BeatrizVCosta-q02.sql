-- Inserir endereço
INSERT INTO endereco (rua, numero, cep, bairro, cidade)
VALUES ('Rua das Flores', 123, '59000-000', 'Centro', 'Natal')
RETURNING id;

-- Suponha que o id retornado foi 1

-- Inserir pessoa (funcionário)
INSERT INTO pessoa (cpf, rg, nome, telefone, email, data_nascimento, status, endereco_id)
VALUES ('12345678901', 'MG1234567', 'Carlos Silva', '99999-9999', 'carlos@email.com', '1980-05-15', TRUE, 1);

-- Inserir funcionário
INSERT INTO funcionario (cpf, funcao, salario, carga_horaria, login, senha_hash, is_admin)
VALUES ('12345678901', 'Instrutor de Pilates', 3500.00, 40, 'carloss', 'hashdaSenha', FALSE);

-- Inserir agendamento
INSERT INTO agendamento (data, horario, local, vagas_totais, vagas_disponiveis, instrutor_cpf)
VALUES (CURRENT_DATE, '18:00', 'Sala 1', 10, 10, '12345678901')
RETURNING codigo;

-- Suponha que o codigo retornado foi 1

-- Inserir aulas ligadas ao agendamento
INSERT INTO aula (agendamento_codigo, data, frequencia)
VALUES (1, CURRENT_DATE, TRUE),
       (1, CURRENT_DATE - INTERVAL '5 days', TRUE),
       (1, CURRENT_DATE - INTERVAL '10 days', FALSE);  -- aula sem frequência

