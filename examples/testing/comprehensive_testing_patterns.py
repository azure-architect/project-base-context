# Testing Patterns & Best Practices

*Comprehensive testing approaches for Context Engineering + IADPVEC projects.*

```python
"""
Testing patterns that ensure high-quality, maintainable code
following Context Engineering principles.

Key patterns demonstrated:
- Test isolation and independence
- Fixture-based test data management
- Mock/patch strategies for external dependencies
- Performance and integration testing
- Quality gates and coverage requirements
"""

# File: tests/conftest.py
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import app
from src.core.database import get_db, Base
from src.models.user import User
from src.core.security import get_password_hash

# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Provide a clean database session for each test.
    
    Creates fresh tables, yields session, then cleans up.
    This ensures complete test isolation.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables for complete isolation
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session) -> TestClient:
    """
    FastAPI test client with database session override.
    
    Args:
        db_session: Test database session
        
    Returns:
        TestClient: Configured test client
    """
    def override_get_db():
        yield db_session
    
    # Override dependency
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # Clean up override
        app.dependency_overrides.clear()


@pytest.fixture
async def async_client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client for testing async endpoints.
    
    Args:
        db_session: Test database session
        
    Yields:
        AsyncClient: Async HTTP test client
    """
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data() -> dict:
    """
    Sample user data for testing.
    
    Returns:
        dict: User creation data
    """
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "securepassword123"
    }


@pytest.fixture
def authenticated_user(db_session, sample_user_data) -> User:
    """
    Create and return an authenticated test user.
    
    Args:
        db_session: Database session
        sample_user_data: User data fixture
        
    Returns:
        User: Created and persisted user
    """
    user_data = sample_user_data.copy()
    password = user_data.pop("password")
    
    user = User(
        **user_data,
        hashed_password=get_password_hash(password),
        is_active=True,
        is_verified=True,
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def auth_headers(authenticated_user) -> dict:
    """
    Create authentication headers for test requests.
    
    Args:
        authenticated_user: Authenticated user fixture
        
    Returns:
        dict: Headers with bearer token
    """
    from src.core.auth import create_access_token
    
    token = create_access_token(data={"sub": str(authenticated_user.id)})
    return {"Authorization": f"Bearer {token}"}


# File: tests/test_patterns/test_unit_patterns.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from pydantic import ValidationError

from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.services.user_service import UserService
from src.models.user import User


class TestUserSchemas:
    """
    Unit tests for Pydantic schemas.
    
    Tests validation, serialization, and edge cases
    without database dependencies.
    """
    
    def test_user_create_valid_data(self):
        """Test UserCreate schema with valid data."""
        # Arrange
        valid_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "securepassword123"
        }
        
        # Act
        user = UserCreate(**valid_data)
        
        # Assert
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.password == "securepassword123"
    
    def test_user_create_invalid_email(self):
        """Test UserCreate schema with invalid email."""
        # Arrange
        invalid_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "securepassword123"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**invalid_data)
        
        assert "email" in str(exc_info.value)
    
    def test_user_create_short_password(self):
        """Test UserCreate schema with short password."""
        # Arrange
        invalid_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "short"  # Less than 8 characters
        }
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**invalid_data)
        
        assert "password" in str(exc_info.value)
    
    def test_user_update_partial_data(self):
        """Test UserUpdate schema allows partial updates."""
        # Arrange
        partial_data = {"full_name": "Updated Name"}
        
        # Act
        user_update = UserUpdate(**partial_data)
        
        # Assert
        assert user_update.full_name == "Updated Name"
        assert user_update.email is None
        assert user_update.username is None


class TestUserService:
    """
    Unit tests for UserService business logic.
    
    Uses mocking to isolate business logic from database.
    """
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session."""
        return Mock()
    
    @pytest.fixture
    def user_service(self, mock_db_session):
        """UserService instance with mocked database."""
        return UserService(mock_db_session)
    
    async def test_get_user_by_id_success(self, user_service, mock_db_session):
        """Test successful user retrieval by ID."""
        # Arrange
        expected_user = User(id=1, email="test@example.com", username="testuser")
        mock_db_session.query.return_value.filter.return_value.first.return_value = expected_user
        
        # Act
        result = await user_service.get_user_by_id(1)
        
        # Assert
        assert result == expected_user
        mock_db_session.query.assert_called_once_with(User)
    
    async def test_get_user_by_id_not_found(self, user_service, mock_db_session):
        """Test user retrieval when user doesn't exist."""
        # Arrange
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = await user_service.get_user_by_id(999)
        
        # Assert
        assert result is None
    
    @patch('src.services.user_service.get_password_hash')
    async def test_create_user_success(self, mock_hash, user_service, mock_db_session):
        """Test successful user creation."""
        # Arrange
        mock_hash.return_value = "hashed_password"
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="plainpassword"
        )
        
        # Act
        result = await user_service.create_user(user_data)
        
        # Assert
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
        mock_hash.assert_called_once_with("plainpassword")


# File: tests/test_patterns/test_integration_patterns.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import app


class TestHealthEndpointIntegration:
    """
    Integration tests for health check endpoint.
    
    Tests full HTTP request/response cycle including
    middleware, routing, and response formatting.
    """
    
    def test_health_endpoint_success(self, client: TestClient):
        """Test health endpoint returns expected structure."""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
        assert "uptime_seconds" in data
        
        assert data["status"] == "healthy"
        assert isinstance(data["uptime_seconds"], (int, float))
    
    def test_health_endpoint_performance(self, client: TestClient):
        """Test health endpoint response time."""
        import time
        
        # Act
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        # Assert
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < 0.1  # Less than 100ms


class TestUserEndpointIntegration:
    """
    Integration tests for user endpoints.
    
    Tests authentication, authorization, and data persistence
    through the full application stack.
    """
    
    def test_get_user_profile_authenticated(self, client: TestClient, auth_headers: dict):
        """Test authenticated user can retrieve own profile."""
        # Act
        response = client.get("/users/me", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "username" in data
        assert "hashed_password" not in data  # Sensitive data excluded
    
    def test_get_user_profile_unauthenticated(self, client: TestClient):
        """Test unauthenticated request returns 401."""
        # Act
        response = client.get("/users/me")
        
        # Assert
        assert response.status_code == 401
    
    def test_update_user_profile_success(self, client: TestClient, auth_headers: dict):
        """Test successful user profile update."""
        # Arrange
        update_data = {
            "full_name": "Updated Name",
            "bio": "Updated bio"
        }
        
        # Act
        response = client.patch("/users/me", headers=auth_headers, json=update_data)
        
        # Assert
        assert response.status_code == 200
        
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["bio"] == "Updated bio"


# File: tests/test_patterns/test_async_patterns.py
import pytest
import asyncio
from httpx import AsyncClient


class TestAsyncEndpoints:
    """
    Test patterns for async endpoint testing.
    
    Demonstrates proper async test setup and execution
    for async FastAPI endpoints.
    """
    
    @pytest.mark.asyncio
    async def test_async_health_endpoint(self, async_client: AsyncClient):
        """Test health endpoint using async client."""
        # Act
        response = await async_client.get("/health")
        
        # Assert
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, async_client: AsyncClient):
        """Test handling of concurrent requests."""
        # Arrange
        num_requests = 5
        
        # Act - Send multiple concurrent requests
        tasks = [
            async_client.get("/health")
            for _ in range(num_requests)
        ]
        responses = await asyncio.gather(*tasks)
        
        # Assert
        assert len(responses) == num_requests
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"


# File: tests/test_patterns/test_mock_patterns.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio


class TestMockingPatterns:
    """
    Demonstrate effective mocking patterns for testing.
    
    Shows how to mock external dependencies, async functions,
    and database operations.
    """
    
    @patch('src.services.email_service.EmailService.send_email')
    async def test_mock_external_service(self, mock_send_email):
        """Test mocking external email service."""
        # Arrange
        mock_send_email.return_value = {"status": "sent", "message_id": "123"}
        
        from src.services.email_service import EmailService
        email_service = EmailService()
        
        # Act
        result = await email_service.send_welcome_email("test@example.com")
        
        # Assert
        mock_send_email.assert_called_once_with(
            to="test@example.com",
            template="welcome",
            context={}
        )
        assert result["status"] == "sent"
    
    @patch('src.core.redis.Redis')
    async def test_mock_redis_cache(self, mock_redis_class):
        """Test mocking Redis cache operations."""
        # Arrange
        mock_redis = AsyncMock()
        mock_redis_class.return_value = mock_redis
        mock_redis.get.return_value = '{"cached": "data"}'
        
        from src.services.cache_service import CacheService
        cache_service = CacheService()
        
        # Act
        result = await cache_service.get("test_key")
        
        # Assert
        mock_redis.get.assert_called_once_with("test_key")
        assert result == {"cached": "data"}
    
    def test_mock_database_session(self):
        """Test mocking database session operations."""
        # Arrange
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        from src.services.user_service import UserService
        service = UserService(mock_session)
        
        # Act
        result = asyncio.run(service.get_user_by_email("test@example.com"))
        
        # Assert
        assert result is None
        mock_session.query.assert_called_once()


# File: tests/test_patterns/test_performance_patterns.py
import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient


class TestPerformancePatterns:
    """
    Performance testing patterns and benchmarks.
    
    Ensures endpoints meet performance requirements
    and can handle expected load.
    """
    
    def test_endpoint_response_time(self, client: TestClient):
        """Test endpoint meets response time requirements."""
        # Arrange
        max_response_time = 0.1  # 100ms
        
        # Act
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        # Assert
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < max_response_time
    
    def test_concurrent_load(self, client: TestClient):
        """Test endpoint handles concurrent requests."""
        # Arrange
        num_threads = 10
        requests_per_thread = 5
        
        def make_requests():
            responses = []
            for _ in range(requests_per_thread):
                response = client.get("/health")
                responses.append(response.status_code)
            return responses
        
        # Act
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(make_requests) for _ in range(num_threads)]
            results = [future.result() for future in futures]
        
        # Assert
        for thread_results in results:
            assert all(status == 200 for status in thread_results)
    
    @pytest.mark.performance
    def test_memory_usage(self, client: TestClient):
        """Test endpoint memory usage stays within bounds."""
        import psutil
        import os
        
        # Arrange
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Act - Make many requests
        for _ in range(100):
            response = client.get("/health")
            assert response.status_code == 200
        
        # Assert
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 10MB)
        assert memory_increase < 10 * 1024 * 1024
```

