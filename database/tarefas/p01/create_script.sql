-- Tabela ENDERECO
CREATE TABLE endereco (
    id SERIAL PRIMARY KEY,
    rua VARCHAR(100) NOT NULL,
    numero INTEGER NOT NULL,
    cep VARCHAR(9) NOT NULL,
    bairro VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL
);

-- Tabela PESSOA
CREATE TABLE pessoa (
    cpf VARCHAR(11) PRIMARY KEY,
    rg VARCHAR(20) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    data_nascimento DATE NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    endereco_id INTEGER NOT NULL,
    FOREIGN KEY (endereco_id) REFERENCES endereco(id)
);

-- Tabela PLANO
CREATE TABLE plano (
    codigo SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    qtd_aulas INTEGER NOT NULL,
    valor_aula DECIMAL(10,2) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    limite_vigencia DATE
);

-- Tabela ALUNO (herda de PESSOA)
CREATE TABLE aluno (
    cpf VARCHAR(11) PRIMARY KEY,
    profissao VARCHAR(50),
    historico_saude TEXT,
    plano_codigo INTEGER,
    data_inicio_plano DATE,
    data_vencimento_plano DATE,
    plano_ativo BOOLEAN DEFAULT FALSE,
    evolucao TEXT,
    FOREIGN KEY (cpf) REFERENCES pessoa(cpf),
    FOREIGN KEY (plano_codigo) REFERENCES plano(codigo)
);

-- Tabela FUNCIONARIO (herda de PESSOA)
CREATE TABLE funcionario (
    cpf VARCHAR(11) PRIMARY KEY,
    funcao VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    carga_horaria DECIMAL(5,2) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    ultimo_acesso TIMESTAMP,
    FOREIGN KEY (cpf) REFERENCES pessoa(cpf)
);

-- Tabela de array "horarios_trabalho" convertido para relacionamento seguindo a regra de normalizacao 1NF que exige que cada coluna contenha apenas valores atômicos
CREATE TABLE funcionario_horarios (
    funcionario_cpf VARCHAR(11) NOT NULL,
    horario VARCHAR(50) NOT NULL,
    PRIMARY KEY (funcionario_cpf, horario),
    FOREIGN KEY (funcionario_cpf) REFERENCES funcionario(cpf)
);

-- Tabela de array "permissoes" convertido para relacionamento seguindo a regra de normalizacao 1NF que exige que cada coluna contenha apenas valores atômicos
CREATE TABLE funcionario_permissoes (
    funcionario_cpf VARCHAR(11) NOT NULL,
    permissao VARCHAR(50) NOT NULL,
    PRIMARY KEY (funcionario_cpf, permissao),
    FOREIGN KEY (funcionario_cpf) REFERENCES funcionario(cpf)
);

-- SERVICOS
CREATE TABLE servicos (
    codigo SERIAL PRIMARY KEY,
    modalidade VARCHAR(50) NOT NULL,
    niveis_dificuldade CHAR(1) NOT NULL
);

-- AGENDAMENTO
CREATE TABLE agendamento (
    codigo SERIAL PRIMARY KEY,
    data TIMESTAMP NOT NULL,
    horario VARCHAR(20) NOT NULL,
    local VARCHAR(100) NOT NULL,
    vagas_totais INTEGER NOT NULL,
    vagas_disponiveis INTEGER NOT NULL,
    instrutor_cpf VARCHAR(11) NOT NULL,
    FOREIGN KEY (instrutor_cpf) REFERENCES funcionario(cpf)
);

-- AULA
CREATE TABLE aula (
    codigo SERIAL PRIMARY KEY,
    agendamento_codigo INTEGER NOT NULL,
    data TIMESTAMP NOT NULL,
    frequencia BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (agendamento_codigo) REFERENCES agendamento(codigo)
);

-- Tabela de relacionamento entre AULA e ALUNO. Criada pq em um banco relacionais, n podemos ter um relacionamento M-M, quebraria a 1° forma de normalização: não se pode ter múltiplos valores em uma única tabela.
CREATE TABLE aula_aluno (
    aula_codigo INTEGER NOT NULL,
    aluno_cpf VARCHAR(11) NOT NULL,
    PRIMARY KEY (aula_codigo, aluno_cpf),
    FOREIGN KEY (aula_codigo) REFERENCES aula(codigo),
    FOREIGN KEY (aluno_cpf) REFERENCES aluno(cpf)
);

-- Tabela de relacionamento entre AULA e SERVICOS. Criada pq em um banco relacionais, n podemos ter um relacionamento M-M, quebraria a 1° forma de normalização: não se pode ter múltiplos valores em uma única tabela.
CREATE TABLE aula_servicos (
    aula_codigo INTEGER NOT NULL,
    servicos_codigo INTEGER NOT NULL,
    PRIMARY KEY (aula_codigo, servicos_codigo),
    FOREIGN KEY (aula_codigo) REFERENCES aula(codigo),
    FOREIGN KEY (servicos_codigo) REFERENCES servicos(codigo)
);

-- CONTA_RECEBER
CREATE TABLE conta_receber (
    codigo SERIAL PRIMARY KEY,
    aluno_cpf VARCHAR(11) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    vencimento DATE NOT NULL,
    status BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (aluno_cpf) REFERENCES aluno(cpf)
);

-- PAGAMENTO
CREATE TABLE pagamento (
    codigo SERIAL PRIMARY KEY,
    conta_receber_codigo INTEGER NOT NULL,
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (conta_receber_codigo) REFERENCES conta_receber(codigo)
);