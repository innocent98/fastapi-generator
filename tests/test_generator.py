"""Tests for the FastAPI generator."""

import os
import shutil
import tempfile
from pathlib import Path

import pytest

from fastapi_gen.generator import FastAPIGenerator


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    original_dir = os.getcwd()
    temp_path = tempfile.mkdtemp()
    os.chdir(temp_path)
    yield temp_path
    os.chdir(original_dir)
    shutil.rmtree(temp_path)


class TestFastAPIGenerator:
    """Test cases for FastAPIGenerator class."""

    def test_project_slug_generation(self):
        """Test that project slug is correctly generated."""
        generator = FastAPIGenerator("My Test Project")
        assert generator.project_slug == "my-test-project"
        assert generator.package_name == "my_test_project"

    def test_project_slug_with_underscores(self):
        """Test project slug with underscores."""
        generator = FastAPIGenerator("my_test_project")
        assert generator.project_slug == "my-test-project"

    def test_default_values(self):
        """Test default values are set correctly."""
        generator = FastAPIGenerator("Test")
        assert generator.author == "Your Name"
        assert generator.email == "your.email@example.com"
        assert generator.description == "A FastAPI project"
        assert generator.use_postgres is True
        assert generator.use_redis is True
        assert generator.use_docker is True
        assert generator.use_celery is False

    def test_custom_values(self):
        """Test custom values are set correctly."""
        generator = FastAPIGenerator(
            project_name="Custom Project",
            author="John Doe",
            email="john@example.com",
            description="A custom project",
            use_postgres=False,
            use_redis=False,
            use_docker=False,
            use_celery=True,
        )
        assert generator.author == "John Doe"
        assert generator.email == "john@example.com"
        assert generator.description == "A custom project"
        assert generator.use_postgres is False
        assert generator.use_redis is False
        assert generator.use_docker is False
        assert generator.use_celery is True

    def test_generate_creates_directory_structure(self, temp_dir):
        """Test that generate creates the correct directory structure."""
        generator = FastAPIGenerator("test-api", use_docker=False)
        generator.generate()

        project_path = Path(temp_dir) / "test-api"
        assert project_path.exists()
        assert (project_path / "app").exists()
        assert (project_path / "app" / "api").exists()
        assert (project_path / "app" / "core").exists()
        assert (project_path / "app" / "db").exists()
        assert (project_path / "tests").exists()
        assert (project_path / "alembic").exists()

    def test_generate_creates_pyproject_toml(self, temp_dir):
        """Test that generate creates pyproject.toml."""
        generator = FastAPIGenerator("test-api", use_docker=False)
        generator.generate()

        project_path = Path(temp_dir) / "test-api"
        pyproject = project_path / "pyproject.toml"
        assert pyproject.exists()

        content = pyproject.read_text()
        assert "[tool.poetry]" in content
        assert 'name = "test-api"' in content
        assert "fastapi" in content

    def test_generate_creates_env_files(self, temp_dir):
        """Test that generate creates .env files."""
        generator = FastAPIGenerator("test-api", use_docker=False)
        generator.generate()

        project_path = Path(temp_dir) / "test-api"
        assert (project_path / ".env").exists()
        assert (project_path / ".env.example").exists()

    def test_generate_creates_gitignore(self, temp_dir):
        """Test that generate creates .gitignore."""
        generator = FastAPIGenerator("test-api", use_docker=False)
        generator.generate()

        project_path = Path(temp_dir) / "test-api"
        gitignore = project_path / ".gitignore"
        assert gitignore.exists()

        content = gitignore.read_text()
        assert "__pycache__" in content
        assert ".env" in content
        assert "poetry.lock" in content

    def test_generate_without_postgres(self, temp_dir):
        """Test generation without PostgreSQL."""
        generator = FastAPIGenerator("test-api", use_postgres=False, use_docker=False)
        generator.generate()

        project_path = Path(temp_dir) / "test-api"
        pyproject = project_path / "pyproject.toml"
        content = pyproject.read_text()
        assert "psycopg2-binary" not in content

    def test_generate_without_redis(self, temp_dir):
        """Test generation without Redis."""
        generator = FastAPIGenerator("test-api", use_redis=False, use_docker=False)
        generator.generate()

        project_path = Path(temp_dir) / "test-api"
        pyproject = project_path / "pyproject.toml"
        content = pyproject.read_text()
        assert "redis" not in content
        assert "slowapi" not in content

    def test_generate_with_celery(self, temp_dir):
        """Test generation with Celery."""
        generator = FastAPIGenerator("test-api", use_celery=True, use_docker=False)
        generator.generate()

        project_path = Path(temp_dir) / "test-api"
        pyproject = project_path / "pyproject.toml"
        content = pyproject.read_text()
        assert "celery" in content
        assert "flower" in content

    def test_generate_with_docker(self, temp_dir):
        """Test generation with Docker files."""
        generator = FastAPIGenerator("test-api", use_docker=True)
        generator.generate()

        project_path = Path(temp_dir) / "test-api"
        assert (project_path / "Dockerfile").exists()
        assert (project_path / "docker-compose.yml").exists()
        assert (project_path / ".dockerignore").exists()

        # Check Dockerfile uses Poetry
        dockerfile = (project_path / "Dockerfile").read_text()
        assert "poetry" in dockerfile.lower()
