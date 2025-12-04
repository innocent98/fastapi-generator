# FastAPI Generator - Quick Start Guide

Get a production-ready FastAPI project running in under 5 minutes!

## Installation (One-Time Setup)

### Option 1: Direct Usage

```bash
cd /path/to/fastapi-generator
chmod +x generate_project.py
```

### Option 2: Global Alias (Recommended)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias fastapi-gen="python3 /path/to/fastapi-generator/generate_project.py"
```

Then run:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now you can use `fastapi-gen` from anywhere!

## Generate Your First Project

### Simple API (30 seconds)

```bash
# Using direct method
python3 generate_project.py "My API"

# Using alias
fastapi-gen "My API"
```

### Full-Featured API (1 minute)

```bash
fastapi-gen "E-Commerce API" \
  --author "Your Name" \
  --email "your@email.com" \
  --description "Backend for e-commerce platform"
```

### Minimal API (no database)

```bash
fastapi-gen "Microservice API" --no-postgres --no-redis --no-docker
```

## Get Your API Running

### Method 1: Quick Start (No Docker)

```bash
cd my-api

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and set SECRET_KEY (use: openssl rand -hex 32)

# Run
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/api/v1/docs

### Method 2: Docker (Recommended for Full Stack)

```bash
cd my-api

# Edit .env first!
docker-compose up -d
```

Visit: http://localhost:8000/api/v1/docs

### Method 3: Using Makefile

```bash
cd my-api

# Setup
make dev-install

# Configure .env
nano .env

# Run
make run
```

## Essential Commands

```bash
# Development
make run              # Start dev server
make test             # Run tests
make format           # Format code
make lint             # Check code quality

# Docker
make docker-up        # Start containers
make docker-down      # Stop containers
make docker-build     # Rebuild image

# Database
make migrate          # Apply migrations
make migrate-create   # Create new migration
```

## Common Use Cases

### 1. REST API with Database

```bash
fastapi-gen "User Management API"
cd user-management-api
# Edit .env with database credentials
make dev-install
make migrate
make run
```

### 2. Microservice (Minimal)

```bash
fastapi-gen "Email Service" --no-postgres --no-redis
cd email-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### 3. Background Task API

```bash
fastapi-gen "Task Processor" --celery
cd task-processor
# Setup Redis for Celery
docker-compose up -d redis
make dev-install
make run
```

## Project Structure Overview

```
my-api/
├── app/
│   ├── api/v1/endpoints/    # Your API endpoints go here
│   ├── core/                # Config, security, logging
│   ├── db/models/           # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── main.py              # FastAPI app
├── tests/                   # Test files
├── .env                     # Your configuration
├── Makefile                 # Common commands
└── README.md                # Project documentation
```

## Next Steps After Generation

### 1. Add Your First Endpoint

Create `app/api/v1/endpoints/users.py`:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def get_users():
    return {"users": []}

@router.post("")
def create_user(name: str):
    return {"user": {"name": name}}
```

Add to `app/api/v1/api.py`:

```python
from app.api.v1.endpoints import users

api_router.include_router(users.router, prefix="/users", tags=["users"])
```

### 2. Add a Database Model

Create `app/db/models/user.py`:

```python
from sqlalchemy import Column, String, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
```

Create migration:

```bash
make migrate-create
# Enter: "add user model"
make migrate
```

### 3. Add Tests

Create `tests/api/test_users.py`:

```python
def test_get_users(client):
    response = client.get("/api/v1/users")
    assert response.status_code == 200
```

Run tests:

```bash
make test
```

## Configuration Checklist

Before deploying, ensure you've configured:

- [ ] `SECRET_KEY` - Generate with `openssl rand -hex 32`
- [ ] `DATABASE_URL` - Your PostgreSQL connection string
- [ ] `REDIS_URL` - Your Redis connection (if using)
- [ ] `BACKEND_CORS_ORIGINS` - Your frontend URLs
- [ ] `FIRST_SUPERUSER_EMAIL` - Admin email
- [ ] `FIRST_SUPERUSER_PASSWORD` - Admin password
- [ ] Email settings (if using)

## Troubleshooting

### Issue: Module not found

```bash
# Ensure you're in virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Database connection error

```bash
# Check DATABASE_URL in .env
# Start PostgreSQL with Docker
docker-compose up -d db
```

### Issue: Port already in use

```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

## Tips & Tricks

### Quick Database Reset

```bash
docker-compose down -v  # Remove volumes
docker-compose up -d db
make migrate
```

### Run Tests on File Change

```bash
pip install pytest-watch
ptw
```

### API Testing with HTTPie

```bash
# Install
pip install httpie

# Test endpoints
http GET localhost:8000/api/v1/health
http POST localhost:8000/api/v1/users name="John"
```

### Interactive API Testing

```bash
# Install
pip install ipython

# Run
ipython

# In IPython
from app.main import app
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get("/api/v1/health")
print(response.json())
```

## Best Practices

1. **Always use virtual environments**
2. **Never commit .env file** (it's in .gitignore)
3. **Run tests before committing** (`make test`)
4. **Format code before committing** (`make format`)
5. **Use Makefile commands** for consistency
6. **Keep dependencies up to date**
7. **Write tests for new features**
8. **Document API endpoints**

## Common Patterns

### Protected Endpoint

```python
from app.api.deps import get_current_user

@router.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"user": current_user}
```

### Database Query

```python
from app.db.session import get_db

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### Async Endpoint

```python
@router.get("/async")
async def async_endpoint():
    # Async operations here
    return {"status": "ok"}
```

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Pydantic Docs**: https://docs.pydantic.dev
- **Alembic Docs**: https://alembic.sqlalchemy.org

## Getting Help

If you encounter issues:

1. Check the generated README.md in your project
2. Review FastAPI documentation
3. Check .env configuration
4. Verify all services are running (database, redis)
5. Look at application logs

## What's Included Out of the Box

- JWT Authentication
- Password Hashing (bcrypt)
- CORS Configuration
- Request Logging
- Health Check Endpoint
- Database Session Management
- Migration System
- Test Framework
- Code Quality Tools
- Docker Configuration
- CI/CD Pipeline
- API Documentation
- Error Handling
- Environment Management

## Production Deployment

### Using Docker

```bash
# Build
docker build -t my-api:latest .

# Run
docker run -p 8000:8000 --env-file .env my-api:latest
```

### Using Gunicorn

```bash
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000
```

### Environment Variables

Set `ENVIRONMENT=production` in your .env for production settings.

---

**You're all set!** Start building amazing APIs! 🚀

For detailed documentation, see [README.md](README.md)
