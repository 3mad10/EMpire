import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, StaticPool
from unittest.mock import Mock
from uuid import uuid4
from sqlmodel import SQLModel
from smart_solutions.app.schemas.solution import SolutionCreate, ImageCreate, VideoCreate
from smart_solutions.app.api.routes.solutions import router
from smart_solutions.app.api.deps import get_session, get_current_user
from smart_solutions.app.core.config import settings
from smart_solutions.app.models.solution import Solution, Image, Video, Tag, SolutionTagLink
from smart_solutions.app.models.user import User
from smart_solutions.app.models.solution import Solution


# ----------------------
# Test app + DB setup
# ----------------------
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


# ----------------------
# Fixtures
# ----------------------
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def mock_current_user():
    return User(
        id=uuid4(),
        email="test@example.com",
        name="test_user",
        password="not_a_real_hash"
    )

@pytest.fixture
def sample_solution_create():
    return {
        "name": "Test Solution",
        "description": "Test Description",
        "tags": ["technology", "innovation"],
        "images": [{"url": "http://example.com/img.jpg", "name": "test.jpg"}],
        "videos": [{"url": "http://example.com/vid.mp4", "name": "test.mp4"}]
    }