## 🎯 **Key Testing Patterns**

### **1. Test Isolation**
- **Fresh database per test**: Prevents test interdependencies
- **Dependency overrides**: Mock external services cleanly
- **Fixture cleanup**: Automatic resource management

### **2. Comprehensive Coverage**
- **Unit tests**: Business logic without external dependencies
- **Integration tests**: Full request/response cycles
- **Performance tests**: Response time and load testing
- **Async tests**: Proper async/await testing patterns

### **3. Effective Mocking**
- **External services**: Email, payment, API integrations
- **Database operations**: Test business logic in isolation
- **Cache systems**: Redis, Memcached mocking
- **Time-based operations**: Freeze time for consistent tests

### **4. Quality Gates**
- **Response time requirements**: Performance thresholds
- **Memory usage limits**: Resource consumption monitoring
- **Concurrent load handling**: Multi-threading tests
- **Error scenario coverage**: Failure mode testing

---

## 🚀 **Usage in IADPVEC**

### **ASSESS Phase**
- **Coverage analysis**: Identify untested code paths
- **Performance baseline**: Current response times and limits
- **Test quality review**: Existing test patterns and gaps

### **PLAN Phase**
- **Test strategy**: Unit, integration, performance test plans
- **Mock strategy**: External dependency isolation approach
- **Coverage targets**: Specific coverage requirements

### **VALIDATE Phase**
- **Run test suite**: Ensure all tests pass
- **Coverage verification**: Meet minimum coverage thresholds
- **Performance validation**: Response time requirements met

---

**These patterns ensure robust, maintainable test suites that support confident refactoring and reliable deployments.**