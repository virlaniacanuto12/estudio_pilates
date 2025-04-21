-- Inserções na tabela endereco
INSERT INTO endereco (rua, numero, cep, bairro, cidade) VALUES
('Rua A', 101, '12345-678', 'Centro', 'Caicó'),
('Rua B', 102, '23456-789', 'Jardim', 'Jardim de Piranhas'),
('Rua C', 103, '34567-890', 'Vila Nova', 'Caicó'),
('Rua D', 104, '45678-901', 'Centro', 'Jucurutu'),
('Rua E', 105, '56789-012', 'Jardim das Flores', 'Jucurutu'),
('Rua F', 106, '67890-123', 'Vila Bela', 'Caicó'),
('Rua G', 107, '78901-234', 'Centro', 'Caicó'),
('Rua H', 108, '89012-345', 'Jardim das Palmeiras', 'Jucurutu'),
('Rua I', 109, '90123-456', 'Vila Verde', 'Caicó'),
('Rua J', 110, '01234-567', 'Vila Santa', 'Patos');

-- Inserções na tabela pessoa
INSERT INTO pessoa (cpf, rg, nome, telefone, email, data_nascimento, endereco_id) VALUES
('12345678901', '12345678', 'João Silva', '1234-5678', 'joao@email.com', '1990-01-01', 1),
('23456789012', '23456789', 'Maria Souza', '2345-6789', 'maria@email.com', '1985-02-02', 2),
('34567890123', '34567890', 'Pedro Santos', '3456-7890', 'pedro@email.com', '1980-03-03', 3),
('45678901234', '45678901', 'Ana Oliveira', '4567-8901', 'ana@email.com', '1992-04-04', 4),
('56789012345', '56789012', 'Carlos Pereira', '5678-9012', 'carlos@email.com', '1983-05-05', 5),
('67890123456', '67890123', 'Fernanda Costa', '6789-0123', 'fernanda@email.com', '1995-06-06', 6),
('78901234567', '78901234', 'Lucas Almeida', '7890-1234', 'lucas@email.com', '1988-07-07', 7),
('89012345678', '89012345', 'Juliana Lima', '8901-2345', 'juliana@email.com', '1997-08-08', 8),
('90123456789', '90123456', 'Roberto Silva', '9012-3456', 'roberto@email.com', '1982-09-09', 9),
('01234567890', '01234567', 'Tatiane Martins', '0123-4567', 'tatiane@email.com', '1991-10-10', 10);

-- Inserções na tabela plano
INSERT INTO plano (nome, qtd_aulas, valor_aula, status, limite_vigencia) VALUES
('Plano A', 20, 50.00, TRUE, '2025-12-31'),
('Plano B', 30, 40.00, TRUE, '2026-01-01'),
('Plano C', 25, 45.00, TRUE, '2026-06-30'),
('Plano D', 10, 60.00, FALSE, '2025-06-30'),
('Plano E', 40, 35.00, TRUE, '2026-07-31'),
('Plano F', 35, 55.00, TRUE, '2027-12-31'),
('Plano G', 50, 30.00, TRUE, '2027-01-01'),
('Plano H', 20, 70.00, TRUE, '2025-01-01'),
('Plano I', 30, 65.00, FALSE, '2026-12-31'),
('Plano J', 45, 60.00, TRUE, '2026-10-31');

