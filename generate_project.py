#!/usr/bin/env python3
"""
FastAPI Project Generator
Generates a production-ready FastAPI project with best practices
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any
import subprocess


class FastAPIGenerator:
    def __init__(self, project_name: str, author: str = "Your Name",
                 email: str = "your.email@example.com",
                 description: str = "A FastAPI project",
                 use_postgres: bool = True,
                 use_redis: bool = True,
                 use_docker: bool = True,
                 use_celery: bool = False):
        self.project_name = project_name
        self.project_slug = project_name.lower().replace(" ", "-").replace("_", "-")
        self.author = author
        self.email = email
        self.description = description
        self.use_postgres = use_postgres
        self.use_redis = use_redis
        self.use_docker = use_docker
        self.use_celery = use_celery

        # Directory structure
        self.base_path = Path.cwd() / self.project_slug

    def create_directory_structure(self):
        """Create the project directory structure"""
        print(f"Creating project structure for {self.project_name}...")

        directories = [
            self.base_path,
            self.base_path / "app",
            self.base_path / "app" / "api",
            self.base_path / "app" / "api" / "v1",
            self.base_path / "app" / "api" / "v1" / "endpoints",
            self.base_path / "app" / "core",
            self.base_path / "app" / "db",
            self.base_path / "app" / "db" / "models",
            self.base_path / "app" / "schemas",
            self.base_path / "app" / "services",
            self.base_path / "app" / "utils",
            self.base_path / "app" / "middleware",
            self.base_path / "tests",
            self.base_path / "tests" / "api",
            self.base_path / "tests" / "services",
            self.base_path / "alembic",
            self.base_path / "alembic" / "versions",
            self.base_path / "scripts",
            self.base_path / "docs",
            self.base_path / ".github",
            self.base_path / ".github" / "workflows",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        print(f"✓ Directory structure created at {self.base_path}")

    def create_requirements_files(self):
        """Create requirements.txt and requirements-dev.txt"""
        print("Creating requirements files...")

        requirements = """# Core
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.11.4
pydantic-settings==2.9.1
python-multipart==0.0.20
python-dotenv==1.1.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.0.1

# Database
sqlalchemy==2.0.41
alembic==1.15.2
"""

        if self.use_postgres:
            requirements += "psycopg2-binary==2.9.10\n"

        if self.use_redis:
            requirements += "\n# Caching and Rate Limiting\nredis==5.0.0\nslowapi==0.1.9\n"

        if self.use_celery:
            requirements += "\n# Background Tasks\ncelery==5.3.4\nflower==2.0.1\n"

        requirements += """
# Logging
loguru==0.7.3

# Email
emails==0.6
jinja2==3.1.6
email-validator==2.2.0

# Utilities
httpx==0.27.0
python-dateutil==2.8.2

# Production
gunicorn==23.0.0
"""

        requirements_dev = """# Testing
pytest==8.3.0
pytest-asyncio==0.24.0
pytest-cov==6.0.0
pytest-mock==3.14.0
httpx==0.27.0

# Code Quality
black==24.10.0
flake8==7.1.0
mypy==1.13.0
isort==5.13.0
pylint==3.3.0

# Pre-commit
pre-commit==4.0.0

# Development
ipython==8.29.0
"""

        with open(self.base_path / "requirements.txt", "w") as f:
            f.write(requirements.strip())

        with open(self.base_path / "requirements-dev.txt", "w") as f:
            f.write(requirements_dev.strip())

        print("✓ Requirements files created")

    def create_core_config(self):
        """Create core configuration files"""
        print("Creating core configuration...")

        config_content = """from typing import List, Optional, Any, Dict
