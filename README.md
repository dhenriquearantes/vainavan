# Vainobus API - Python (FastAPI)

API para gerenciamento de eventos de transporte de alunos, organizada com estrutura similar ao Laravel.

## Estrutura do Projeto

```
projeto-vainobus/
├── app/
│   ├── controllers/      # Controllers (rotas/endpoints)
│   ├── models/          # Models SQLAlchemy
│   ├── repositories/    # Repositories (acesso a dados)
│   ├── services/        # Services (lógica de negócio)
│   ├── schemas/         # Schemas Pydantic (validação)
│   └── core/            # Configurações core (database)
├── main.py              # Aplicação principal
├── docker-compose.yml   # Docker Compose
├── Dockerfile           # Dockerfile da aplicação
└── requirements.txt     # Dependências
```

## Instalação e Execução

### Opção 1: Docker Compose (Recomendado)

1. Crie o arquivo `.env` na raiz:
```bash
cat > .env << EOF
DB_HOST=postgres
DB_PORT=5432
DB_NAME=banco_vainobus
DB_USER=postgres
DB_PASS=vainobus
EOF
```

2. Inicie os serviços:
```bash
docker-compose up -d
```

O PostgreSQL será inicializado automaticamente com o script `sql/init.sql`.

3. A API estará disponível em `http://localhost:8099`
4. Documentação interativa: `http://localhost:8099/docs`

### Opção 2: Local (sem Docker)

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure o arquivo `.env` com as credenciais do PostgreSQL

3. Execute a aplicação:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8099
```

## Configuração do Banco de Dados

O docker-compose já configura o PostgreSQL automaticamente. Se precisar criar o banco manualmente, execute o script SQL em `sql/init.sql` (ou `backend/public/sql/banco.sql`).

## Endpoints

### Recursos Humanos

- `GET /recursos-humanos/pessoa` - Listar pessoas
- `GET /recursos-humanos/pessoa/{id}` - Obter pessoa
- `POST /recursos-humanos/pessoa` - Criar pessoa
- `PUT /recursos-humanos/pessoa/{id}` - Atualizar pessoa
- `DELETE /recursos-humanos/pessoa/{id}` - Desativar pessoa

### Instituição

#### Campus
- `GET /instituicao/campus` - Listar campus (filtros: `?ativo=true&municipio=1`)
- `GET /instituicao/campus/{id}` - Obter campus
- `POST /instituicao/campus` - Criar campus
- `PUT /instituicao/campus/{id}` - Atualizar campus
- `DELETE /instituicao/campus/{id}` - Desativar campus

#### Curso
- `GET /instituicao/curso` - Listar cursos (filtro: `?ativo=true`)
- `GET /instituicao/curso/{id}` - Obter curso
- `POST /instituicao/curso` - Criar curso
- `PUT /instituicao/curso/{id}` - Atualizar curso
- `DELETE /instituicao/curso/{id}` - Desativar curso

#### Curso-Campus
- `GET /instituicao/curso-campus` - Listar relações (filtros: `?campus=1&curso=2`)
- `POST /instituicao/curso-campus` - Criar relação curso-campus

### Inscrição

- `GET /inscricao/evento` - Listar eventos (filtros: `?ativo=true&criador=1`)
- `GET /inscricao/evento/{id}` - Obter evento
- `POST /inscricao/evento` - Criar evento
- `PUT /inscricao/evento/{id}` - Atualizar evento
- `DELETE /inscricao/evento/{id}` - Desativar evento

### Geolocalização (API IBGE)

Todos os dados de municípios e estados são obtidos diretamente da API oficial do IBGE.

- `GET /geolocalizacao/estado` - Listar todos os estados do Brasil
- `GET /geolocalizacao/municipio` - Listar municípios (filtros: `?estado=SP&nome=São Paulo`)
- `GET /geolocalizacao/municipio/{id}` - Obter município por ID do IBGE
- `GET /geolocalizacao/municipio/estado/{sigla_uf}` - Listar municípios por estado (ex: SP, RJ, MG)

**Nota:** O campo `id_municipio` usado em Campus deve ser o ID do IBGE (não mais o ID local).

## Comandos Docker

```bash
# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Parar serviços
docker-compose down

# Reconstruir e iniciar
docker-compose up -d --build

# Acessar PostgreSQL
docker-compose exec postgres psql -U postgres -d banco_vainobus
```

