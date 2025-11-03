"""
Enhanced Pokemon Data Updater
Updates national_dex.csv with all 1025 Pokemon including enhanced data from PokeAPI
"""

import requests
import pandas as pd
import time
from pathlib import Path
from typing import Dict, Optional
import numpy as np

# Configuration
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
RATE_LIMIT_DELAY = 0.15
CSV_PATH = Path("data/national_dex.csv")
BACKUP_PATH = Path("data/national_dex_backup.csv")

# Type effectiveness chart
TYPE_CHART = {
    'Normal': {'Rock': 0.5, 'Ghost': 0, 'Steel': 0.5},
    'Fire': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 2, 'Bug': 2, 'Rock': 0.5, 'Dragon': 0.5, 'Steel': 2},
    'Water': {'Fire': 2, 'Water': 0.5, 'Grass': 0.5, 'Ground': 2, 'Rock': 2, 'Dragon': 0.5},
    'Electric': {'Water': 2, 'Electric': 0.5, 'Grass': 0.5, 'Ground': 0, 'Flying': 2, 'Dragon': 0.5},
    'Grass': {'Fire': 0.5, 'Water': 2, 'Grass': 0.5, 'Poison': 0.5, 'Ground': 2, 'Flying': 0.5, 'Bug': 0.5, 'Rock': 2, 'Dragon': 0.5, 'Steel': 0.5},
    'Ice': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 0.5, 'Ground': 2, 'Flying': 2, 'Dragon': 2, 'Steel': 0.5},
    'Fighting': {'Normal': 2, 'Ice': 2, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2, 'Ghost': 0, 'Dark': 2, 'Steel': 2, 'Fairy': 0.5},
    'Poison': {'Grass': 2, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0, 'Fairy': 2},
    'Ground': {'Fire': 2, 'Electric': 2, 'Grass': 0.5, 'Poison': 2, 'Flying': 0, 'Bug': 0.5, 'Rock': 2, 'Steel': 2},
    'Flying': {'Electric': 0.5, 'Grass': 2, 'Fighting': 2, 'Bug': 2, 'Rock': 0.5, 'Steel': 0.5},
    'Psychic': {'Fighting': 2, 'Poison': 2, 'Psychic': 0.5, 'Dark': 0, 'Steel': 0.5},
    'Bug': {'Fire': 0.5, 'Grass': 2, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 2, 'Ghost': 0.5, 'Dark': 2, 'Steel': 0.5, 'Fairy': 0.5},
    'Rock': {'Fire': 2, 'Ice': 2, 'Fighting': 0.5, 'Ground': 0.5, 'Flying': 2, 'Bug': 2, 'Steel': 0.5},
    'Ghost': {'Normal': 0, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5},
    'Dragon': {'Dragon': 2, 'Steel': 0.5, 'Fairy': 0},
    'Dark': {'Fighting': 0.5, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5, 'Fairy': 0.5},
    'Steel': {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Ice': 2, 'Rock': 2, 'Steel': 0.5, 'Fairy': 2},
    'Fairy': {'Fire': 0.5, 'Fighting': 2, 'Poison': 0.5, 'Dragon': 2, 'Dark': 2, 'Steel': 0.5}
}