from pydantic import AnyHttpUrl, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "{project_name}"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Server
    SERVER_HOST: str = "http://localhost"
    SERVER_PORT: int = 8000

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
""".format(project_name=self.project_name)

        if self.use_postgres:
            config_content += """
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
"""

        if self.use_redis:
            config_content += """
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
"""

        config_content += """
    # Email (optional)
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Admin
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
"""

        with open(self.base_path / "app" / "core" / "config.py", "w") as f:
            f.write(config_content)

        # Create __init__.py files
        (self.base_path / "app" / "__init__.py").touch()
        (self.base_path / "app" / "core" / "__init__.py").touch()
        (self.base_path / "app" / "api" / "__init__.py").touch()
        (self.base_path / "app" / "api" / "v1" / "__init__.py").touch()
        (self.base_path / "app" / "api" / "v1" / "endpoints" / "__init__.py").touch()
        (self.base_path / "app" / "db" / "__init__.py").touch()
        (self.base_path / "app" / "db" / "models" / "__init__.py").touch()
        (self.base_path / "app" / "schemas" / "__init__.py").touch()
        (self.base_path / "app" / "services" / "__init__.py").touch()
        (self.base_path / "app" / "utils" / "__init__.py").touch()
        (self.base_path / "app" / "middleware" / "__init__.py").touch()

        print("✓ Core configuration created")

    def create_security_module(self):
        """Create security utilities"""
        print("Creating security module...")

        security_content = """from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
"""

        with open(self.base_path / "app" / "core" / "security.py", "w") as f:
            f.write(security_content)

        print("✓ Security module created")

    def create_logger_module(self):
        """Create logging configuration"""
        print("Creating logger module...")

        logger_content = """import sys
from loguru import logger
from app.core.config import settings


def setup_logging():
    logger.remove()

    log_level = "DEBUG" if settings.ENVIRONMENT == "development" else "INFO"

    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 week",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    return logger


log = setup_logging()
"""

        with open(self.base_path / "app" / "core" / "logger.py", "w") as f:
            f.write(logger_content)

        # Create logs directory
        (self.base_path / "logs").mkdir(exist_ok=True)
        (self.base_path / "logs" / ".gitkeep").touch()

        print("✓ Logger module created")

    def create_database_module(self):
        """Create database configuration"""
        print("Creating database module...")

        if self.use_postgres:
            base_content = """from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
"""

            session_content = """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

            with open(self.base_path / "app" / "db" / "base.py", "w") as f:
                f.write(base_content)

            with open(self.base_path / "app" / "db" / "session.py", "w") as f:
                f.write(session_content)

        print("✓ Database module created")

    def create_api_dependencies(self):
        """Create API dependencies"""
        print("Creating API dependencies...")

        deps_content = """from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # TODO: Fetch user from database
    # user = db.query(User).filter(User.id == user_id).first()
    # if user is None:
    #     raise credentials_exception
    # return user

    return {"user_id": user_id}
"""

        with open(self.base_path / "app" / "api" / "deps.py", "w") as f:
            f.write(deps_content)

        print("✓ API dependencies created")

    def create_main_app(self):
        """Create main FastAPI application"""
        print("Creating main application...")

        main_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time

from app.core.config import settings
from app.core.logger import log
from app.api.v1.api import api_router


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        log.info(
            f"{request.method} {request.url.path} "
            f"completed in {process_time:.4f}s with status {response.status_code}"
        )

        return response


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.SERVER_PORT,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
"""

        with open(self.base_path / "app" / "main.py", "w") as f:
            f.write(main_content)

        print("✓ Main application created")

    def create_api_router(self):
        """Create API router and sample endpoints"""
        print("Creating API router...")

        api_router_content = """from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
"""

        health_endpoint_content = """from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }
"""

        with open(self.base_path / "app" / "api" / "v1" / "api.py", "w") as f:
            f.write(api_router_content)

        with open(self.base_path / "app" / "api" / "v1" / "endpoints" / "health.py", "w") as f:
            f.write(health_endpoint_content)

        print("✓ API router created")

    def create_env_files(self):
        """Create .env and .env.example files"""
        print("Creating environment files...")

        # Generate a random SECRET_KEY
        import secrets
        secret_key = secrets.token_hex(32)

        env_example = f"""# Application
PROJECT_NAME={self.project_name}
VERSION=1.0.0
API_V1_STR=/api/v1
ENVIRONMENT=development

# Server
SERVER_HOST=http://localhost
SERVER_PORT=8000

# Security (Generated automatically - change in production)
SECRET_KEY={secret_key}
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ALGORITHM=HS256

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

