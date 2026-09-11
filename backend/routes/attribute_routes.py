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

        current_user_id = int(get_jwt_identity())

  
        attribute = crud.get_by_id(id)


        if not attribute:
            return jsonify({
                "error": "Atributo não encontrado"
            }), 404

 
        character = Character.query.filter_by(
            id=attribute.character_id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Acesso não autorizado"
            }), 403


        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Dados inválidos"
            }), 400


        name = data.get('name')
        value = data.get('value')


        if not isinstance(name, str) or not name.strip():
            return jsonify({
                "error": "Nome do atributo é obrigatório"
            }), 400


        if value is None:
            return jsonify({
                "error": "Valor do atributo é obrigatório"
            }), 400

        if isinstance(value, bool) or not isinstance(value, int):
            return jsonify({
                "error": "Valor do atributo deve ser um número inteiro"
            }), 400

        # O valor permitido para atributos é de -4 até 5
        if not -4 <= value <= 5:
            return jsonify({
                "error": "Valor do atributo deve estar entre -4 e 5"
            }), 400

        # Atualiza somente os campos permitidos
        update_data = {
            "name": name.strip(),
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