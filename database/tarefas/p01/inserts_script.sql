INSERT INTO endereco (id, rua, numero, cep, bairro, cidade) VALUES
(1, 'Rua Renato Dantas', 120, '59300-000', 'Centro', 'Caicó'),
(2, 'Rua Otávio Lamartine', 450, '59300-000', 'Penedo', 'Caicó'),
(3, 'Rua Celso Dantas', 305, '59300-000', 'Paraíba', 'Caicó'),
(4, 'Rua Augusto Monteiro', 98, '59300-000', 'Centro', 'Caicó'),
(5, 'Rua José Evaristo', 182, '59300-000', 'Boa Passagem', 'Caicó'),
(6, 'Rua Pedro Velho', 77, '59300-000', 'Maynard', 'Caicó'),
(7, 'Rua Marinheiro Manoel Inácio', 45, '59300-000', 'Acampamento', 'Caicó'),
(8, 'Rua Francisco Medeiros', 210, '59300-000', 'Salviano Santos', 'Caicó'),
(9, 'Rua Comandante Ezequiel', 36, '59300-000', 'Vila Altiva', 'Caicó'),
(10, 'Rua Professor Viana', 12, '59300-000', 'Centro', 'Caicó');

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
('35725815900', 'RG010', 'Ricardo Almeida', '84995544332', 'ricardo@email.com', '1983-08-03', TRUE, 10),
('23456789012', 'RG011', 'André Costa Silva', '84998887777', 'andre@email.com', '1980-01-01', TRUE, 1),
('34567890123', 'RG012', 'Juliana Oliveira Santos', '84997766555', 'juliana_oliveira@email.com', '1985-02-15', TRUE, 2),
('45678901234', 'RG013', 'Ricardo Gomes Pereira', '84996655444', 'ricardo_gomes@email.com', '1990-03-20', TRUE, 3),
('56789012345', 'RG014', 'Fernanda Lima Souza', '84995544333', 'fernanda_llima@email.com', '1992-04-25', TRUE, 4),
('67890123456', 'RG015', 'Luiz Felipe Martins', '84994433222', 'luiz@email.com', '1993-05-30', TRUE, 5),
('78901234567', 'RG016', 'Patrícia Alves Costa', '84993322111', 'patricia@email.com', '1994-06-10', TRUE, 6),
('89012345678', 'RG017', 'Carlos Henrique Rocha', '84992211000', 'carlos_rocha@email.com', '1995-07-12', TRUE, 7),
('90123456789', 'RG018', 'Amanda Ribeiro Silva', '84991109999', 'amanda@email.com', '1996-08-22', TRUE, 8),
('01234567890', 'RG019', 'Marcos Antônio Pereira', '84990098888', 'marcos@email.com', '1997-09-10', TRUE, 9),
('12345678909', 'RG020', 'Mario Florencio Lira', '84999871432', 'mario@email.com', '1990-07-15', TRUE, 10);

INSERT INTO plano (codigo, nome, qtd_aulas, valor_aula, status, limite_vigencia) VALUES
(1, 'Plano Nuvem de Flexibilidade', 4, 20.00, TRUE, '2025-06-30'),  
(2, 'Plano Pulsar do Equilíbrio', 8, 25.00, TRUE, '2025-06-30'),  
(3, 'Plano Voo Alto de Força', 12, 18.00, TRUE, '2025-06-30'),  
(4, 'Plano Fogo Vivo de Postura', 16, 22.00, TRUE, '2025-06-30'),  
(5, 'Plano Turbo de Desempenho', 20, 19.00, TRUE, '2025-06-30'),  
(6, 'Plano Nuvem de Flexibilidade (Promocional)', 4, 10.00, TRUE, '2025-04-30'),  
(7, 'Plano Pulsar do Equilíbrio (Promocional)', 8, 12.50, TRUE, '2025-04-30'),  
(8, 'Plano Voo Alto de Força (Promocional)', 12, 9.00, TRUE, '2025-04-30'),  
(9, 'Plano Fogo Vivo de Postura (Promocional)', 16, 11.00, TRUE, '2025-04-30'),  
(10, 'Plano Turbo de Desempenho (Promocional)', 20, 9.50, TRUE, '2025-04-30');

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
('12345678909', 'Instrutor', 2500.00, 40.00, 'instrutor1', 'senha123', FALSE, '2025-04-20 08:00:00'),
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
('12345678909', '08:00-12:00'),
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
('12345678909', 'Acesso Parcial'),
('23456789012', 'Acesso Completo'),
('34567890123', 'Acesso Parcial'),
('45678901234', 'Acesso Completo'),
('56789012345', 'Acesso Parcial'),
('67890123456', 'Acesso Parcial'),
('78901234567', 'Acesso Parcial'),
('89012345678', 'Acesso Completo'),
('90123456789', 'Acesso Parcial'),
('01234567890', 'Acesso Completo');

