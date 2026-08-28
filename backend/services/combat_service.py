import random
from db import db, Character, Enemy, CombatLog

class CombatService:
    """Servicio que maneja toda la lógica de combate"""
    
    @staticmethod
    def calculate_damage(attacker_attack, defender_defense):
        """Calcula el daño con variación aleatoria"""
        base_damage = max(1, attacker_attack - (defender_defense // 2))
        variance = random.randint(-3, 5)
        return max(1, base_damage + variance)
    
    @staticmethod
    def start_combat(character_id, enemy_id):
        """Inicia un combate y retorna el estado inicial"""
        character = Character.query.get(character_id)
        enemy = Enemy.query.get(enemy_id)
        
        if not character or not enemy:
            return {"error": "Personaje o enemigo no encontrado"}
        
        return {
            "combat_id": f"combat_{character_id}_{enemy_id}_{random.randint(1000, 9999)}",
            "character": {
                "name": character.name,
                "hp": character.hp,
                "max_hp": character.max_hp,
                "attack": character.attack,
                "defense": character.defense,
                "speed": character.speed
            },
            "enemy": {
                "id": enemy.id,
                "name": enemy.name,
                "hp": enemy.hp,
                "attack": enemy.attack,
                "defense": enemy.defense,
                "speed": enemy.speed,
                "is_boss": enemy.is_boss
            },
            "turn": 0,
            "log": [f"¡Combate iniciado contra {enemy.name}!"]
        }
    
    @staticmethod
    def execute_turn(combat_state, action="attack"):
        """Ejecuta un turno de combate"""
        character = Character.query.get_by_name(combat_state["character"]["name"])
        
        # Determinar orden (por velocidad)
        char_speed = combat_state["character"]["speed"]
        enemy_speed = combat_state["enemy"]["speed"]
        
        log = combat_state["log"]
        
        if char_speed >= enemy_speed:
            # Ataque del jugador primero
            char_damage = CombatService.calculate_damage(
                combat_state["character"]["attack"],
                combat_state["enemy"]["defense"]
            )
            combat_state["enemy"]["hp"] -= char_damage
            log.append(f"¡{combat_state['character']['name']} ataca! {char_damage} daño")
            
            if combat_state["enemy"]["hp"] <= 0:
                return CombatService._finish_combat(combat_state, "win", log)
            
            # Contraataque del enemigo
            enemy_damage = CombatService.calculate_damage(
                combat_state["enemy"]["attack"],
                combat_state["character"]["defense"]
            )
            combat_state["character"]["hp"] -= enemy_damage
            log.append(f"{combat_state['enemy']['name']} contraataca! {enemy_damage} daño")
            
            if combat_state["character"]["hp"] <= 0:
                return CombatService._finish_combat(combat_state, "lose", log)
        else:
            # Ataque del enemigo primero
            enemy_damage = CombatService.calculate_damage(
                combat_state["enemy"]["attack"],
                combat_state["character"]["defense"]
            )
            combat_state["character"]["hp"] -= enemy_damage
            log.append(f"{combat_state['enemy']['name']} ataca! {enemy_damage} daño")
            
            if combat_state["character"]["hp"] <= 0:
                return CombatService._finish_combat(combat_state, "lose", log)
            
            # Contraataque del jugador
            char_damage = CombatService.calculate_damage(
                combat_state["character"]["attack"],
                combat_state["enemy"]["defense"]
            )
            combat_state["enemy"]["hp"] -= char_damage
            log.append(f"¡{combat_state['character']['name']} contraataca! {char_damage} daño")
            
            if combat_state["enemy"]["hp"] <= 0:
                return CombatService._finish_combat(combat_state, "win", log)
        
        combat_state["turn"] += 1
        combat_state["log"] = log
        return {"status": "ongoing", "combat": combat_state}
    
    @staticmethod
    def _finish_combat(combat_state, result, log):
        """Finaliza el combate y retorna recompensas"""
        enemy = Enemy.query.get(combat_state["enemy"]["id"])
        
        if result == "win":
            log.append(f"¡{combat_state['enemy']['name']} ha sido derrotado!")
            return {
                "status": "finished",
                "result": "win",
                "log": log,
                "rewards": {
                    "exp": enemy.exp_reward,
                    "col": enemy.col_reward
                }
            }
        else:
            log.append(f"Has sido derrotado por {combat_state['enemy']['name']}...")
            return {
                "status": "finished",
                "result": "lose",
                "log": log,
                "rewards": {
                    "exp": 0,
                    "col": 0
                }
            }
    
    @staticmethod
    def save_combat_log(character_id, enemy_id, result, char_damage, enemy_damage):
        """Guarda el registro del combate en la BD"""
        log = CombatLog(
            character_id=character_id,
            enemy_id=enemy_id,
            result=result,
            character_damage_dealt=char_damage,
            enemy_damage_dealt=enemy_damage
        )
        db.session.add(log)
        db.session.commit()
        return log
