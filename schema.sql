-- Script de criação do Banco de Dados para Gestão de Laboratórios
-- DBMS: PostgreSQL

-- Remover tabelas se já existirem para permitir a reexecução limpa do script
DROP TABLE IF EXISTS reservas CASCADE;
DROP TABLE IF EXISTS equipamentos CASCADE;
DROP TABLE IF EXISTS laboratorios CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- 1. Tabela de Usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('ALUNO', 'PROFESSOR', 'ADMINISTRADOR'))
);

-- 2. Tabela de Laboratórios
CREATE TABLE laboratorios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sala VARCHAR(50) NOT NULL,
    capacidade INT NOT NULL CHECK (capacidade > 0),
    descricao TEXT
);

-- 3. Tabela de Equipamentos
CREATE TABLE equipamentos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    num_serie VARCHAR(100) UNIQUE NOT NULL,
    laboratorio_id INT REFERENCES laboratorios(id) ON DELETE SET NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ATIVO', 'MANUTENCAO', 'INATIVO'))
);

-- 4. Tabela de Reservas
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    laboratorio_id INT NOT NULL REFERENCES laboratorios(id) ON DELETE CASCADE,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    data_inicio TIMESTAMP NOT NULL,
    data_fim TIMESTAMP NOT NULL,
    finalidade VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDENTE', 'APROVADA', 'CANCELADA')),
    CONSTRAINT chk_datas CHECK (data_fim > data_inicio)
);

-- Inserção de Dados Básicos (mínimo de 3 linhas por tabela)

-- Usuários
INSERT INTO usuarios (nome, email, senha, tipo) VALUES
('Ana Silva', 'ana.silva@universidade.edu', 'senha123', 'ALUNO'),
('Dr. Carlos Souza', 'carlos.souza@universidade.edu', 'prof456', 'PROFESSOR'),
('Mariana Costa', 'mariana.costa@universidade.edu', 'admin789', 'ADMINISTRADOR');

-- Laboratórios
INSERT INTO laboratorios (nome, sala, capacidade, descricao) VALUES
('Laboratório de Química Geral', 'Sala 201-A', 25, 'Laboratório destinado a aulas práticas de química e pesquisa de polímeros.'),
('Laboratório de Programação Avançada', 'Sala 104-B', 30, 'Laboratório de informática equipado com computadores de alto desempenho.'),
('Laboratório de Física Experimental', 'Sala 305-C', 20, 'Laboratório equipado com kits de óptica, termodinâmica e eletromagnetismo.');

-- Equipamentos
INSERT INTO equipamentos (nome, marca, num_serie, laboratorio_id, status) VALUES
('Espectrofotômetro UV-Vis', 'Thermo Fisher', 'UV-123456', 1, 'ATIVO'),
('Osciloscópio Digital', 'Tektronix', 'OSC-789012', 3, 'ATIVO'),
('Servidor de Testes Rack 2U', 'Dell', 'SRV-345678', 2, 'MANUTENCAO');

-- Reservas
INSERT INTO reservas (laboratorio_id, usuario_id, data_inicio, data_fim, finalidade, status) VALUES
(1, 2, '2026-06-20 08:00:00', '2026-06-20 12:00:00', 'Aula prática de Química Orgânica I', 'APROVADA'),
(2, 1, '2026-06-21 14:00:00', '2026-06-21 16:00:00', 'Estudo em grupo de Estruturas de Dados', 'PENDENTE'),
(3, 2, '2026-06-22 10:00:00', '2026-06-22 13:00:00', 'Pesquisa de iniciação científica em óptica', 'APROVADA');
