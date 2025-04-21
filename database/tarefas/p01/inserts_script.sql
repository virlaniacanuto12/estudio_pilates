INSERT INTO endereco (rua, numero, cep, bairro, cidade) VALUES
('Rua Renato Dantas', 120, '59300-000', 'Centro', 'Caicó'),
('Rua Otávio Lamartine', 450, '59300-000', 'Penedo', 'Caicó'),
('Rua Celso Dantas', 305, '59300-000', 'Paraíba', 'Caicó'),
('Rua Augusto Monteiro', 98, '59300-000', 'Centro', 'Caicó'),
('Rua José Evaristo', 182, '59300-000', 'Boa Passagem', 'Caicó'),
('Rua Pedro Velho', 77, '59300-000', 'Maynard', 'Caicó'),
('Rua Marinheiro Manoel Inácio', 45, '59300-000', 'Acampamento', 'Caicó'),
('Rua Francisco Medeiros', 210, '59300-000', 'Salviano Santos', 'Caicó'),
('Rua Comandante Ezequiel', 36, '59300-000', 'Vila Altiva', 'Caicó'),
('Rua Professor Viana', 12, '59300-000', 'Centro', 'Caicó');

INSERT INTO pessoa (cpf, rg, nome, telefone, email, data_nascimento, status, endereco_id) VALUES
('12345678901', 'RG001', 'Maria Clara Fernandes', '84999001122', 'maria@email.com', '1990-04-15', TRUE, 1),
('98765432100', 'RG002', 'João Pedro Alves', '84988556677', 'joao@email.com', '1985-09-20', TRUE, 2),
('45678912300', 'RG003', 'Ana Beatriz Lima', '84991010203', 'ana@email.com', '1995-01-10', TRUE, 3),
('32165498700', 'RG004', 'Carlos Eduardo Silva', '84996000300', 'carlos@email.com', '1988-07-22', TRUE, 4),
('74185296300', 'RG005', 'Fernanda Souza', '84992345678', 'fernanda@email.com', '1993-11-05', TRUE, 5),
('85296374100', 'RG006', 'Lucas Rocha', '84999887766', 'lucas@email.com', '1999-06-18', TRUE, 6),
('96374185200', 'RG007', 'Juliana Castro', '84998877665', 'juliana@email.com', '1997-02-25', TRUE, 7),
('15935725800', 'RG008', 'Bruno Ferreira', '84997766554', 'bruno@email.com', '1991-12-30', TRUE, 8),
('25815935700', 'RG009', 'Camila Duarte', '84996655443', 'camila@email.com', '1987-05-14', TRUE, 9),
('35725815900', 'RG010', 'Ricardo Almeida', '84995544332', 'ricardo@email.com', '1983-08-03', TRUE, 10);

INSERT INTO plano (nome, qtd_aulas, valor_aula, status, limite_vigencia) VALUES
('Plano Nuvem de Flexibilidade', 4, 20.00, TRUE, '2025-06-30'),  
('Plano Pulsar do Equilíbrio', 8, 25.00, TRUE, '2025-06-30'),  
('Plano Voo Alto de Força', 12, 18.00, TRUE, '2025-06-30'),  
('Plano Fogo Vivo de Postura', 16, 22.00, TRUE, '2025-06-30'),  
('Plano Turbo de Desempenho', 20, 19.00, TRUE, '2025-06-30'),  
('Plano Nuvem de Flexibilidade (Promocional)', 4, 10.00, TRUE, '2025-04-30'),  
('Plano Pulsar do Equilíbrio (Promocional)', 8, 12.50, TRUE, '2025-04-30'),  
('Plano Voo Alto de Força (Promocional)', 12, 9.00, TRUE, '2025-04-30'),  
('Plano Fogo Vivo de Postura (Promocional)', 16, 11.00, TRUE, '2025-04-30'),  
('Plano Turbo de Desempenho (Promocional)', 20, 9.50, TRUE, '2025-04-30');

