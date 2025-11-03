"""
Update Pokemon Legends: Z-A game availability data
Based on research: Released Oct 16, 2025, set in Kalos (Lumiose City)

Key findings from research:
- All Gen 6 (Kalos) Pokemon are in the game
- NO Gen 9 (Paldea) Pokemon are in the game  
- Many Pokemon from other generations are included
- Starters: Chikorita, Tepig, Totodile
- Features Eternal Flower Floette
- 26 new Mega Evolutions added
"""

import json
from pathlib import Path

# Load the comprehensive game data
data_path = Path("data/enhanced/comprehensive_game_data.json")
with open(data_path, 'r', encoding='utf-8') as f:
    game_data = json.load(f)

print(f"Total Pokemon in database: {len(game_data)}")

# Gen ranges
gen_ranges = {
    1: (1, 151),
    2: (152, 251),
    3: (252, 386),
    4: (387, 493),
    5: (494, 649),
    6: (650, 721),
    7: (722, 809),
    8: (810, 905),
    9: (906, 1025)
}

# According to research:
# - ALL Gen 6 Pokemon (650-721) are in the game
# - NO Gen 9 Pokemon (906-1025) are in the game
# - The game features many Pokemon from other gens including:
#   - Chikorita line (Gen 2: 152-154)
#   - Totodile line (Gen 2: 158-160)  
#   - Tepig line (Gen 5: 498-500)
#   - Patrat line (Gen 5: 504-505)
#   - Elemental monkeys (Gen 5: 511-518)
#   - Furfrou (Gen 6: 676)
#   - Eternal Flower Floette (Gen 6 special form)

# Count updates
updated_count = 0
gen6_count = 0
excluded_gen9_count = 0

for pokemon in game_data:
    dex_num = pokemon.get('pokedex_number', 0)
    games = pokemon.get('games', [])
    
    # All Gen 6 Pokemon (650-721) should have Legends: Z-A
    if 650 <= dex_num <= 721:
        if 'legends-z-a' not in games:
            games.append('legends-z-a')
            pokemon['games'] = games
            updated_count += 1
        gen6_count += 1
    
    # NO Gen 9 Pokemon (906-1025)
    elif 906 <= dex_num <= 1025:
        if 'legends-z-a' in games:
            games.remove('legends-z-a')
            pokemon['games'] = games
            updated_count += 1
        excluded_gen9_count += 1
    
    # Specific Pokemon mentioned in research that ARE in the game
    # Gen 2 starters
    elif dex_num in [152, 153, 154, 158, 159, 160]:  # Chikorita, Totodile lines
        if 'legends-z-a' not in games:
            games.append('legends-z-a')
            pokemon['games'] = games
            updated_count += 1
    
    # Gen 5 starter and specific Pokemon
    elif dex_num in [498, 499, 500,  # Tepig line
                     504, 505,  # Patrat line
                     511, 512, 513, 514, 515, 516, 517, 518]:  # Elemental monkeys
        if 'legends-z-a' not in games:
            games.append('legends-z-a')
            pokemon['games'] = games
            updated_count += 1

print(f"\nUpdate Summary:")
print(f"✅ Gen 6 (Kalos) Pokemon: {gen6_count} (ALL included in Legends: Z-A)")
print(f"❌ Gen 9 (Paldea) Pokemon: {excluded_gen9_count} (NONE included)")
print(f"🔄 Total updates made: {updated_count}")

# Save the updated data
with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(game_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Updated {data_path}")
print(f"📊 Total Pokemon in database: {len(game_data)}")
