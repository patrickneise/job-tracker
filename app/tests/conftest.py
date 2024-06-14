import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def job_payload():
    return {
        "id": 1,
        "company": "Netflix",
        "title": "Chief Technology Officer",
        "description": "CTO at Netflix",
        "posting": "https://www.netflix.com/posting/1",
        "website": "https://www.netflix.com/",
        "status": "watching",
    }


@pytest.fixture()
def jobs_payload():
    return [
        {
            "id": 1,
            "company": "Netflix",
            "title": "Chief Technology Officer",
            "description": "CTO at Netflix",
            "posting": "https://www.netflix.com/posting/1",
            "website": "https://www.netflix.com/",
            "status": "watching",
        },
        {
            "id": 2,
            "company": "GitHub",
            "title": "VP, Engineering",
            "description": "VP of Eng at GitHub",
            "posting": "https://www.github.com.com/posting/1",
            "website": "https://www.github.com/",
            "status": "applied",
        },
    ]


@pytest.fixture()
def interview_payload():
    return {
        "id": 1,
        "start": "2024-06-12T18:57:19.274000",
        "stop": "2024-06-12T18:57:19.274000",
        "details": "Interview at Netflix",
        "url": "https://www.zoom.com/meeting/1",
    }


@pytest.fixture()
def interviews_payload():
    return [
        {
            "id": 1,
            "start": "2024-06-12T18:57:19.274000",
            "stop": "2024-06-12T18:57:19.274000",
            "details": "Interview at Netflix",
            "url": "https://www.zoom.com/meeting/1",
        },
        {
            "id": 2,
            "start": "2024-07-12T18:57:19.274000",
            "stop": "2024-07-12T18:57:19.274000",
            "details": "Follow UP Interview at Netflix",
            "url": "https://www.zoom.com/meeting/2",
        },
    ]
