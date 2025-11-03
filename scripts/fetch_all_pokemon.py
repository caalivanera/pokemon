"""
Comprehensive Pokemon Data Fetcher
Fetches complete data for all 1025 Pokemon from PokeAPI
"""

import requests
import json
import time
import csv
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Configuration
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
TOTAL_POKEMON = 1025
START_ID = 707  # Start from first missing Pokemon
RATE_LIMIT_DELAY = 0.1  # Delay between API calls to be respectful
OUTPUT_DIR = Path("data")
SPRITES_DIR = Path("assets/sprites")

class PokemonDataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pokemon-Dashboard-Data-Fetcher/1.0'
        })
        
    def fetch_pokemon_data(self, pokemon_id: int) -> Optional[Dict]:
        """Fetch comprehensive data for a single Pokemon"""
        try:
            print(f"Fetching data for Pokemon #{pokemon_id}...")
            
            # Fetch main Pokemon data
            response = self.session.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_id}")
            response.raise_for_status()
            pokemon_data = response.json()
            
            time.sleep(RATE_LIMIT_DELAY)
            
            # Fetch species data for additional info
            species_response = self.session.get(pokemon_data['species']['url'])
            species_response.raise_for_status()
            species_data = species_response.json()
            
            time.sleep(RATE_LIMIT_DELAY)
            
            return {
                'pokemon': pokemon_data,
                'species': species_data
            }
            
        except Exception as e:
            print(f"Error fetching Pokemon #{pokemon_id}: {e}")
            return None
    
    def extract_pokemon_info(self, data: Dict) -> Dict:
        """Extract and format Pokemon information"""
        pokemon = data['pokemon']
        species = data['species']
        
        # Get English name
        name = pokemon['name'].replace('-', ' ').title()
        for name_entry in species['names']:
            if name_entry['language']['name'] == 'en':
                name = name_entry['name']
                break
        
        # Get Japanese name
        japanese_name = ""
        for name_entry in species['names']:
            if name_entry['language']['name'] == 'ja':
                japanese_name = name_entry['name']
                break
        
        # Get generation
        generation = int(species['generation']['url'].split('/')[-2])
        
        # Get types
        types = sorted(pokemon['types'], key=lambda x: x['slot'])
        type_1 = types[0]['type']['name'].capitalize()
        type_2 = types[1]['type']['name'].capitalize() if len(types) > 1 else ""
        
        # Get abilities
        abilities = [a for a in pokemon['abilities'] if not a['is_hidden']]
        ability_1 = abilities[0]['ability']['name'].replace('-', ' ').title() if len(abilities) > 0 else ""
        ability_2 = abilities[1]['ability']['name'].replace('-', ' ').title() if len(abilities) > 1 else ""
        
        hidden_abilities = [a for a in pokemon['abilities'] if a['is_hidden']]
        ability_hidden = hidden_abilities[0]['ability']['name'].replace('-', ' ').title() if hidden_abilities else ""
        
        # Get stats
        stats_dict = {stat['stat']['name']: stat['base_stat'] for stat in pokemon['stats']}
        hp = stats_dict.get('hp', 0)
        attack = stats_dict.get('attack', 0)
        defense = stats_dict.get('defense', 0)
        sp_attack = stats_dict.get('special-attack', 0)
        sp_defense = stats_dict.get('special-defense', 0)
        speed = stats_dict.get('speed', 0)
        total_points = sum([hp, attack, defense, sp_attack, sp_defense, speed])
        
        # Get physical attributes
        height_m = pokemon['height'] / 10  # Decimeters to meters
        weight_kg = pokemon['weight'] / 10  # Hectograms to kilograms
        
        # Get species info
        species_name = ""
        for genus in species['genera']:
            if genus['language']['name'] == 'en':
                species_name = genus['genus']
                break
        
        # Get description (Bulbapedia format)
        description = ""
        for entry in species['flavor_text_entries']:
            if entry['language']['name'] == 'en':
                description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                break
        
        # Get egg groups
        egg_groups = [eg['name'].capitalize() for eg in species['egg_groups']]
        egg_type_1 = egg_groups[0] if len(egg_groups) > 0 else ""
        egg_type_2 = egg_groups[1] if len(egg_groups) > 1 else ""
        
        # Get other breeding info
        percentage_male = species['gender_rate']
        if percentage_male >= 0:
            percentage_male = 100 - (percentage_male * 12.5)
        else:
            percentage_male = -1  # Genderless
        
        egg_cycles = species['hatch_counter']
        
        # Get catch rate
        catch_rate = species['capture_rate']
        
        # Get base friendship
        base_friendship = species['base_happiness']
        
        # Get base experience
        base_experience = pokemon['base_experience'] or 0
        
        # Get growth rate
        growth_rate = species['growth_rate']['name'].replace('-', ' ').title()
        
        # Determine legendary/mythical status
        is_legendary = species['is_legendary']
        is_mythical = species['is_mythical']
        status = "Legendary" if is_legendary else ("Mythical" if is_mythical else "Normal")
        
        # Get sprites
        sprites = {
            'front_default': pokemon['sprites']['front_default'],
            'front_shiny': pokemon['sprites']['front_shiny'],
            'official_artwork': pokemon['sprites']['other']['official-artwork']['front_default'],
            'home': pokemon['sprites']['other']['home']['front_default'] if pokemon['sprites']['other'].get('home') else None,
        }
        
        return {
            'pokedex_number': pokemon['id'],
            'name': name,
            'japanese_name': japanese_name,
            'generation': generation,
            'status': status,
            'species': species_name,
            'type_1': type_1,
            'type_2': type_2,
            'height_m': height_m,
            'weight_kg': weight_kg,
            'ability_1': ability_1,
            'ability_2': ability_2,
            'ability_hidden': ability_hidden,
            'total_points': total_points,
            'hp': hp,
            'attack': attack,
            'defense': defense,
            'sp_attack': sp_attack,
            'sp_defense': sp_defense,
            'speed': speed,
            'catch_rate': catch_rate,
            'base_friendship': base_friendship,
            'base_experience': base_experience,
            'growth_rate': growth_rate,
            'egg_type_1': egg_type_1,
            'egg_type_2': egg_type_2,
            'percentage_male': percentage_male,
            'egg_cycles': egg_cycles,
            'description': description,
            'sprites': sprites,
        }
    
    def fetch_all_pokemon(self, start_id: int = START_ID, end_id: int = TOTAL_POKEMON) -> List[Dict]:
        """Fetch all Pokemon data from start_id to end_id"""
        all_pokemon = []
        
        for pokemon_id in range(start_id, end_id + 1):
            data = self.fetch_pokemon_data(pokemon_id)
            if data:
                pokemon_info = self.extract_pokemon_info(data)
                all_pokemon.append(pokemon_info)
                print(f"✓ Successfully processed #{pokemon_id} - {pokemon_info['name']}")
            else:
                print(f"✗ Failed to process #{pokemon_id}")
            
            # Progress indicator
            if pokemon_id % 50 == 0:
                print(f"\n=== Progress: {pokemon_id - start_id + 1}/{end_id - start_id + 1} Pokemon processed ===\n")
        
        return all_pokemon
    
    def save_to_json(self, pokemon_list: List[Dict], filename: str = "new_pokemon_data.json"):
        """Save Pokemon data to JSON file"""
        output_path = OUTPUT_DIR / filename
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(pokemon_list, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved data to {output_path}")
    
    def download_sprite(self, url: str, pokemon_id: int, sprite_type: str) -> bool:
        """Download a sprite image"""
        if not url:
            return False
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            sprite_dir = SPRITES_DIR / sprite_type
            sprite_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine file extension
            ext = '.png'
            if 'svg' in url.lower():
                ext = '.svg'
            elif 'gif' in url.lower():
                ext = '.gif'
            
            sprite_path = sprite_dir / f"{pokemon_id:04d}{ext}"
            
            with open(sprite_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"Error downloading sprite: {e}")
            return False

def main():
    """Main execution function"""
    print("=" * 60)
    print("Pokemon Data Fetcher - Comprehensive Update")
    print("=" * 60)
    print(f"\nFetching Pokemon #{START_ID} to #{TOTAL_POKEMON}")
    print(f"Total Pokemon to fetch: {TOTAL_POKEMON - START_ID + 1}")
    print("\nThis may take a while due to API rate limiting...")
    print("=" * 60 + "\n")
    
    fetcher = PokemonDataFetcher()
    
    # Fetch all Pokemon data
    pokemon_list = fetcher.fetch_all_pokemon()
    
    # Save to JSON
    if pokemon_list:
        fetcher.save_to_json(pokemon_list)
        print(f"\n✓ Successfully fetched data for {len(pokemon_list)} Pokemon!")
    else:
        print("\n✗ No Pokemon data was fetched.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Data fetching complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
