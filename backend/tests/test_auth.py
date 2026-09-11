import pytest

from models.user import User

from flask_bcrypt import Bcrypt


# ============================================================
# LOGIN
# ============================================================

def test_login_success(client, test_adm):
    json = {
        "email": test_adm["user"].email,
        "password": test_adm["password"]
    }

    response = client.post("/auth/login", json=json)

    assert response.status_code == 200
    assert response.json["message"] == "Acesso permitido"
    assert response.json["token"]


def test_login_wrong_password(client, test_adm):
    json = {
        "email": test_adm["user"].email,
        "password": "87654321"
    }

    response = client.post("/auth/login", json=json)

    assert response.status_code == 401
    assert response.json["error"] == "Dados inválidos"


def test_login_wrong_email(client, test_adm):
    json = {
        "email": "wrong@email.com",
        "password": test_adm["password"]
    }

    response = client.post("/auth/login", json=json)

    assert response.status_code == 401
    assert response.json["error"] == "Dados inválidos"


# ============================================================
# LOGIN - VALIDAÇÃO DOS CAMPOS
# ============================================================

def test_login_password_less(client, test_adm):
    json = {
        "email": test_adm["user"].email,
        "password": "123"
    }

    response = client.post("/auth/login", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Senha inválida"


def test_login_invalid_email(client, test_adm):
    json = {
        "email": "wrongemail",
        "password": test_adm["password"]
    }

    response = client.post("/auth/login", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Email inválido"


def test_login_without_data(client):
    json = {}

    response = client.post("/auth/login", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Dados vazios"


def test_login_missing_password(client, test_adm):
    json = {
        "email": test_adm["user"].email
    }

    response = client.post("/auth/login", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Dados incompletos"


def test_login_missing_email(client, test_adm):
    json = {
        "password": test_adm["password"]
    }

    response = client.post("/auth/login", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Dados incompletos"


# ============================================================
# REGISTER
# ============================================================

def test_register_success(client):
    bcrypt = Bcrypt()

    json = {
        "name": "test_user",
        "email": "test@email.com",
        "password": "12345678"
    }

    response = client.post("/auth/register", json=json)

    user = User.query.filter_by(email="test@email.com").first()

    assert response.status_code == 201
    assert response.json["message"] == "Usuário criado"
    assert response.json["token"]
    assert user.name == "test_user"
    assert bcrypt.check_password_hash(user.password, json["password"])


def test_register_existing_user(client, test_adm):
    json = {
        "name": test_adm["user"].name,
        "email": test_adm["user"].email,
        "password": test_adm["password"]
    }

    response = client.post("/auth/register", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Usuário já cadastrado"


# ============================================================
# REGISTER - VALIDAÇÃO DOS CAMPOS
# ============================================================

def test_register_password_less(client):
    json = {
        "name": "test_user",
        "email": "test@email.com",
        "password": "123"
    }

    response = client.post("/auth/register", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Senha inválida"


def test_register_invalid_email(client):
    json = {
        "name": "test_user",
        "email": "wrongemail",
        "password": "12345678"
    }

    response = client.post("/auth/register", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Email inválido"


def test_register_without_data(client):
    json = {}

    response = client.post("/auth/register", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Dados vazios"


def test_register_missing_fields(client):
    json = {
        "password": "12345678"
    }

    response = client.post("/auth/register", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Dados incompletos"


def test_register_missing_name(client):
    json = {
        "email": "test@email.com",
        "password": "12345678"
    }

    response = client.post("/auth/register", json=json)

    assert response.status_code == 400
    assert response.json["error"] == "Dados incompletos"