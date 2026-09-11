import pytest

from database.connection import db
from models.user import User
from models.character import Character

from flask_bcrypt import Bcrypt


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def character_data():
    return {
        "name": "Personagem Teste",
        "current_hp": 20,
        "max_hp": 20,
        "current_sanity": 15,
        "max_sanity": 20,
        "defense": 10,

        "notes": "Personagem criado durante os testes.",

        "attributes": [
            {
                "name": "Força",
                "value": 2
            },
            {
                "name": "Agilidade",
                "value": 3
            },
            {
                "name": "Intelecto",
                "value": 1
            },
            {
                "name": "Presença",
                "value": 2
            },
            {
                "name": "Vigor",
                "value": 4
            }
        ],

        "skills": [
            {
                "name": "Investigação",
                "value": 10
            },
            {
                "name": "Percepção",
                "value": 5
            },
            {
                "name": "Luta",
                "value": 8
            }
        ],

        "abilities": [
            {
                "name": "Ataque Especial",
                "description": "Um ataque poderoso."
            },
            {
                "name": "Defesa Sobrenatural",
                "description": "Aumenta a defesa temporariamente."
            }
        ]
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
        email="second@test.com",
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


# ============================================================
# POST /characters
# ============================================================

def test_create_character_success(
    client,
    auth_headers,
    character_data
):

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "Personagem criado"
    assert "id" in data

    character = db.session.get(
        Character,
        data["id"]
    )

    assert character is not None
    assert character.name == "Personagem Teste"
    assert character.current_hp == 20
    assert character.max_hp == 20
    assert character.current_sanity == 15
    assert character.max_sanity == 20
    assert character.defense == 10

    assert len(character.attributes) == 5
    assert len(character.skills) == 3
    assert len(character.abilities) == 2


def test_create_character_without_authentication(
    client,
    character_data
):

    response = client.post(
        "/characters",
        json=character_data
    )

    assert response.status_code == 401


def test_create_character_without_data(
    client,
    auth_headers
):

    response = client.post(
        "/characters",
        headers=auth_headers
    )

    assert response.status_code == 400


def test_create_character_without_name(
    client,
    auth_headers,
    character_data
):

    character_data.pop("name")

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == (
        "Nome do personagem é obrigatório"
    )


@pytest.mark.parametrize(
    "field",
    [
        "current_hp",
        "max_hp",
        "current_sanity",
        "max_sanity",
        "defense"
    ]
)
def test_create_character_without_required_field(
    client,
    auth_headers,
    character_data,
    field
):

    character_data.pop(field)

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400


# ============================================================
# POST - VALIDAÇÃO DOS CAMPOS NUMÉRICOS
# ============================================================

@pytest.mark.parametrize(
    "field",
    [
        "current_hp",
        "max_hp"
    ]
)
def test_create_character_invalid_hp(
    client,
    auth_headers,
    character_data,
    field
):

    character_data[field] = "vinte"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == "HP inválido"


@pytest.mark.parametrize(
    "field",
    [
        "current_sanity",
        "max_sanity"
    ]
)
def test_create_character_invalid_sanity(
    client,
    auth_headers,
    character_data,
    field
):

    character_data[field] = "vinte"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == "Sanidade inválida"


def test_create_character_invalid_defense(
    client,
    auth_headers,
    character_data
):

    character_data["defense"] = "dez"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == "Defesa inválida"


# ============================================================
# POST - QUANTIDADE DE ATRIBUTOS
# ============================================================

def test_create_character_with_less_than_five_attributes(
    client,
    auth_headers,
    character_data
):

    character_data["attributes"].pop()

    assert len(character_data["attributes"]) == 4

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == (
        "O personagem deve possuir exatamente 5 atributos"
    )


def test_create_character_with_more_than_five_attributes(
    client,
    auth_headers,
    character_data
):

    character_data["attributes"].append({
        "name": "Sorte",
        "value": 2
    })

    assert len(character_data["attributes"]) == 6

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == (
        "O personagem deve possuir exatamente 5 atributos"
    )


def test_create_character_without_attributes(
    client,
    auth_headers,
    character_data
):

    character_data.pop("attributes")

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400


def test_create_character_attributes_not_list(
    client,
    auth_headers,
    character_data
):

    character_data["attributes"] = "atributos"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400


# ============================================================
# POST - VALIDAÇÃO DOS ATRIBUTOS
# ============================================================

def test_create_character_attribute_without_name(
    client,
    auth_headers,
    character_data
):

    character_data["attributes"][0].pop("name")

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == "Atributo inválido"


def test_create_character_attribute_without_value(
    client,
    auth_headers,
    character_data
):

    character_data["attributes"][0].pop("value")

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json["error"] == "Atributo inválido"


@pytest.mark.parametrize(
    "value",
    [-5, 6]
)
def test_create_character_attribute_value_out_of_range(
    client,
    auth_headers,
    character_data,
    value
):

    character_data["attributes"][0]["value"] = value

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == (
        "Valor do atributo deve estar entre -4 e 5"
    )


def test_create_character_attribute_value_not_integer(
    client,
    auth_headers,
    character_data
):

    character_data["attributes"][0]["value"] = "dois"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == (
        "Valor do atributo deve ser um número"
    )


def test_create_character_attribute_not_object(
    client,
    auth_headers,
    character_data
):

    character_data["attributes"][0] = "Força"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400


# ============================================================
# POST - VALIDAÇÃO DAS SKILLS
# ============================================================

def test_create_character_skills_not_list(
    client,
    auth_headers,
    character_data
):

    character_data["skills"] = "skills"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400


def test_create_character_skill_without_name(
    client,
    auth_headers,
    character_data
):

    character_data["skills"][0].pop("name")

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == "Perícia inválida"


def test_create_character_skill_without_value(
    client,
    auth_headers,
    character_data
):

    character_data["skills"][0].pop("value")

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == "Perícia inválida"


@pytest.mark.parametrize(
    "value",
    [-21, 21]
)
def test_create_character_skill_value_out_of_range(
    client,
    auth_headers,
    character_data,
    value
):

    character_data["skills"][0]["value"] = value

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == (
        "Valor da perícia deve estar entre -20 e 20"
    )


def test_create_character_skill_value_not_integer(
    client,
    auth_headers,
    character_data
):

    character_data["skills"][0]["value"] = "dez"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == (
        "Valor da perícia deve ser um número"
    )


def test_create_character_skill_not_object(
    client,
    auth_headers,
    character_data
):

    character_data["skills"][0] = "Investigação"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400


# ============================================================
# POST - VALIDAÇÃO DAS HABILIDADES
# ============================================================

def test_create_character_abilities_not_list(
    client,
    auth_headers,
    character_data
):

    character_data["abilities"] = "abilities"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400


def test_create_character_ability_without_name(
    client,
    auth_headers,
    character_data
):

    character_data["abilities"][0].pop("name")

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == "Habilidade inválida"


def test_create_character_ability_not_object(
    client,
    auth_headers,
    character_data
):

    character_data["abilities"][0] = "Ataque Especial"

    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 400


# ============================================================
# GET /characters
# ============================================================

def test_get_characters_success(
    client,
    auth_headers,
    character_data
):

    create_response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert create_response.status_code == 201

    response = client.get(
        "/characters",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 1

    character = next(
        item
        for item in data
        if item["name"] == "Personagem Teste"
    )

    assert character["current_hp"] == 20
    assert character["max_hp"] == 20
    assert character["current_sanity"] == 15
    assert character["max_sanity"] == 20
    assert character["defense"] == 10

    assert len(character["attributes"]) == 5
    assert len(character["skills"]) == 3
    assert len(character["abilities"]) == 2


def test_get_characters_without_authentication(
    client
):

    response = client.get("/characters")

    assert response.status_code == 401


def test_get_characters_only_returns_authenticated_user_characters(
    client,
    auth_headers,
    second_auth_headers,
    character_data
):

    # Usuário 1 cria personagem
    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    assert response.status_code == 201

    # Usuário 2 cria outro personagem
    second_character_data = character_data.copy()
    second_character_data["name"] = "Personagem do Segundo Usuário"

    # É necessário copiar as listas para não compartilhar
    # estruturas mutáveis entre os dados
    second_character_data["attributes"] = [
        attr.copy()
        for attr in character_data["attributes"]
    ]

    second_character_data["skills"] = [
        skill.copy()
        for skill in character_data["skills"]
    ]

    second_character_data["abilities"] = [
        ability.copy()
        for ability in character_data["abilities"]
    ]

    response = client.post(
        "/characters",
        json=second_character_data,
        headers=second_auth_headers
    )

    assert response.status_code == 201

    # Usuário 1 consulta seus personagens
    response = client.get(
        "/characters",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.get_json()

    names = [
        character["name"]
        for character in data
    ]

    assert "Personagem Teste" in names
    assert "Personagem do Segundo Usuário" not in names


# ============================================================
# GET /characters/<id>
# ============================================================

def test_get_character_success(
    client,
    auth_headers,
    character_data
):

    create_response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = create_response.json["id"]

    response = client.get(
        f"/characters/{character_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == character_id
    assert data["name"] == "Personagem Teste"

    assert len(data["attributes"]) == 5
    assert len(data["skills"]) == 3
    assert len(data["abilities"]) == 2


def test_get_character_without_authentication(
    client
):

    response = client.get("/characters/1")

    assert response.status_code == 401


def test_get_character_not_found(
    client,
    auth_headers
):

    response = client.get(
        "/characters/999999",
        headers=auth_headers
    )

    assert response.status_code == 404

    assert response.json["error"] == (
        "Personagem não encontrado"
    )


def test_user_cannot_get_another_users_character(
    client,
    auth_headers,
    second_auth_headers,
    character_data
):

    # Usuário 1 cria personagem
    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = response.json["id"]

    # Usuário 2 tenta acessar
    response = client.get(
        f"/characters/{character_id}",
        headers=second_auth_headers
    )

    assert response.status_code == 404

    assert response.json["error"] == (
        "Personagem não encontrado"
    )


# ============================================================
# PUT /characters/<id>
# ============================================================

def test_update_character_success(
    client,
    auth_headers,
    character_data
):

    create_response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = create_response.json["id"]

    response = client.put(
        f"/characters/{character_id}",
        data={
            "name": "Personagem Atualizado",
            "current_hp": "10",
            "max_hp": "30",
            "current_sanity": "12",
            "max_sanity": "25",
            "defense": "15",
            "notes": "Notas atualizadas."
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    assert response.json["message"] == (
        "Personagem atualizado"
    )

    character = db.session.get(
        Character,
        character_id
    )

    assert character.name == "Personagem Atualizado"
    assert character.current_hp == 10
    assert character.max_hp == 30
    assert character.current_sanity == 12
    assert character.max_sanity == 25
    assert character.defense == 15
    assert character.notes == "Notas atualizadas."


def test_update_character_without_authentication(
    client
):

    response = client.put(
        "/characters/1",
        data={
            "name": "Atualizado"
        }
    )

    assert response.status_code == 401


def test_update_character_not_found(
    client,
    auth_headers
):

    response = client.put(
        "/characters/999999",
        data={
            "name": "Atualizado"
        },
        headers=auth_headers
    )

    assert response.status_code == 404

    assert response.json["error"] == (
        "Personagem não encontrado"
    )


def test_update_character_without_data(
    client,
    auth_headers,
    character_data
):

    create_response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = create_response.json["id"]

    response = client.put(
        f"/characters/{character_id}",
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == (
        "Dados inválidos"
    )


def test_update_character_invalid_name(
    client,
    auth_headers,
    character_data
):

    create_response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = create_response.json["id"]

    response = client.put(
        f"/characters/{character_id}",
        data={
            "name": ""
        },
        headers=auth_headers
    )

    assert response.status_code == 400

    assert response.json["error"] == "Nome inválido"


@pytest.mark.parametrize(
    "field",
    [
        "current_hp",
        "max_hp",
        "current_sanity",
        "max_sanity",
        "defense"
    ]
)
def test_update_character_invalid_numeric_field(
    client,
    auth_headers,
    character_data,
    field
):

    create_response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = create_response.json["id"]

    response = client.put(
        f"/characters/{character_id}",
        data={
            field: "abc"
        },
        headers=auth_headers
    )

    assert response.status_code == 400

    assert field in response.json["error"]


def test_user_cannot_update_another_users_character(
    client,
    auth_headers,
    second_auth_headers,
    character_data
):

    # Usuário 1 cria
    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = response.json["id"]

    # Usuário 2 tenta atualizar
    response = client.put(
        f"/characters/{character_id}",
        data={
            "name": "Tentativa de invasão"
        },
        headers=second_auth_headers
    )

    assert response.status_code == 404


# ============================================================
# DELETE /characters/<id>
# ============================================================

def test_delete_character_success(
    client,
    auth_headers,
    character_data
):

    create_response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = create_response.json["id"]

    response = client.delete(
        f"/characters/{character_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    assert response.json["message"] == (
        "Personagem removido"
    )

    character = db.session.get(
        Character,
        character_id
    )

    assert character is None


def test_delete_character_without_authentication(
    client
):

    response = client.delete(
        "/characters/1"
    )

    assert response.status_code == 401


def test_delete_character_not_found(
    client,
    auth_headers
):

    response = client.delete(
        "/characters/999999",
        headers=auth_headers
    )

    assert response.status_code == 404

    assert response.json["error"] == (
        "Personagem não encontrado"
    )


def test_user_cannot_delete_another_users_character(
    client,
    auth_headers,
    second_auth_headers,
    character_data
):

    # Usuário 1 cria personagem
    response = client.post(
        "/characters",
        json=character_data,
        headers=auth_headers
    )

    character_id = response.json["id"]

    # Usuário 2 tenta deletar
    response = client.delete(
        f"/characters/{character_id}",
        headers=second_auth_headers
    )

    assert response.status_code == 404

    # Personagem ainda deve existir
    character = db.session.get(
        Character,
        character_id
    )

    assert character is not None


# ============================================================
# GET /characters/uploads/<filename>
# ============================================================

def test_get_character_image_not_found(
    client
):

    response = client.get(
        "/characters/uploads/imagem-que-nao-existe.jpg"
    )

    assert response.status_code == 404