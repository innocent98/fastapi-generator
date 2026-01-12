# FastAPI Project Generator

A powerful CLI tool to generate production-ready FastAPI projects with Poetry and industry best practices in seconds.

## Features

### What This Generator Creates

- **Complete FastAPI Application** with async support
- **Poetry** for modern dependency management
- **Clean Architecture** with separation of concerns
- **API Versioning** (v1 by default, easily extensible)
- **JWT Authentication** with security best practices
- **Database Setup**:
  - SQLAlchemy 2.0 ORM
  - Alembic migrations
  - PostgreSQL support (optional)
- **Caching & Rate Limiting**:
  - Redis integration (optional)
  - SlowAPI for rate limiting
- **Testing Framework**:
  - Pytest with fixtures
  - Coverage reporting
  - Sample tests
- **Code Quality**:
  - Pre-commit hooks
  - Black, isort, Ruff, mypy
  - Comprehensive linting setup
- **CI/CD**:
  - GitHub Actions workflow with Poetry
  - Automated testing
  - Code coverage integration
- **Docker Support**:
  - Production-ready Dockerfile with Poetry
  - Docker Compose for local development
  - Multi-stage builds
- **Documentation**:
  - Auto-generated OpenAPI docs
  - Comprehensive README
  - Code documentation
- **Logging**:
  - Structured logging with Loguru
  - Request tracking
  - File and console output
- **Utilities**:
  - Makefile for common tasks
  - Scripts directory
  - Environment configuration

## Installation

### Prerequisites

- Python 3.11 or higher
- Poetry 1.8+ (for development)
- Git (optional, for repository initialization)

### Install from PyPI (Recommended)

```bash
# Using pip
pip install fastapi-gen

# Using pipx (recommended for CLI tools)
pipx install fastapi-gen
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/fastapi-generator.git
cd fastapi-generator

# Install with Poetry
poetry install

# Now you can use the generator
poetry run fastapi-gen --help
```

### Development Installation

```bash
git clone https://github.com/yourusername/fastapi-generator.git
cd fastapi-generator

# Install all dependencies including dev
poetry install

# Run tests
poetry run pytest

# Run the generator
poetry run fastapi-gen "My Test API"
```

## Usage

### Basic Usage

```bash
fastapi-gen "My Awesome API"
```

This creates a new project with:
- Poetry for dependency management
- PostgreSQL database support
- Redis caching
- Docker support
- All best practices enabled

### Advanced Options

```bash
fastapi-gen "My API" \
  --author "John Doe" \
  --email "john@example.com" \
  --description "My awesome FastAPI project" \
  --no-postgres \
  --no-redis \
  --no-docker \
  --celery
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `project_name` | Name of your project (required) | - |
| `--author` | Author name | "Your Name" |
| `--email` | Author email | "your.email@example.com" |
| `--description` | Project description | "A FastAPI project" |
| `--no-postgres` | Skip PostgreSQL setup | False |
| `--no-redis` | Skip Redis setup | False |
| `--no-docker` | Skip Docker files | False |
| `--celery` | Include Celery for background tasks | False |
| `--version` | Show version and exit | - |

### Examples

#### 1. Simple API (no database)

```bash
fastapi-gen "Simple API" --no-postgres --no-redis
```

#### 2. Microservice with Celery

```bash
fastapi-gen "Email Service" \
  --description "Microservice for email processing" \
  --celery
```

#### 3. Full-Stack Backend

```bash
fastapi-gen "E-Commerce Backend" \
  --author "Jane Smith" \
  --email "jane@startup.com" \
  --description "Backend API for e-commerce platform"
```

## Generated Project Structure

```
my-awesome-api/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   └── health.py
│   │   │   └── api.py
│   │   └── deps.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── security.py        # JWT & password hashing
│   │   └── logger.py          # Logging setup
│   ├── db/
│   │   ├── models/
│   │   │   └── __init__.py
│   │   ├── base.py            # SQLAlchemy base
│   │   └── session.py         # Database session
│   ├── schemas/               # Pydantic models
│   ├── services/              # Business logic
│   ├── utils/                 # Utility functions
│   ├── middleware/            # Custom middleware
│   └── main.py                # FastAPI application
├── tests/
│   ├── api/
│   ├── services/
│   ├── conftest.py
│   └── test_health.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── scripts/                   # Utility scripts
├── docs/                      # Documentation
├── logs/                      # Application logs
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions with Poetry
├── pyproject.toml             # Poetry configuration
├── Dockerfile                 # Multi-stage Poetry build
├── docker-compose.yml
├── alembic.ini
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── .pre-commit-config.yaml
├── Makefile
└── README.md
```

## After Generation

### 1. Navigate to Project

```bash
cd my-awesome-api
```

### 2. Install Dependencies with Poetry

```bash
# Install all dependencies (recommended for development)
poetry install

# Or install only production dependencies
poetry install --only main
```

### 3. Activate Virtual Environment

```bash
# Option 1: Activate shell
poetry shell

# Option 2: Run commands with poetry run prefix
poetry run uvicorn app.main:app --reload
```

### 4. Configure Environment

```bash
# Edit .env file with your settings
cp .env.example .env
nano .env

