from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db, init_db, Character, Enemy, Floor
from services.combat_service import CombatService
from services.floor_service import FloorService
from services.progression_service import ProgressionService
from services.loot_service import LootService
import os

app = Flask(__name__)

# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///aincrad_game.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Inicializar extensiones
db.init_app(app)
CORS(app)

# ============================================================================
# RUTAS DE INICIALIZACIÓN
# ============================================================================

@app.route('/api/init', methods=['POST'])
def initialize_game():
    """Inicializa la base de datos del juego"""
    try:
        with app.app_context():
            init_db(app)
            
            # Inicializar pisos
            floors_result = FloorService.initialize_floors()
            
            # Inicializar enemigos
            enemies_result = FloorService.initialize_enemies()
            
            # Inicializar items
            items_result = LootService.initialize_items()
            
            return jsonify({
                "status": "initialized",
                "floors": floors_result,
                "enemies": enemies_result,
                "items": items_result
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# RUTAS DE PERSONAJE
# ============================================================================

@app.route('/api/character', methods=['POST'])
def create_character():
    """Crea un nuevo personaje"""
    try:
        data = request.json
        
        if not data.get('name'):
            return jsonify({"error": "El nombre es requerido"}), 400
        
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
        return jsonify({"error": str(e)}), 500

@app.route('/api/character/<int:character_id>', methods=['GET'])
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

@app.route('/api/character/<int:character_id>/stats', methods=['GET'])
def get_character_stats(character_id):
    """Obtiene todas las estadísticas del personaje"""
    try:
        stats = ProgressionService.get_character_stats(character_id)
        
        if "error" in stats:
            return jsonify(stats), 404
        
        return jsonify({"status": "success", "stats": stats}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# RUTAS DE COMBATE
# ============================================================================

@app.route('/api/combat/start', methods=['POST'])
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

@app.route('/api/combat/turn', methods=['POST'])
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

@app.route('/api/combat/finish', methods=['POST'])
def finish_combat():
    """Finaliza un combate y aplica recompensas"""
    try:
        data = request.json
        character_id = data.get('character_id')
        enemy_id = data.get('enemy_id')
        result = data.get('result')  # 'win' o 'lose'
        
        if not all([character_id, enemy_id, result]):
            return jsonify({"error": "Parámetros requeridos faltantes"}), 400
        
        enemy = db.session.get(Enemy, enemy_id)
        
        if not enemy:
            return jsonify({"error": "Enemigo no encontrado"}), 404
        
        # Aplicar recompensas
        if result == "win":
            exp_result = ProgressionService.add_experience(character_id, enemy.exp_reward)
            col_result = ProgressionService.add_currency(character_id, enemy.col_reward)
            
            # Chance de loot
            import random
            if random.random() < 0.3:  # 30% chance de loot
                loot_item = LootService.roll_loot(
                    db.session.get(Character, character_id).level,
                    db.session.get(Character, character_id).current_floor
                )
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

# ============================================================================
# RUTAS DE PISOS
# ============================================================================

@app.route('/api/floor/<int:floor_number>', methods=['GET'])
def get_floor(floor_number):
    """Obtiene información de un piso"""
    try:
        floor_info = FloorService.get_floor_info(floor_number)
        
        if "error" in floor_info:
            return jsonify(floor_info), 404
        
        return jsonify({
            "status": "success",
            "floor": floor_info
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/floor/<int:floor_number>/enemies', methods=['GET'])
def get_floor_enemies(floor_number):
    """Obtiene enemigos de un piso"""
    try:
        enemies = FloorService.get_floor_enemies(floor_number)
        
        if not enemies:
            return jsonify({"error": "No hay enemigos en este piso"}), 404
        
        return jsonify({
            "status": "success",
            "enemies": [e.to_dict() for e in enemies]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/floor/<int:floor_number>/boss', methods=['GET'])
def get_floor_boss(floor_number):
    """Obtiene el boss de un piso"""
    try:
        boss = FloorService.get_floor_boss(floor_number)
        
        if not boss:
            return jsonify({"error": "No hay boss en este piso"}), 404
        
        return jsonify({
            "status": "success",
            "boss": boss
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/character/<int:character_id>/advance-floor', methods=['POST'])
def advance_floor(character_id):
    """Avanza un personaje al siguiente piso"""
    try:
        result = FloorService.advance_floor(character_id)
        
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# RUTAS DE PROGRESIÓN
# ============================================================================

@app.route('/api/character/<int:character_id>/heal', methods=['POST'])
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

# ============================================================================
# RUTAS DE INVENTARIO
# ============================================================================

@app.route('/api/character/<int:character_id>/inventory', methods=['GET'])
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

@app.route('/api/character/<int:character_id>/equip', methods=['POST'])
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

@app.route('/api/character/<int:character_id>/use-item', methods=['POST'])
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

# ============================================================================
# RUTAS DE SALUD
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica el estado de la API"""
    return jsonify({
        "status": "healthy",
        "message": "SAO Game API is running"
    }), 200

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
