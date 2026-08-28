import random
from db import db, Item, InventoryItem, Character

class LootService:
    """Servicio que maneja el sistema de loot y items"""
    
    RARITY_WEIGHTS = {
        "common": 50,
        "uncommon": 30,
        "rare": 15,
        "epic": 4,
        "legendary": 1
    }
    
    RARITY_COLORS = {
        "common": "#FFFFFF",
        "uncommon": "#1EFF00",
        "rare": "#0070DD",
        "epic": "#A335EE",
        "legendary": "#FF8000"
    }
    
    @staticmethod
    def initialize_items():
        """Inicializa items base en la BD"""
        existing_items = Item.query.count()
        if existing_items > 0:
            return {"status": "already_initialized", "items": existing_items}
        
        base_items = [
            # Armas
            {"name": "Rusty Sword", "type": "weapon", "rarity": "common", "min_floor": 1, "attack_bonus": 2},
            {"name": "Iron Sword", "type": "weapon", "rarity": "uncommon", "min_floor": 3, "attack_bonus": 5},
            {"name": "Steel Blade", "type": "weapon", "rarity": "rare", "min_floor": 10, "attack_bonus": 10},
            {"name": "Excalibur", "type": "weapon", "rarity": "legendary", "min_floor": 50, "attack_bonus": 25},
            
            # Armadura
            {"name": "Leather Armor", "type": "armor", "rarity": "common", "min_floor": 1, "defense_bonus": 2},
            {"name": "Plate Mail", "type": "armor", "rarity": "uncommon", "min_floor": 5, "defense_bonus": 5},
            {"name": "Mithril Plate", "type": "armor", "rarity": "rare", "min_floor": 15, "defense_bonus": 10},
            {"name": "Legendary Armor", "type": "armor", "rarity": "legendary", "min_floor": 60, "defense_bonus": 20},
            
            # Pociones
            {"name": "Health Potion", "type": "potion", "rarity": "common", "min_floor": 1, "hp_bonus": 30},
            {"name": "Greater Health Potion", "type": "potion", "rarity": "uncommon", "min_floor": 5, "hp_bonus": 100},
            {"name": "Elixir of Life", "type": "potion", "rarity": "rare", "min_floor": 20, "hp_bonus": 200},
            
            # Accesorios
            {"name": "Ring of Power", "type": "accessory", "rarity": "rare", "min_floor": 10, "attack_bonus": 3, "defense_bonus": 3},
            {"name": "Amulet of Wisdom", "type": "accessory", "rarity": "epic", "min_floor": 30, "attack_bonus": 5, "defense_bonus": 5},
        ]
        
        for item_data in base_items:
            item = Item(
                name=item_data["name"],
                item_type=item_data["type"],
                rarity=item_data["rarity"],
                min_floor=item_data["min_floor"],
                attack_bonus=item_data.get("attack_bonus", 0),
                defense_bonus=item_data.get("defense_bonus", 0),
                hp_bonus=item_data.get("hp_bonus", 0),
                description=f"A {item_data['rarity']} quality {item_data['type']}"
            )
            db.session.add(item)
        
        db.session.commit()
        return {"status": "initialized", "total_items": len(base_items)}
    
    @staticmethod
    def roll_loot(character_level, current_floor):
        """Genera un loot aleatorio basado en el nivel del personaje"""
        # Determinar rareza
        roll = random.randint(1, 100)
        cumulative = 0
        rarity = "common"
        
        for r, weight in LootService.RARITY_WEIGHTS.items():
            cumulative += weight
            if roll <= cumulative:
                rarity = r
                break
        
        # Obtener item de esa rareza disponible en el piso
        available_items = Item.query.filter(
            Item.rarity == rarity,
            Item.min_floor <= current_floor
        ).all()
        
        if not available_items:
            # Si no hay items de esa rareza, obtener común
            available_items = Item.query.filter_by(rarity="common").all()
        
        if not available_items:
            return None
        
        selected_item = random.choice(available_items)
        return selected_item
    
    @staticmethod
    def add_to_inventory(character_id, item_id, quantity=1):
        """Añade un item al inventario del personaje"""
        character = db.session.get(Character, character_id)
        
        if not character:
            return {"error": "Personaje no encontrado"}
        
        item = db.session.get(Item, item_id)
        
        if not item:
            return {"error": "Item no encontrado"}
        
        # Verificar si el item ya existe en el inventario
        inv_item = InventoryItem.query.filter_by(
            character_id=character_id,
            item_id=item_id
        ).first()
        
        if inv_item:
            inv_item.quantity += quantity
        else:
            inv_item = InventoryItem(
                character_id=character_id,
                item_id=item_id,
                quantity=quantity
            )
            db.session.add(inv_item)
        
        db.session.commit()
        
        return {
            "status": "added",
            "item": item.to_dict(),
            "quantity": inv_item.quantity
        }
    
    @staticmethod
    def equip_item(character_id, inventory_item_id):
        """Equipa un item del inventario"""
        inv_item = db.session.get(InventoryItem, inventory_item_id)
        
        if not inv_item or inv_item.character_id != character_id:
            return {"error": "Item no encontrado o no pertenece al personaje"}
        
        # Desequipar items del mismo tipo
        same_type_items = InventoryItem.query.join(Item).filter(
            InventoryItem.character_id == character_id,
            Item.item_type == inv_item.item.item_type,
            InventoryItem.equipped == True
        ).all()
        
        for item in same_type_items:
            item.equipped = False
        
        inv_item.equipped = True
        db.session.commit()
        
        return {
            "status": "equipped",
            "item": inv_item.item.to_dict()
        }
    
    @staticmethod
    def unequip_item(character_id, inventory_item_id):
        """Desequipa un item"""
        inv_item = db.session.get(InventoryItem, inventory_item_id)
        
        if not inv_item or inv_item.character_id != character_id:
            return {"error": "Item no encontrado"}
        
        inv_item.equipped = False
        db.session.commit()
        
        return {"status": "unequipped", "item": inv_item.item.to_dict()}
    
    @staticmethod
    def get_equipped_items(character_id):
        """Obtiene todos los items equipados de un personaje"""
        equipped = InventoryItem.query.filter_by(
            character_id=character_id,
            equipped=True
        ).all()
        
        return [e.to_dict() for e in equipped]
    
    @staticmethod
    def calculate_equipment_bonus(character_id):
        """Calcula el bonus de ataque y defensa de los items equipados"""
        equipped = InventoryItem.query.filter_by(
            character_id=character_id,
            equipped=True
        ).all()
        
        attack_bonus = 0
        defense_bonus = 0
        
        for inv_item in equipped:
            attack_bonus += inv_item.item.attack_bonus
            defense_bonus += inv_item.item.defense_bonus
        
        return {
            "attack_bonus": attack_bonus,
            "defense_bonus": defense_bonus
        }
    
    @staticmethod
    def use_consumable(character_id, inventory_item_id):
        """Usa un item consumible (poción, etc)"""
        inv_item = db.session.get(InventoryItem, inventory_item_id)
        
        if not inv_item or inv_item.character_id != character_id:
            return {"error": "Item no encontrado"}
        
        item = inv_item.item
        
        if item.item_type not in ["potion", "consumable"]:
            return {"error": "Este item no es consumible"}
        
        character = db.session.get(Character, character_id)
        old_hp = character.hp
        character.hp = min(character.max_hp, character.hp + item.hp_bonus)
        actual_heal = character.hp - old_hp
        
        inv_item.quantity -= 1
        
        if inv_item.quantity <= 0:
            db.session.delete(inv_item)
        
        db.session.commit()
        
        return {
            "status": "consumed",
            "item": item.to_dict(),
            "hp_restored": actual_heal,
            "current_hp": character.hp
        }
