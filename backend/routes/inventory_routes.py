"""
Rutas de inventario e items
"""
from flask import Blueprint, request, jsonify
from db import db, Character
from services.loot_service import LootService

bp = Blueprint('inventory', __name__, url_prefix='/api/character')

@bp.route('/<int:character_id>/inventory', methods=['GET'])
def get_inventory(character_id):
    """Obtiene el inventario del personaje"""
    try:
        character = db.session.get(Character, character_id)
        
        if not character:
            return jsonify({"error": "Personaje no encontrado"}), 404
        
        return jsonify({
            "status": "success",
            "inventory": [item.to_dict() for item in character.inventory]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:character_id>/equip', methods=['POST'])
def equip_item(character_id):
    """Equipa un item"""
    try:
        data = request.json
        inventory_item_id = data.get('inventory_item_id')
        
        result = LootService.equip_item(character_id, inventory_item_id)
        
        if "error" in result:
            return jsonify(result), 404
        
        return jsonify({
            "status": "success",
            "equipment": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:character_id>/use-item', methods=['POST'])
def use_item(character_id):
    """Usa un item consumible"""
    try:
        data = request.json
        inventory_item_id = data.get('inventory_item_id')
        
        result = LootService.use_consumable(character_id, inventory_item_id)
        
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify({
            "status": "success",
            "usage": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
