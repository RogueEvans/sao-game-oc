"""
Blueprint initialization for routes
"""
from flask import Blueprint

def register_blueprints(app):
    """Registra todos los blueprints en la aplicación"""
    from .character_routes import bp as character_bp
    from .combat_routes import bp as combat_bp
    from .floor_routes import bp as floor_bp
    from .inventory_routes import bp as inventory_bp
    
    app.register_blueprint(character_bp)
    app.register_blueprint(combat_bp)
    app.register_blueprint(floor_bp)
    app.register_blueprint(inventory_bp)
