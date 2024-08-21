import pytest
# from alembic import command
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app

from app.config import settings
from app.oauth2 import create_access_token
from app import models

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


@pytest.fixture
def test_user(client):
    user_data = {"email": "test6@mail.com",
                 "password": "1337"}
    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test62@mail.com",
                 "password": "1337"}
    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def create_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "test1",
        "content": "test_content_1",
        "user_id": test_user["id"]
    },
        {
            "title": "test2",
            "content": "test_content_2",
            "user_id": test_user["id"]
        },
        {
            "title": "test3",
            "content": "test_content_3",
            "user_id": test_user["id"]
        },
        {
            "title": "test1",
            "content": "test_content_1",
            "user_id": test_user2["id"]
        }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
