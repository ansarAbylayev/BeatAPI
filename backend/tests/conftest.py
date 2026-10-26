import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import create_engine,  SQLModel, Session
from app.database import get_session
from sqlalchemy import StaticPool


@pytest.fixture
def client():
    return TestClient(app)


test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass= StaticPool)
SQLModel.metadata.create_all(test_engine)
def get_test_session():
    with Session(test_engine) as session:
        yield session
app.dependency_overrides[get_session] = get_test_session