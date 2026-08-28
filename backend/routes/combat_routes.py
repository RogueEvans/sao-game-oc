"""
Rutas de combate
"""
from flask import Blueprint, request, jsonify
from db import db, Character, Enemy
from services.combat_service import CombatService
from services.progression_service import ProgressionService
from services.loot_service import LootService
import random

bp = Blueprint('combat', __name__, url_prefix='/api/combat')

@bp.route('/start', methods=['POST'])
def start_combat():
    """Inicia un combate"""
    try:
        data = request.json
        character_id = data.get('character_id')
        enemy_id = data.get('enemy_id')
        
        if not character_id or not enemy_id:
            return jsonify({"error": "character_id y enemy_id son requeridos"}), 400
        
        result = CombatService.start_combat(character_id, enemy_id)
        
        if "error" in result:
            return jsonify(result), 404
        
        return jsonify({
            "status": "combat_started",
            "combat": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/turn', methods=['POST'])
def execute_combat_turn():
    """Ejecuta un turno de combate"""
    try:
        data = request.json
        combat_state = data.get('combat_state')
        action = data.get('action', 'attack')
        
        if not combat_state:
            return jsonify({"error": "combat_state es requerido"}), 400
        
        result = CombatService.execute_turn(combat_state, action)
        
        return jsonify({
            "status": "success",
            "result": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/finish', methods=['POST'])
def finish_combat():
    """Finaliza un combate y aplica recompensas"""
    try:
        data = request.json
        character_id = data.get('character_id')
        enemy_id = data.get('enemy_id')
        result = data.get('result')  # 'win' o 'lose'
        
        if not all([character_id, enemy_id, result]):
            return jsonify({"error": "Parámetros requeridos faltantes"}), 400
        
        character = db.session.get(Character, character_id)
        enemy = db.session.get(Enemy, enemy_id)
        
        if not character or not enemy:
            return jsonify({"error": "Personaje o enemigo no encontrado"}), 404
        
        # Aplicar recompensas
        if result == "win":
            exp_result = ProgressionService.add_experience(character_id, enemy.exp_reward)
            col_result = ProgressionService.add_currency(character_id, enemy.col_reward)
            
            # Chance de loot
            if random.random() < 0.3:  # 30% chance de loot
                loot_item = LootService.roll_loot(character.level, character.current_floor)
                if loot_item:
                    LootService.add_to_inventory(character_id, loot_item.id)
            
            return jsonify({
                "status": "combat_finished",
                "result": "win",
                "rewards": {
                    "exp": exp_result,
                    "col": col_result
                }
            }), 200
        else:
            return jsonify({
                "status": "combat_finished",
                "result": "lose",
                "rewards": {"exp": 0, "col": 0}
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