INSERT INTO servicos (codigo, modalidade, niveis_dificuldade)
VALUES 
(1, 'Yoga para iniciantes', '1'),
(2, 'Yoga Avançada', '2'),
(3, 'Pilates no Tecido', '2'),
(4, 'Pilates no Solo com Bola', '1'),
(5, 'Alongamento para Atletas', '1'),
(6, 'Treinamento Funcional', '2'),
(7, 'Pilates Reformer', '3'),
(8, 'Yoga para Gestantes', '1'),
(9, 'Pilates para Reabilitação', '2'),
(10, 'Meditação Guiada', '1');


INSERT INTO agendamento (codigo, data, horario, local, vagas_totais, vagas_disponiveis, instrutor_cpf) VALUES
(1, '2025-04-21 08:00:00', '08:00-10:00', 'Sala A', 20, 20, '12345678909'),
(2, '2025-04-21 10:00:00', '10:00-12:00', 'Sala B', 15, 15, '23456789012'),
(3, '2025-04-21 14:00:00', '14:00-16:00', 'Sala A', 20, 20, '34567890123'),
(4, '2025-04-21 16:00:00', '16:00-18:00', 'Sala B', 15, 15, '45678901234'),
(5, '2025-04-22 08:00:00', '08:00-10:00', 'Sala A', 20, 20, '56789012345'),
(6, '2025-04-22 10:00:00', '10:00-12:00', 'Sala B', 15, 15, '67890123456'),
(7, '2025-04-22 14:00:00', '14:00-16:00', 'Sala A', 20, 20, '78901234567'),
(8, '2025-04-22 16:00:00', '16:00-18:00', 'Sala B', 15, 15, '89012345678'),
(9, '2025-04-23 08:00:00', '08:00-10:00', 'Sala A', 20, 20, '90123456789'),
(10, '2025-04-23 10:00:00', '10:00-12:00', 'Sala B', 15, 15, '01234567890');

INSERT INTO aula (codigo, agendamento_codigo, data, frequencia) VALUES
(1, 1, '2025-04-21 08:00:00', FALSE),
(2, 2, '2025-04-21 10:00:00', FALSE),
(3, 3, '2025-04-21 14:00:00', FALSE),
(4, 4, '2025-04-21 16:00:00', FALSE),
(5, 5, '2025-04-22 08:00:00', FALSE),
(6, 6, '2025-04-22 10:00:00', FALSE),
(7, 7, '2025-04-22 14:00:00', FALSE),
(8, 8, '2025-04-22 16:00:00', FALSE),
(9, 9, '2025-04-23 08:00:00', FALSE),
(10, 10, '2025-04-23 10:00:00', FALSE);

INSERT INTO aula_aluno (aula_codigo, aluno_cpf) VALUES
(1, '12345678901'),
(2, '45678912300'),
(3, '32165498700'),
(4, '74185296300'),
(5, '85296374100'),
(6, '96374185200'),
(7, '15935725800'),
(8, '25815935700'),
(9, '35725815900'),
(10, '98765432100');

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

INSERT INTO conta_receber (codigo, aluno_cpf, valor, vencimento, status) VALUES
(1, '12345678901', 200.00, '2025-05-01', FALSE),
(2, '45678912300', 250.00, '2025-05-01', FALSE),
(3, '32165498700', 300.00, '2025-05-01', FALSE),
(4, '74185296300', 350.00, '2025-05-01', FALSE),
(5, '85296374100', 220.00, '2025-05-01', FALSE),
(6, '96374185200', 270.00, '2025-05-01', FALSE),
(7, '15935725800', 280.00, '2025-05-01', FALSE),
(8, '25815935700', 240.00, '2025-05-01', FALSE),
(9, '35725815900', 230.00, '2025-05-01', FALSE),
(10, '98765432100', 260.00, '2025-05-01', FALSE);

INSERT INTO pagamento (codigo, conta_receber_codigo, data, metodo, valor, status) VALUES
(1, 1, '2025-04-20 08:00:00', 'Cartão', 200.00, TRUE),
(2, 2, '2025-04-20 08:00:00', 'Boleto', 250.00, TRUE),
(3, 3, '2025-04-20 08:00:00', 'Cartão', 300.00, TRUE),
(4, 4, '2025-04-20 08:00:00', 'Boleto', 350.00, TRUE),
(5, 5, '2025-04-20 08:00:00', 'Cartão', 220.00, TRUE),
(6, 6, '2025-04-20 08:00:00', 'Boleto', 270.00, TRUE),
(7, 7, '2025-04-20 08:00:00', 'Cartão', 280.00, TRUE),
(8, 8, '2025-04-20 08:00:00', 'Boleto', 240.00, TRUE),
(9, 9, '2025-04-20 08:00:00', 'Cartão', 230.00, TRUE),
(10, 10, '2025-04-20 08:00:00', 'Boleto', 260.00, TRUE);