"""
Fetch competitive Pokemon data including IVs, EVs, Natures, and competitive stats
Sources: PokeAPI, Smogon data structures, competitive analysis
"""

import requests
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List

# Configuration
POKEAPI_BASE = "https://pokeapi.co/api/v2"
OUTPUT_DIR = Path("data/competitive")
CSV_PATH = Path("data/national_dex.csv")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class CompetitiveDataEnhancer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pokemon-Dashboard-Competitive-Data/1.0'
        })
        
        # IV/EV ranges (standard Pokemon mechanics)
        self.iv_range = (0, 31)  # Individual Values
        self.ev_range = (0, 252)  # Effort Values per stat
        self.ev_total_max = 510  # Max total EVs
        
        # Nature data (affects stats)
        self.natures = {
            'Hardy': {'increases': None, 'decreases': None},
            'Lonely': {'increases': 'attack', 'decreases': 'defense'},
            'Brave': {'increases': 'attack', 'decreases': 'speed'},
            'Adamant': {'increases': 'attack', 'decreases': 'sp_attack'},
            'Naughty': {'increases': 'attack', 'decreases': 'sp_defense'},
            'Bold': {'increases': 'defense', 'decreases': 'attack'},
            'Docile': {'increases': None, 'decreases': None},
            'Relaxed': {'increases': 'defense', 'decreases': 'speed'},
            'Impish': {'increases': 'defense', 'decreases': 'sp_attack'},
            'Lax': {'increases': 'defense', 'decreases': 'sp_defense'},
            'Timid': {'increases': 'speed', 'decreases': 'attack'},
            'Hasty': {'increases': 'speed', 'decreases': 'defense'},
            'Serious': {'increases': None, 'decreases': None},
            'Jolly': {'increases': 'speed', 'decreases': 'sp_attack'},
            'Naive': {'increases': 'speed', 'decreases': 'sp_defense'},
            'Modest': {'increases': 'sp_attack', 'decreases': 'attack'},
            'Mild': {'increases': 'sp_attack', 'decreases': 'defense'},
            'Quiet': {'increases': 'sp_attack', 'decreases': 'speed'},
            'Bashful': {'increases': None, 'decreases': None},
            'Rash': {'increases': 'sp_attack', 'decreases': 'sp_defense'},
            'Calm': {'increases': 'sp_defense', 'decreases': 'attack'},
            'Gentle': {'increases': 'sp_defense', 'decreases': 'defense'},
            'Sassy': {'increases': 'sp_defense', 'decreases': 'speed'},
            'Careful': {'increases': 'sp_defense', 'decreases': 'sp_attack'},
            'Quirky': {'increases': None, 'decreases': None},
        }
    
    def calculate_stat_with_iv_ev(
        self, 
        base_stat: int, 
        iv: int, 
        ev: int, 
        level: int = 100,
        nature_modifier: float = 1.0,
        is_hp: bool = False
    ) -> int:
        """Calculate actual stat value with IV/EV"""
        if is_hp:
            # HP formula
            return int(((2 * base_stat + iv + (ev // 4)) * level // 100) + level + 10)
        else:
            # Other stats formula
            return int((((2 * base_stat + iv + (ev // 4)) * level // 100) + 5) * nature_modifier)
    
    def get_optimal_evs(self, pokemon_id: int, base_stats: Dict) -> Dict:
        """Suggest optimal EV spreads based on base stats"""
        # Physical Attacker spread
        physical_spread = {
            'hp': 0,
            'attack': 252,
            'defense': 0,
            'sp_attack': 0,
            'sp_defense': 4,
            'speed': 252
        }
        
        # Special Attacker spread
        special_spread = {
            'hp': 0,
            'attack': 0,
            'defense': 0,
            'sp_attack': 252,
            'sp_defense': 4,
            'speed': 252
        }
        
        # Tank/Wall spread
        tank_spread = {
            'hp': 252,
            'attack': 0,
            'defense': 252,
            'sp_attack': 0,
            'sp_defense': 4,
            'speed': 0
        }
        
        # Determine optimal based on stats
        if base_stats['attack'] > base_stats['sp_attack']:
            if base_stats['speed'] >= 80:
                return {'type': 'Physical Sweeper', 'spread': physical_spread}
            else:
                return {'type': 'Physical Tank', 'spread': tank_spread}
        else:
            if base_stats['speed'] >= 80:
                return {'type': 'Special Sweeper', 'spread': special_spread}
            else:
                return {'type': 'Special Tank', 'spread': tank_spread}
    
    def get_optimal_nature(self, pokemon_role: str) -> str:
        """Suggest optimal nature based on role"""
        nature_suggestions = {
            'Physical Sweeper': 'Jolly',  # +Speed, -Sp.Atk
            'Special Sweeper': 'Timid',   # +Speed, -Attack
            'Physical Tank': 'Impish',    # +Defense, -Sp.Atk
            'Special Tank': 'Calm',       # +Sp.Def, -Attack
            'Mixed Attacker': 'Hasty',    # +Speed, -Defense
        }
        return nature_suggestions.get(pokemon_role, 'Hardy')
    
    def calculate_stat_ranges(self, base_stat: int, is_hp: bool = False) -> Dict:
        """Calculate min/max stat ranges at level 100"""
        # Minimum: 0 IV, 0 EV, hindering nature
        min_stat = self.calculate_stat_with_iv_ev(
            base_stat, 0, 0, 100, 0.9 if not is_hp else 1.0, is_hp
        )
        
        # Maximum: 31 IV, 252 EV, beneficial nature
        max_stat = self.calculate_stat_with_iv_ev(
            base_stat, 31, 252, 100, 1.1 if not is_hp else 1.0, is_hp
        )
        
        return {'min': min_stat, 'max': max_stat}
    
    def fetch_ability_competitive_info(self, ability_name: str) -> Dict:
        """Fetch competitive viability of abilities"""
        try:
            url = f"{POKEAPI_BASE}/ability/{ability_name.lower().replace(' ', '-')}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Get effect
            effect = ""
            for entry in data.get('effect_entries', []):
                if entry['language']['name'] == 'en':
                    effect = entry['effect']
                    break
            
            # Count how many Pokemon have this ability
            pokemon_count = len(data.get('pokemon', []))
            
            return {
                'name': ability_name,
                'effect': effect,
                'pokemon_count': pokemon_count,
                'is_hidden': False  # Updated per Pokemon
            }
            
        except Exception as e:
            print(f"Error fetching ability {ability_name}: {e}")
            return {}
    
    def enhance_pokemon_competitive_data(self, pokemon_row: pd.Series) -> Dict:
        """Add comprehensive competitive data to a Pokemon"""
        pokemon_id = int(pokemon_row['pokedex_number'])
        name = pokemon_row['name']
        
        print(f"Enhancing #{pokemon_id} {name}...")
        
        # Base stats
        base_stats = {
            'hp': int(pokemon_row['hp']),
            'attack': int(pokemon_row['attack']),
            'defense': int(pokemon_row['defense']),
            'sp_attack': int(pokemon_row['sp_attack']),
            'sp_defense': int(pokemon_row['sp_defense']),
            'speed': int(pokemon_row['speed'])
        }
        
        # Calculate stat ranges
        stat_ranges = {}
        stat_ranges['hp'] = self.calculate_stat_ranges(base_stats['hp'], True)
        for stat in ['attack', 'defense', 'sp_attack', 'sp_defense', 'speed']:
            stat_ranges[stat] = self.calculate_stat_ranges(base_stats[stat], False)
        
        # Optimal EV spread
        optimal_ev = self.get_optimal_evs(pokemon_id, base_stats)
        optimal_nature = self.get_optimal_nature(optimal_ev['type'])
        
        # Calculate stats with optimal setup
        optimal_stats = {}
        for stat, base_val in base_stats.items():
            is_hp = (stat == 'hp')
            nature_mod = 1.0
            
            # Apply nature modifier
            if not is_hp:
                nature_info = self.natures[optimal_nature]
                if nature_info['increases'] == stat:
                    nature_mod = 1.1
                elif nature_info['decreases'] == stat:
                    nature_mod = 0.9
            
            optimal_stats[stat] = self.calculate_stat_with_iv_ev(
                base_val,
                31,  # Max IV
                optimal_ev['spread'][stat],
                100,
                nature_mod,
                is_hp
            )
        
        # Competitive tier estimation (simplified)
        bst = int(pokemon_row['total_points'])
        if bst >= 600:
            tier = 'Uber' if pokemon_row['status'] == 'Legendary' else 'OU'
        elif bst >= 500:
            tier = 'OU' if pokemon_row['status'] == 'Normal' else 'UU'
        elif bst >= 450:
            tier = 'UU'
        elif bst >= 400:
            tier = 'RU'
        else:
            tier = 'NU'
        
        return {
            'pokedex_number': pokemon_id,
            'name': name,
            'competitive_tier': tier,
            'optimal_role': optimal_ev['type'],
            'optimal_nature': optimal_nature,
            'optimal_ev_spread': optimal_ev['spread'],
            'stat_ranges': stat_ranges,
            'optimal_stats_lv100': optimal_stats,
            'iv_requirements': {
                'hp': '31 (max HP)',
                'attack': '31 or 0 (0 if special attacker to minimize confusion damage)',
                'defense': '31',
                'sp_attack': '31 or 0 (0 if physical attacker)',
                'sp_defense': '31',
                'speed': '31 or 0 (0 for Trick Room teams)'
            },
            'natures_list': list(self.natures.keys()),
            'nature_effects': self.natures
        }
    
    def enhance_all_pokemon(self):
        """Add competitive data to all Pokemon in CSV"""
        print("=" * 80)
        print("ENHANCING POKEMON WITH COMPETITIVE DATA")
        print("=" * 80 + "\n")
        
        # Load CSV
        df = pd.read_csv(CSV_PATH)
        print(f"Loaded {len(df)} Pokemon\n")
        
        competitive_data = []
        
        for idx, row in df.iterrows():
            try:
                comp_data = self.enhance_pokemon_competitive_data(row)
                competitive_data.append(comp_data)
                
                if (idx + 1) % 50 == 0:
                    print(f"\n--- Progress: {idx + 1}/{len(df)} ---\n")
                    
            except Exception as e:
                print(f"✗ Error with #{row['pokedex_number']}: {e}")
        
        # Save to JSON
        output_file = OUTPUT_DIR / "competitive_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(competitive_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved competitive data to {output_file}")
        print(f"✓ Total Pokemon processed: {len(competitive_data)}")
        
        # Also save natures reference
        natures_file = OUTPUT_DIR / "natures_reference.json"
        with open(natures_file, 'w', encoding='utf-8') as f:
            json.dump(self.natures, f, indent=2)
        
        print(f"✓ Saved natures reference to {natures_file}")


def main():
    enhancer = CompetitiveDataEnhancer()
    enhancer.enhance_all_pokemon()


if __name__ == "__main__":
    main()
