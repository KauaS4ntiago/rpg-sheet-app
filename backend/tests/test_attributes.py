import pytest

from database.connection import db

from models.user import User

from models.character import Character

from models.attribute import Attribute

from flask_bcrypt import Bcrypt


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def attribute_data():
    return {
        "name": "Força",
        "value": 2
    }


@pytest.fixture
def second_user(app):
    """
    Cria um segundo usuário para testar
    isolamento entre usuários.
    """
    bcrypt = Bcrypt()

    user = User(
        name="Segundo Usuário",
        email="second_attribute@test.com",
        password=bcrypt.generate_password_hash(
            "12345678"
        ).decode("utf-8")
    )

    db.session.add(user)
    db.session.commit()

    yield {
        "user": user,
        "password": "12345678"
    }

    db.session.delete(user)
    db.session.commit()


@pytest.fixture
def second_auth_headers(client, second_user):
    response = client.post(
        "/auth/login",
        json={
            "email": second_user["user"].email,
            "password": second_user["password"]
        }
    )

    return {
        "Authorization": f"Bearer {response.json['token']}"
    }


@pytest.fixture
def test_character(app, test_adm):
    character = Character(
        user_id=test_adm["user"].id,
        name="Personagem Teste",
        current_hp=20,
        max_hp=20,
        current_sanity=15,
        max_sanity=20,
        defense=10,
        notes="Personagem criado durante os testes."
    )

    db.session.add(character)
    db.session.commit()

    yield character

    db.session.delete(character)
    db.session.commit()


@pytest.fixture
def test_attribute(app, test_character):
    attribute = Attribute(
        character_id=test_character.id,
        name="Força",
        value=2
    )

    db.session.add(attribute)
    db.session.commit()

    yield attribute

    db.session.delete(attribute)
    db.session.commit()


@pytest.fixture
def second_user_attribute(app, second_user):
    character = Character(
        user_id=second_user["user"].id,
        name="Personagem do Segundo Usuário",
        current_hp=20,
        max_hp=20,
        current_sanity=15,
        max_sanity=20,
        defense=10,
        notes="Personagem do segundo usuário."
    )

    db.session.add(character)
    db.session.commit()

    attribute = Attribute(
        character_id=character.id,
        name="Força",
        value=2
    )

    db.session.add(attribute)
    db.session.commit()

    yield attribute

    db.session.delete(attribute)
    db.session.delete(character)
    db.session.commit()


# ============================================================
# PUT /attributes/<id>
# ============================================================

def test_update_attribute_success(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "Força",
            "value": 4
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["message"] == (
        "Atributo atualizado"
    )

    attribute = db.session.get(
        Attribute,
        test_attribute.id
    )

    assert attribute is not None
    assert attribute.name == "Força"
    assert attribute.value == 4


def test_update_attribute_without_authentication(
    client,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "Força",
            "value": 4
        }
    )

    assert response.status_code == 401


def test_update_attribute_not_found(
    client,
    auth_headers
):

    response = client.put(
        "/attributes/999999",
        json={
            "name": "Força",
            "value": 4
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json["error"] == (
        "Registro não encontrado"
    )


def test_update_attribute_without_data(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Dados inválidos"
    )


def test_update_attribute_without_name(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "value": 4
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome do atributo é obrigatório"
    )


def test_update_attribute_empty_name(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "",
            "value": 4
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome do atributo é obrigatório"
    )


def test_update_attribute_name_not_string(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": 123,
            "value": 4
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome do atributo é obrigatório"
    )


def test_update_attribute_without_value(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "Força"
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor do atributo é obrigatório"
    )


# ============================================================
# PUT - VALIDAÇÃO DO VALOR
# ============================================================

@pytest.mark.parametrize(
    "value",
    [-5, 6]
)
def test_update_attribute_value_out_of_range(
    client,
    auth_headers,
    test_attribute,
    value
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "Força",
            "value": value
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor do atributo deve estar entre -4 e 5"
    )


def test_update_attribute_value_not_integer(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "Força",
            "value": "dois"
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor do atributo deve ser um número inteiro"
    )


def test_update_attribute_boolean_value(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "Força",
            "value": True
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor do atributo deve ser um número inteiro"
    )


def test_update_attribute_min_value(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "Força",
            "value": -4
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["value"] == -4


def test_update_attribute_max_value(
    client,
    auth_headers,
    test_attribute
):

    response = client.put(
        f"/attributes/{test_attribute.id}",
        json={
            "name": "Força",
            "value": 5
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["value"] == 5


# ============================================================
# PUT - SEGURANÇA ENTRE USUÁRIOS
# ============================================================

def test_user_cannot_update_another_users_attribute(
    client,
    auth_headers,
    second_auth_headers,
    second_user_attribute
):

    response = client.put(
        f"/attributes/{second_user_attribute.id}",
        json={
            "name": "Força Alterada",
            "value": 5
        },
        headers=auth_headers
    )

    assert response.status_code == 403
    assert response.json["error"] == (
        "Acesso não autorizado"
    )

    # Atributo não deve ter sido alterado
    attribute = db.session.get(
        Attribute,
        second_user_attribute.id
    )

    assert attribute.name == "Força"
    assert attribute.value == 2