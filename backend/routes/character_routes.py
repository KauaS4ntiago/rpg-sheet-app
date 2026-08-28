from flask import Blueprint, request, jsonify, send_from_directory

from database.connection import db

from models.character import Character
from models.attribute import Attribute
from models.skill import Skill
from models.ability import Ability

from utils.generic_crud import GenericCrud
from utils.file_upload import save_image, UPLOAD_FOLDER

from flask_jwt_extended import jwt_required, get_jwt_identity


characters_bp = Blueprint(
    'character',
    __name__,
    url_prefix='/characters'
)

crud = GenericCrud(Character)


# POST - CRIAR PERSONAGEM

@characters_bp.route('', methods=['POST'])
@jwt_required()
def create_character():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Dados inválidos"
            }), 400

        current_user_id = int(get_jwt_identity())

        attributes = data.pop('attributes', [])
        skills = data.pop('skills', [])
        abilities = data.pop('abilities', [])

        name = data.get('name')
        current_hp = data.get('current_hp')
        max_hp = data.get('max_hp')
        current_sanity = data.get('current_sanity')
        max_sanity = data.get('max_sanity')
        defense = data.get('defense')

        # Validação dos campos obrigatórios
        if not name:
            return jsonify({
                "error": "Nome do personagem é obrigatório"
            }), 400

        if (
            current_hp is None or
            max_hp is None or
            current_sanity is None or
            max_sanity is None or
            defense is None
        ):
            return jsonify({
                "error": "Todos os campos obrigatórios devem ser preenchidos"
            }), 400

        # Validação dos tipos
        if (
            not isinstance(current_hp, int) or
            not isinstance(max_hp, int)
        ):
            return jsonify({
                "error": "HP inválido"
            }), 400

        if (
            not isinstance(current_sanity, int) or
            not isinstance(max_sanity, int)
        ):
            return jsonify({
                "error": "Sanidade inválida"
            }), 400

        if not isinstance(defense, int):
            return jsonify({
                "error": "Defesa inválida"
            }), 400

        # O usuário vem do JWT, não do JSON
        data['user_id'] = current_user_id

        character = crud.create(data)

        for attr in attributes:

            attr_name = attr.get('name')
            attr_value = attr.get('value')

            if not attr_name or attr_value is None:
                raise ValueError("Atributo inválido")

            if (
                not isinstance(attr_value, int) or
                not -4 <= attr_value <= 5
            ):
                raise ValueError(
                    "Valor do atributo deve estar entre -4 e 5"
                )

            attribute = Attribute(
                name=attr_name,
                value=attr_value,
                character_id=character.id
            )

            db.session.add(attribute)


        for skill in skills:

            skill_name = skill.get('name')
            skill_value = skill.get('value')

            if not skill_name or skill_value is None:
                raise ValueError("Perícia inválida")

            if (
                not isinstance(skill_value, int) or
                not -20 <= skill_value <= 20
            ):
                raise ValueError(
                    "Valor da perícia deve estar entre -20 e 20"
                )

            skill_obj = Skill(
                name=skill_name,
                value=skill_value,
                character_id=character.id
            )

            db.session.add(skill_obj)

        for ability in abilities:

            ability_name = ability.get('name')

            if not ability_name:
                raise ValueError("Habilidade inválida")

            ability_obj = Ability(
                name=ability_name,
                description=ability.get('description'),
                image=ability.get('image'),
                character_id=character.id
            )

            db.session.add(ability_obj)

        db.session.commit()

        return jsonify({
            "message": "Personagem criado",
            "id": character.id
        }), 201

    except ValueError as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 400


# GET - LISTAR PERSONAGENS DO USUÁRIO AUTENTICADO

@characters_bp.route('', methods=['GET'])
@jwt_required()
def get_characters():

    current_user_id = int(get_jwt_identity())

    characters = Character.query.filter_by(
        user_id=current_user_id
    ).all()

    return jsonify([
        {
            "id": character.id,
            "name": character.name,
            "current_hp": character.current_hp,
            "max_hp": character.max_hp,
            "current_sanity": character.current_sanity,
            "max_sanity": character.max_sanity,
            "defense": character.defense,
            "image": character.image,
            "notes": character.notes,

            "attributes": [
                {
                    "id": attr.id,
                    "name": attr.name,
                    "value": attr.value
                }
                for attr in character.attributes
            ],

            "skills": [
                {
                    "id": skill.id,
                    "name": skill.name,
                    "value": skill.value
                }
                for skill in character.skills
            ],

            "abilities": [
                {
                    "id": ability.id,
                    "image": ability.image,
                    "name": ability.name,
                    "description": ability.description
                }
                for ability in character.abilities
            ]
        }
        for character in characters
    ]), 200

# GET - RETORNAR PERSONAGEM POR ID

@characters_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_character(id):

    current_user_id = int(get_jwt_identity())

    character = Character.query.filter_by(
        id=id,
        user_id=current_user_id
    ).first()

    if not character:
        return jsonify({
            "error": "Personagem não encontrado"
        }), 404

    return jsonify({
        "id": character.id,
        "name": character.name,
        "current_hp": character.current_hp,
        "max_hp": character.max_hp,
        "current_sanity": character.current_sanity,
        "max_sanity": character.max_sanity,
        "defense": character.defense,
        "image": character.image,
        "notes": character.notes,

        "attributes": [
            {
                "id": attr.id,
                "name": attr.name,
                "value": attr.value
            }
            for attr in character.attributes
        ],

        "skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "value": skill.value
            }
            for skill in character.skills
        ],

        "abilities": [
            {
                "id": ability.id,
                "image": ability.image,
                "name": ability.name,
                "description": ability.description
            }
            for ability in character.abilities
        ]
    }), 200


# PUT - ATUALIZAR PERSONAGEM

@characters_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_character(id):

    try:
        current_user_id = int(get_jwt_identity())

        character = Character.query.filter_by(
            id=id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Personagem não encontrado"
            }), 404

        data = request.form.to_dict()
        image_file = request.files.get('image')

        if not data and not image_file:
            return jsonify({
                "error": "Dados inválidos"
            }), 400

        allowed_fields = {
            "name",
            "current_hp",
            "max_hp",
            "current_sanity",
            "max_sanity",
            "defense",
            "notes"
        }

        update_data = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        if "name" in update_data and not update_data["name"]:
            return jsonify({
                "error": "Nome inválido"
            }), 400

        numeric_fields = {
            "current_hp",
            "max_hp",
            "current_sanity",
            "max_sanity",
            "defense"
        }

        for field in numeric_fields:

            if field in update_data:

                try:
                    update_data[field] = int(update_data[field])

                except ValueError:
                    return jsonify({
                        "error": f"{field} inválido"
                    }), 400

        if image_file:

            update_data['image'] = save_image(
                image_file,
                subfolder='characters'
            )

        character = crud.update(
            id,
            update_data
        )

        return jsonify({
            "message": "Personagem atualizado",
            "id": character.id
        }), 200

    except ValueError as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 400


# DELETE - DELETAR PERSONAGEM

@characters_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_character(id):

    try:
        current_user_id = int(get_jwt_identity())

        character = Character.query.filter_by(
            id=id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Personagem não encontrado"
            }), 404

        crud.delete(id)

        return jsonify({
            "message": "Personagem removido"
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404


# GET - SERVIR IMAGEM DO PERSONAGEM

@characters_bp.route('/uploads/<path:filename>', methods=['GET'])
def get_character_image(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )