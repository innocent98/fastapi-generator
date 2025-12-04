# FastAPI Project Generator

A powerful CLI tool to generate production-ready FastAPI projects with industry best practices in seconds.

## Features

### What This Generator Creates

- **Complete FastAPI Application** with async support
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
  - Black, isort, flake8, mypy
  - Comprehensive linting setup
- **CI/CD**:
  - GitHub Actions workflow
  - Automated testing
  - Code coverage integration
- **Docker Support**:
  - Production-ready Dockerfile
  - Docker Compose for local development
  - Multi-service orchestration
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
- Git (optional, for repository initialization)

### Setup

```bash
# Clone or download this generator
cd fastapi-generator

# Make the script executable
chmod +x generate_project.py

# Optional: Create an alias for easy access
echo 'alias fastapi-gen="python3 /path/to/generate_project.py"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Basic Usage

```bash
python generate_project.py "My Awesome API"
```

This creates a new project with:
- PostgreSQL database
- Redis caching
- Docker support
- All best practices enabled

### Advanced Options

```bash
python generate_project.py "My API" \
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

### Examples

#### 1. Simple API (no database)

```bash
python generate_project.py "Simple API" --no-postgres --no-redis
```

#### 2. Microservice with Celery

```bash
python generate_project.py "Email Service" \
  --description "Microservice for email processing" \
  --celery
```

#### 3. Full-Stack Backend

```bash
python generate_project.py "E-Commerce Backend" \
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
│       └── ci.yml            # GitHub Actions
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pytest.ini
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

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Using Makefile (recommended)
make dev-install

# Or manually
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

### 4. Configure Environment

```bash
# Edit .env file with your settings
nano .env

# At minimum, generate a secure SECRET_KEY:
openssl rand -hex 32
```

### 5. Set Up Database (if using PostgreSQL)

```bash
# Start database with Docker
docker-compose up -d db

# Run migrations
make migrate

# Or manually
alembic upgrade head
```

### 6. Run Development Server

```bash
# Using Makefile
make run

# Or manually
uvicorn app.main:app --reload

# Or with Docker
docker-compose up
```

### 7. Access Your API

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **Health Check**: http://localhost:8000/health

## Makefile Commands

The generated project includes a Makefile with common commands:

```bash
make help           # Show all available commands
make install        # Install production dependencies
make dev-install    # Install dev dependencies + pre-commit hooks
make run            # Run development server
make test           # Run tests
make test-cov       # Run tests with coverage report
make lint           # Check code quality
make format         # Format code with black and isort
make clean          # Remove cache and generated files
make docker-build   # Build Docker image
make docker-up      # Start Docker containers
make docker-down    # Stop Docker containers
make migrate        # Run database migrations
make migrate-create # Create new migration
```

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
- Linting (black, isort, flake8, mypy)
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

- Docker containerization
- Docker Compose orchestration
- Health check endpoints
- GitHub Actions CI/CD
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

### Adding Tests

```bash
# Create test file
touch tests/api/test_users.py

# Run tests
make test
```

## Comparison with Other Tools

| Feature | This Generator | Cookiecutter | Manual Setup |
|---------|---------------|--------------|--------------|
| Setup Time | < 1 minute | 2-3 minutes | 30-60 minutes |
| Customization | High | Medium | Unlimited |
| Best Practices | Built-in | Template dependent | Manual |
| Updates | Script update | Template update | Manual |
| Learning Curve | Low | Medium | High |
| Flexibility | High | Medium | Unlimited |

## Troubleshooting

### Issue: Import errors

**Solution**: Ensure you're in the virtual environment and installed dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Database connection failed

**Solution**: Check DATABASE_URL in .env and ensure PostgreSQL is running
```bash
docker-compose up -d db
```

### Issue: Port 8000 already in use

**Solution**: Either stop the process using port 8000 or change the port
```bash
uvicorn app.main:app --reload --port 8001
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
4. Submit a pull request

## License

MIT License - feel free to use this for personal or commercial projects.

## Author

This generator was created to speed up FastAPI development while maintaining best practices and production readiness.

## Support

If you find this helpful, please star the repository and share it with others!

For issues or questions, please open an issue on GitHub.

---

**Happy Coding!** 🚀
