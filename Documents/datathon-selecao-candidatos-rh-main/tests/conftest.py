from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from datathon.app import app
from datathon.db.database import get_session
from datathon.db.models import User, table_registry
from datathon.dependencies.security import get_current_user, get_password_hash
from datathon.schemas import UserPublic


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def client_without_db():
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


@pytest.fixture
def auth_headers(token):
    """
    Retorna headers com token Bearer pronto para usar nos testes.
    """
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def client_with_auth(session, user):
    """
    TestClient que sobrescreve get_session e get_current_user
    para simular autenticação sem precisar da rota /auth/token.
    """
    def get_session_override():
        return session

    def get_current_user_override():
        # Retorna o usuário mock direto
        return UserPublic.model_validate(user)

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def client_with_auth(client):
    # Sobrescreve get_current_user para simular autenticação
    def override_current_user():
        class MockUser:
            id = 1
            email = "teste@teste.com"
        return MockUser()

    from datathon.routers.predict import get_current_user
    client.app.dependency_overrides[get_current_user] = override_current_user
    yield client
    client.app.dependency_overrides.clear()
