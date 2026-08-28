from flask import Blueprint, request, jsonify

from models.skill import Skill
from models.character import Character

from utils.generic_crud import GenericCrud

from flask_jwt_extended import jwt_required, get_jwt_identity


skills_bp = Blueprint(
    'skill',
    __name__,
    url_prefix='/skills'
)

crud = GenericCrud(Skill)


# POST - CRIAR

@skills_bp.route('', methods=['POST'])
@jwt_required()
def create_skill():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Dados inválidos"
            }), 400

        name = data.get('name')
        value = data.get('value')
        character_id = data.get('character_id')

        if not name or value is None or character_id is None:
            return jsonify({
                "error": "Preencha todos os campos obrigatórios"
            }), 400

        if not isinstance(value, int) or not -20 <= value <= 20:
            return jsonify({
                "error": "Valor da perícia deve estar entre -20 e 20"
            }), 400

        current_user_id = int(get_jwt_identity())

        character = Character.query.filter_by(
            id=character_id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Personagem não encontrado"
            }), 404

        skill_data = {
            "name": name,
            "value": value,
            "character_id": character_id
        }

        skill = crud.create(skill_data)

        return jsonify({
            "message": "Perícia criada",
            "id": skill.id
        }), 201

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400


# PUT - ATUALIZAR POR ID

@skills_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_skill(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Dados inválidos"
            }), 400

        current_user_id = int(get_jwt_identity())

        skill = crud.get_by_id(id)

        character = Character.query.filter_by(
            id=skill.character_id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Acesso não autorizado"
            }), 403

        name = data.get('name')
        value = data.get('value')

        if not name or value is None:
            return jsonify({
                "error": "Preencha todos os campos obrigatórios"
            }), 400

        if not isinstance(value, int) or not -20 <= value <= 20:
            return jsonify({
                "error": "Valor da perícia deve estar entre -20 e 20"
            }), 400

        update_data = {
            "name": name,
            "value": value
        }

        skill = crud.update(id, update_data)

        return jsonify({
            "message": "Perícia atualizada",
            "id": skill.id,
            "name": skill.name,
            "value": skill.value
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 404


# DELETE - DELETAR POR ID

@skills_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_skill(id):
    try:
        current_user_id = int(get_jwt_identity())

        skill = crud.get_by_id(id)

        character = Character.query.filter_by(
            id=skill.character_id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Acesso não autorizado"
            }), 403

        crud.delete(id)

        return jsonify({
            "message": "Perícia removida"
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 404