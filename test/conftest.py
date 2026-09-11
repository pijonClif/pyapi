from fastapi.testclient import TestClient

from alembic import command

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.main import app
from app.config import settings
from app.oauth2 import create_access_token
from app.database import get_db, Base
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine=create_engine(SQLALCHEMY_DATABASE_URL)
#engine=create_async_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)
#SessionLocal=async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    #command.downgrade("downgrade")
    #command.upgrade("head")

    db=TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data={
        "email": "test123@mail.com",
        "password": "abc123"
    }
    res=client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data={
        "email": "test456@mail.com",
        "password": "abc123"
    }
    res=client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorised_client(client, token):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data=[{
        "title": "title 1",
        "content": "content 1",
        "owner_id": test_user['id']
    }, {
        "title": "title 2",
        "content": "content 2",
        "owner_id": test_user['id']
    }, {
        "title": "title 3",
        "content": "content 3",
        "owner_id": test_user['id']
    }, {
        "title": "title 4",
        "content": "content 4",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts