from flask import Blueprint, request, jsonify
from models.user import User
from utils.generic_crud import GenericCrud
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
import jwt
import datetime

auth_bp = Blueprint('auth',__name__,url_prefix='/auth')

crud = GenericCrud(User)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:

        data = request.get_json()
        existing_user = User.query.filter_by(email=data['email']).first()
        
        if existing_user:
            return jsonify({
                "error": "Usuário já cadastrado"
            }), 400

        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = crud.create(data)
        
        token = create_access_token(identity=str(user.id))
        
        return jsonify({
            "message": "Usuário criado",
            "token": token,
            "user_id": user.id
        }), 201

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
    
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()    
        
        if not user:
            return jsonify({
                "error": "Usuário não encontrado"
            }), 400
        
        authentication = bcrypt.check_password_hash(user.password, data['password'])
        
        if authentication:
            token = create_access_token(identity=str(user.id))
            return jsonify({
                "message": "Acesso permitido",
                "token": token,
                "user_id": user.id
            }), 200
        
        return jsonify({
            "error": "Acesso negado"
        }), 400
        
    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400