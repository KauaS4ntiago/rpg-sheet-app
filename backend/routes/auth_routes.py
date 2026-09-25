from flask import Blueprint, request, jsonify
from models.user import User
from utils.generic_crud import GenericCrud
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth',__name__,url_prefix='/auth')

crud = GenericCrud(User)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:

        data = request.get_json()
        
        if not data:
                return jsonify({
                    "error": "Dados vazios"
            }), 400   
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not name or not email or not password: 
            return jsonify({
                "error": "Dados incompletos"
            }), 400
                        
        if '@' not in email: 
            return jsonify({
                "error": "Email inválido, tente novamente."
            }), 400
        
        if len(password) < 8:
            return jsonify({
                "error": "A senha deve conter no mínimo 8 digitos, tente novamente."
            }), 400
        
        
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            return jsonify({
                "error": "Usuário já cadastrado com esse email."
            }), 400

        data['password'] = bcrypt.generate_password_hash(password).decode('utf-8')
        user = crud.create(data)
        
        token = create_access_token(identity=str(user.id))
        
        return jsonify({
            "message": "Cadastro realizado com sucesso!",
            "token": token,
            "user_id": user.id
        }), 201

    except ValueError:

        return jsonify({
            "error": "Ocorreu um erro, tente novamente mais tarde."
        }), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
    
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Dados vazios"
        }), 400 
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password: 
            return jsonify({
                    "error": "Dados incompletos"
            }), 400
            
        if '@' not in email or '.com' not in email: 
            return jsonify({
                "error": "Email inválido"
            }), 400
        
        if len(password) < 8:
            return jsonify({
                "error": "Senha inválida"
            }), 400
            
        user = User.query.filter_by(email=email).first()    
        
        if not user:
            return jsonify({
                "error": "Dados inválidos"
            }), 401
        
        authentication = bcrypt.check_password_hash(user.password, password)
        
        if authentication:
            token = create_access_token(identity=str(user.id))
            return jsonify({
                "message": "Acesso permitido",
                "token": token,
                "user_id": user.id
            }), 200
        
        return jsonify({
            "error": "Dados inválidos"
        }), 401
        
    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400