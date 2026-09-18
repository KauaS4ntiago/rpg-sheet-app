import pytest

from database.connection import db

from models.user import User
from models.character import Character
from models.skill import Skill

from flask_bcrypt import Bcrypt


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def skill_data():
    return {
        "name": "Luta",
        "value": 5
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
        email="second_skill@test.com",
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
def test_skill(app, test_character):
    skill = Skill(
        character_id=test_character.id,
        name="Luta",
        value=5
    )

    db.session.add(skill)
    db.session.commit()

    yield skill

    db.session.delete(skill)
    db.session.commit()


@pytest.fixture
def second_user_skill(app, second_user):
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

    skill = Skill(
        character_id=character.id,
        name="Luta",
        value=5
    )

    db.session.add(skill)
    db.session.commit()

    yield skill

    db.session.delete(skill)
    db.session.delete(character)
    db.session.commit()


# ============================================================
# POST /skills
# ============================================================

def test_create_skill_success(
    client,
    auth_headers,
    test_character,
    skill_data
):
    response = client.post(
        "/skills",
        json={
            **skill_data,
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    assert response.json["message"] == "Perícia criada"
    assert "id" in response.json

    skill = db.session.get(
        Skill,
        response.json["id"]
    )

    assert skill is not None
    assert skill.name == "Luta"
    assert skill.value == 5
    assert skill.character_id == test_character.id

    db.session.delete(skill)
    db.session.commit()


def test_create_skill_without_authentication(
    client,
    test_character,
    skill_data
):
    response = client.post(
        "/skills",
        json={
            **skill_data,
            "character_id": test_character.id
        }
    )

    assert response.status_code == 401


def test_create_skill_without_data(
    client,
    auth_headers
):
    response = client.post(
        "/skills",
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == "Dados inválidos"


def test_create_skill_without_name(
    client,
    auth_headers,
    test_character
):
    response = client.post(
        "/skills",
        json={
            "value": 5,
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome da perícia é obrigatório"
    )


def test_create_skill_empty_name(
    client,
    auth_headers,
    test_character
):
    response = client.post(
        "/skills",
        json={
            "name": "",
            "value": 5,
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome da perícia é obrigatório"
    )


def test_create_skill_name_not_string(
    client,
    auth_headers,
    test_character
):
    response = client.post(
        "/skills",
        json={
            "name": 123,
            "value": 5,
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome da perícia é obrigatório"
    )


def test_create_skill_without_value(
    client,
    auth_headers,
    test_character
):
    response = client.post(
        "/skills",
        json={
            "name": "Luta",
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor da perícia é obrigatório"
    )


def test_create_skill_without_character(
    client,
    auth_headers
):
    response = client.post(
        "/skills",
        json={
            "name": "Luta",
            "value": 5
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Personagem é obrigatório"
    )


# ============================================================
# POST - VALIDAÇÃO DO VALOR
# ============================================================

@pytest.mark.parametrize(
    "value",
    [-21, 21]
)
def test_create_skill_value_out_of_range(
    client,
    auth_headers,
    test_character,
    value
):
    response = client.post(
        "/skills",
        json={
            "name": "Luta",
            "value": value,
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor da perícia deve estar entre -20 e 20"
    )


def test_create_skill_value_not_integer(
    client,
    auth_headers,
    test_character
):
    response = client.post(
        "/skills",
        json={
            "name": "Luta",
            "value": "cinco",
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor da perícia deve ser um número inteiro"
    )


def test_create_skill_boolean_value(
    client,
    auth_headers,
    test_character
):
    response = client.post(
        "/skills",
        json={
            "name": "Luta",
            "value": True,
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor da perícia deve ser um número inteiro"
    )


def test_create_skill_min_value(
    client,
    auth_headers,
    test_character
):
    response = client.post(
        "/skills",
        json={
            "name": "Luta",
            "value": -20,
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    skill = db.session.get(
        Skill,
        response.json["id"]
    )

    assert skill.value == -20

    db.session.delete(skill)
    db.session.commit()


def test_create_skill_max_value(
    client,
    auth_headers,
    test_character
):
    response = client.post(
        "/skills",
        json={
            "name": "Luta",
            "value": 20,
            "character_id": test_character.id
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    skill = db.session.get(
        Skill,
        response.json["id"]
    )

    assert skill.value == 20

    db.session.delete(skill)
    db.session.commit()


def test_create_skill_character_not_found(
    client,
    auth_headers
):
    response = client.post(
        "/skills",
        json={
            "name": "Luta",
            "value": 5,
            "character_id": 999999
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json["error"] == (
        "Personagem não encontrado"
    )


# ============================================================
# PUT /skills/<id>
# ============================================================

def test_update_skill_success(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "Luta",
            "value": 10
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["message"] == (
        "Perícia atualizada"
    )

    skill = db.session.get(
        Skill,
        test_skill.id
    )

    assert skill is not None
    assert skill.name == "Luta"
    assert skill.value == 10


def test_update_skill_without_authentication(
    client,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "Luta",
            "value": 10
        }
    )

    assert response.status_code == 401


def test_update_skill_not_found(
    client,
    auth_headers
):
    response = client.put(
        "/skills/999999",
        json={
            "name": "Luta",
            "value": 10
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json["error"] == (
        "Registro não encontrado"
    )


def test_update_skill_without_data(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Dados inválidos"
    )


def test_update_skill_without_name(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "value": 10
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome da perícia é obrigatório"
    )


def test_update_skill_empty_name(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "",
            "value": 10
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome da perícia é obrigatório"
    )


def test_update_skill_name_not_string(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": 123,
            "value": 10
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome da perícia é obrigatório"
    )


def test_update_skill_without_value(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "Luta"
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor da perícia é obrigatório"
    )


# ============================================================
# PUT - VALIDAÇÃO DO VALOR
# ============================================================

@pytest.mark.parametrize(
    "value",
    [-21, 21]
)
def test_update_skill_value_out_of_range(
    client,
    auth_headers,
    test_skill,
    value
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "Luta",
            "value": value
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor da perícia deve estar entre -20 e 20"
    )


def test_update_skill_value_not_integer(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "Luta",
            "value": "dez"
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor da perícia deve ser um número inteiro"
    )


def test_update_skill_boolean_value(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "Luta",
            "value": True
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Valor da perícia deve ser um número inteiro"
    )


def test_update_skill_min_value(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "Luta",
            "value": -20
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["value"] == -20


def test_update_skill_max_value(
    client,
    auth_headers,
    test_skill
):
    response = client.put(
        f"/skills/{test_skill.id}",
        json={
            "name": "Luta",
            "value": 20
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["value"] == 20


# ============================================================
# PUT - SEGURANÇA ENTRE USUÁRIOS
# ============================================================

def test_user_cannot_update_another_users_skill(
    client,
    auth_headers,
    second_auth_headers,
    second_user_skill
):
    response = client.put(
        f"/skills/{second_user_skill.id}",
        json={
            "name": "Luta Alterada",
            "value": 10
        },
        headers=auth_headers
    )

    assert response.status_code == 403
    assert response.json["error"] == (
        "Acesso não autorizado"
    )

    skill = db.session.get(
        Skill,
        second_user_skill.id
    )

    assert skill.name == "Luta"
    assert skill.value == 5


# ============================================================
# DELETE /skills/<id>
# ============================================================

def test_delete_skill_success(
    client,
    auth_headers,
    test_skill
):
    skill_id = test_skill.id

    response = client.delete(
        f"/skills/{skill_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json["message"] == (
        "Perícia removida"
    )

    skill = db.session.get(
        Skill,
        skill_id
    )

    assert skill is None


def test_delete_skill_without_authentication(
    client,
    test_skill
):
    response = client.delete(
        f"/skills/{test_skill.id}"
    )

    assert response.status_code == 401


def test_delete_skill_not_found(
    client,
    auth_headers
):
    response = client.delete(
        "/skills/999999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json["error"] == (
        "Registro não encontrado"
    )


# ============================================================
# DELETE - SEGURANÇA ENTRE USUÁRIOS
# ============================================================

def test_user_cannot_delete_another_users_skill(
    client,
    auth_headers,
    second_auth_headers,
    second_user_skill
):
    skill_id = second_user_skill.id

    response = client.delete(
        f"/skills/{skill_id}",
        headers=auth_headers
    )

    assert response.status_code == 403
    assert response.json["error"] == (
        "Acesso não autorizado"
    )

    skill = db.session.get(
        Skill,
        skill_id
    )

    assert skill is not None
    assert skill.name == "Luta"
    assert skill.value == 5
