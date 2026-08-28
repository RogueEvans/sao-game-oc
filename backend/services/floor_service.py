import random
from db import db, Floor, Enemy
from data.floors_data import get_floor_by_number, FLOOR_NARRATIVES

class FloorService:
    """Servicio que maneja la lógica de pisos y exploración"""
    
    @staticmethod
    def initialize_floors():
        """Inicializa todos los pisos en la BD desde los datos"""
        from data.floors_data import FLOORS_DATA
        
        existing_floors = Floor.query.count()
        if existing_floors > 0:
            return {"status": "already_initialized", "floors": existing_floors}
        
        for floor_data in FLOORS_DATA:
            floor = Floor(
                floor_number=floor_data["floor"],
                name=floor_data["name"],
                description=floor_data["description"],
                main_city=floor_data.get("main_city"),
                boss_name=floor_data.get("boss_name"),
                boss_level=floor_data.get("boss_level", 1),
                theme=floor_data.get("theme")
            )
            db.session.add(floor)
        
        db.session.commit()
        return {"status": "initialized", "total_floors": len(FLOORS_DATA)}
    
    @staticmethod
    def initialize_enemies():
        """Inicializa los enemigos de cada piso"""
        from data.floors_data import FLOORS_DATA
        
        existing_enemies = Enemy.query.count()
        if existing_enemies > 0:
            return {"status": "already_initialized", "enemies": existing_enemies}
        
        enemy_count = 0
        for floor_data in FLOORS_DATA:
            for enemy_data in floor_data.get("enemies", []):
                enemy = Enemy(
                    name=enemy_data["name"],
                    floor=floor_data["floor"],
                    level=enemy_data.get("level", 1),
                    hp=enemy_data.get("hp", 50),
                    attack=enemy_data.get("attack", 5),
                    defense=enemy_data.get("defense", 2),
                    speed=enemy_data.get("speed", 3),
                    exp_reward=enemy_data.get("level", 1) * 10,
                    col_reward=enemy_data.get("level", 1) * 5,
                    is_boss=False
                )
                db.session.add(enemy)
                enemy_count += 1
            
            # Crear boss del piso
            boss = Enemy(
                name=floor_data["boss_name"],
                floor=floor_data["floor"],
                level=floor_data.get("boss_level", 1),
                hp=floor_data.get("boss_level", 1) * 20,
                attack=floor_data.get("boss_level", 1) // 2,
                defense=floor_data.get("boss_level", 1) // 3,
                speed=floor_data.get("boss_level", 1) // 4 + 5,
                exp_reward=floor_data.get("boss_level", 1) * 100,
                col_reward=floor_data.get("boss_level", 1) * 50,
                is_boss=True
            )
            db.session.add(boss)
            enemy_count += 1
        
        db.session.commit()
        return {"status": "initialized", "total_enemies": enemy_count}
    
    @staticmethod
    def get_floor_info(floor_number):
        """Obtiene información completa de un piso"""
        floor = Floor.query.filter_by(floor_number=floor_number).first()
        
        if not floor:
            return {"error": "Piso no encontrado"}
        
        enemies = Enemy.query.filter_by(floor=floor_number, is_boss=False).all()
        boss = Enemy.query.filter_by(floor=floor_number, is_boss=True).first()
        
        return {
            "floor": floor.to_dict(),
            "enemies": [e.to_dict() for e in enemies],
            "boss": boss.to_dict() if boss else None,
            "narrative": FLOOR_NARRATIVES.get(floor_number, "Continúa tu aventura en este piso de Aincrad...")
        }
    
    @staticmethod
    def get_floor_enemies(floor_number, count=3):
        """Obtiene enemigos aleatorios de un piso para exploración"""
        enemies = Enemy.query.filter_by(floor=floor_number, is_boss=False).all()
        
        if not enemies:
            return []
        
        return random.sample(enemies, min(count, len(enemies)))
    
    @staticmethod
    def get_floor_boss(floor_number):
        """Obtiene el boss de un piso"""
        boss = Enemy.query.filter_by(floor=floor_number, is_boss=True).first()
        return boss.to_dict() if boss else None
    
    @staticmethod
    def can_advance_floor(character):
        """Verifica si un personaje puede avanzar al siguiente piso"""
        # Verificar si existe el siguiente piso
        next_floor = Floor.query.filter_by(floor_number=character.current_floor + 1).first()
        
        if not next_floor:
            return False, "No hay más pisos disponibles"
        
        # Requisito: nivel mínimo
        min_level = character.current_floor
        if character.level < min_level:
            return False, f"Necesitas nivel {min_level} para avanzar"
        
        return True, "Puedes avanzar al siguiente piso"
    
    @staticmethod
    def advance_floor(character_id):
        """Avanza un personaje al siguiente piso"""
        character = db.session.get(Character, character_id)
        
        if not character:
            return {"error": "Personaje no encontrado"}
        
        can_advance, message = FloorService.can_advance_floor(character)
        
        if not can_advance:
            return {"error": message}
        
        character.current_floor += 1
        character.hp = character.max_hp  # Restaurar HP al cambiar piso
        db.session.commit()
        
        floor_info = FloorService.get_floor_info(character.current_floor)
        
        return {
            "status": "floor_advanced",
            "new_floor": character.current_floor,
            "floor_info": floor_info,
            "message": f"¡Bienvenido al Piso {character.current_floor}!"
        }
    
    @staticmethod
    def generate_random_encounter(floor_number):
        """Genera un encuentro aleatorio en un piso"""
        enemies = FloorService.get_floor_enemies(floor_number, count=1)
        
        if not enemies:
            return {"error": "No hay enemigos disponibles en este piso"}
        
        enemy = enemies[0]
        
        return {
            "encounter_type": random.choice(["normal", "stronger", "weaker"]),
            "enemy": enemy.to_dict()
        }


from db import Character
