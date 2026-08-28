"""
Rutas de personaje
"""
from flask import Blueprint, request, jsonify
from db import db, Character
from services.progression_service import ProgressionService
from utils import ValidationUtils

bp = Blueprint('character', __name__, url_prefix='/api/character')

@bp.route('', methods=['POST'])
def create_character():
    """Crea un nuevo personaje"""
    try:
        data = request.json
        
        if not data.get('name'):
            return jsonify({"error": "El nombre es requerido"}), 400
        
        # Validar nombre
        is_valid, error_msg = ValidationUtils.validate_character_name(data['name'])
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Verificar si el nombre ya existe
        existing = Character.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({"error": "Ese nombre ya está en uso"}), 409
        
        character = Character(
            name=data['name'],
            title=data.get('title', 'Novato de Aincrad')
        )
        
        db.session.add(character)
        db.session.commit()
        
        return jsonify({
            "status": "created",
            "character": character.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:character_id>', methods=['GET'])
def get_character(character_id):
    """Obtiene información del personaje"""
    try:
        character = db.session.get(Character, character_id)
        
        if not character:
            return jsonify({"error": "Personaje no encontrado"}), 404
        
        return jsonify({
            "status": "success",
            "character": character.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:character_id>/stats', methods=['GET'])
def get_character_stats(character_id):
    """Obtiene todas las estadísticas del personaje"""
    try:
        stats = ProgressionService.get_character_stats(character_id)
        
        if "error" in stats:
            return jsonify(stats), 404
        
        return jsonify({"status": "success", "stats": stats}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:character_id>/heal', methods=['POST'])
def heal_character(character_id):
    """Recupera HP del personaje"""
    try:
        data = request.json
        amount = data.get('amount')
        
        result = ProgressionService.heal_character(character_id, amount)
        
        if "error" in result:
            return jsonify(result), 404
        
        return jsonify({
            "status": "success",
            "healing": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