INSERT INTO aluno (cpf, profissao, historico_saude, plano_codigo, data_inicio_plano, data_vencimento_plano, plano_ativo, evolucao) VALUES
('12345678901', 'Professora', 'Dor lombar ocasional.', 1, '2025-04-01', '2025-06-30', TRUE, 'Adaptação'),
('45678912300', 'Estudante', 'Nenhum problema de saúde.', 2, '2025-04-01', '2025-06-30', TRUE, 'Boa evolução'),
('32165498700', 'Engenheiro', 'Cirurgia no joelho em 2022.', 3, '2025-03-15', '2025-06-30', TRUE, 'Reabilitação'),
('74185296300', 'Recepcionista', 'Asma leve.', 4, '2025-02-01', '2025-06-30', TRUE, 'Controle respiratório'),
('85296374100', 'Advogada', 'Nenhuma condição relevante.', 5, '2025-04-01', '2025-06-30', TRUE, 'Condicionamento em progresso'),
('96374185200', 'Designer', 'Problemas na coluna cervical.', 6, '2025-03-01', '2025-04-30', TRUE, 'Alongamento diário'),
('15935725800', 'Programador', 'Sedentarismo.', 7, '2025-01-10', '2025-04-30', TRUE, 'Iniciando rotina'),
('25815935700', 'Comerciante', 'Pressão alta controlada.', 8, '2025-03-20', '2025-04-30', TRUE, 'Monitoramento em dia'),
('35725815900', 'Técnico de TI', 'Hérnia de disco.', 9, '2025-02-15', '2025-04-30', TRUE, 'Foco em reabilitação'),
('98765432100', 'Fisioterapeuta', 'Ativo e sem restrições.', 10, '2025-04-10', '2025-06-30', TRUE, 'Boa performance');

INSERT INTO funcionario (cpf, funcao, salario, carga_horaria, login, senha_hash, is_admin, ultimo_acesso) VALUES
('12345678901', 'Instrutor', 2500.00, 40.00, 'instrutor1', 'senha123', FALSE, '2025-04-20 08:00:00'),
('23456789012', 'Gerente', 5000.00, 40.00, 'gerente1', 'senha456', TRUE, '2025-04-20 08:00:00'),
('34567890123', 'Instrutor', 2800.00, 40.00, 'instrutor2', 'senha789', FALSE, '2025-04-20 08:00:00'),
('45678901234', 'Gerente', 5500.00, 40.00, 'gerente2', 'senha101', TRUE, '2025-04-20 08:00:00'),
('56789012345', 'Instrutor', 2400.00, 40.00, 'instrutor3', 'senha102', FALSE, '2025-04-20 08:00:00'),
('67890123456', 'Instrutor', 2300.00, 40.00, 'instrutor4', 'senha103', FALSE, '2025-04-20 08:00:00'),
('78901234567', 'Instrutor', 2700.00, 40.00, 'instrutor5', 'senha104', FALSE, '2025-04-20 08:00:00'),
('89012345678', 'Gerente', 6000.00, 40.00, 'gerente3', 'senha105', TRUE, '2025-04-20 08:00:00'),
('90123456789', 'Instrutor', 2200.00, 40.00, 'instrutor6', 'senha106', FALSE, '2025-04-20 08:00:00'),
('01234567890', 'Gerente', 6500.00, 40.00, 'gerente4', 'senha107', TRUE, '2025-04-20 08:00:00');

INSERT INTO funcionario_horarios (funcionario_cpf, horario) VALUES
('12345678901', '08:00-12:00'),
('23456789012', '08:00-12:00'),
('34567890123', '14:00-18:00'),
('45678901234', '14:00-18:00'),
('56789012345', '08:00-12:00'),
('67890123456', '14:00-18:00'),
('78901234567', '08:00-12:00'),
('89012345678', '14:00-18:00'),
('90123456789', '08:00-12:00'),
('01234567890', '14:00-18:00');

INSERT INTO funcionario_permissoes (funcionario_cpf, permissao) VALUES
('12345678901', 'Acesso Parcial'),
('23456789012', 'Acesso Completo'),
('34567890123', 'Acesso Parcial'),
('45678901234', 'Acesso Completo'),
('56789012345', 'Acesso Parcial'),
('67890123456', 'Acesso Parcial'),
('78901234567', 'Acesso Parcial'),
('89012345678', 'Acesso Completo'),
('90123456789', 'Acesso Parcial'),
('01234567890', 'Acesso Completo');

