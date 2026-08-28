"""
Aplicación Flask principal - API del juego SAO
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import get_config
from db import db, init_db
from routes import register_blueprints
import os

def create_app(config_name=None):
    """Factory para crear la aplicación Flask"""
    
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Cargar configuración
    if config_name:
        from config import config
        app.config.from_object(config[config_name])
    else:
        config_obj = get_config()
        app.config.from_object(config_obj)
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app)
    
    # Registrar blueprints de rutas
    register_blueprints(app)
    
    # Rutas de salud y utilidad
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Verifica el estado de la API"""
        return jsonify({
            "status": "healthy",
            "service": "SAO Game API",
            "version": "1.0.0"
        }), 200
    
    @app.route('/api/init', methods=['POST'])
    def initialize_database():
        """Inicializa la base de datos con datos de prueba"""
        try:
            init_db(app)
            
            from services.floor_service import FloorService
            from services.loot_service import LootService
            
            # Inicializar datos por defecto
            floors_result = FloorService.initialize_floors()
            enemies_result = FloorService.initialize_enemies()
            items_result = LootService.initialize_items()
            
            return jsonify({
                "status": "success",
                "message": "Base de datos inicializada correctamente",
                "data": {
                    "floors": floors_result,
                    "enemies": enemies_result,
                    "items": items_result
                }
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Maneja errores 404"""
        return jsonify({
            "error": "No encontrado",
            "message": "El endpoint solicitado no existe"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores 500"""
        db.session.rollback()
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(error)
        }), 500
    
    return app

# Crear instancia global de la aplicación
app = create_app()

if __name__ == '__main__':
    # Crear contexto de aplicación para inicializar DB
    with app.app_context():
        db.create_all()
    
    # Ejecutar servidor
    port = int(os.getenv('API_PORT', 5000))
    host = os.getenv('API_HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
