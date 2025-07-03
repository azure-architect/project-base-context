# FastAPI Project Structure Example

*Demonstrating clean, scalable FastAPI application organization following Context Engineering + IADPVEC principles.*

```python
"""
Example FastAPI project structure that follows established patterns
for maintainable, testable, and scalable web applications.

This structure is designed to support:
- Clean separation of concerns
- Easy testing and mocking
- Scalable team development
- Clear dependency management
- Proper configuration handling
"""

# File: src/main.py
from datetime import datetime
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import get_settings
from .core.database import engine, get_db
from .api import health, users, auth
from .core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown tasks."""
    # Startup tasks
    app.state.startup_time = datetime.utcnow()
    setup_logging()
    
    # Yield control to the application
    yield
    
    # Shutdown tasks
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Application factory pattern for creating FastAPI instances.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    )
    
    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(auth.router, prefix="/auth", tags=["authentication"])
    app.include_router(users.router, prefix="/users", tags=["users"])
    
    return app


# Create the app instance
app = create_app()
```

## 🎯 **Key Patterns Demonstrated**

### **1. Clean Architecture**
- **Separation of Concerns**: API, business logic, data access clearly separated
- **Dependency Injection**: Database sessions and services injected as dependencies
- **Service Layer**: Business logic encapsulated in service classes
- **Factory Pattern**: Application factory for flexible configuration

### **2. FastAPI Best Practices**
- **Pydantic Schemas**: Input validation and response serialization
- **Router Organization**: Logical grouping of related endpoints
- **Dependency System**: Leveraging FastAPI's dependency injection
- **Lifecycle Management**: Proper startup/shutdown handling

### **3. Database Patterns**
- **SQLAlchemy ORM**: Declarative models with relationships
- **Session Management**: Proper session lifecycle handling
- **Migration Ready**: Structure supports Alembic migrations
- **Connection Pooling**: Configured for production use

### **4. Testing Excellence**
- **Test Isolation**: Each test gets fresh database
- **Fixture Pattern**: Reusable test data and setup
- **Dependency Override**: Mock external dependencies
- **AAA Pattern**: Arrange, Act, Assert test structure

### **5. Configuration Management**
- **Environment Variables**: Secure configuration handling
- **Settings Validation**: Pydantic ensures valid configuration
- **Environment Specific**: Different settings per environment
- **Cached Settings**: Performance optimization

---

## 🚀 **Usage in Context Engineering**

### **As Reference Pattern**
When implementing new features, reference this structure:
- **New endpoints**: Follow the router → service → model pattern
- **New models**: Use the User model as template for relationships and constraints
- **New services**: Follow UserService pattern for business logic encapsulation
- **New tests**: Use the test patterns for comprehensive coverage

### **In INITIAL.md Requests**
```markdown
## EXAMPLES:
- examples/architecture/fastapi_structure.py - Follow this overall structure
- examples/architecture/fastapi_structure.py (UserService class) - Service layer pattern
- examples/architecture/fastapi_structure.py (test patterns) - Testing approach
```

### **IADPVEC Integration**
- **INGEST**: Reference this structure when analyzing project requirements
- **ASSESS**: Compare current implementation against these patterns
- **DISCUSS**: Propose solutions following these architectural principles
- **PLAN**: Use these patterns as building blocks for implementation plans
- **VALIDATE**: Ensure implementations follow these structural guidelines

---

**This structure provides a solid foundation for scalable FastAPI applications while maintaining clean architecture principles and comprehensive testing coverage.**