from flask import Blueprint, request, jsonify

from models.attribute import Attribute
from models.character import Character

from utils.generic_crud import GenericCrud

from flask_jwt_extended import jwt_required, get_jwt_identity


attributes_bp = Blueprint(
    'attribute',
    __name__,
    url_prefix='/attributes'
)

crud = GenericCrud(Attribute)


# PUT - ATUALIZAR ATRIBUTO POR ID

@attributes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_attribute(id):

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Dados inválidos"
            }), 400

        current_user_id = int(get_jwt_identity())

        attribute = crud.get_by_id(id)

        # Verifica se o personagem pertence ao usuário autenticado
        character = Character.query.filter_by(
            id=attribute.character_id,
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

        if not isinstance(value, int) or not -4 <= value <= 5:
            return jsonify({
                "error": "Valor do atributo deve estar entre -4 e 5"
            }), 400

        update_data = {
            "name": name,
            "value": value
        }

        attribute = crud.update(
            id,
            update_data
        )

        return jsonify({
            "message": "Atributo atualizado",
            "id": attribute.id,
            "name": attribute.name,
            "value": attribute.value
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404