"""

        if self.use_postgres:
            env_example += """# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

"""

        if self.use_redis:
            env_example += """# Redis
REDIS_URL=redis://localhost:6379/0

"""

        env_example += """# Email (Optional)
SMTP_TLS=true
SMTP_PORT=587
SMTP_HOST=smtp.example.com
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-password
EMAILS_FROM_EMAIL=noreply@example.com
EMAILS_FROM_NAME=Your App Name

# Admin
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis
"""

        with open(self.base_path / ".env.example", "w") as f:
            f.write(env_example)

        with open(self.base_path / ".env", "w") as f:
            f.write(env_example)

        print("✓ Environment files created")

    def create_docker_files(self):
        """Create Docker and docker-compose files"""
        if not self.use_docker:
            return

        print("Creating Docker files...")

        dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    netcat-traditional \\
    libpq-dev \\
    gcc \\
    && apt-get clean \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app /app/app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

        docker_compose = f"""version: '3.8'

services:
  api:
    build: .
    container_name: {self.project_slug}_api
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app
    env_file:
      - .env
    depends_on:
"""

        if self.use_postgres:
            docker_compose += "      - db\n"
        if self.use_redis:
            docker_compose += "      - redis\n"

        docker_compose += """    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

"""

        if self.use_postgres:
            docker_compose += """  db:
    image: postgres:15
    container_name: {project_slug}_db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: {project_slug}_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

""".format(project_slug=self.project_slug)

        if self.use_redis:
            docker_compose += f"""  redis:
    image: redis:7-alpine
    container_name: {self.project_slug}_redis
    ports:
      - "6379:6379"
    restart: unless-stopped

"""

        docker_compose += """volumes:
  postgres_data:
"""

        with open(self.base_path / "Dockerfile", "w") as f:
            f.write(dockerfile)

        with open(self.base_path / "docker-compose.yml", "w") as f:
            f.write(docker_compose)

        dockerignore = """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.env
.env.local
*.db
*.sqlite
.DS_Store
"""

        with open(self.base_path / ".dockerignore", "w") as f:
            f.write(dockerignore)

        print("✓ Docker files created")

    def create_gitignore(self):
        """Create .gitignore file"""
        print("Creating .gitignore...")

        gitignore = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.env.local
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Alembic
alembic/versions/*.pyc

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pytest
.pytest_cache/
"""

        with open(self.base_path / ".gitignore", "w") as f:
            f.write(gitignore)

        print("✓ .gitignore created")

    def create_alembic_config(self):
        """Create Alembic configuration"""
        if not self.use_postgres:
            return

        print("Creating Alembic configuration...")

        alembic_ini = """[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

[alembic:exclude]
tables = spatial_ref_sys

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""

        env_py = """from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.db.base import Base
# Import all models here
# from app.db.models import user, item, etc.

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

        script_py_mako = '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
