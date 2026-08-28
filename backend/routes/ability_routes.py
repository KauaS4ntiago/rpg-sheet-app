from flask import Blueprint, request, jsonify, send_from_directory

from models.ability import Ability
from models.character import Character

from utils.generic_crud import GenericCrud
from utils.file_upload import save_image, UPLOAD_FOLDER

from flask_jwt_extended import jwt_required, get_jwt_identity


abilities_bp = Blueprint(
    'ability',
    __name__,
    url_prefix='/abilities'
)

crud = GenericCrud(Ability)

# POST - CRIAR HABILIDADE

@abilities_bp.route('', methods=['POST'])
@jwt_required()
def create_ability():

    try:
        data = request.form.to_dict()
        image_file = request.files.get('image')

        current_user_id = int(get_jwt_identity())

        character_id = data.get('character_id')
        name = data.get('name')
        description = data.get('description')

        if not character_id or not name:
            return jsonify({
                "error": "Dados inválidos"
            }), 400

        try:
            character_id = int(character_id)
        except ValueError:
            return jsonify({
                "error": "Personagem inválido"
            }), 400

        character = Character.query.filter_by(
            id=character_id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Personagem não encontrado"
            }), 404

        if image_file:
            data['image'] = save_image(
                image_file,
                subfolder='abilities'
            )

        data['character_id'] = character_id

        ability = crud.create(data)

        return jsonify({
            "message": "Habilidade criada",
            "id": ability.id
        }), 201

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


# PUT - ATUALIZAR HABILIDADE

@abilities_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_ability(id):

    try:
        current_user_id = int(get_jwt_identity())

        ability = crud.get_by_id(id)

        character = Character.query.filter_by(
            id=ability.character_id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Acesso não autorizado"
            }), 403

        data = request.form.to_dict()
        image_file = request.files.get('image')

        if not data and not image_file:
            return jsonify({
                "error": "Dados inválidos"
            }), 400

        name = data.get('name')

        if 'name' in data and not name:
            return jsonify({
                "error": "Nome inválido"
            }), 400

        if image_file:
            data['image'] = save_image(
                image_file,
                subfolder='abilities'
            )

        data.pop('character_id', None)

        ability = crud.update(
            id,
            data
        )

        return jsonify({
            "message": "Habilidade atualizada",
            "id": ability.id,
            "name": ability.name,
            "description": ability.description,
            "image": ability.image
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404

# DELETE - DELETAR HABILIDADE

@abilities_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ability(id):

    try:
        current_user_id = int(get_jwt_identity())

        ability = crud.get_by_id(id)

        character = Character.query.filter_by(
            id=ability.character_id,
            user_id=current_user_id
        ).first()

        if not character:
            return jsonify({
                "error": "Acesso não autorizado"
            }), 403

        crud.delete(id)

        return jsonify({
            "message": "Habilidade removida"
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404

# GET - SERVIR IMAGEM

@abilities_bp.route('/uploads/<path:filename>', methods=['GET'])
def get_ability_image(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )
