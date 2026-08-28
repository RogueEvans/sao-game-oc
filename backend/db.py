from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Character(db.Model):
    """Modelo del personaje jugable"""
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), default="Novato de Aincrad")
    level = db.Column(db.Integer, default=1)
    current_floor = db.Column(db.Integer, default=1)
    exp = db.Column(db.Integer, default=0)
    exp_to_level = db.Column(db.Integer, default=100)
    
    # Stats
    hp = db.Column(db.Integer, default=100)
    max_hp = db.Column(db.Integer, default=100)
    attack = db.Column(db.Integer, default=10)
    defense = db.Column(db.Integer, default=5)
    speed = db.Column(db.Integer, default=5)
    
    # Recursos
    col = db.Column(db.Integer, default=0)  # Moneda
    
    # Relaciones
    skills = db.relationship('Skill', backref='character', lazy=True, cascade='all, delete-orphan')
    inventory = db.relationship('InventoryItem', backref='character', lazy=True, cascade='all, delete-orphan')
    quests = db.relationship('Quest', backref='character', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'level': self.level,
            'floor': self.current_floor,
            'exp': self.exp,
            'exp_to_level': self.exp_to_level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'defense': self.defense,
            'speed': self.speed,
            'col': self.col,
            'skills': [s.to_dict() for s in self.skills],
            'inventory': [i.item.to_dict() for i in self.inventory],
            'quests': [q.to_dict() for q in self.quests]
        }

class Skill(db.Model):
    """Modelo de habilidades del personaje"""
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=1)
    exp = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'exp': self.exp
        }

class Item(db.Model):
    """Modelo de items disponibles"""
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500))
    item_type = db.Column(db.String(50), nullable=False)  # weapon, armor, potion, etc
    rarity = db.Column(db.String(20), default='common')  # common, uncommon, rare, epic, legendary
    min_floor = db.Column(db.Integer, default=1)
    attack_bonus = db.Column(db.Integer, default=0)
    defense_bonus = db.Column(db.Integer, default=0)
    hp_bonus = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.item_type,
            'rarity': self.rarity,
            'min_floor': self.min_floor,
            'attack_bonus': self.attack_bonus,
            'defense_bonus': self.defense_bonus,
            'hp_bonus': self.hp_bonus
        }

class InventoryItem(db.Model):
    """Modelo del inventario del personaje"""
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    equipped = db.Column(db.Boolean, default=False)
    
    item = db.relationship('Item')
    
    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item.to_dict(),
            'quantity': self.quantity,
            'equipped': self.equipped
        }

class Enemy(db.Model):
    """Modelo de enemigos"""
    __tablename__ = 'enemies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, default=1)
    hp = db.Column(db.Integer, default=50)
    attack = db.Column(db.Integer, default=5)
    defense = db.Column(db.Integer, default=2)
    speed = db.Column(db.Integer, default=3)
    exp_reward = db.Column(db.Integer, default=20)
    col_reward = db.Column(db.Integer, default=10)
    is_boss = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'floor': self.floor,
            'level': self.level,
            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'speed': self.speed,
            'exp_reward': self.exp_reward,
            'col_reward': self.col_reward,
            'is_boss': self.is_boss
        }

class Floor(db.Model):
    """Modelo de pisos de Aincrad"""
    __tablename__ = 'floors'
    
    id = db.Column(db.Integer, primary_key=True)
    floor_number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    main_city = db.Column(db.String(100))
    boss_name = db.Column(db.String(100))
    boss_level = db.Column(db.Integer, default=1)
    theme = db.Column(db.String(50))  # forest, desert, snow, dungeon, etc
    
    def to_dict(self):
        return {
            'id': self.id,
            'floor_number': self.floor_number,
            'name': self.name,
            'description': self.description,
            'main_city': self.main_city,
            'boss_name': self.boss_name,
            'boss_level': self.boss_level,
            'theme': self.theme
        }

class Quest(db.Model):
    """Modelo de misiones"""
    __tablename__ = 'quests'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, completed, failed
    floor = db.Column(db.Integer, default=1)
    reward_exp = db.Column(db.Integer, default=50)
    reward_col = db.Column(db.Integer, default=100)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'floor': self.floor,
            'reward': f"{self.reward_exp} EXP + {self.reward_col} Col"
        }

class CombatLog(db.Model):
    """Modelo para guardar combates"""
    __tablename__ = 'combat_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    enemy_id = db.Column(db.Integer, db.ForeignKey('enemies.id'), nullable=False)
    result = db.Column(db.String(20))  # win, lose
    character_damage_dealt = db.Column(db.Integer, default=0)
    enemy_damage_dealt = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    enemy = db.relationship('Enemy')

def init_db(app):
    """Inicializar la base de datos"""
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente")
