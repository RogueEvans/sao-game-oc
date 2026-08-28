"""
Modelos de base de datos para el juego SAO
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

# ============================================================================
# MODELO DE PERSONAJE
# ============================================================================

class Character(db.Model):
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), default='Novato de Aincrad')
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    current_floor = db.Column(db.Integer, default=1)
    
    # Estadísticas
    max_hp = db.Column(db.Integer, default=100)
    current_hp = db.Column(db.Integer, default=100)
    atk = db.Column(db.Integer, default=10)
    defense = db.Column(db.Integer, default=5)
    spd = db.Column(db.Integer, default=10)
    acc = db.Column(db.Integer, default=20)
    lck = db.Column(db.Integer, default=10)
    
    # Moneda del juego
    col = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    inventory = db.relationship('InventoryItem', backref='character', lazy=True, cascade='all, delete-orphan')
    equipment = db.relationship('Equipment', backref='character', lazy=True, uselist=False, cascade='all, delete-orphan')
    combat_history = db.relationship('CombatLog', backref='character', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'level': self.level,
            'experience': self.experience,
            'current_floor': self.current_floor,
            'stats': {
                'hp': {'current': self.current_hp, 'max': self.max_hp},
                'atk': self.atk,
                'def': self.defense,
                'spd': self.spd,
                'acc': self.acc,
                'lck': self.lck
            },
            'col': self.col,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# ============================================================================
# MODELO DE ENEMIGO
# ============================================================================

class Enemy(db.Model):
    __tablename__ = 'enemies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    floor = db.Column(db.Integer, nullable=False)
    is_boss = db.Column(db.Boolean, default=False)
    
    # Estadísticas
    level = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    atk = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    spd = db.Column(db.Integer, nullable=False)
    acc = db.Column(db.Integer, nullable=False)
    
    # Recompensas
    exp_reward = db.Column(db.Integer, default=0)
    col_reward = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'floor': self.floor,
            'is_boss': self.is_boss,
            'level': self.level,
            'stats': {
                'hp': self.max_hp,
                'atk': self.atk,
                'def': self.defense,
                'spd': self.spd,
                'acc': self.acc
            },
            'rewards': {
                'exp': self.exp_reward,
                'col': self.col_reward
            }
        }

# ============================================================================
# MODELO DE PISO
# ============================================================================

class Floor(db.Model):
    __tablename__ = 'floors'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    recommended_level = db.Column(db.Integer, default=1)
    
    # Información del piso
    total_enemies = db.Column(db.Integer, default=10)
    boss_id = db.Column(db.Integer, db.ForeignKey('enemies.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    boss = db.relationship('Enemy', foreign_keys=[boss_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'description': self.description,
            'recommended_level': self.recommended_level,
            'total_enemies': self.total_enemies,
            'boss': self.boss.to_dict() if self.boss else None
        }

# ============================================================================
# MODELO DE ITEM
# ============================================================================

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    item_type = db.Column(db.String(50), nullable=False)  # 'weapon', 'armor', 'consumable'
    rarity = db.Column(db.String(20), default='common')  # 'common', 'uncommon', 'rare', 'epic', 'legendary'
    
    # Estadísticas
    required_level = db.Column(db.Integer, default=1)
    atk_bonus = db.Column(db.Integer, default=0)
    def_bonus = db.Column(db.Integer, default=0)
    hp_bonus = db.Column(db.Integer, default=0)
    spd_bonus = db.Column(db.Integer, default=0)
    
    # Para consumibles
    heal_amount = db.Column(db.Integer, default=0)
    
    # Precio
    value = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.item_type,
            'rarity': self.rarity,
            'required_level': self.required_level,
            'bonuses': {
                'atk': self.atk_bonus,
                'def': self.def_bonus,
                'hp': self.hp_bonus,
                'spd': self.spd_bonus
            },
            'heal_amount': self.heal_amount,
            'value': self.value
        }

# ============================================================================
# MODELO DE INVENTARIO
# ============================================================================

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    acquired_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    item = db.relationship('Item')
    
    def to_dict(self):
        item_data = self.item.to_dict()
        return {
            'id': self.id,
            'item': item_data,
            'quantity': self.quantity,
            'acquired_at': self.acquired_at.isoformat()
        }

# ============================================================================
# MODELO DE EQUIPO
# ============================================================================

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    
    # Slots
    weapon_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    armor_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    accessory_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    equipped_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    weapon = db.relationship('Item', foreign_keys=[weapon_id])
    armor = db.relationship('Item', foreign_keys=[armor_id])
    accessory = db.relationship('Item', foreign_keys=[accessory_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'weapon': self.weapon.to_dict() if self.weapon else None,
            'armor': self.armor.to_dict() if self.armor else None,
            'accessory': self.accessory.to_dict() if self.accessory else None,
            'equipped_at': self.equipped_at.isoformat()
        }

# ============================================================================
# MODELO DE LOG DE COMBATE
# ============================================================================

class CombatLog(db.Model):
    __tablename__ = 'combat_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    enemy_id = db.Column(db.Integer, db.ForeignKey('enemies.id'), nullable=False)
    
    result = db.Column(db.String(10), nullable=False)  # 'win', 'lose'
    damage_dealt = db.Column(db.Integer, default=0)
    damage_taken = db.Column(db.Integer, default=0)
    exp_gained = db.Column(db.Integer, default=0)
    col_gained = db.Column(db.Integer, default=0)
    
    duration_seconds = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    enemy = db.relationship('Enemy')
    
    def to_dict(self):
        return {
            'id': self.id,
            'result': self.result,
            'damage_dealt': self.damage_dealt,
            'damage_taken': self.damage_taken,
            'exp_gained': self.exp_gained,
            'col_gained': self.col_gained,
            'duration_seconds': self.duration_seconds,
            'created_at': self.created_at.isoformat()
        }

# ============================================================================
# FUNCIÓN DE INICIALIZACIÓN
# ============================================================================

def init_db(app):
    """Inicializa la base de datos"""
    with app.app_context():
        db.create_all()
