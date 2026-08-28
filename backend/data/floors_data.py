# Datos de los 100 pisos de Aincrad basados en lore original de SAO
# Con adaptaciones para OC original

FLOORS_DATA = [
    # Pisos 1-10: Iniciación
    {
        "floor": 1,
        "name": "The Elf Capital",
        "description": "Puerta de entrada a Aincrad. Ciudad tecnológica con toques élficos. Aquí comienza tu aventura.",
        "main_city": "Tolbana",
        "boss_name": "Illfang the Kobold Lord",
        "boss_level": 5,
        "theme": "urban_fantasy",
        "enemies": [
            {"name": "Horned Boar", "level": 1, "hp": 20, "attack": 3, "defense": 1},
            {"name": "Frenzy Boar", "level": 2, "hp": 30, "attack": 4, "defense": 2},
        ]
    },
    {
        "floor": 2,
        "name": "Forestland",
        "description": "Bosque antiguo lleno de magia. Primer encuentro real con la naturaleza de Aincrad.",
        "main_city": "Urbus",
        "boss_name": "Elven King",
        "boss_level": 10,
        "theme": "forest",
        "enemies": [
            {"name": "Wind Wasp", "level": 2, "hp": 25, "attack": 4, "defense": 2},
            {"name": "Dryad Sapling", "level": 3, "hp": 35, "attack": 5, "defense": 3},
        ]
    },
    {
        "floor": 3,
        "name": "The Stonewall Mountains",
        "description": "Montañas rocosas donde resuena el eco de mil batallas. Paisaje árido pero hermoso.",
        "main_city": "Zumfut",
        "boss_name": "Stone Golem",
        "boss_level": 15,
        "theme": "mountain",
        "enemies": [
            {"name": "Stone Lizard", "level": 3, "hp": 40, "attack": 5, "defense": 4},
            {"name": "Rock Armadillo", "level": 4, "hp": 50, "attack": 6, "defense": 5},
        ]
    },
    {
        "floor": 4,
        "name": "Rovia",
        "description": "Ciudad portuaria con playas de arena dorada. Lugar de descanso y abastecimiento.",
        "main_city": "Rovia Port",
        "boss_name": "Sea Serpent",
        "boss_level": 20,
        "theme": "ocean",
        "enemies": [
            {"name": "Giant Crab", "level": 4, "hp": 45, "attack": 6, "defense": 5},
            {"name": "Poison Jellyfish", "level": 5, "hp": 40, "attack": 7, "defense": 3},
        ]
    },
    {
        "floor": 5,
        "name": "Mishe Forest",
        "description": "Bosque misterioso donde la luz apenas penetra. Hogar de criaturas ancestrales.",
        "main_city": "Lindarth",
        "boss_name": "Forest Wyvern",
        "boss_level": 25,
        "theme": "dark_forest",
        "enemies": [
            {"name": "Shadow Wolf", "level": 5, "hp": 55, "attack": 8, "defense": 4},
            {"name": "Corrupted Treant", "level": 6, "hp": 65, "attack": 9, "defense": 6},
        ]
    },
    {
        "floor": 6,
        "name": "The Maze of Mirrors",
        "description": "Laberinto sin fin donde la realidad se retuerce. Prueba de cordura mental.",
        "main_city": "Illyaster",
        "boss_name": "Mirror Golem",
        "boss_level": 30,
        "theme": "dungeon",
        "enemies": [
            {"name": "Phantom Echo", "level": 6, "hp": 50, "attack": 10, "defense": 5},
            {"name": "Mirrored Beast", "level": 7, "hp": 70, "attack": 11, "defense": 7},
        ]
    },
    {
        "floor": 7,
        "name": "Kamdet Valley",
        "description": "Valle donde los acantilados tocan las nubes. Belleza vertiginosa y peligrosa.",
        "main_city": "Kamdet Town",
        "boss_name": "Sky Guardian",
        "boss_level": 35,
        "theme": "canyon",
        "enemies": [
            {"name": "Cliff Harpy", "level": 7, "hp": 60, "attack": 11, "defense": 6},
            {"name": "Wind Drake", "level": 8, "hp": 80, "attack": 12, "defense": 7},
        ]
    },
    {
        "floor": 8,
        "name": "The Inferno Volcano",
        "description": "Volcán activo lleno de lava y fuego ardiente. Solo los valientes avanzan aquí.",
        "main_city": "Magma Town",
        "boss_name": "Fire Lord",
        "boss_level": 40,
        "theme": "volcano",
        "enemies": [
            {"name": "Lava Elemental", "level": 8, "hp": 75, "attack": 13, "defense": 8},
            {"name": "Obsidian Dragon", "level": 9, "hp": 90, "attack": 14, "defense": 9},
        ]
    },
    {
        "floor": 9,
        "name": "Snowfield",
        "description": "Tundra helada eterna. El frio aquí no es solo físico sino espiritual.",
        "main_city": "Snowpeak Village",
        "boss_name": "Frost Queen",
        "boss_level": 45,
        "theme": "snow",
        "enemies": [
            {"name": "Frost Wolf", "level": 9, "hp": 70, "attack": 14, "defense": 9},
            {"name": "Ice Wyvern", "level": 10, "hp": 100, "attack": 15, "defense": 10},
        ]
    },
    {
        "floor": 10,
        "name": "The Goblin Fortress",
        "description": "Fortaleza goblin antigua. Primer punto de control importante en la escalada.",
        "main_city": "Goblin's Rest",
        "boss_name": "Goblin King",
        "boss_level": 50,
        "theme": "fortress",
        "enemies": [
            {"name": "Goblin Archer", "level": 10, "hp": 65, "attack": 12, "defense": 8},
            {"name": "Goblin Knight", "level": 11, "hp": 85, "attack": 15, "defense": 11},
        ]
    },
    
    # Pisos 11-25: Zona intermedia
    {
        "floor": 11,
        "name": "The Dark Marshes",
        "description": "Pantano oscuro lleno de miasma. Zona de transición a regiones más peligrosas.",
        "main_city": "Bog Town",
        "boss_name": "Swamp Hydra",
        "boss_level": 55,
        "theme": "swamp",
        "enemies": [
            {"name": "Toxic Toad", "level": 11, "hp": 75, "attack": 13, "defense": 9},
            {"name": "Poisonous Serpent", "level": 12, "hp": 90, "attack": 14, "defense": 10},
        ]
    },
    {
        "floor": 12,
        "name": "The Pirate's Graveyard",
        "description": "Ruinas de un imperio pirata antiguo. Tesoros y maldiciones acechan.",
        "main_city": "Pirate's Haven",
        "boss_name": "Phantom Pirate",
        "boss_level": 60,
        "theme": "ruins",
        "enemies": [
            {"name": "Undead Pirate", "level": 12, "hp": 80, "attack": 14, "defense": 11},
            {"name": "Cursed Sailor", "level": 13, "hp": 95, "attack": 15, "defense": 12},
        ]
    },
    {
        "floor": 13,
        "name": "The Angel's Throne",
        "description": "Templo celestial antiguo. Luz y oscuridad coexisten en equilibrio.",
        "main_city": "Celestial Town",
        "boss_name": "Fallen Angel",
        "boss_level": 65,
        "theme": "celestial",
        "enemies": [
            {"name": "Holy Guardian", "level": 13, "hp": 85, "attack": 15, "defense": 12},
            {"name": "Corrupted Seraph", "level": 14, "hp": 105, "attack": 16, "defense": 13},
        ]
    },
    {
        "floor": 14,
        "name": "The Demon's Lair",
        "description": "Guarida demoníaca. La maldad pura emana de cada rincón.",
        "main_city": "Demon's Market",
        "boss_name": "Lesser Demon",
        "boss_level": 70,
        "theme": "demon_realm",
        "enemies": [
            {"name": "Imp Servant", "level": 14, "hp": 80, "attack": 16, "defense": 13},
            {"name": "Demon Warrior", "level": 15, "hp": 110, "attack": 17, "defense": 14},
        ]
    },
    {
        "floor": 15,
        "name": "The Cursed Library",
        "description": "Biblioteca antigüa donde el conocimiento es poder y peligro.",
        "main_city": "Scholar's Rest",
        "boss_name": "Grimoire Guardian",
        "boss_level": 75,
        "theme": "library",
        "enemies": [
            {"name": "Haunted Tome", "level": 15, "hp": 75, "attack": 17, "defense": 14},
            {"name": "Spectral Scholar", "level": 16, "hp": 115, "attack": 18, "defense": 15},
        ]
    },
    {
        "floor": 25,
        "name": "The Gleameyes Lair",
        "description": "Madriguera del legendario Gleameyes. Boss de importancia mitológica.",
        "main_city": "Crystal City",
        "boss_name": "The Gleameyes",
        "boss_level": 100,
        "theme": "crystal_palace",
        "enemies": [
            {"name": "Crystal Golem", "level": 25, "hp": 150, "attack": 25, "defense": 20},
            {"name": "Gleameyes Servant", "level": 26, "hp": 180, "attack": 28, "defense": 22},
        ]
    },
    
    # Piso 50: Zona Alta
    {
        "floor": 50,
        "name": "The Sky Citadel",
        "description": "Ciudadela flotante en las nubes. Punto medio de la travesía por Aincrad.",
        "main_city": "Floating City",
        "boss_name": "Sky Sovereign",
        "boss_level": 150,
        "theme": "sky_palace",
        "enemies": [
            {"name": "Sky Knight", "level": 50, "hp": 200, "attack": 40, "defense": 35},
            {"name": "Celestial Guardian", "level": 51, "hp": 250, "attack": 45, "defense": 40},
        ]
    },
    
    # Piso 74: Cercano al Final
    {
        "floor": 74,
        "name": "The Frozen Throne",
        "description": "Trono antiguo congelado en hielo eterno. La nieve aquí es polvo de estrella.",
        "main_city": "Frozen Capital",
        "boss_name": "Winter King",
        "boss_level": 200,
        "theme": "frost_palace",
        "enemies": [
            {"name": "Frost Paladin", "level": 74, "hp": 250, "attack": 50, "defense": 45},
            {"name": "Eternal Blizzard", "level": 75, "hp": 300, "attack": 55, "defense": 50},
        ]
    },
    
    # Piso 75: BOSS FINAL - Akihiko Kayaba (Heathcliff)
    {
        "floor": 75,
        "name": "The Aincrad Castle",
        "description": "Castillo principal de Aincrad. Centro del poder. Aquí reside el creador del juego.",
        "main_city": "Aincrad Town",
        "boss_name": "Heathcliff - The Paladin",
        "boss_level": 250,
        "theme": "main_castle",
        "enemies": [
            {"name": "Heathcliff's Guard", "level": 75, "hp": 200, "attack": 60, "defense": 50},
            {"name": "Paladin of Aincrad", "level": 76, "hp": 300, "attack": 70, "defense": 60},
        ]
    },
]

