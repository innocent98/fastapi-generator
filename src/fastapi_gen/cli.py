"""Command-line interface for FastAPI Generator."""

import argparse
import sys

from fastapi_gen import __version__
from fastapi_gen.generator import FastAPIGenerator


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="fastapi-gen",
        description="Generate a production-ready FastAPI project with best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fastapi-gen "My API"
  fastapi-gen "E-Commerce API" --author "John Doe" --email "john@example.com"
  fastapi-gen "Simple API" --no-postgres --no-redis
  fastapi-gen "Task API" --celery
        """,
    )

    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--author", default="Your Name", help="Author name")
    parser.add_argument("--email", default="your.email@example.com", help="Author email")
    parser.add_argument("--description", default="A FastAPI project", help="Project description")
    parser.add_argument(
        "--no-postgres", action="store_true", help="Don't include PostgreSQL setup"
    )
    parser.add_argument("--no-redis", action="store_true", help="Don't include Redis setup")
    parser.add_argument("--no-docker", action="store_true", help="Don't include Docker setup")
    parser.add_argument(
        "--celery", action="store_true", help="Include Celery for background tasks"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

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

    try:
        generator.generate()
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