class EnhancedPokemonUpdater:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pokemon-Dashboard-Enhanced-Updater/2.0'
        })
        self.cache = {}
    
    def fetch_pokemon_complete(self, pokemon_id: int) -> Optional[Dict]:
        """Fetch complete Pokemon data with caching"""
        if pokemon_id in self.cache:
            return self.cache[pokemon_id]
        
        try:
            print(f"Fetching #{pokemon_id}...", end=' ')
            
            # Fetch main data
            response = self.session.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_id}", timeout=10)
            response.raise_for_status()
            pokemon_data = response.json()
            time.sleep(RATE_LIMIT_DELAY)
            
            # Fetch species data
            species_response = self.session.get(pokemon_data['species']['url'], timeout=10)
            species_response.raise_for_status()
            species_data = species_response.json()
            time.sleep(RATE_LIMIT_DELAY)
            
            result = {'pokemon': pokemon_data, 'species': species_data}
            self.cache[pokemon_id] = result
            
            print(f"✓ {pokemon_data['name']}")
            return result
            
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def calculate_type_effectiveness(self, type_1: str, type_2: Optional[str] = None) -> Dict:
        """Calculate defensive type effectiveness"""
        effectiveness = {t: 1.0 for t in TYPE_CHART.keys()}
        
        # Apply type 1
        for attack_type, matchups in TYPE_CHART.items():
            if type_1 in matchups:
                effectiveness[attack_type] *= matchups[type_1]
        
        # Apply type 2 if exists
        if type_2 and type_2 != "":
            for attack_type, matchups in TYPE_CHART.items():
                if type_2 in matchups:
                    effectiveness[attack_type] *= matchups[type_2]
        
        return effectiveness
    
    def extract_complete_row(self, data: Dict, pokemon_id: int) -> Dict:
        """Extract complete row data for CSV"""
        pokemon = data['pokemon']
        species = data['species']
        
        # Basic info
        name = pokemon['name'].replace('-', ' ').title()
        for name_entry in species['names']:
            if name_entry['language']['name'] == 'en':
                name = name_entry['name']
                break
        
        japanese_name = ""
        for name_entry in species['names']:
            if name_entry['language']['name'] == 'ja-Hrkt':
                japanese_name = name_entry['name']
                break
        
        generation = int(species['generation']['url'].split('/')[-2])
        
        # Species
        species_name = ""
        for genus in species['genera']:
            if genus['language']['name'] == 'en':
                species_name = genus['genus']
                break
        
        # Status
        is_legendary = species['is_legendary']
        is_mythical = species['is_mythical']
        status = "Legendary" if is_legendary else ("Mythical" if is_mythical else "Normal")
        
        # Types
        types = sorted(pokemon['types'], key=lambda x: x['slot'])
        type_1 = types[0]['type']['name'].capitalize()
        type_2 = types[1]['type']['name'].capitalize() if len(types) > 1 else ""
        type_number = len(types)
        
        # Abilities
        regular_abilities = [a for a in pokemon['abilities'] if not a['is_hidden']]
        ability_1 = regular_abilities[0]['ability']['name'].replace('-', ' ').title() if len(regular_abilities) > 0 else ""
        ability_2 = regular_abilities[1]['ability']['name'].replace('-', ' ').title() if len(regular_abilities) > 1 else ""
        
        hidden_abilities = [a for a in pokemon['abilities'] if a['is_hidden']]
        ability_hidden = hidden_abilities[0]['ability']['name'].replace('-', ' ').title() if hidden_abilities else ""
        abilities_number = len(pokemon['abilities'])
        
        # Stats
        stats_dict = {stat['stat']['name']: stat['base_stat'] for stat in pokemon['stats']}
        hp = stats_dict.get('hp', 0)
        attack = stats_dict.get('attack', 0)
        defense = stats_dict.get('defense', 0)
        sp_attack = stats_dict.get('special-attack', 0)
        sp_defense = stats_dict.get('special-defense', 0)
        speed = stats_dict.get('speed', 0)
        total_points = hp + attack + defense + sp_attack + sp_defense + speed
        
        # Physical attributes
        height_m = round(pokemon['height'] / 10, 2)
        weight_kg = round(pokemon['weight'] / 10, 1)
        
        # Breeding info
        egg_groups = [eg['name'].capitalize() for eg in species['egg_groups']]
        egg_type_1 = egg_groups[0] if len(egg_groups) > 0 else ""
        egg_type_2 = egg_groups[1] if len(egg_groups) > 1 else ""
        egg_type_number = len(egg_groups)
        
        gender_rate = species['gender_rate']
        percentage_male = 100 - (gender_rate * 12.5) if gender_rate >= 0 else -1
        
        egg_cycles = species['hatch_counter']
        
        # Other stats
        catch_rate = species['capture_rate']
        base_friendship = species['base_happiness']
        base_experience = pokemon['base_experience'] or 0
        growth_rate = species['growth_rate']['name'].replace('-', ' ').title()
        
        # Description
        description = ""
        for entry in species['flavor_text_entries']:
            if entry['language']['name'] == 'en' and entry['version']['name'] == 'sword':
                description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                break
        if not description:
            for entry in species['flavor_text_entries']:
                if entry['language']['name'] == 'en':
                    description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                    break
        
        # Type effectiveness
        effectiveness = self.calculate_type_effectiveness(type_1, type_2)
        
        # Calculate derived stats
        is_dual_type = type_number > 1
        full_type = f"{type_1}/{type_2}" if type_2 else type_1
        
        # Size and weight categories
        if height_m < 0.5:
            size_category = "Tiny"
        elif height_m < 1.0:
            size_category = "Small"
        elif height_m < 2.0:
            size_category = "Medium"
        elif height_m < 5.0:
            size_category = "Large"
        else:
            size_category = "Huge"
        
        if weight_kg < 10:
            weight_category = "Very Light"
        elif weight_kg < 50:
            weight_category = "Light"
        elif weight_kg < 100:
            weight_category = "Medium"
        elif weight_kg < 200:
            weight_category = "Heavy"
        else:
            weight_category = "Very Heavy"
        
        # Check if starter
        is_starter = pokemon_id in [1, 4, 7, 152, 155, 158, 252, 255, 258, 387, 390, 393, 
                                     495, 498, 501, 650, 653, 656, 722, 725, 728, 810, 813, 816, 906, 909, 912]
        
        # Check if pseudo-legendary (BST 600, 3-stage evolution)
        is_pseudo_legendary = total_points == 600 and pokemon_id in [149, 248, 376, 445, 612, 635, 706, 887]
        
        # BMI calculation
        bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0
        
        # Tiers
        if speed < 50:
            speed_tier = "Very Slow"
        elif speed < 80:
            speed_tier = "Slow"
        elif speed < 110:
            speed_tier = "Fast"
        else:
            speed_tier = "Very Fast"
        
        if total_points < 300:
            bst_tier = "Very Low"
        elif total_points < 450:
            bst_tier = "Low"
        elif total_points < 550:
            bst_tier = "Medium"
        elif total_points < 600:
            bst_tier = "High"
        else:
            bst_tier = "Very High"
        
        # Count resistances, weaknesses, immunities
        resistances_count = sum(1 for v in effectiveness.values() if v < 1.0 and v > 0)
        weaknesses_count = sum(1 for v in effectiveness.values() if v > 1.0)
        immunities_count = sum(1 for v in effectiveness.values() if v == 0)
        
        defensive_score = resistances_count - weaknesses_count + (immunities_count * 2)
        
        # Ratios
        physical_special_ratio = attack / sp_attack if sp_attack > 0 else attack
        offensive_rating = max(attack, sp_attack)
        defensive_rating = (defense + sp_defense) / 2
        
        # Percentiles (approximate - will be calculated properly later)
        hp_percentile = (hp / 255) * 100
        attack_percentile = (attack / 190) * 100
        defense_percentile = (defense / 230) * 100
        sp_attack_percentile = (sp_attack / 194) * 100
        sp_defense_percentile = (sp_defense / 230) * 100
        speed_percentile = (speed / 200) * 100
        total_points_percentile = (total_points / 720) * 100
        
        return {
            'pokedex_number': pokemon_id,
            'name': name,
            'japanese_name': japanese_name,
            'generation': generation,
            'status': status,
            'species': species_name,
            'type_number': type_number,
            'type_1': type_1,
            'type_2': type_2,
            'height_m': height_m,
            'weight_kg': weight_kg,
            'abilities_number': abilities_number,
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
            'egg_type_number': egg_type_number,
            'egg_type_1': egg_type_1,
            'egg_type_2': egg_type_2,
            'percentage_male': percentage_male,
            'egg_cycles': egg_cycles,
            'against_normal': effectiveness.get('Normal', 1.0),
            'against_fire': effectiveness.get('Fire', 1.0),
            'against_water': effectiveness.get('Water', 1.0),
            'against_electric': effectiveness.get('Electric', 1.0),
            'against_grass': effectiveness.get('Grass', 1.0),
            'against_ice': effectiveness.get('Ice', 1.0),
            'against_fight': effectiveness.get('Fighting', 1.0),
            'against_poison': effectiveness.get('Poison', 1.0),
            'against_ground': effectiveness.get('Ground', 1.0),
            'against_flying': effectiveness.get('Flying', 1.0),
            'against_psychic': effectiveness.get('Psychic', 1.0),
            'against_bug': effectiveness.get('Bug', 1.0),
            'against_rock': effectiveness.get('Rock', 1.0),
            'against_ghost': effectiveness.get('Ghost', 1.0),
            'against_dragon': effectiveness.get('Dragon', 1.0),
            'against_dark': effectiveness.get('Dark', 1.0),
            'against_steel': effectiveness.get('Steel', 1.0),
            'against_fairy': effectiveness.get('Fairy', 1.0),
            'bulba_description': description,
            'ability_1': ability_1,
            'ability_2': ability_2,
            'ability_hidden': ability_hidden,
            'hp_percentile': round(hp_percentile, 2),
            'attack_percentile': round(attack_percentile, 2),
            'defense_percentile': round(defense_percentile, 2),
            'sp_attack_percentile': round(sp_attack_percentile, 2),
            'sp_defense_percentile': round(sp_defense_percentile, 2),
            'speed_percentile': round(speed_percentile, 2),
            'total_points_percentile': round(total_points_percentile, 2),
            'physical_special_ratio': round(physical_special_ratio, 2),
            'offensive_rating': offensive_rating,
            'defensive_rating': round(defensive_rating, 2),
            'bmi': round(bmi, 2),
            'speed_tier': speed_tier,
            'bst_tier': bst_tier,
            'resistances_count': resistances_count,
            'weaknesses_count': weaknesses_count,
            'immunities_count': immunities_count,
            'defensive_score': defensive_score,
            'is_legendary': is_legendary,
            'is_starter': is_starter,
            'is_pseudo_legendary': is_pseudo_legendary,
            'type_count': type_number,
            'is_dual_type': is_dual_type,
            'full_type': full_type,
            'size_category': size_category,
            'weight_category': weight_category,
        }
    
    def update_csv_with_missing_pokemon(self):
        """Update the CSV file with all missing Pokemon"""
        print("=" * 80)
        print("ENHANCED POKEMON DATA UPDATER")
        print("=" * 80)
        
        # Create backup
        print("\nCreating backup...")
        try:
            df = pd.read_csv(CSV_PATH)
            df.to_csv(BACKUP_PATH, index=False)
            print(f"✓ Backup created at {BACKUP_PATH}")
        except Exception as e:
            print(f"✗ Error creating backup: {e}")
            return
        
        # Get current max Pokemon
        current_max = df['pokedex_number'].max()
        print(f"\nCurrent dataset: Pokemon #1 to #{current_max}")
        print(f"Target: Add Pokemon #{current_max + 1} to #1025")
        print(f"Missing Pokemon: {1025 - current_max}")
        
        # Fetch missing Pokemon
        print("\n" + "=" * 80)
        print("FETCHING MISSING POKEMON DATA")
        print("=" * 80 + "\n")
        
        new_rows = []
        for pokemon_id in range(current_max + 1, 1026):
            data = self.fetch_pokemon_complete(pokemon_id)
            if data:
                row = self.extract_complete_row(data, pokemon_id)
                new_rows.append(row)
            
            # Progress update every 50 Pokemon
            if pokemon_id % 50 == 0:
                print(f"\n--- Progress: {len(new_rows)}/{1025 - current_max} Pokemon added ---\n")
        
        # Create new DataFrame and append
        if new_rows:
            print(f"\n✓ Successfully fetched {len(new_rows)} new Pokemon!")
            print("\nUpdating CSV file...")
            
            new_df = pd.DataFrame(new_rows)
            
            # Ensure column order matches original
            # Fill missing columns with empty values
            for col in df.columns:
                if col not in new_df.columns:
                    new_df[col] = ""
            
            # Reorder columns to match original
            new_df = new_df[df.columns]
            
            # Append to original dataframe
            updated_df = pd.concat([df, new_df], ignore_index=True)
            
            # Save updated CSV
            updated_df.to_csv(CSV_PATH, index=False)
            print(f"✓ CSV updated with {len(new_rows)} new Pokemon!")
            print(f"✓ Total Pokemon in dataset: {len(updated_df)}")
        else:
            print("\n✗ No new Pokemon were fetched.")
        
        print("\n" + "=" * 80)
        print("UPDATE COMPLETE!")
        print("=" * 80)

def main():
    updater = EnhancedPokemonUpdater()
    updater.update_csv_with_missing_pokemon()

if __name__ == "__main__":
    main()
