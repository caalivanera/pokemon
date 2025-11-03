"""
Enhanced Pokemon Data Loader with YAML Integration
Loads and merges data from CSV files and YAML structured data
"""

import pandas as pd
import yaml
import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path


class PokemonDataLoader:
    """Centralized data loader for all Pokemon data sources."""
    
    def __init__(self, base_path: str = '../..'):
        self.base_path = Path(base_path)
        self.yaml_path = self.base_path / 'pokemondbgit'
        self.cache = {}
        
    def load_yaml_file(self, filename: str) -> Dict[str, Any]:
        """Load a YAML file from pokemondbgit folder."""
        filepath = self.yaml_path / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def load_all_yaml_data(self) -> Dict[str, Any]:
        """Load all YAML data files."""
        yaml_files = [
            'pokemon.yaml',
            'moves.yaml',
            'abilities.yaml',
            'types.yaml',
            'type-chart.yaml',
            'items.yaml',
            'locations.yaml',
            'egg-groups.yaml',
            'games.yaml',
            'releases.yaml',
            'pokemon-forms.yaml'
        ]
        
        data = {}
        for filename in yaml_files:
            key = filename.replace('.yaml', '').replace('-', '_')
            print(f"Loading {filename}...")
            data[key] = self.load_yaml_file(filename)
            
        return data
    
    def get_type_effectiveness(
        self, 
        attacking_type: str,
        defending_type: str,
        type_chart: Dict[str, Any]
    ) -> float:
        """Calculate type effectiveness multiplier."""
        attacking_data = type_chart.get(attacking_type.lower(), {})
        
        if defending_type.lower() in attacking_data.get('super-effective', []):
            return 2.0
        elif defending_type.lower() in attacking_data.get('not-very-effective', []):
            return 0.5
        elif defending_type.lower() in attacking_data.get('no-effect', []):
            return 0.0
        else:
            return 1.0
    
    def get_all_moves(self, moves_yaml: Dict[str, Any]) -> pd.DataFrame:
        """Convert moves YAML to DataFrame."""
        moves_list = []
        
        for move_id, move_data in moves_yaml.items():
            move_info = {
                'move_id': move_id,
                'name': move_data.get('name', move_id),
                'type': move_data.get('type', ''),
                'category': move_data.get('category', ''),
                'power': move_data.get('power', 0),
                'accuracy': move_data.get('accuracy', 0),
                'pp': move_data.get('pp', 0),
                'priority': move_data.get('priority', 0)
            }
            moves_list.append(move_info)
        
        return pd.DataFrame(moves_list)
    
    def get_all_abilities(self, abilities_yaml: Dict[str, Any]) -> pd.DataFrame:
        """Convert abilities YAML to DataFrame."""
        abilities_list = []
        
        for ability_id, ability_data in abilities_yaml.items():
            if isinstance(ability_data, dict):
                ability_info = {
                    'ability_id': ability_id,
                    'name': ability_data.get('name', ability_id)
                }
                abilities_list.append(ability_info)
        
        return pd.DataFrame(abilities_list)


if __name__ == "__main__":
    # Test the enhanced loader
    loader = PokemonDataLoader()
    yaml_data = loader.load_all_yaml_data()
    
    print(f"\n✅ Successfully loaded {len(yaml_data)} YAML datasets")
    print(f"   - Pokemon entries: {len(yaml_data.get('pokemon', {}))}")
    print(f"   - Moves: {len(yaml_data.get('moves', {}))}")
    print(f"   - Abilities: {len(yaml_data.get('abilities', {}))}")
