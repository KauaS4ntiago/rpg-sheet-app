from flask import Blueprint, request, jsonify
from models.user import User
from utils.generic_crud import GenericCrud
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt


users_bp = Blueprint(
    'user',
    __name__,
    url_prefix='/users'
)

crud = GenericCrud(User)
bcrypt = Bcrypt()


# GET ONE - RETORNAR USUÁRIO AUTENTICADO

@users_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != id:
            return jsonify({
                "error": "Acesso não autorizado"
            }), 403

        user = crud.get_by_id(id)

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 404


# PUT - ATUALIZAR USUÁRIO

@users_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != id:
            return jsonify({
                "error": "Acesso não autorizado"
            }), 403

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Dados inválidos"
            }), 400

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({
                "error": "Nome e email são obrigatórios"
            }), 400

        if '@' not in email or '.' not in email:
            return jsonify({
                "error": "Email inválido"
            }), 400

        user = crud.get_by_id(id)

        # Verifica se o email já pertence a outro usuário
        existing_user = User.query.filter(
            User.email == email,
            User.id != id
        ).first()

        if existing_user:
            return jsonify({
                "error": "Email já cadastrado"
            }), 409

        update_data = {
            "name": name,
            "email": email
        }

        user = crud.update(id, update_data)

        return jsonify({
            "message": "Usuário atualizado",
            "id": user.id
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400


# DELETE - DELETAR USUÁRIO

@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != id:
            return jsonify({
                "error": "Acesso não autorizado"
            }), 403

        crud.delete(id)

        return jsonify({
            "message": "Usuário removido"
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 404
