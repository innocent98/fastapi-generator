# FastAPI Generator - Usage Examples

Real-world examples of generating different types of FastAPI projects.

## Table of Contents

1. [Simple REST API](#1-simple-rest-api)
2. [E-Commerce Backend](#2-e-commerce-backend)
3. [Authentication Service](#3-authentication-service)
4. [Microservice Architecture](#4-microservice-architecture)
5. [Background Task Processor](#5-background-task-processor)
6. [Real-time Chat API](#6-real-time-chat-api)
7. [Minimal Serverless API](#7-minimal-serverless-api)
8. [Multi-Tenant SaaS Backend](#8-multi-tenant-saas-backend)

---

## 1. Simple REST API

**Use Case**: Basic CRUD operations, learning FastAPI

### Generate

```bash
python3 generate_project.py "Simple Todo API" \
  --description "A simple todo list API for learning"
```

### Setup

```bash
cd simple-todo-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Add Todo Model

`app/db/models/todo.py`:

```python
from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from app.db.base import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Add Todo Endpoints

`app/api/v1/endpoints/todos.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.todo import Todo
from uuid import uuid4

router = APIRouter()

@router.get("")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@router.post("")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(id=str(uuid4()), title=title)
    db.add(todo)
    db.commit()
    return todo

@router.put("/{todo_id}")
def update_todo(todo_id: str, completed: bool, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = completed
    db.commit()
    return todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: str, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
```

### Run

```bash
alembic revision --autogenerate -m "add todo model"
alembic upgrade head
uvicorn app.main:app --reload
```

---

## 2. E-Commerce Backend

**Use Case**: Product catalog, orders, payments

### Generate

```bash
python3 generate_project.py "ShopifyClone Backend" \
  --author "Your Name" \
  --email "you@company.com" \
  --description "E-commerce platform backend API"
```

### Setup

```bash
cd shopifyclone-backend
cp .env.example .env
# Edit .env with database and payment provider credentials
docker-compose up -d
```

### Models Structure

```
app/db/models/
├── user.py
├── product.py
├── category.py
├── order.py
├── order_item.py
├── payment.py
└── inventory.py
```

### Example Product Model

`app/db/models/product.py`:

```python
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    category_id = Column(String, ForeignKey("categories.id"))
    image_url = Column(String)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
```

### Key Endpoints

```
POST   /api/v1/products
GET    /api/v1/products
GET    /api/v1/products/{id}
PUT    /api/v1/products/{id}
DELETE /api/v1/products/{id}

POST   /api/v1/orders
GET    /api/v1/orders/my-orders
POST   /api/v1/payments/process
GET    /api/v1/categories
```

---

## 3. Authentication Service

**Use Case**: Centralized auth for microservices

### Generate

```bash
python3 generate_project.py "Auth Service" \
  --description "Authentication and authorization microservice"
```

### Features to Add

1. **User Registration with Email Verification**
2. **Login with JWT**
3. **Refresh Token**
4. **Password Reset**
5. **2FA (Two-Factor Authentication)**
6. **OAuth2 (Google, GitHub)**
7. **Role-Based Access Control**

### Enhanced Auth Endpoint

`app/api/v1/endpoints/auth.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    # Check if user exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = User(
        id=str(uuid4()),
        email=email,
        hashed_password=get_password_hash(password)
    )
    db.add(user)
    db.commit()

    # Send verification email
    send_verification_email(email)

    return {"message": "User created. Please verify your email."}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email}
    }

@router.post("/refresh")
def refresh_token(refresh_token: str):
    # Implement refresh token logic
    pass

@router.post("/forgot-password")
def forgot_password(email: str):
    # Send password reset email
    pass
```

---

## 4. Microservice Architecture

**Use Case**: Multiple independent services

### Generate Multiple Services

```bash
# User Service
python3 generate_project.py "User Service" --no-redis

# Product Service
python3 generate_project.py "Product Service" --no-redis

# Order Service
python3 generate_project.py "Order Service" --celery

# Notification Service
python3 generate_project.py "Notification Service" --no-postgres
```

### Docker Compose for All Services

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  user-service:
    build: ./user-service
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres/user_db
      - SERVICE_NAME=user-service

  product-service:
    build: ./product-service
    ports:
      - "8002:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres/product_db
      - SERVICE_NAME=product-service

  order-service:
    build: ./order-service
    ports:
      - "8003:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres/order_db
      - REDIS_URL=redis://redis:6379/0
      - SERVICE_NAME=order-service

  notification-service:
    build: ./notification-service
    ports:
      - "8004:8000"
    environment:
      - SERVICE_NAME=notification-service

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
```

---

## 5. Background Task Processor

**Use Case**: Email sending, report generation, data processing

### Generate

```bash
python3 generate_project.py "Task Processor" \
  --celery \
  --description "Background job processing service"
```

### Add Celery Tasks

`app/services/tasks.py`:

```python
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task
def send_email_task(to: str, subject: str, body: str):
    # Send email logic
    print(f"Sending email to {to}")
    return {"status": "sent"}

@celery_app.task
def generate_report_task(report_id: str):
    # Generate report logic
    print(f"Generating report {report_id}")
    return {"status": "completed"}

@celery_app.task
def process_image_task(image_url: str):
    # Process image logic
    print(f"Processing image {image_url}")
    return {"status": "processed"}
```

### Use Tasks in Endpoints

`app/api/v1/endpoints/tasks.py`:

```python
from fastapi import APIRouter
from app.services.tasks import send_email_task, generate_report_task

router = APIRouter()

@router.post("/send-email")
def send_email(to: str, subject: str, body: str):
    task = send_email_task.delay(to, subject, body)
    return {"task_id": task.id, "status": "queued"}

@router.post("/generate-report")
def generate_report(report_id: str):
    task = generate_report_task.delay(report_id)
    return {"task_id": task.id, "status": "processing"}

@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }
```

### Run Celery Worker

```bash
celery -A app.services.tasks worker --loglevel=info
```

---

## 6. Real-time Chat API

**Use Case**: WebSocket-based real-time communication

### Generate

```bash
python3 generate_project.py "Chat API" \
  --description "Real-time chat application backend"
```

### Add WebSocket Support

`app/api/v1/endpoints/chat.py`:

```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "room_id": room_id,
                "message": data,
                "timestamp": datetime.utcnow().isoformat()
            }
            await manager.broadcast(json.dumps(message))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## 7. Minimal Serverless API

**Use Case**: AWS Lambda, Google Cloud Functions

### Generate

```bash
python3 generate_project.py "Serverless API" \
  --no-postgres \
  --no-redis \
  --no-docker \
  --description "Lightweight API for serverless deployment"
```

### Add Mangum for AWS Lambda

`requirements.txt`:

```
fastapi==0.115.0
mangum==0.17.0
```

### Lambda Handler

`app/lambda.py`:

```python
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

### Deploy to AWS Lambda

```bash
pip install -r requirements.txt -t package/
cp -r app package/
cd package
zip -r ../lambda.zip .
cd ..
zip -g lambda.zip app/lambda.py

aws lambda update-function-code \
  --function-name my-api \
  --zip-file fileb://lambda.zip
```

---

## 8. Multi-Tenant SaaS Backend

**Use Case**: B2B SaaS application with tenant isolation

### Generate

```bash
python3 generate_project.py "SaaS Platform" \
  --description "Multi-tenant SaaS backend"
```

### Add Tenant Model

`app/db/models/tenant.py`:

```python
from sqlalchemy import Column, String, Boolean, DateTime
from app.db.base import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Tenant Middleware

`app/middleware/tenant.py`:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract tenant from subdomain or header
        host = request.headers.get("host", "")
        subdomain = host.split(".")[0]

        # Fetch tenant
        tenant = db.query(Tenant).filter(Tenant.subdomain == subdomain).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        request.state.tenant = tenant
        response = await call_next(request)
        return response
```

### Tenant-Scoped Queries

```python
@router.get("/users")
def get_users(request: Request, db: Session = Depends(get_db)):
    tenant = request.state.tenant
    users = db.query(User).filter(User.tenant_id == tenant.id).all()
    return users
```

---

## Tips for All Examples

### 1. Environment Configuration

Always configure `.env` before running:

```bash
cp .env.example .env
nano .env
```

### 2. Database Migrations

After adding models:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### 3. Testing

Write tests for all endpoints:

```bash
pytest --cov=app
```

### 4. Code Quality

Format and lint before committing:

```bash
make format
make lint
```

### 5. Docker Development

Use Docker for consistent environments:

```bash
docker-compose up -d
```

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Alembic Migrations](https://alembic.sqlalchemy.org)
- [Celery Documentation](https://docs.celeryproject.org)
- [WebSocket Guide](https://fastapi.tiangolo.com/advanced/websockets/)

---

**Need more examples?** Check the [README](README.md) and [QUICKSTART](QUICKSTART.md) guides!