-- Inserções na tabela aluno
INSERT INTO aluno (cpf, profissao, historico_saude, plano_codigo, data_inicio_plano, data_vencimento_plano, plano_ativo, evolucao) VALUES
('12345678901', 'Estudante', 'Nenhuma', 1, '2023-01-01', '2024-01-01', TRUE, 'Progresso excelente'),
('23456789012', 'Professor', 'Nenhuma', 2, '2023-02-01', '2024-02-01', TRUE, 'Progresso bom'),
('34567890123', 'Advogado', 'Nenhuma', 3, '2023-03-01', '2024-03-01', FALSE, 'Progresso médio'),
('45678901234', 'Médica', 'Nenhuma', 4, '2023-04-01', '2024-04-01', TRUE, 'Progresso excelente'),
('56789012345', 'Engenheiro', 'Nenhuma', 5, '2023-05-01', '2024-05-01', TRUE, 'Progresso bom'),
('67890123456', 'Arquiteta', 'Nenhuma', 6, '2023-06-01', '2024-06-01', FALSE, 'Progresso bom'),
('78901234567', 'Designer', 'Nenhuma', 7, '2023-07-01', '2024-07-01', TRUE, 'Progresso excelente'),
('89012345678', 'Chef', 'Nenhuma', 8, '2023-08-01', '2024-08-01', TRUE, 'Progresso bom'),
('90123456789', 'Psicólogo', 'Nenhuma', 9, '2023-09-01', '2024-09-01', FALSE, 'Progresso médio'),
('01234567890', 'Contador', 'Nenhuma', 10, '2023-10-01', '2024-10-01', TRUE, 'Progresso excelente');

-- Inserções na tabela funcionario
INSERT INTO funcionario (cpf, funcao, salario, carga_horaria, login, senha_hash, is_admin, ultimo_acesso) VALUES
('12345678901', 'Instrutor', 2500.00, 40, 'joao_silva', 'senha_hash_1', TRUE, '2023-01-01 08:00:00'),
('23456789012', 'Recepcionista', 1500.00, 30, 'maria_souza', 'senha_hash_2', FALSE, '2023-02-01 09:00:00'),
('34567890123', 'Coordenador', 3500.00, 40, 'pedro_santos', 'senha_hash_3', TRUE, '2023-03-01 10:00:00'),
('45678901234', 'Instrutor', 2800.00, 35, 'ana_oliveira', 'senha_hash_4', FALSE, '2023-04-01 08:30:00'),
('56789012345', 'Gestor', 5000.00, 40, 'carlos_pereira', 'senha_hash_5', TRUE, '2023-05-01 10:30:00'),
('67890123456', 'Instrutor', 2700.00, 40, 'fernanda_costa', 'senha_hash_6', FALSE, '2023-06-01 07:30:00'),
('78901234567', 'Assistente', 1800.00, 30, 'lucas_almeida', 'senha_hash_7', TRUE, '2023-07-01 09:00:00'),
('89012345678', 'Recepcionista', 1600.00, 30, 'juliana_lima', 'senha_hash_8', FALSE, '2023-08-01 08:30:00'),
('90123456789', 'Gestor', 5200.00, 40, 'roberto_silva', 'senha_hash_9', TRUE, '2023-09-01 09:15:00'),
('01234567890', 'Instrutor', 2600.00, 35, 'tatiane_martins', 'senha_hash_10', FALSE, '2023-10-01 08:45:00');

-- Inserções na tabela funcionario_horarios
INSERT INTO funcionario_horarios (funcionario_cpf, horario) VALUES
('12345678901', '08:00-12:00'),
('23456789012', '09:00-13:00'),
('34567890123', '10:00-14:00'),
('45678901234', '08:30-12:30'),
('56789012345', '09:30-13:30'),
('67890123456', '07:00-11:00'),
('78901234567', '09:00-13:00'),
('89012345678', '08:30-12:30'),
('90123456789', '10:00-14:00'),
('01234567890', '08:00-12:00');

-- Inserções na tabela funcionario_permissoes
INSERT INTO funcionario_permissoes (funcionario_cpf, permissao) VALUES
('12345678901', 'admin'),
('23456789012', 'recepcionista'),
('34567890123', 'coordenador'),
('45678901234', 'instrutor'),
('56789012345', 'gestor'),
('67890123456', 'instrutor'),
('78901234567', 'assistente'),
('89012345678', 'recepcionista'),
('90123456789', 'gestor'),
('01234567890', 'instrutor');