# Generate a secure SECRET_KEY:
openssl rand -hex 32
```

### 5. Set Up Database (if using PostgreSQL)

```bash
# Start database with Docker
docker-compose up -d db

# Run migrations
poetry run alembic upgrade head
# Or with Makefile
make migrate
```

### 6. Run Development Server

```bash
# Using Makefile (recommended)
make run

# Or with Poetry
poetry run uvicorn app.main:app --reload

# Or with Docker
docker-compose up
```

### 7. Access Your API

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **Health Check**: http://localhost:8000/health

## Makefile Commands

The generated project includes a Makefile with Poetry-based commands:

```bash
make help           # Show all available commands
make install        # Install production dependencies
make dev-install    # Install all deps + pre-commit hooks
make run            # Run development server
make test           # Run tests
make test-cov       # Run tests with coverage report
make lint           # Check code quality
make format         # Format code with black, isort, ruff
make clean          # Remove cache and generated files
make docker-build   # Build Docker image
make docker-up      # Start Docker containers
make docker-down    # Stop Docker containers
make migrate        # Run database migrations
make migrate-create # Create new migration
make shell          # Activate poetry shell
```

## Why Poetry?

The generated projects use Poetry instead of pip/requirements.txt for several advantages:

| Feature | requirements.txt | Poetry |
|---------|-----------------|--------|
| **Dependency Resolution** | Manual | Automatic with conflict detection |
| **Lock File** | None (or manual) | `poetry.lock` for reproducibility |
| **Virtual Environments** | Manual setup | Automatic management |
| **Dev Dependencies** | Separate file | Built-in groups |
| **Version Constraints** | Basic pinning | Semantic versioning (`^1.0`, `~1.0`) |
| **Reproducible Builds** | Difficult | Guaranteed |

## Best Practices Included

### 1. Security

- JWT token authentication
- Password hashing with bcrypt
- CORS configuration
- Environment variable management
- Secret key generation guidance

### 2. Code Quality

- Type hints throughout
- Pydantic for validation
- Pre-commit hooks
- Linting (black, isort, ruff, mypy)
- Comprehensive .gitignore

### 3. Testing

- Pytest configuration
- Test fixtures
- Coverage reporting
- Separated test database
- Example test cases

### 4. Database

- SQLAlchemy 2.0 patterns
- Alembic migrations
- Connection pooling
- Async support ready

### 5. API Design

- RESTful conventions
- API versioning
- Proper HTTP status codes
- Request/response validation
- Auto-generated documentation

### 6. DevOps

- Docker containerization with Poetry
- Docker Compose orchestration
- Health check endpoints
- GitHub Actions CI/CD with Poetry caching
- Production-ready gunicorn setup

### 7. Logging

- Structured logging
- Request tracking
- Log rotation
- Multiple output formats
- Environment-based log levels

## Customization

### Adding New Endpoints

```bash
# Create new endpoint file
touch app/api/v1/endpoints/users.py

# Add to router in app/api/v1/api.py
from app.api.v1.endpoints import users
api_router.include_router(users.router, prefix="/users", tags=["users"])
```

### Adding Database Models

```bash
# Create model file
touch app/db/models/user.py

# Create migration
make migrate-create
# Enter: "add user model"

# Apply migration
make migrate
```

### Adding Dependencies

```bash
# Add a production dependency
poetry add package-name

# Add a dev dependency
poetry add --group dev package-name

# Update all dependencies
poetry update
```

### Adding Tests

```bash
# Create test file
touch tests/api/test_users.py

# Run tests
make test
```

## Troubleshooting

### Issue: Poetry not found

**Solution**: Install Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Issue: Import errors

**Solution**: Ensure dependencies are installed
```bash
poetry install
poetry shell
```

### Issue: Database connection failed

**Solution**: Check DATABASE_URL in .env and ensure PostgreSQL is running
```bash
docker-compose up -d db
```

### Issue: Port 8000 already in use

**Solution**: Either stop the process using port 8000 or change the port
```bash
poetry run uvicorn app.main:app --reload --port 8001
```

### Issue: Alembic can't detect models

**Solution**: Ensure models are imported in alembic/env.py
```python
# In alembic/env.py
from app.db.models import user, item  # Import your models
```

## Roadmap

- [ ] Add authentication templates (OAuth2, API Keys)
- [ ] Add CRUD generator for models
- [ ] Add WebSocket support templates
- [ ] Add GraphQL option
- [ ] Add monitoring setup (Prometheus, Grafana)
- [ ] Add Kubernetes manifests
- [ ] Interactive CLI mode
- [ ] More database options (MySQL, MongoDB)

## Contributing

Found a bug or want to add a feature? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `poetry run pytest`
5. Submit a pull request

## License

MIT License - feel free to use this for personal or commercial projects.

## Author

This generator was created to speed up FastAPI development while maintaining best practices and production readiness.

## Support

If you find this helpful, please star the repository and share it with others!

For issues or questions, please open an issue on GitHub.

---

**Happy Coding!**