'''

        with open(self.base_path / "alembic.ini", "w") as f:
            f.write(alembic_ini)

        with open(self.base_path / "alembic" / "env.py", "w") as f:
            f.write(env_py)

        with open(self.base_path / "alembic" / "script.py.mako", "w") as f:
            f.write(script_py_mako)

        (self.base_path / "alembic" / "versions" / ".gitkeep").touch()

        print("✓ Alembic configuration created")

    def create_test_files(self):
        """Create test configuration and sample tests"""
        print("Creating test files...")

        conftest = """import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
"""

        test_health = """def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
"""

        pytest_ini = """[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=app
    --cov-report=term-missing
    --cov-report=html
"""

        with open(self.base_path / "tests" / "conftest.py", "w") as f:
            f.write(conftest)

        with open(self.base_path / "tests" / "test_health.py", "w") as f:
            f.write(test_health)

        with open(self.base_path / "pytest.ini", "w") as f:
            f.write(pytest_ini)

        (self.base_path / "tests" / "__init__.py").touch()
        (self.base_path / "tests" / "api" / "__init__.py").touch()
        (self.base_path / "tests" / "services" / "__init__.py").touch()

        print("✓ Test files created")

    def create_precommit_config(self):
        """Create pre-commit configuration"""
        print("Creating pre-commit configuration...")

        precommit = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/PyCQA/flake8
    rev: 7.1.0
    hooks:
      - id: flake8
        args: ["--max-line-length=100", "--extend-ignore=E203,W503"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
"""

        with open(self.base_path / ".pre-commit-config.yaml", "w") as f:
            f.write(precommit)

        print("✓ Pre-commit configuration created")

    def create_github_actions(self):
        """Create GitHub Actions CI/CD workflow"""
        print("Creating GitHub Actions workflow...")

        ci_workflow = f"""name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Cache dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{{{ runner.os }}}}-pip-${{{{ hashFiles('requirements*.txt') }}}}
        restore-keys: |
          ${{{{ runner.os }}}}-pip-

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run linting
      run: |
        black --check app tests
        isort --check-only app tests
        flake8 app tests

    - name: Run tests
      env:
        DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
        SECRET_KEY: test-secret-key-for-ci
        FIRST_SUPERUSER_EMAIL: admin@test.com
        FIRST_SUPERUSER_PASSWORD: testpassword
      run: |
        pytest --cov=app --cov-report=xml --cov-report=html

    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
"""

        with open(self.base_path / ".github" / "workflows" / "ci.yml", "w") as f:
            f.write(ci_workflow)

        print("✓ GitHub Actions workflow created")

    def create_readme(self):
        """Create comprehensive README"""
        print("Creating README...")

        readme = f"""# {self.project_name}

{self.description}

## Features

- FastAPI framework with async support
- Pydantic v2 for data validation
- SQLAlchemy 2.0 for database ORM
- Alembic for database migrations
- JWT authentication
- Docker and docker-compose support
- Comprehensive testing setup with pytest
- Pre-commit hooks for code quality
- GitHub Actions CI/CD
- Structured logging with Loguru
- API documentation with Swagger UI and ReDoc

## Requirements

- Python 3.11+
- PostgreSQL (if using database)
- Redis (if using caching)
- Docker & Docker Compose (optional)

## Project Structure

```
{self.project_slug}/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
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
│   ├── api/
│   └── services/
├── alembic/
│   └── versions/
├── scripts/
├── docs/
├── .github/
│   └── workflows/
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── pytest.ini
└── README.md
```

## Getting Started

### 1. Clone and Setup

```bash
cd {self.project_slug}
cp .env.example .env
# Edit .env with your configuration
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Database Setup

```bash
# Run migrations
alembic upgrade head

# Create initial data (if needed)
python scripts/init_db.py
```

### 4. Run Development Server

```bash
# With uvicorn
uvicorn app.main:app --reload

# Or with python
python -m app.main
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### 5. Using Docker

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_health.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black app tests
isort app tests

# Lint code
flake8 app tests
mypy app

# Run pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## Environment Variables

See `.env.example` for all available environment variables.

Key variables:
- `SECRET_KEY`: Secret key for JWT tokens (generate with `openssl rand -hex 32`)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `ENVIRONMENT`: development/staging/production

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Deployment

### Using Docker

```bash
# Build production image
docker build -t {self.project_slug}:latest .

# Run container
docker run -p 8000:8000 --env-file .env {self.project_slug}:latest
```

### Manual Deployment

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT License

## Author

{self.author} ({self.email})
"""

        with open(self.base_path / "README.md", "w") as f:
            f.write(readme)

        print("✓ README created")

    def create_makefile(self):
        """Create Makefile for common tasks"""
        print("Creating Makefile...")

        makefile = f"""# Makefile for {self.project_name}

.PHONY: help install dev-install run test lint format clean docker-build docker-up docker-down migrate

help:
\t@echo "Available commands:"
\t@echo "  make install       - Install production dependencies"
\t@echo "  make dev-install   - Install development dependencies"
\t@echo "  make run           - Run development server"
\t@echo "  make test          - Run tests"
\t@echo "  make test-cov      - Run tests with coverage"
\t@echo "  make lint          - Run linting"
\t@echo "  make format        - Format code"
\t@echo "  make clean         - Clean up generated files"
\t@echo "  make docker-build  - Build Docker image"
\t@echo "  make docker-up     - Start Docker containers"
\t@echo "  make docker-down   - Stop Docker containers"
\t@echo "  make migrate       - Run database migrations"

install:
\tpip install -r requirements.txt

dev-install:
\tpip install -r requirements.txt -r requirements-dev.txt
\tpre-commit install

run:
\tuvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
\tpytest

test-cov:
\tpytest --cov=app --cov-report=html --cov-report=term

lint:
\tblack --check app tests
\tisort --check-only app tests
\tflake8 app tests
\tmypy app

format:
\tblack app tests
\tisort app tests

clean:
\tfind . -type d -name "__pycache__" -exec rm -rf {{}} +
\tfind . -type f -name "*.pyc" -delete
\tfind . -type f -name "*.pyo" -delete
\tfind . -type d -name "*.egg-info" -exec rm -rf {{}} +
\trm -rf .pytest_cache .coverage htmlcov/ .mypy_cache/

docker-build:
\tdocker-compose build

docker-up:
\tdocker-compose up -d

docker-down:
\tdocker-compose down

migrate:
\talembic upgrade head

migrate-create:
\t@read -p "Enter migration message: " msg; \\
\talembic revision --autogenerate -m "$$msg"
"""

        with open(self.base_path / "Makefile", "w") as f:
            f.write(makefile)

        print("✓ Makefile created")

    def initialize_git(self):
        """Initialize git repository"""
        print("Initializing git repository...")

        try:
            subprocess.run(["git", "init"], cwd=self.base_path, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=self.base_path, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit: FastAPI project boilerplate"],
                cwd=self.base_path,
                check=True,
                capture_output=True
            )
            print("✓ Git repository initialized")
        except subprocess.CalledProcessError as e:
            print(f"⚠ Git initialization failed: {e}")

    def generate(self):
        """Generate the complete project"""
        print(f"\n{'='*60}")
        print(f"Generating FastAPI project: {self.project_name}")
        print(f"{'='*60}\n")

        try:
            self.create_directory_structure()
            self.create_requirements_files()
            self.create_core_config()
            self.create_security_module()
            self.create_logger_module()
            self.create_database_module()
            self.create_api_dependencies()
            self.create_main_app()
            self.create_api_router()
            self.create_env_files()
            self.create_docker_files()
            self.create_gitignore()
            self.create_alembic_config()
            self.create_test_files()
            self.create_precommit_config()
            self.create_github_actions()
            self.create_readme()
            self.create_makefile()
            self.initialize_git()

            print(f"\n{'='*60}")
            print(f"✓ Project generated successfully!")
            print(f"{'='*60}\n")

            print("Next steps:")
            print(f"1. cd {self.project_slug}")
            print("2. Create a virtual environment: python -m venv venv")
            print("3. Activate it: source venv/bin/activate")
            print("4. Install dependencies: make dev-install")
            print("5. Update .env with your configuration")
            print("6. Run migrations: make migrate")
            print("7. Start development server: make run")
            print(f"\nAPI will be available at: http://localhost:8000")
            print(f"Documentation: http://localhost:8000/api/v1/docs\n")

        except Exception as e:
            print(f"\n✗ Error generating project: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a production-ready FastAPI project"
    )
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--author", default="Your Name", help="Author name")
    parser.add_argument("--email", default="your.email@example.com", help="Author email")
    parser.add_argument("--description", default="A FastAPI project", help="Project description")
    parser.add_argument("--no-postgres", action="store_true", help="Don't include PostgreSQL setup")
    parser.add_argument("--no-redis", action="store_true", help="Don't include Redis setup")
    parser.add_argument("--no-docker", action="store_true", help="Don't include Docker setup")
    parser.add_argument("--celery", action="store_true", help="Include Celery for background tasks")

    args = parser.parse_args()

    generator = FastAPIGenerator(
        project_name=args.project_name,
        author=args.author,
        email=args.email,
        description=args.description,
        use_postgres=not args.no_postgres,
        use_redis=not args.no_redis,
        use_docker=not args.no_docker,
        use_celery=args.celery,
    )

    generator.generate()


if __name__ == "__main__":
    main()
