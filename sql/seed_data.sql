-- Script para popular o banco de dados com dados de exemplo
-- Execute após o init.sql

-- ============================================
-- RECURSOS HUMANOS (RH)
-- ============================================

-- Tipos de Documento
INSERT INTO rh.documento_tipo (id, ds_documento) VALUES
(1, 'CPF'),
(2, 'RG'),
(3, 'CNH')
ON CONFLICT DO NOTHING;

-- Tipos de Perfil
INSERT INTO rh.perfil_tipo (id, ds_perfil, bo_ativo) VALUES
(1, 'Administrador', true),
(2, 'Coordenador', true),
(3, 'Motorista', true),
(4, 'Aluno', true)
ON CONFLICT DO NOTHING;

-- Pessoas
INSERT INTO rh.pessoa (id, nome, dt_nascimento, email, bo_ativo) VALUES
(1, 'João Silva', '1985-03-15', 'joao.silva@email.com', true),
(2, 'Maria Santos', '1990-07-22', 'maria.santos@email.com', true),
(3, 'Pedro Oliveira', '1988-11-10', 'pedro.oliveira@email.com', true),
(4, 'Ana Costa', '1992-05-30', 'ana.costa@email.com', true),
(5, 'Carlos Pereira', '1987-09-18', 'carlos.pereira@email.com', true),
(6, 'Juliana Ferreira', '1995-01-25', 'juliana.ferreira@email.com', true),
(7, 'Roberto Alves', '1983-12-05', 'roberto.alves@email.com', true),
(8, 'Fernanda Lima', '1991-08-14', 'fernanda.lima@email.com', true)
ON CONFLICT DO NOTHING;

-- Documentos
INSERT INTO rh.documento (id_pessoa, id_documento_tipo, numero, bo_ativo) VALUES
(1, 1, '12345678901', true),
(1, 2, 'MG1234567', true),
(2, 1, '98765432100', true),
(2, 2, 'SP9876543', true),
(3, 1, '11122233344', true),
(3, 2, 'RJ1112223', true),
(4, 1, '55566677788', true),
(4, 2, 'GO5556667', true),
(5, 1, '99988877766', true),
(5, 2, 'BA9998887', true),
(6, 1, '44433322211', true),
(6, 2, 'RS4443332', true),
(7, 1, '77788899900', true),
(7, 2, 'PR7778889', true),
(8, 1, '22233344455', true),
(8, 2, 'SC2223334', true)
ON CONFLICT DO NOTHING;

-- Telefones
INSERT INTO rh.telefone (id, telefone) VALUES
(1, '(11) 98765-4321'),
(2, '(11) 91234-5678'),
(3, '(21) 98765-4321'),
(4, '(21) 91234-5678'),
(5, '(62) 98765-4321'),
(6, '(62) 91234-5678'),
(7, '(71) 98765-4321'),
(8, '(51) 98765-4321'),
(9, '(41) 98765-4321'),
(10, '(48) 98765-4321')
ON CONFLICT DO NOTHING;

-- Pessoa-Telefone
INSERT INTO rh.pessoa_telefone (id_pessoa, id_telefone, bo_ativo) VALUES
(1, 1, true),
(2, 2, true),
(3, 3, true),
(4, 4, true),
(5, 5, true),
(6, 6, true),
(7, 7, true),
(8, 8, true),
(1, 9, true),
(2, 10, true)
ON CONFLICT DO NOTHING;

