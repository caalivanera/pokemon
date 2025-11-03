# Pokemon Moveset Database Structure

## Overview

Comprehensive moveset database for all 1,194 Pokemon forms covering all generations.

## Data Structure

### moves_database.json Format

```json
{
  "pokemon_id": {
    "name": "Pikachu",
    "level_up_moves": [
      {
        "level": 1,
        "move": "Thunder Shock",
        "type": "Electric",
        "category": "Special",
        "power": 40,
        "accuracy": 100,
        "pp": 30,
        "generation": 1
      }
    ],
    "tm_hm_moves": [
      {
        "move": "Thunderbolt",
        "tm_number": "TM24",
        "type": "Electric",
        "category": "Special",
        "power": 90,
        "accuracy": 100
      }
    ],
    "egg_moves": [
      {
        "move": "Volt Tackle",
        "type": "Electric",
        "category": "Physical",
        "power": 120,
        "accuracy": 100
      }
    ],
    "tutor_moves": [
      {
        "move": "Iron Tail",
        "type": "Steel",
        "category": "Physical",
        "power": 100,
        "accuracy": 75
      }
    ]
  }
}
```

### move_details.csv Format

| Column | Type | Description |
|--------|------|-------------|
| move_id | int | Unique move identifier |
| move_name | str | Name of the move |
| type | str | Move type (Fire, Water, etc.) |
| category | str | Physical, Special, or Status |
| power | int | Base power (null for status moves) |
| accuracy | int | Accuracy percentage |
| pp | int | Power Points |
| priority | int | Priority level (-6 to +5) |
| effect | str | Move effect description |
| effect_chance | int | Chance of secondary effect |
| generation | int | Generation introduced |

## Data Sources

1. **PokeAPI** (https://pokeapi.co/)
   - Complete moveset data via API
   - Rate limited: 100 requests/minute
   
2. **Bulbapedia**
   - Comprehensive move tables
   - Requires web scraping
   
3. **Serebii.net**
   - Moveset databases per generation
   - Alternative source

4. **Veekun Database**
   - Open source Pokemon data
   - SQLite database format

## Implementation Strategy

### Phase 1: Data Collection
```python
import requests
import time

def fetch_pokemon_moves(pokemon_id):
    """Fetch moves for a Pokemon from PokeAPI"""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return parse_moves(data['moves'])
    return None

def parse_moves(moves_data):
    """Parse move data into structured format"""
    level_up = []
    tm_hm = []
    egg = []
    tutor = []
    
    for move in moves_data:
        move_name = move['move']['name']
        for version_detail in move['version_group_details']:
            method = version_detail['move_learn_method']['name']
            if method == 'level-up':
                level = version_detail['level_learned_at']
                level_up.append({'move': move_name, 'level': level})
            elif method == 'machine':
                tm_hm.append({'move': move_name})
            elif method == 'egg':
                egg.append({'move': move_name})
            elif method == 'tutor':
                tutor.append({'move': move_name})
    
    return {
        'level_up': level_up,
        'tm_hm': tm_hm,
        'egg': egg,
        'tutor': tutor
    }
```

### Phase 2: Data Processing
```python
def collect_all_movesets():
    """Collect movesets for all Pokemon"""
    movesets = {}
    
    for pokemon_id in range(1, 1195):  # All 1,194 forms
        print(f"Fetching moves for Pokemon {pokemon_id}...")
        moves = fetch_pokemon_moves(pokemon_id)
        if moves:
            movesets[pokemon_id] = moves
        time.sleep(0.6)  # Rate limiting
    
    return movesets
```

### Phase 3: Storage
```python
import json

def save_movesets(movesets, filename='data/moves/movesets_database.json'):
    """Save moveset database to JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(movesets, f, indent=2, ensure_ascii=False)
```

## Estimated Metrics

- **Total Moves:** ~900 unique moves across all generations
- **Database Size:** 5-10 MB (JSON format)
- **Collection Time:** ~2 hours (with API rate limiting)
- **Pokemon Covered:** 1,194 forms

## Dashboard Integration

### Moveset Viewer Tab

```python
def display_moveset_viewer(df):
    """Display Pokemon moveset viewer"""
    st.header("📚 Pokemon Moveset Database")
    
    # Pokemon selector
    selected_pokemon = st.selectbox(
        "Select Pokemon",
        options=df['name'].tolist()
    )
    
    # Load moveset data
    movesets = load_movesets()
    pokemon_id = df[df['name'] == selected_pokemon]['pokedex_number'].iloc[0]
    
    if str(pokemon_id) in movesets:
        moveset = movesets[str(pokemon_id)]
        
        # Display moves by category
        tab1, tab2, tab3, tab4 = st.tabs([
            "Level-Up Moves", "TM/HM Moves", "Egg Moves", "Tutor Moves"
        ])
        
        with tab1:
            display_level_up_moves(moveset['level_up'])
        
        with tab2:
            display_tm_moves(moveset['tm_hm'])
        
        with tab3:
            display_egg_moves(moveset['egg'])
        
        with tab4:
            display_tutor_moves(moveset['tutor'])
```

## Status

**Current Status:** ⏳ Structure Defined, Data Collection Pending

**To Complete:**
1. Run PokeAPI data collection script (~2 hours)
2. Process and validate data
3. Store in JSON format
4. Integrate into dashboard
5. Add move details CSV

**Alternative:** Use existing Veekun database or PokeAPI directly in app (slower but no storage needed)

## Quick Start (When Ready)

```bash
# Install dependencies
pip install requests

# Run collection script
python scripts/collect_movesets.py

# This will create:
# - data/moves/movesets_database.json (~5-10MB)
# - data/moves/move_details.csv (~200KB)
```

## Notes

- Move data varies by game/generation
- Some forms have unique movesets (regional variants, mega evolutions)
- TM numbers changed between generations
- Egg moves depend on parent Pokemon
- Tutor moves vary by game

**Recommendation:** Start with PokeAPI for consistency, supplement with manual data for missing entries.
