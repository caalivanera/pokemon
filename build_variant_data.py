"""
Pokemon Variant Data Builder
Creates comprehensive variant entries for all Pokemon forms

This script will:
1. Read existing national_dex.csv
2. Create variant entries for Mega, Regional, Gigantamax forms
3. Generate proper stat distributions
4. Map sprite paths
5. Output enhanced CSV with all variants
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# ==================== VARIANT DEFINITIONS ====================

# Mega Evolutions with stat changes
MEGA_EVOLUTIONS = {
    # Format: base_id: {'form': 'X/Y/None', 'stats': {...}, 'ability': '...', 'types': [...]}
    3: {  # Venusaur
        'form': 'Mega Venusaur',
        'stats': {'hp': 80, 'attack': 100, 'defense': 123, 'sp_attack': 122, 'sp_defense': 120, 'speed': 80},
        'ability': 'Thick Fat',
        'types': ['Grass', 'Poison'],
        'stone': 'Venusaurite'
    },
    6: {  # Charizard - TWO forms!
        'X': {
            'form': 'Mega Charizard X',
            'stats': {'hp': 78, 'attack': 130, 'defense': 111, 'sp_attack': 130, 'sp_defense': 85, 'speed': 100},
            'ability': 'Tough Claws',
            'types': ['Fire', 'Dragon'],
            'stone': 'Charizardite X',
            'description': 'Black dragon with blue flames. Fire/Dragon type.'
        },
        'Y': {
            'form': 'Mega Charizard Y',
            'stats': {'hp': 78, 'attack': 104, 'defense': 78, 'sp_attack': 159, 'sp_defense': 115, 'speed': 100},
            'ability': 'Drought',
            'types': ['Fire', 'Flying'],
            'stone': 'Charizardite Y',
            'description': 'Sleeker form with enhanced special attack. Sets harsh sunlight.'
        }
    },
    9: {  # Blastoise
        'form': 'Mega Blastoise',
        'stats': {'hp': 79, 'attack': 103, 'defense': 120, 'sp_attack': 135, 'sp_defense': 115, 'speed': 78},
        'ability': 'Mega Launcher',
        'types': ['Water', None],
        'stone': 'Blastoisite'
    },
    15: {  # Beedrill
        'form': 'Mega Beedrill',
        'stats': {'hp': 65, 'attack': 150, 'defense': 40, 'sp_attack': 15, 'sp_defense': 80, 'speed': 145},
        'ability': 'Adaptability',
        'types': ['Bug', 'Poison'],
        'stone': 'Beedrillite'
    },
    18: {  # Pidgeot
        'form': 'Mega Pidgeot',
        'stats': {'hp': 83, 'attack': 80, 'defense': 80, 'sp_attack': 135, 'sp_defense': 80, 'speed': 121},
        'ability': 'No Guard',
        'types': ['Normal', 'Flying'],
        'stone': 'Pidgeotite'
    },
    65: {  # Alakazam
        'form': 'Mega Alakazam',
        'stats': {'hp': 55, 'attack': 50, 'defense': 65, 'sp_attack': 175, 'sp_defense': 105, 'speed': 150},
        'ability': 'Trace',
        'types': ['Psychic', None],
        'stone': 'Alakazite'
    },
    80: {  # Slowbro
        'form': 'Mega Slowbro',
        'stats': {'hp': 95, 'attack': 75, 'defense': 180, 'sp_attack': 130, 'sp_defense': 80, 'speed': 30},
        'ability': 'Shell Armor',
        'types': ['Water', 'Psychic'],
        'stone': 'Slowbronite'
    },
    94: {  # Gengar
        'form': 'Mega Gengar',
        'stats': {'hp': 60, 'attack': 65, 'defense': 80, 'sp_attack': 170, 'sp_defense': 95, 'speed': 130},
        'ability': 'Shadow Tag',
        'types': ['Ghost', 'Poison'],
        'stone': 'Gengarite'
    },
    115: {  # Kangaskhan
        'form': 'Mega Kangaskhan',
        'stats': {'hp': 105, 'attack': 125, 'defense': 100, 'sp_attack': 60, 'sp_defense': 100, 'speed': 100},
        'ability': 'Parental Bond',
        'types': ['Normal', None],
        'stone': 'Kangaskhanite'
    },
    127: {  # Pinsir
        'form': 'Mega Pinsir',
        'stats': {'hp': 65, 'attack': 155, 'defense': 120, 'sp_attack': 65, 'sp_defense': 90, 'speed': 105},
        'ability': 'Aerilate',
        'types': ['Bug', 'Flying'],
        'stone': 'Pinsirite'
    },
    130: {  # Gyarados
        'form': 'Mega Gyarados',
        'stats': {'hp': 95, 'attack': 155, 'defense': 109, 'sp_attack': 70, 'sp_defense': 130, 'speed': 81},
        'ability': 'Mold Breaker',
        'types': ['Water', 'Dark'],
        'stone': 'Gyaradosite'
    },
    142: {  # Aerodactyl
        'form': 'Mega Aerodactyl',
        'stats': {'hp': 80, 'attack': 135, 'defense': 85, 'sp_attack': 70, 'sp_defense': 95, 'speed': 150},
        'ability': 'Tough Claws',
        'types': ['Rock', 'Flying'],
        'stone': 'Aerodactylite'
    },
    150: {  # Mewtwo - TWO forms!
        'X': {
            'form': 'Mega Mewtwo X',
            'stats': {'hp': 106, 'attack': 190, 'defense': 100, 'sp_attack': 154, 'sp_defense': 100, 'speed': 130},
            'ability': 'Steadfast',
            'types': ['Psychic', 'Fighting'],
            'stone': 'Mewtwonite X'
        },
        'Y': {
            'form': 'Mega Mewtwo Y',
            'stats': {'hp': 106, 'attack': 150, 'defense': 70, 'sp_attack': 194, 'sp_defense': 120, 'speed': 140},
            'ability': 'Insomnia',
            'types': ['Psychic', None],
            'stone': 'Mewtwonite Y'
        }
    },
    # Gen 3 Megas
    181: {'form': 'Mega Ampharos', 'stats': {'hp': 90, 'attack': 95, 'defense': 105, 'sp_attack': 165, 'sp_defense': 110, 'speed': 45}, 'ability': 'Mold Breaker', 'types': ['Electric', 'Dragon'], 'stone': 'Ampharosite'},
    208: {'form': 'Mega Steelix', 'stats': {'hp': 75, 'attack': 125, 'defense': 230, 'sp_attack': 55, 'sp_defense': 95, 'speed': 30}, 'ability': 'Sand Force', 'types': ['Steel', 'Ground'], 'stone': 'Steelixite'},
    212: {'form': 'Mega Scizor', 'stats': {'hp': 70, 'attack': 150, 'defense': 140, 'sp_attack': 65, 'sp_defense': 100, 'speed': 75}, 'ability': 'Technician', 'types': ['Bug', 'Steel'], 'stone': 'Scizorite'},
    214: {'form': 'Mega Heracross', 'stats': {'hp': 80, 'attack': 185, 'defense': 115, 'sp_attack': 40, 'sp_defense': 105, 'speed': 75}, 'ability': 'Skill Link', 'types': ['Bug', 'Fighting'], 'stone': 'Heracronite'},
    229: {'form': 'Mega Houndoom', 'stats': {'hp': 75, 'attack': 90, 'defense': 90, 'sp_attack': 140, 'sp_defense': 90, 'speed': 115}, 'ability': 'Solar Power', 'types': ['Dark', 'Fire'], 'stone': 'Houndoominite'},
    248: {'form': 'Mega Tyranitar', 'stats': {'hp': 100, 'attack': 164, 'defense': 150, 'sp_attack': 95, 'sp_defense': 120, 'speed': 71}, 'ability': 'Sand Stream', 'types': ['Rock', 'Dark'], 'stone': 'Tyranitarite'},
    # Gen 3 Megas
    254: {'form': 'Mega Sceptile', 'stats': {'hp': 70, 'attack': 110, 'defense': 75, 'sp_attack': 145, 'sp_defense': 85, 'speed': 145}, 'ability': 'Lightning Rod', 'types': ['Grass', 'Dragon'], 'stone': 'Sceptilite'},
    257: {'form': 'Mega Blaziken', 'stats': {'hp': 80, 'attack': 160, 'defense': 80, 'sp_attack': 130, 'sp_defense': 80, 'speed': 100}, 'ability': 'Speed Boost', 'types': ['Fire', 'Fighting'], 'stone': 'Blazikenite'},
    260: {'form': 'Mega Swampert', 'stats': {'hp': 100, 'attack': 150, 'defense': 110, 'sp_attack': 95, 'sp_defense': 110, 'speed': 70}, 'ability': 'Swift Swim', 'types': ['Water', 'Ground'], 'stone': 'Swampertite'},
    282: {'form': 'Mega Gardevoir', 'stats': {'hp': 68, 'attack': 85, 'defense': 65, 'sp_attack': 165, 'sp_defense': 135, 'speed': 100}, 'ability': 'Pixilate', 'types': ['Psychic', 'Fairy'], 'stone': 'Gardevoirite'},
    302: {'form': 'Mega Sableye', 'stats': {'hp': 50, 'attack': 85, 'defense': 125, 'sp_attack': 85, 'sp_defense': 115, 'speed': 20}, 'ability': 'Magic Bounce', 'types': ['Dark', 'Ghost'], 'stone': 'Sablenite'},
    303: {'form': 'Mega Mawile', 'stats': {'hp': 50, 'attack': 105, 'defense': 125, 'sp_attack': 55, 'sp_defense': 95, 'speed': 50}, 'ability': 'Huge Power', 'types': ['Steel', 'Fairy'], 'stone': 'Mawilite'},
    306: {'form': 'Mega Aggron', 'stats': {'hp': 70, 'attack': 140, 'defense': 230, 'sp_attack': 60, 'sp_defense': 80, 'speed': 50}, 'ability': 'Filter', 'types': ['Steel', None], 'stone': 'Aggronite'},
    308: {'form': 'Mega Medicham', 'stats': {'hp': 60, 'attack': 100, 'defense': 85, 'sp_attack': 80, 'sp_defense': 85, 'speed': 100}, 'ability': 'Pure Power', 'types': ['Fighting', 'Psychic'], 'stone': 'Medichamite'},
    310: {'form': 'Mega Manectric', 'stats': {'hp': 70, 'attack': 75, 'defense': 80, 'sp_attack': 135, 'sp_defense': 80, 'speed': 135}, 'ability': 'Intimidate', 'types': ['Electric', None], 'stone': 'Manectite'},
    319: {'form': 'Mega Sharpedo', 'stats': {'hp': 70, 'attack': 140, 'defense': 70, 'sp_attack': 110, 'sp_defense': 65, 'speed': 105}, 'ability': 'Strong Jaw', 'types': ['Water', 'Dark'], 'stone': 'Sharpedonite'},
    323: {'form': 'Mega Camerupt', 'stats': {'hp': 70, 'attack': 120, 'defense': 100, 'sp_attack': 145, 'sp_defense': 105, 'speed': 20}, 'ability': 'Sheer Force', 'types': ['Fire', 'Ground'], 'stone': 'Cameruptite'},
    334: {'form': 'Mega Altaria', 'stats': {'hp': 75, 'attack': 110, 'defense': 110, 'sp_attack': 110, 'sp_defense': 105, 'speed': 80}, 'ability': 'Pixilate', 'types': ['Dragon', 'Fairy'], 'stone': 'Altarianite'},
    354: {'form': 'Mega Banette', 'stats': {'hp': 64, 'attack': 165, 'defense': 75, 'sp_attack': 93, 'sp_defense': 83, 'speed': 75}, 'ability': 'Prankster', 'types': ['Ghost', None], 'stone': 'Banettite'},
    359: {'form': 'Mega Absol', 'stats': {'hp': 65, 'attack': 150, 'defense': 60, 'sp_attack': 115, 'sp_defense': 60, 'speed': 115}, 'ability': 'Magic Bounce', 'types': ['Dark', None], 'stone': 'Absolite'},
    362: {'form': 'Mega Glalie', 'stats': {'hp': 80, 'attack': 120, 'defense': 80, 'sp_attack': 120, 'sp_defense': 80, 'speed': 100}, 'ability': 'Refrigerate', 'types': ['Ice', None], 'stone': 'Glalitite'},
    373: {'form': 'Mega Salamence', 'stats': {'hp': 95, 'attack': 145, 'defense': 130, 'sp_attack': 120, 'sp_defense': 90, 'speed': 120}, 'ability': 'Aerilate', 'types': ['Dragon', 'Flying'], 'stone': 'Salamencite'},
    376: {'form': 'Mega Metagross', 'stats': {'hp': 80, 'attack': 145, 'defense': 150, 'sp_attack': 105, 'sp_defense': 110, 'speed': 110}, 'ability': 'Tough Claws', 'types': ['Steel', 'Psychic'], 'stone': 'Metagrossite'},
    380: {'form': 'Mega Latias', 'stats': {'hp': 80, 'attack': 100, 'defense': 120, 'sp_attack': 140, 'sp_defense': 150, 'speed': 110}, 'ability': 'Levitate', 'types': ['Dragon', 'Psychic'], 'stone': 'Latiasite'},
    381: {'form': 'Mega Latios', 'stats': {'hp': 80, 'attack': 130, 'defense': 100, 'sp_attack': 160, 'sp_defense': 120, 'speed': 110}, 'ability': 'Levitate', 'types': ['Dragon', 'Psychic'], 'stone': 'Latiosite'},
    384: {'form': 'Mega Rayquaza', 'stats': {'hp': 105, 'attack': 180, 'defense': 100, 'sp_attack': 180, 'sp_defense': 100, 'speed': 115}, 'ability': 'Delta Stream', 'types': ['Dragon', 'Flying'], 'stone': None},  # No stone!
    # Gen 4-6 Megas
    428: {'form': 'Mega Lopunny', 'stats': {'hp': 65, 'attack': 136, 'defense': 94, 'sp_attack': 54, 'sp_defense': 96, 'speed': 135}, 'ability': 'Scrappy', 'types': ['Normal', 'Fighting'], 'stone': 'Lopunnite'},
    445: {'form': 'Mega Garchomp', 'stats': {'hp': 108, 'attack': 170, 'defense': 115, 'sp_attack': 120, 'sp_defense': 95, 'speed': 92}, 'ability': 'Sand Force', 'types': ['Dragon', 'Ground'], 'stone': 'Garchompite'},
    448: {'form': 'Mega Lucario', 'stats': {'hp': 70, 'attack': 145, 'defense': 88, 'sp_attack': 140, 'sp_defense': 70, 'speed': 112}, 'ability': 'Adaptability', 'types': ['Fighting', 'Steel'], 'stone': 'Lucarionite'},
    460: {'form': 'Mega Abomasnow', 'stats': {'hp': 90, 'attack': 132, 'defense': 105, 'sp_attack': 132, 'sp_defense': 105, 'speed': 30}, 'ability': 'Snow Warning', 'types': ['Grass', 'Ice'], 'stone': 'Abomasite'},
    475: {'form': 'Mega Gallade', 'stats': {'hp': 68, 'attack': 165, 'defense': 95, 'sp_attack': 65, 'sp_defense': 115, 'speed': 110}, 'ability': 'Inner Focus', 'types': ['Psychic', 'Fighting'], 'stone': 'Galladite'},
    531: {'form': 'Mega Audino', 'stats': {'hp': 103, 'attack': 60, 'defense': 126, 'sp_attack': 80, 'sp_defense': 126, 'speed': 50}, 'ability': 'Healer', 'types': ['Normal', 'Fairy'], 'stone': 'Audinite'},
    719: {'form': 'Mega Diancie', 'stats': {'hp': 50, 'attack': 160, 'defense': 110, 'sp_attack': 160, 'sp_defense': 110, 'speed': 110}, 'ability': 'Magic Bounce', 'types': ['Rock', 'Fairy'], 'stone': 'Diancieite'},
}

# Regional Forms (Alolan, Galarian, Hisuian, Paldean)
REGIONAL_FORMS = {
    # Alolan Forms
    19: {'form': 'Alolan Rattata', 'types': ['Dark', 'Normal'], 'stats': {'hp': 30, 'attack': 56, 'defense': 35, 'sp_attack': 25, 'sp_defense': 35, 'speed': 72}},
    20: {'form': 'Alolan Raticate', 'types': ['Dark', 'Normal'], 'stats': {'hp': 75, 'attack': 71, 'defense': 70, 'sp_attack': 40, 'sp_defense': 80, 'speed': 77}},
    26: {'form': 'Alolan Raichu', 'types': ['Electric', 'Psychic'], 'stats': {'hp': 60, 'attack': 85, 'defense': 50, 'sp_attack': 95, 'sp_defense': 85, 'speed': 110}},
    27: {'form': 'Alolan Sandshrew', 'types': ['Ice', 'Steel'], 'stats': {'hp': 50, 'attack': 75, 'defense': 90, 'sp_attack': 10, 'sp_defense': 35, 'speed': 40}},
    28: {'form': 'Alolan Sandslash', 'types': ['Ice', 'Steel'], 'stats': {'hp': 75, 'attack': 100, 'defense': 120, 'sp_attack': 25, 'sp_defense': 65, 'speed': 65}},
    37: {'form': 'Alolan Vulpix', 'types': ['Ice', None], 'stats': {'hp': 38, 'attack': 41, 'defense': 40, 'sp_attack': 50, 'sp_defense': 65, 'speed': 65}},
    38: {'form': 'Alolan Ninetales', 'types': ['Ice', 'Fairy'], 'stats': {'hp': 73, 'attack': 67, 'defense': 75, 'sp_attack': 81, 'sp_defense': 100, 'speed': 109}},
    50: {'form': 'Alolan Diglett', 'types': ['Ground', 'Steel'], 'stats': {'hp': 10, 'attack': 55, 'defense': 30, 'sp_attack': 35, 'sp_defense': 45, 'speed': 90}},
    51: {'form': 'Alolan Dugtrio', 'types': ['Ground', 'Steel'], 'stats': {'hp': 35, 'attack': 100, 'defense': 60, 'sp_attack': 50, 'sp_defense': 70, 'speed': 110}},
    52: {'form': 'Alolan Meowth', 'types': ['Dark', None], 'stats': {'hp': 40, 'attack': 35, 'defense': 35, 'sp_attack': 50, 'sp_defense': 40, 'speed': 90}},
    53: {'form': 'Alolan Persian', 'types': ['Dark', None], 'stats': {'hp': 65, 'attack': 60, 'defense': 60, 'sp_attack': 75, 'sp_defense': 65, 'speed': 115}},
    74: {'form': 'Alolan Geodude', 'types': ['Rock', 'Electric'], 'stats': {'hp': 40, 'attack': 80, 'defense': 100, 'sp_attack': 30, 'sp_defense': 30, 'speed': 20}},
    75: {'form': 'Alolan Graveler', 'types': ['Rock', 'Electric'], 'stats': {'hp': 55, 'attack': 95, 'defense': 115, 'sp_attack': 45, 'sp_defense': 45, 'speed': 35}},
    76: {'form': 'Alolan Golem', 'types': ['Rock', 'Electric'], 'stats': {'hp': 80, 'attack': 120, 'defense': 130, 'sp_attack': 55, 'sp_defense': 65, 'speed': 45}},
    88: {'form': 'Alolan Grimer', 'types': ['Poison', 'Dark'], 'stats': {'hp': 80, 'attack': 80, 'defense': 50, 'sp_attack': 40, 'sp_defense': 50, 'speed': 25}},
    89: {'form': 'Alolan Muk', 'types': ['Poison', 'Dark'], 'stats': {'hp': 105, 'attack': 105, 'defense': 75, 'sp_attack': 65, 'sp_defense': 100, 'speed': 50}},
    103: {'form': 'Alolan Exeggutor', 'types': ['Grass', 'Dragon'], 'stats': {'hp': 95, 'attack': 105, 'defense': 85, 'sp_attack': 125, 'sp_defense': 75, 'speed': 45}},
    105: {'form': 'Alolan Marowak', 'types': ['Fire', 'Ghost'], 'stats': {'hp': 60, 'attack': 80, 'defense': 110, 'sp_attack': 50, 'sp_defense': 80, 'speed': 45}},
    
    # Galarian Forms (selected examples)
    52: {'form': 'Galarian Meowth', 'types': ['Steel', None], 'stats': {'hp': 50, 'attack': 65, 'defense': 55, 'sp_attack': 40, 'sp_defense': 40, 'speed': 40}},
    77: {'form': 'Galarian Ponyta', 'types': ['Psychic', None], 'stats': {'hp': 50, 'attack': 85, 'defense': 55, 'sp_attack': 65, 'sp_defense': 65, 'speed': 90}},
    78: {'form': 'Galarian Rapidash', 'types': ['Psychic', 'Fairy'], 'stats': {'hp': 65, 'attack': 100, 'defense': 70, 'sp_attack': 80, 'sp_defense': 80, 'speed': 105}},
    79: {'form': 'Galarian Slowpoke', 'types': ['Psychic', None], 'stats': {'hp': 90, 'attack': 65, 'defense': 65, 'sp_attack': 40, 'sp_defense': 40, 'speed': 15}},
    80: {'form': 'Galarian Slowbro', 'types': ['Poison', 'Psychic'], 'stats': {'hp': 95, 'attack': 100, 'defense': 95, 'sp_attack': 100, 'sp_defense': 70, 'speed': 30}},
    83: {'form': 'Galarian Farfetch\'d', 'types': ['Fighting', None], 'stats': {'hp': 52, 'attack': 95, 'defense': 55, 'sp_attack': 58, 'sp_defense': 62, 'speed': 55}},
    110: {'form': 'Galarian Weezing', 'types': ['Poison', 'Fairy'], 'stats': {'hp': 65, 'attack': 90, 'defense': 120, 'sp_attack': 85, 'sp_defense': 70, 'speed': 60}},
    122: {'form': 'Galarian Mr. Mime', 'types': ['Ice', 'Psychic'], 'stats': {'hp': 50, 'attack': 65, 'defense': 65, 'sp_attack': 90, 'sp_defense': 90, 'speed': 100}},
}

# Gigantamax Forms
GIGANTAMAX_FORMS = {
    3: {'form': 'Gigantamax Venusaur', 'move': 'G-Max Vine Lash'},
    6: {'form': 'Gigantamax Charizard', 'move': 'G-Max Wildfire'},
    9: {'form': 'Gigantamax Blastoise', 'move': 'G-Max Cannonade'},
    12: {'form': 'Gigantamax Butterfree', 'move': 'G-Max Befuddle'},
    25: {'form': 'Gigantamax Pikachu', 'move': 'G-Max Volt Crash'},
    52: {'form': 'Gigantamax Meowth', 'move': 'G-Max Gold Rush'},
    68: {'form': 'Gigantamax Machamp', 'move': 'G-Max Chi Strike'},
    94: {'form': 'Gigantamax Gengar', 'move': 'G-Max Terror'},
    99: {'form': 'Gigantamax Kingler', 'move': 'G-Max Foam Burst'},
    131: {'form': 'Gigantamax Lapras', 'move': 'G-Max Resonance'},
    133: {'form': 'Gigantamax Eevee', 'move': 'G-Max Cuddle'},
    143: {'form': 'Gigantamax Snorlax', 'move': 'G-Max Replenish'},
    569: {'form': 'Gigantamax Garbodor', 'move': 'G-Max Malodor'},
    809: {'form': 'Gigantamax Melmetal', 'move': 'G-Max Meltdown'},
    812: {'form': 'Gigantamax Rillaboom', 'move': 'G-Max Drum Solo'},
    815: {'form': 'Gigantamax Cinderace', 'move': 'G-Max Fireball'},
    818: {'form': 'Gigantamax Inteleon', 'move': 'G-Max Hydrosnipe'},
    823: {'form': 'Gigantamax Corviknight', 'move': 'G-Max Wind Rage'},
    826: {'form': 'Gigantamax Orbeetle', 'move': 'G-Max Gravitas'},
    834: {'form': 'Gigantamax Drednaw', 'move': 'G-Max Stonesurge'},
    839: {'form': 'Gigantamax Coalossal', 'move': 'G-Max Volcalith'},
    841: {'form': 'Gigantamax Flapple', 'move': 'G-Max Tartness'},
    842: {'form': 'Gigantamax Appletun', 'move': 'G-Max Sweetness'},
    844: {'form': 'Gigantamax Sandaconda', 'move': 'G-Max Sandblast'},
    849: {'form': 'Gigantamax Toxtricity', 'move': 'G-Max Stun Shock'},  # Low Key and Amped forms
    851: {'form': 'Gigantamax Centiskorch', 'move': 'G-Max Centiferno'},
    858: {'form': 'Gigantamax Hatterene', 'move': 'G-Max Smite'},
    861: {'form': 'Gigantamax Grimmsnarl', 'move': 'G-Max Snooze'},
    869: {'form': 'Gigantamax Alcremie', 'move': 'G-Max Finale'},
    879: {'form': 'Gigantamax Copperajah', 'move': 'G-Max Steelsurge'},
    884: {'form': 'Gigantamax Duraludon', 'move': 'G-Max Depletion'},
    892: {'form': 'Gigantamax Urshifu', 'move': 'G-Max One Blow / G-Max Rapid Flow'},
}

# ==================== DATA GENERATION FUNCTIONS ====================

def create_variant_entry(base_row, variant_data, variant_type):
    """Create a new row for a Pokemon variant"""
    new_row = base_row.copy()
    
    # Update core fields
    new_row['name'] = variant_data['form']
    new_row['variant_type'] = variant_type
    new_row['base_pokemon_id'] = base_row['pokedex_number']
    new_row['form_name'] = variant_data['form']
    
    # Update stats if provided
    if 'stats' in variant_data:
        for stat, value in variant_data['stats'].items():
            new_row[stat] = value
        new_row['total_points'] = sum(variant_data['stats'].values())
    
    # Update types if provided
    if 'types' in variant_data:
        new_row['type_1'] = variant_data['types'][0]
        new_row['type_2'] = variant_data['types'][1] if variant_data['types'][1] else None
    
    # Update ability
    if 'ability' in variant_data:
        new_row['ability_1'] = variant_data['ability']
    
    # Add variant-specific fields
    if variant_type == 'mega' or variant_type == 'mega-x' or variant_type == 'mega-y':
        new_row['mega_stone'] = variant_data.get('stone', '')
    elif variant_type == 'gigantamax':
        new_row['gmax_move'] = variant_data.get('move', '')
    
    # Sprite paths (will be updated after download)
    dex_num = str(base_row['pokedex_number']).zfill(3)
    variant_suffix = variant_type.replace('-', '_')
    new_row['sprite_path_static'] = f"assets/sprites/{dex_num}_{variant_suffix}.png"
    new_row['sprite_path_animated'] = f"assets/animated/{dex_num}_{variant_suffix}.gif"
    new_row['sprite_path_shiny'] = f"assets/sprites/{dex_num}_{variant_suffix}_shiny.png"
    
    # Description
    if 'description' in variant_data:
        new_row['form_description'] = variant_data['description']
    
    return new_row


def generate_variant_csv():
    """Generate enhanced CSV with all variants"""
    print("🔄 Loading existing national_dex.csv...")
    df = pd.read_csv('data/national_dex.csv')
    
    print(f"✅ Loaded {len(df)} existing Pokemon entries")
    
    # Add new columns if they don't exist
    new_columns = [
        'variant_type', 'base_pokemon_id', 'sprite_path_static',
        'sprite_path_animated', 'sprite_path_shiny', 'form_name',
        'mega_stone', 'gmax_move', 'form_description'
    ]
    
    for col in new_columns:
        if col not in df.columns:
            df[col] = None
    
    # Set default values for existing entries
    df['variant_type'] = df['variant_type'].fillna('base')
    df['base_pokemon_id'] = df.apply(
        lambda row: row['pokedex_number'] if row['variant_type'] == 'base' else row['base_pokemon_id'],
        axis=1
    )
    df['form_name'] = df.apply(
        lambda row: row['name'] if pd.isna(row['form_name']) else row['form_name'],
        axis=1
    )
    
    # Generate sprite paths for base forms
    df['sprite_path_static'] = df.apply(
        lambda row: f"assets/sprites/{str(row['pokedex_number']).zfill(3)}.png"
        if pd.isna(row['sprite_path_static']) else row['sprite_path_static'],
        axis=1
    )
    
    variant_rows = []
    
    # Generate Mega Evolutions
    print("\n🔥 Generating Mega Evolution variants...")
    for base_id, mega_data in MEGA_EVOLUTIONS.items():
        base_row = df[df['pokedex_number'] == base_id]
        if base_row.empty:
            print(f"⚠️  Warning: Base Pokemon #{base_id} not found")
            continue
        
        base_row = base_row.iloc[0]
        
        # Handle Pokemon with multiple Mega forms (Charizard, Mewtwo)
        if 'X' in mega_data or 'Y' in mega_data:
            if 'X' in mega_data:
                variant_row = create_variant_entry(base_row, mega_data['X'], 'mega-x')
                variant_rows.append(variant_row)
                print(f"  ✓ {mega_data['X']['form']}")
            if 'Y' in mega_data:
                variant_row = create_variant_entry(base_row, mega_data['Y'], 'mega-y')
                variant_rows.append(variant_row)
                print(f"  ✓ {mega_data['Y']['form']}")
        else:
            variant_row = create_variant_entry(base_row, mega_data, 'mega')
            variant_rows.append(variant_row)
            print(f"  ✓ {mega_data['form']}")
    
    # Generate Regional Forms
    print("\n🌍 Generating Regional Form variants...")
    for base_id, regional_data in REGIONAL_FORMS.items():
        base_row = df[df['pokedex_number'] == base_id]
        if base_row.empty:
            continue
        
        base_row = base_row.iloc[0]
        form_name = regional_data['form']
        
        if 'Alolan' in form_name:
            variant_type = 'alolan'
        elif 'Galarian' in form_name:
            variant_type = 'galarian'
        elif 'Hisuian' in form_name:
            variant_type = 'hisuian'
        elif 'Paldean' in form_name:
            variant_type = 'paldean'
        else:
            variant_type = 'regional'
        
        variant_row = create_variant_entry(base_row, regional_data, variant_type)
        variant_rows.append(variant_row)
        print(f"  ✓ {form_name}")
    
    # Generate Gigantamax Forms
    print("\n⚡ Generating Gigantamax variants...")
    for base_id, gmax_data in GIGANTAMAX_FORMS.items():
        base_row = df[df['pokedex_number'] == base_id]
        if base_row.empty:
            continue
        
        base_row = base_row.iloc[0]
        variant_row = create_variant_entry(base_row, gmax_data, 'gigantamax')
        variant_rows.append(variant_row)
        print(f"  ✓ {gmax_data['form']}")
    
    # Combine all data
    print(f"\n📊 Generated {len(variant_rows)} variant entries")
    variant_df = pd.DataFrame(variant_rows)
    enhanced_df = pd.concat([df, variant_df], ignore_index=True)
    
    # Sort by pokedex_number, then by variant_type
    variant_order = ['base', 'mega', 'mega-x', 'mega-y', 'alolan', 'galarian', 
                     'hisuian', 'paldean', 'gigantamax', 'shiny']
    enhanced_df['variant_sort'] = enhanced_df['variant_type'].apply(
        lambda x: variant_order.index(x) if x in variant_order else 99
    )
    enhanced_df = enhanced_df.sort_values(['pokedex_number', 'variant_sort']).drop('variant_sort', axis=1)
    
    # Save to new file
    output_path = 'data/national_dex_with_variants.csv'
    enhanced_df.to_csv(output_path, index=False)
    print(f"\n✅ Saved enhanced data to: {output_path}")
    print(f"📈 Total entries: {len(enhanced_df)} ({len(df)} base + {len(variant_rows)} variants)")
    
    # Generate summary stats
    print("\n📊 Variant Summary:")
    print(enhanced_df['variant_type'].value_counts())
    
    return enhanced_df


def generate_variant_summary():
    """Generate JSON summary of all variants for reference"""
    summary = {
        'total_base_pokemon': 1025,
        'variant_counts': {
            'mega_evolutions': len(MEGA_EVOLUTIONS),
            'regional_forms': len(REGIONAL_FORMS),
            'gigantamax_forms': len(GIGANTAMAX_FORMS),
        },
        'mega_evolutions': {k: v.get('form', v.get('X', {}).get('form')) for k, v in MEGA_EVOLUTIONS.items()},
        'gigantamax': {k: v['form'] for k, v in GIGANTAMAX_FORMS.items()},
        'data_generated': pd.Timestamp.now().isoformat()
    }
    
    with open('data/variant_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("✅ Generated variant_summary.json")


if __name__ == '__main__':
    print("=" * 60)
    print("   POKEMON VARIANT DATA BUILDER")
    print("=" * 60)
    print()
    
    try:
        # Generate the enhanced CSV
        enhanced_df = generate_variant_csv()
        
        # Generate summary
        generate_variant_summary()
        
        print("\n" + "=" * 60)
        print("   ✅ VARIANT DATA GENERATION COMPLETE!")
        print("=" * 60)
        print(f"\n📁 Output files:")
        print(f"   • data/national_dex_with_variants.csv")
        print(f"   • data/variant_summary.json")
        print(f"\n🎯 Next steps:")
        print(f"   1. Review the generated CSV")
        print(f"   2. Run sprite download script")
        print(f"   3. Update app.py to use new data structure")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