-- Usuários (senha padrão: 123456 - hash bcrypt)
-- Nota: Em produção, use hash real. Aqui é apenas exemplo.
INSERT INTO rh.usuario (id, numero_cpf, senha, bo_ativo) VALUES
(1, '12345678901', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJZ5Q5Q5O', true),
(2, '98765432100', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJZ5Q5Q5O', true),
(3, '11122233344', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJZ5Q5Q5O', true),
(4, '55566677788', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJZ5Q5Q5O', true)
ON CONFLICT DO NOTHING;

-- Usuário-Perfil
INSERT INTO rh.usuario_perfil (id_usuario, id_perfil, bo_ativo) VALUES
(1, 1, true), -- João é Administrador
(2, 2, true), -- Maria é Coordenadora
(3, 3, true), -- Pedro é Motorista
(4, 4, true)  -- Ana é Aluna
ON CONFLICT DO NOTHING;

-- ============================================
-- GEOLOCALIZAÇÃO (GEO)
-- ============================================

-- Municípios (usando códigos IBGE reais)
-- Goiânia - GO (5208707)
-- São Paulo - SP (3550308)
-- Rio de Janeiro - RJ (3304557)
-- Belo Horizonte - MG (3106200)
-- Brasília - DF (5300108)
-- Salvador - BA (2927408)
-- Porto Alegre - RS (4314902)
-- Curitiba - PR (4106902)
-- Florianópolis - SC (4205407)

INSERT INTO geo.municipio (id, no_municipio, uf, cod_ibge, bo_ativo) VALUES
(5208707, 'Goiânia', 'GO', '5208707', true),
(3550308, 'São Paulo', 'SP', '3550308', true),
(3304557, 'Rio de Janeiro', 'RJ', '3304557', true),
(3106200, 'Belo Horizonte', 'MG', '3106200', true),
(5300108, 'Brasília', 'DF', '5300108', true),
(2927408, 'Salvador', 'BA', '2927408', true),
(4314902, 'Porto Alegre', 'RS', '4314902', true),
(4106902, 'Curitiba', 'PR', '4106902', true),
(4205407, 'Florianópolis', 'SC', '4205407', true),
(5201405, 'Aparecida de Goiânia', 'GO', '5201405', true),
(3509502, 'Campinas', 'SP', '3509502', true)
ON CONFLICT (id) DO NOTHING;

-- ============================================
-- INSTITUIÇÃO
-- ============================================

-- Campus
INSERT INTO instituicao.campus (id, id_municipio, no_campus, bo_ativo) VALUES
(1, 5208707, 'Campus Goiânia - Centro', true),
(2, 5208707, 'Campus Goiânia - Norte', true),
(3, 3550308, 'Campus São Paulo - Zona Sul', true),
(4, 3304557, 'Campus Rio de Janeiro - Centro', true),
(5, 3106200, 'Campus Belo Horizonte', true),
(6, 5201405, 'Campus Aparecida de Goiânia', true)
ON CONFLICT DO NOTHING;

-- Cursos
INSERT INTO instituicao.curso (id, no_curso, bo_ativo) VALUES
(1, 'Ciência da Computação', true),
(2, 'Engenharia de Software', true),
(3, 'Administração', true),
(4, 'Direito', true),
(5, 'Medicina', true),
(6, 'Enfermagem', true),
(7, 'Pedagogia', true),
(8, 'Engenharia Civil', true)
ON CONFLICT DO NOTHING;

-- Curso-Campus
INSERT INTO instituicao.curso_campus (id_campus, id_curso, bo_ativo) VALUES
(1, 1, true), -- Campus Goiânia Centro - Ciência da Computação
(1, 2, true), -- Campus Goiânia Centro - Engenharia de Software
(1, 3, true), -- Campus Goiânia Centro - Administração
(2, 1, true), -- Campus Goiânia Norte - Ciência da Computação
(2, 4, true), -- Campus Goiânia Norte - Direito
(3, 1, true), -- Campus São Paulo - Ciência da Computação
(3, 2, true), -- Campus São Paulo - Engenharia de Software
(3, 5, true), -- Campus São Paulo - Medicina
(4, 3, true), -- Campus Rio de Janeiro - Administração
(4, 6, true), -- Campus Rio de Janeiro - Enfermagem
(5, 7, true), -- Campus Belo Horizonte - Pedagogia
(5, 8, true), -- Campus Belo Horizonte - Engenharia Civil
(6, 1, true), -- Campus Aparecida - Ciência da Computação
(6, 3, true)  -- Campus Aparecida - Administração
ON CONFLICT DO NOTHING;

-- ============================================
-- INSCRIÇÃO
-- ============================================

-- Eventos (Palestras)
-- Os eventos representam palestras educacionais/acadêmicas onde as pessoas podem se inscrever
INSERT INTO inscricao.evento (id, titulo, descricao, dt_inicio, dt_fim, id_criador, bo_ativo) VALUES
(1, 'Palestra: Inteligência Artificial e Machine Learning', 'Palestra sobre as aplicações práticas de IA e ML no mercado atual, ministrada por especialistas da área de tecnologia.', '2024-02-15', '2024-02-15', 2, true),
(2, 'Palestra: Empreendedorismo Digital', 'Palestra sobre como iniciar um negócio digital, estratégias de marketing e gestão de startups.', '2024-02-20', '2024-02-20', 2, true),
(3, 'Palestra: Direitos Humanos e Cidadania', 'Palestra sobre os direitos fundamentais e o exercício da cidadania na sociedade contemporânea.', '2024-02-25', '2024-02-25', 1, true),
(4, 'Palestra: Inovações em Saúde Pública', 'Palestra sobre novas tecnologias e metodologias aplicadas na área da saúde pública e bem-estar social.', '2024-03-01', '2024-03-01', 2, true),
(5, 'Palestra: Desenvolvimento de Software Ágil', 'Palestra sobre metodologias ágeis, boas práticas de desenvolvimento e gestão de projetos de software.', '2024-03-05', '2024-03-05', 1, true),
(6, 'Palestra: Educação Inclusiva', 'Palestra sobre estratégias e práticas para uma educação inclusiva e acessível a todos.', '2024-03-10', '2024-03-10', 2, true),
(7, 'Palestra: Sustentabilidade e Meio Ambiente', 'Palestra sobre práticas sustentáveis, preservação ambiental e responsabilidade social corporativa.', '2024-03-15', '2024-03-15', 1, true)
ON CONFLICT DO NOTHING;

-- Evento-Inscrição (Inscrições nas Palestras)
INSERT INTO inscricao.evento_inscricao (id_evento, id_pessoa, bo_ativo) VALUES
(1, 4, true), -- Ana se inscreveu na palestra de IA e ML
(1, 5, true), -- Carlos se inscreveu na palestra de IA e ML
(1, 6, true), -- Juliana se inscreveu na palestra de IA e ML
(2, 4, true), -- Ana se inscreveu na palestra de Empreendedorismo
(2, 6, true), -- Juliana se inscreveu na palestra de Empreendedorismo
(2, 8, true), -- Fernanda se inscreveu na palestra de Empreendedorismo
(3, 5, true), -- Carlos se inscreveu na palestra de Direitos Humanos
(3, 7, true), -- Roberto se inscreveu na palestra de Direitos Humanos
(3, 8, true), -- Fernanda se inscreveu na palestra de Direitos Humanos
(4, 4, true), -- Ana se inscreveu na palestra de Saúde Pública
(4, 6, true), -- Juliana se inscreveu na palestra de Saúde Pública
(4, 8, true), -- Fernanda se inscreveu na palestra de Saúde Pública
(5, 5, true), -- Carlos se inscreveu na palestra de Desenvolvimento Ágil
(5, 6, true), -- Juliana se inscreveu na palestra de Desenvolvimento Ágil
(5, 7, true), -- Roberto se inscreveu na palestra de Desenvolvimento Ágil
(6, 4, true), -- Ana se inscreveu na palestra de Educação Inclusiva
(6, 8, true), -- Fernanda se inscreveu na palestra de Educação Inclusiva
(7, 5, true), -- Carlos se inscreveu na palestra de Sustentabilidade
(7, 7, true)  -- Roberto se inscreveu na palestra de Sustentabilidade
ON CONFLICT DO NOTHING;

-- ============================================
-- RESETAR SEQUENCES (para evitar conflitos de IDs)
-- ============================================

-- Ajustar sequences para o próximo ID disponível
SELECT setval('rh.pessoa_id_seq', (SELECT MAX(id) FROM rh.pessoa));
SELECT setval('rh.documento_id_seq', (SELECT MAX(id) FROM rh.documento));
SELECT setval('rh.telefone_id_seq', (SELECT MAX(id) FROM rh.telefone));
SELECT setval('rh.pessoa_telefone_id_seq', (SELECT MAX(id) FROM rh.pessoa_telefone));
SELECT setval('rh.usuario_perfil_id_seq', (SELECT MAX(id) FROM rh.usuario_perfil));
SELECT setval('instituicao.campus_id_seq', (SELECT MAX(id) FROM instituicao.campus));
SELECT setval('instituicao.curso_id_seq', (SELECT MAX(id) FROM instituicao.curso));
SELECT setval('instituicao.curso_campus_id_seq', (SELECT MAX(id) FROM instituicao.curso_campus));
SELECT setval('inscricao.evento_id_seq', (SELECT MAX(id) FROM inscricao.evento));
SELECT setval('inscricao.evento_inscricao_id_seq', (SELECT MAX(id) FROM inscricao.evento_inscricao));

