"""
Fetch comprehensive Pokemon game data from multiple web sources
Includes: moves, evolution chains, locations, game appearances, forms, abilities details
"""

import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
POKEAPI_BASE = "https://pokeapi.co/api/v2"
OUTPUT_DIR = Path("data/enhanced")
RATE_LIMIT = 0.15

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ComprehensiveGameDataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pokemon-Dashboard-Comprehensive-Data/1.0'
        })
        self.cache = {}
    
    def fetch_pokemon_moves(self, pokemon_id: int) -> Dict:
        """Fetch all moves a Pokemon can learn"""
        try:
            url = f"{POKEAPI_BASE}/pokemon/{pokemon_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            moves_data = {
                'level_up': [],
                'tm_hm': [],
                'egg': [],
                'tutor': []
            }
            
            for move_entry in data['moves']:
                move_name = move_entry['move']['name']
                
                for version_detail in move_entry['version_group_details']:
                    method = version_detail['move_learn_method']['name']
                    level = version_detail['level_learned_at']
                    version = version_detail['version_group']['name']
                    
                    move_info = {
                        'name': move_name,
                        'level': level,
                        'version': version
                    }
                    
                    if method == 'level-up':
                        moves_data['level_up'].append(move_info)
                    elif method in ['machine', 'tm', 'hm']:
                        moves_data['tm_hm'].append(move_info)
                    elif method == 'egg':
                        moves_data['egg'].append(move_info)
                    elif method == 'tutor':
                        moves_data['tutor'].append(move_info)
            
            return moves_data
            
        except Exception as e:
            print(f"Error fetching moves for #{pokemon_id}: {e}")
            return {}
    
    def fetch_evolution_chain(self, pokemon_id: int) -> Dict:
        """Fetch complete evolution chain"""
        try:
            # Get species data first
            species_url = f"{POKEAPI_BASE}/pokemon-species/{pokemon_id}"
            species_response = self.session.get(species_url, timeout=10)
            species_response.raise_for_status()
            species_data = species_response.json()
            
            # Get evolution chain
            chain_url = species_data['evolution_chain']['url']
            chain_response = self.session.get(chain_url, timeout=10)
            chain_response.raise_for_status()
            chain_data = chain_response.json()
            
            def parse_chain(chain):
                """Recursively parse evolution chain"""
                pokemon_name = chain['species']['name']
                pokemon_id = int(chain['species']['url'].split('/')[-2])
                
                evolution_details = []
                for detail in chain.get('evolution_details', []):
                    evolution_details.append({
                        'trigger': detail.get('trigger', {}).get('name'),
                        'min_level': detail.get('min_level'),
                        'item': detail.get('item', {}).get('name') if detail.get('item') else None,
                        'held_item': detail.get('held_item', {}).get('name') if detail.get('held_item') else None,
                        'time_of_day': detail.get('time_of_day'),
                        'known_move': detail.get('known_move', {}).get('name') if detail.get('known_move') else None,
                        'min_happiness': detail.get('min_happiness'),
                        'min_beauty': detail.get('min_beauty'),
                        'location': detail.get('location', {}).get('name') if detail.get('location') else None,
                    })
                
                result = {
                    'pokemon': pokemon_name,
                    'pokemon_id': pokemon_id,
                    'evolution_details': evolution_details,
                    'evolves_to': []
                }
                
                for evolution in chain.get('evolves_to', []):
                    result['evolves_to'].append(parse_chain(evolution))
                
                return result
            
            return parse_chain(chain_data['chain'])
            
        except Exception as e:
            print(f"Error fetching evolution chain for #{pokemon_id}: {e}")
            return {}
    
    def fetch_pokemon_forms(self, pokemon_id: int) -> List[Dict]:
        """Fetch all forms/variants of a Pokemon"""
        try:
            url = f"{POKEAPI_BASE}/pokemon-species/{pokemon_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forms = []
            for variety in data.get('varieties', []):
                form_name = variety['pokemon']['name']
                is_default = variety['is_default']
                
                forms.append({
                    'name': form_name,
                    'is_default': is_default
                })
            
            return forms
            
        except Exception as e:
            print(f"Error fetching forms for #{pokemon_id}: {e}")
            return []
    
    def fetch_pokemon_encounters(self, pokemon_id: int) -> List[Dict]:
        """Fetch location data for Pokemon"""
        try:
            url = f"{POKEAPI_BASE}/pokemon/{pokemon_id}/encounters"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            encounters = response.json()
            
            locations = []
            for encounter in encounters:
                location_name = encounter['location_area']['name']
                
                for version_detail in encounter['version_details']:
                    version = version_detail['version']['name']
                    max_chance = version_detail.get('max_chance', 0)
                    
                    locations.append({
                        'location': location_name,
                        'version': version,
                        'chance': max_chance
                    })
            
            return locations
            
        except Exception as e:
            print(f"Error fetching encounters for #{pokemon_id}: {e}")
            return []
    
    def fetch_ability_details(self, ability_name: str) -> Dict:
        """Fetch detailed ability information"""
        if ability_name in self.cache:
            return self.cache[ability_name]
        
        try:
            url = f"{POKEAPI_BASE}/ability/{ability_name.lower().replace(' ', '-')}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Get English description
            effect = ""
            short_effect = ""
            for entry in data.get('effect_entries', []):
                if entry['language']['name'] == 'en':
                    effect = entry['effect']
                    short_effect = entry['short_effect']
                    break
            
            ability_info = {
                'name': data['name'],
                'effect': effect,
                'short_effect': short_effect,
                'generation': data['generation']['name']
            }
            
            self.cache[ability_name] = ability_info
            return ability_info
            
        except Exception as e:
            print(f"Error fetching ability {ability_name}: {e}")
            return {}
    
    def fetch_game_indices(self, pokemon_id: int) -> List[Dict]:
        """Fetch Pokemon's index numbers across different games"""
        try:
            url = f"{POKEAPI_BASE}/pokemon/{pokemon_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            indices = []
            for game_index in data.get('game_indices', []):
                indices.append({
                    'game': game_index['version']['name'],
                    'index': game_index['game_index']
                })
            
            return indices
            
        except Exception as e:
            print(f"Error fetching game indices for #{pokemon_id}: {e}")
            return []
    
    def fetch_comprehensive_data(self, pokemon_id: int, pokemon_name: str) -> Dict:
        """Fetch all comprehensive game data for a Pokemon"""
        print(f"Fetching comprehensive data for #{pokemon_id} {pokemon_name}...")
        
        data = {
            'pokedex_number': pokemon_id,
            'name': pokemon_name,
            'moves': self.fetch_pokemon_moves(pokemon_id),
            'evolution_chain': self.fetch_evolution_chain(pokemon_id),
            'forms': self.fetch_pokemon_forms(pokemon_id),
            'encounters': self.fetch_pokemon_encounters(pokemon_id),
            'game_indices': self.fetch_game_indices(pokemon_id)
        }
        
        time.sleep(RATE_LIMIT)
        return data
    
    def fetch_all_pokemon(self, start_id: int = 1, end_id: int = 1025):
        """Fetch comprehensive data for all Pokemon"""
        print("=" * 80)
        print("FETCHING COMPREHENSIVE POKEMON GAME DATA")
        print("=" * 80 + "\n")
        
        all_data = []
        
        for pokemon_id in range(start_id, end_id + 1):
            try:
                data = self.fetch_comprehensive_data(pokemon_id, f"Pokemon_{pokemon_id}")
                all_data.append(data)
                
                # Progress every 50
                if pokemon_id % 50 == 0:
                    print(f"\n--- Progress: {pokemon_id}/{end_id} ---\n")
                    
            except Exception as e:
                print(f"✗ Error with #{pokemon_id}: {e}")
        
        # Save to JSON
        output_file = OUTPUT_DIR / "comprehensive_game_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved comprehensive data to {output_file}")
        print(f"✓ Total Pokemon processed: {len(all_data)}")


def main():
    fetcher = ComprehensiveGameDataFetcher()
    fetcher.fetch_all_pokemon(1, 1025)


if __name__ == "__main__":
    main()
