"""
Rutas de piso
"""
from flask import Blueprint, request, jsonify
from db import db, Character
from services.floor_service import FloorService
from utils import ValidationUtils

bp = Blueprint('floor', __name__, url_prefix='/api/floor')

@bp.route('/<int:floor_number>', methods=['GET'])
def get_floor(floor_number):
    """Obtiene información de un piso"""
    try:
        is_valid, error_msg = ValidationUtils.validate_floor_number(floor_number)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        floor_info = FloorService.get_floor_info(floor_number)
        
        if "error" in floor_info:
            return jsonify(floor_info), 404
        
        return jsonify({
            "status": "success",
            "floor": floor_info
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:floor_number>/enemies', methods=['GET'])
def get_floor_enemies(floor_number):
    """Obtiene enemigos de un piso"""
    try:
        is_valid, error_msg = ValidationUtils.validate_floor_number(floor_number)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        enemies = FloorService.get_floor_enemies(floor_number)
        
        if not enemies:
            return jsonify({"error": "No hay enemigos en este piso"}), 404
        
        return jsonify({
            "status": "success",
            "enemies": [e.to_dict() for e in enemies]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:floor_number>/boss', methods=['GET'])
def get_floor_boss(floor_number):
    """Obtiene el boss de un piso"""
    try:
        is_valid, error_msg = ValidationUtils.validate_floor_number(floor_number)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        boss = FloorService.get_floor_boss(floor_number)
        
        if not boss:
            return jsonify({"error": "No hay boss en este piso"}), 404
        
        return jsonify({
            "status": "success",
            "boss": boss
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
