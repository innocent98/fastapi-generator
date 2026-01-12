# FastAPI Generator

Generate production-ready FastAPI projects with Poetry in seconds.

## Installation

```bash
# Using pip
pip install fastapi-gen

# Using pipx (recommended)
pipx install fastapi-gen

# From source
git clone https://github.com/innocent98/fastapi-generator.git
cd fastapi-generator
pip install -e .
```

## Usage

```bash
# Basic
fastapi-gen "My API"

# With options
fastapi-gen "My API" \
  --author "Your Name" \
  --email "you@example.com" \
  --description "My awesome API" \
  --no-postgres \
  --no-redis \
  --no-docker \
  --celery
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--author` | Author name | "Your Name" |
| `--email` | Author email | "your.email@example.com" |
| `--description` | Project description | "A FastAPI project" |
| `--no-postgres` | Skip PostgreSQL | False |
| `--no-redis` | Skip Redis | False |
| `--no-docker` | Skip Docker files | False |
| `--celery` | Include Celery | False |

## Generated Structure

```
my-api/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   └── health.py
│   │   │   └── api.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logger.py
│   ├── db/
│   │   ├── models/
│   │   ├── base.py
│   │   └── session.py
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── middleware/
│   └── main.py
├── tests/
├── alembic/
├── .github/workflows/
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

## Quick Start (Generated Project)

```bash
cd my-api
poetry install
cp .env.example .env
poetry run uvicorn app.main:app --reload
```

API: http://localhost:8000
Docs: http://localhost:8000/api/v1/docs

## License

MIT
