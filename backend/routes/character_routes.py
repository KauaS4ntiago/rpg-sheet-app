from flask import Blueprint, request, jsonify, send_from_directory
from database.connection import db
from models.ability import Ability
from models.attribute import Attribute
from models.skill import Skill
from models.character import Character
from utils.generic_crud import GenericCrud
from utils.file_upload import save_image, UPLOAD_FOLDER
from flask_jwt_extended import jwt_required

characters_bp = Blueprint('character',__name__,url_prefix='/characters')

crud = GenericCrud(Character)

#POST - CRIAR
@characters_bp.route('', methods=['POST'])
@jwt_required()
def create_character():
    try:
        data = request.get_json()

        attributes = data.pop('attributes', [])
        skills = data.pop('skills', [])
        abilities = data.pop('abilities', [])

        character = crud.create(data)

        for attr in attributes:
            attr['character_id'] = character.id
            attribute = Attribute(**attr)
            db.session.add(attribute)

        for skill in skills:
            skill['character_id'] = character.id
            skill_obj = Skill(**skill)
            db.session.add(skill_obj)

        for ability in abilities:
            ability['character_id'] = character.id
            ability_obj = Ability(**ability)
            db.session.add(ability_obj)

        db.session.commit()

        return jsonify({
            "message": "Personagem criado",
            "id": character.id
        }), 201

    except Exception as e: 
        db.session.rollback()
        print(f"Erro interno no Flask: {str(e)}")
        return jsonify({"error": str(e)}), 400
        
#GET ALL - RETORNAR TODOS
@characters_bp.route('', methods=['GET'])
@jwt_required()
def get_characters():

    characters = crud.get_all()

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
            "attributes":  [
                {"id": attr.id, "name": attr.name, "value": attr.value}
                for attr in character.attributes
            ],
            "skills": [
                {"id": skill.id, "name": skill.name, "value": skill.value}
                for skill in character.skills
            ],
            "abilities": [
                {"id": ability.id, "image": ability.image, "name": ability.name, "description": ability.description}
                for ability in character.abilities
            ]
        }

        for character in characters
    ])
    
#GET ALL - RETORNAR TODOS OS PERSONAGENS DE 1 USUÁRIO
@characters_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_charactersu(user_id):

    characters = Character.query.filter_by(user_id=user_id).all()

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
            "attributes":  [
                {"id": attr.id, "name": attr.name, "value": attr.value}
                for attr in character.attributes
            ],
            "skills": [
                {"id": skill.id, "name": skill.name, "value": skill.value}
                for skill in character.skills
            ],
            "abilities": [
                {"id": ability.id, "image": ability.image, "name": ability.name, "description": ability.description}
                for ability in character.abilities
            ]
        }

        for character in characters
    ])
    
    
#GET ONE - RETORNAR 1 POR ID
@characters_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_character(id):

    try:

        character = crud.get_by_id(id)

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
            "attributes":  [
                {"id": attr.id, "name": attr.name, "value": attr.value}
                for attr in character.attributes
            ],
            "skills": [
                {"id": skill.id, "name": skill.name, "value": skill.value}
                for skill in character.skills
            ],
            "abilities": [
                {"id": ability.id, "image": ability.image, "name": ability.name, "description": ability.description}
                for ability in character.abilities
            ]
        })


    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404
     
#DELETE - DELETAR POR ID   
@characters_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_character(id):
    
    try:

        crud.delete(id)

        return jsonify({
            "message": "Personagem removido"
        })


    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 404
        
#PUT - ATUALIZAR POR ID
@characters_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_character(id):
    try:
        data = request.form.to_dict()

        image_file = request.files.get('image')
        if image_file:
            data['image'] = save_image(image_file, subfolder='characters')

        character = crud.update(id, data)

        return jsonify({
            "message": "Personagem atualizado",
            "id": character.id
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# GET - SERVIR ARQUIVO DE IMAGEM DO PERSONAGEM
@characters_bp.route('/uploads/<path:filename>', methods=['GET'])
def get_character_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)