INSERT INTO servicos (modalidade, niveis_dificuldade)
VALUES 
    ('Yoga para iniciantes', '1'),
    ('Yoga Avançada', '2'),
    ('Pilates no Tecido', '2'),
    ('Pilates no Solo com Bola', '1'),
    ('Alongamento para Atletas', '1'),
    ('Treinamento Funcional', '2'),
    ('Pilates Reformer', '3'),
    ('Yoga para Gestantes', '1'),
    ('Pilates para Reabilitação', '2'),
    ('Meditação Guiada', '1');


INSERT INTO agendamento (data, horario, local, vagas_totais, vagas_disponiveis, instrutor_cpf) VALUES
('2025-04-21 08:00:00', '08:00-10:00', 'Sala A', 20, 20, '12345678901'),
('2025-04-21 10:00:00', '10:00-12:00', 'Sala B', 15, 15, '23456789012'),
('2025-04-21 14:00:00', '14:00-16:00', 'Sala A', 20, 20, '34567890123'),
('2025-04-21 16:00:00', '16:00-18:00', 'Sala B', 15, 15, '45678901234'),
('2025-04-22 08:00:00', '08:00-10:00', 'Sala A', 20, 20, '56789012345'),
('2025-04-22 10:00:00', '10:00-12:00', 'Sala B', 15, 15, '67890123456'),
('2025-04-22 14:00:00', '14:00-16:00', 'Sala A', 20, 20, '78901234567'),
('2025-04-22 16:00:00', '16:00-18:00', 'Sala B', 15, 15, '89012345678'),
('2025-04-23 08:00:00', '08:00-10:00', 'Sala A', 20, 20, '90123456789'),
('2025-04-23 10:00:00', '10:00-12:00', 'Sala B', 15, 15, '01234567890');

INSERT INTO aula (agendamento_codigo, data, frequencia) VALUES
(1, '2025-04-21 08:00:00', FALSE),
(2, '2025-04-21 10:00:00', FALSE),
(3, '2025-04-21 14:00:00', FALSE),
(4, '2025-04-21 16:00:00', FALSE),
(5, '2025-04-22 08:00:00', FALSE),
(6, '2025-04-22 10:00:00', FALSE),
(7, '2025-04-22 14:00:00', FALSE),
(8, '2025-04-22 16:00:00', FALSE),
(9, '2025-04-23 08:00:00', FALSE),
(10, '2025-04-23 10:00:00', FALSE);

INSERT INTO aula_aluno (aula_codigo, aluno_cpf) VALUES
(1, '12345678901'),
(2, '23456789012'),
(3, '34567890123'),
(4, '45678901234'),
(5, '56789012345'),
(6, '67890123456'),
(7, '78901234567'),
(8, '89012345678'),
(9, '90123456789'),
(10, '01234567890');

INSERT INTO aula_servicos (aula_codigo, servicos_codigo) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO conta_receber (aluno_cpf, valor, vencimento, status) VALUES
('12345678901', 200.00, '2025-05-01', FALSE),
('23456789012', 250.00, '2025-05-01', FALSE),
('34567890123', 300.00, '2025-05-01', FALSE),
('45678901234', 350.00, '2025-05-01', FALSE),
('56789012345', 220.00, '2025-05-01', FALSE),
('67890123456', 270.00, '2025-05-01', FALSE),
('78901234567', 280.00, '2025-05-01', FALSE),
('89012345678', 240.00, '2025-05-01', FALSE),
('90123456789', 230.00, '2025-05-01', FALSE),
('01234567890', 260.00, '2025-05-01', FALSE);

INSERT INTO pagamento (conta_receber_codigo, data, metodo, valor, status) VALUES
(1, '2025-04-20 08:00:00', 'Cartão', 200.00, TRUE),
(2, '2025-04-20 08:00:00', 'Boleto', 250.00, TRUE),
(3, '2025-04-20 08:00:00', 'Cartão', 300.00, TRUE),
(4, '2025-04-20 08:00:00', 'Boleto', 350.00, TRUE),
(5, '2025-04-20 08:00:00', 'Cartão', 220.00, TRUE),
(6, '2025-04-20 08:00:00', 'Boleto', 270.00, TRUE),
(7, '2025-04-20 08:00:00', 'Cartão', 280.00, TRUE),
(8, '2025-04-20 08:00:00', 'Boleto', 240.00, TRUE),
(9, '2025-04-20 08:00:00', 'Cartão', 230.00, TRUE),
(10, '2025-04-20 08:00:00', 'Boleto', 260.00, TRUE);