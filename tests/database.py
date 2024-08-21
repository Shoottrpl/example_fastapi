import pytest
# from alembic import command
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app

from app.config import settings

SQLALCHEMY_DATABASE_URL = (f"postgresql://"
                           f"{settings.db_user}:{settings.db_pass}@{settings.db_host}/test_{settings.db_name}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # run code before run test
    # command.upgrade("head")
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run code after test finish
    # command.downgrade("base")