import random
from db import db, Character, Skill

class ProgressionService:
    """Servicio que maneja la progresión del personaje"""
    
    @staticmethod
    def add_experience(character_id, exp_amount):
        """Añade experiencia al personaje y verifica level up"""
        character = db.session.get(Character, character_id)
        
        if not character:
            return {"error": "Personaje no encontrado"}
        
        character.exp += exp_amount
        level_ups = 0
        
        while character.exp >= character.exp_to_level:
            character.exp -= character.exp_to_level
            character.level += 1
            level_ups += 1
            
            # Aumentar stats con cada nivel
            character.max_hp += 10
            character.hp = character.max_hp
            character.attack += 2
            character.defense += 1
            character.speed += 1
            
            # Aumentar experiencia requerida para el próximo nivel
            character.exp_to_level = int(character.exp_to_level * 1.1)
        
        db.session.commit()
        
        result = {
            "exp_gained": exp_amount,
            "current_exp": character.exp,
            "exp_to_level": character.exp_to_level,
            "level_ups": level_ups,
            "new_level": character.level
        }
        
        if level_ups > 0:
            result["level_up_message"] = f"¡Subiste {level_ups} nivel(es)! Ahora eres nivel {character.level}"
            result["stat_increases"] = {
                "max_hp": 10 * level_ups,
                "attack": 2 * level_ups,
                "defense": 1 * level_ups,
                "speed": 1 * level_ups
            }
        
        return result
    
    @staticmethod
    def add_currency(character_id, col_amount):
        """Añade moneda al personaje"""
        character = db.session.get(Character, character_id)
        
        if not character:
            return {"error": "Personaje no encontrado"}
        
        character.col += col_amount
        db.session.commit()
        
        return {
            "col_gained": col_amount,
            "total_col": character.col
        }
    
    @staticmethod
    def level_up_skill(character_id, skill_name):
        """Sube de nivel una habilidad"""
        character = db.session.get(Character, character_id)
        
        if not character:
            return {"error": "Personaje no encontrado"}
        
        skill = Skill.query.filter_by(character_id=character_id, name=skill_name).first()
        
        if not skill:
            # Crear nueva habilidad si no existe
            skill = Skill(character_id=character_id, name=skill_name, level=1, exp=0)
            db.session.add(skill)
        else:
            skill.level += 1
            skill.exp = 0
        
        db.session.commit()
        
        return {
            "skill_name": skill_name,
            "new_level": skill.level,
            "message": f"Habilidad '{skill_name}' ahora es nivel {skill.level}"
        }
    
    @staticmethod
    def heal_character(character_id, amount=None):
        """Recupera HP del personaje"""
        character = db.session.get(Character, character_id)
        
        if not character:
            return {"error": "Personaje no encontrado"}
        
        if amount is None:
            amount = character.max_hp
        
        old_hp = character.hp
        character.hp = min(character.max_hp, character.hp + amount)
        actual_healed = character.hp - old_hp
        
        db.session.commit()
        
        return {
            "hp_healed": actual_healed,
            "current_hp": character.hp,
            "max_hp": character.max_hp
        }
    
    @staticmethod
    def apply_status_effect(character_id, status_type, duration=3):
        """Aplica un efecto de estado al personaje (poison, stun, etc)"""
        character = db.session.get(Character, character_id)
        
        if not character:
            return {"error": "Personaje no encontrado"}
        
        # Este es un sistema básico. Se puede expandir
        status_effects = {
            "poison": {"hp_per_turn": 5},
            "stun": {"skip_turns": 1},
            "weakness": {"attack_reduction": 0.5},
            "strength": {"attack_bonus": 5}
        }
        
        if status_type not in status_effects:
            return {"error": "Efecto de estado desconocido"}
        
        return {
            "status": status_type,
            "duration": duration,
            "effect": status_effects[status_type]
        }
    
    @staticmethod
    def get_character_stats(character_id):
        """Obtiene todas las estadísticas del personaje"""
        character = db.session.get(Character, character_id)
        
        if not character:
            return {"error": "Personaje no encontrado"}
        
        return {
            "name": character.name,
            "level": character.level,
            "exp": character.exp,
            "exp_to_level": character.exp_to_level,
            "floor": character.current_floor,
            "hp": character.hp,
            "max_hp": character.max_hp,
            "attack": character.attack,
            "defense": character.defense,
            "speed": character.speed,
            "col": character.col,
            "skills": [s.to_dict() for s in character.skills],
            "title": character.title
        }
