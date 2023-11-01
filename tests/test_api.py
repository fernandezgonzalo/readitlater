from fastapi.testclient import TestClient
from api.app import app
from api.dependencies import get_session
from sqlmodel import create_engine, Session
from api.models import Users
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool
from api.routers.auth.utils import get_current_active_user



engine = create_engine("sqlite://",  
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
)
SQLModel.metadata.create_all(engine)

def fake_user():
    user = Users(
        id = 1,
        username = "fakeuser",
        password_hash = "password",
        created = 1698799250,
        disabled = False
    )

    return user

def override_get_session():
    with Session(engine) as session:
        yield session


def override_get_current_active_user():
    user = fake_user()

    return user


def test_read_health():
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}


def test_sites():
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    client = TestClient(app)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwZXBlIiwiZXhwIjoxNjk4NzkwNDQwfQ.3jzDvdTVHEROH7T5w2qh0_7Z6wKFxyhLunkELxT4ZeQ'
    }

    response = client.get('/sites/sites', headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_sites_without_auth():
    client = TestClient(app)
    response = client.get('/sites/sites')
    print(response.json())
    assert response.status_code == 401


def test_create_site():
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    client = TestClient(app)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwZXBlIiwiZXhwIjoxNjk4NzkwNDQwfQ.3jzDvdTVHEROH7T5w2qh0_7Z6wKFxyhLunkELxT4ZeQ'
    }
    payload = {"url": "www.google.com"}

    response = client.post('/sites/sites', headers=headers, json=payload)
    assert response.status_code == 200
    