# Sistema de recompensas por piso
FLOOR_REWARDS = {
    1: {"exp": 50, "col": 100},
    2: {"exp": 75, "col": 150},
    3: {"exp": 100, "col": 200},
    5: {"exp": 150, "col": 300},
    10: {"exp": 300, "col": 600},
    25: {"exp": 1000, "col": 2000},
    50: {"exp": 2000, "col": 5000},
    74: {"exp": 5000, "col": 10000},
    75: {"exp": 10000, "col": 20000},
}

# Descripciones narrativas para cada piso
FLOOR_NARRATIVES = {
    1: "Despiertas en una ciudad extraña pero familiar. Los edificios brillan con una luz sobrenatural. Escuchas voces lejanas... ¿Es este realmente el Aincrad del que todos hablan?",
    2: "Entras en un bosque ancestral. Los árboles susurran historias antiguas. Sientes la presencia de magia antigua en el aire.",
    5: "Has escalado lo suficiente. Ahora eres parte de la élite de Aincrad. Pero los desafíos apenas comienzan.",
    10: "Alcanzas un punto de control importante. Los rumores sobre tu valor llegan a otros jugadores. ¿Serás reconocido como uno de los Frontiersmen?",
    25: "La leyenda del Gleameyes resuena en toda Aincrad. Se dice que es invencible. Pero tú has llegado hasta aquí...",
    50: "Has llegado a la mitad de Aincrad. El camino ha sido largo y lleno de cicatrices. Pero también de gloria.",
    74: "El trono congelado aguarda. Se rumorea que después de esto, solo falta el castillo principal.",
    75: "Finalmente lo ves. El Castillo de Aincrad brilla en el horizonte. Aquí termina tu viaje... o comienza uno nuevo.",
}

def get_floor_by_number(floor_number):
    """Obtener datos de un piso específico"""
    for floor in FLOORS_DATA:
        if floor["floor"] == floor_number:
            return floor
    return None

def get_available_floors():
    """Obtener lista de todos los pisos disponibles"""
    return [f["floor"] for f in FLOORS_DATA]
