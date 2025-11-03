import pandas as pd
import numpy as np
import os
import sys
from typing import Optional, Dict, Any

def load_pokemon_glossary(
    glossary_path: str = None
) -> Dict[str, str]:
    """
    Loads the Pokemon glossary from CSV file.
    
    Args:
        glossary_path (str): Path to the glossary CSV file.
        
    Returns:
        Dict[str, str]: Dictionary mapping terms to their definitions.
    """
    # Get the directory of this script and construct absolute path
    if glossary_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        data_dir = os.path.join(project_root, 'data')
        glossary_path = os.path.join(data_dir, 'pokemon_glossary.csv')
    
    print(f"Loading glossary from: {glossary_path}")
    glossary = {}
    try:
        if os.path.exists(glossary_path):
            df = pd.read_csv(glossary_path, header=None)
            # Parse the glossary structure - terms and definitions
            current_term = None
            for _, row in df.iterrows():
                if pd.notna(row[0]) and row[0] != 'Pokémon glossary':
                    # Check if this is a term (single word/phrase)
                    if len(str(row[0]).split()) <= 3 and not str(row[0]).startswith('"'):
                        current_term = str(row[0]).strip()
                    elif current_term and pd.notna(row[0]):
                        # This is a definition
                        definition = str(row[0]).strip().strip('"')
                        glossary[current_term] = definition
                        current_term = None
        # Ensure Pokédex definition is present using the provided description
        pokedex_def = (
            "A Pokédex is a digital electronic encyclopedia that acts as a guide for Pokémon trainers, "
            "recording data on Pokémon species they encounter. In the games, it tracks the player's "
            "progress in catching or observing Pokémon, with detailed entries unlocked as a trainer "
            "catches or obtains a species. It's an essential tool for any trainer, and in some versions "
            "of the games and the anime, it functions as a reference tool to learn about Pokémon types, "
            "sizes, and locations."
        )
        for key in ("Pokedex", "Pokédex"):
            if key not in glossary:
                glossary[key] = pokedex_def

        print(f"Loaded {len(glossary)} terms from Pokemon glossary.")
    except Exception as e:
        print(f"Error loading glossary: {e}", file=sys.stderr)
    
    return glossary

def load_enhanced_pokemon_data(
    pokedex_path: str = None,
    pokedex_other_path: str = None, 
    poke_corpus_path: str = None
) -> pd.DataFrame:
    """
    Loads and combines Pokemon data from multiple CSV sources.
    
    Args:
        pokedex_path (str): Path to the main pokedex CSV file.
        pokedex_other_path (str): Path to the alternative pokedex CSV file.
        poke_corpus_path (str): Path to the poke corpus CSV file.
        
    Returns:
        pd.DataFrame: Combined and enhanced Pokemon DataFrame.
    """
    print("Loading enhanced Pokemon data from local CSV files...")
    
    # Get the directory of this script and construct absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(project_root, 'data')
    
    # Set default paths if not provided
    if pokedex_path is None:
        pokedex_path = os.path.join(data_dir, 'pokedex.csv')
    if pokedex_other_path is None:
        pokedex_other_path = os.path.join(data_dir, 'pokedex_otherVer.csv')
    if poke_corpus_path is None:
        poke_corpus_path = os.path.join(data_dir, 'poke_corpus.csv')
    
    print(f"Data directory: {data_dir}")
    print(f"Looking for pokedex at: {pokedex_path}")
    
    # Load main pokedex data
    try:
        if not os.path.exists(pokedex_path):
            print(f"ERROR: Main pokedex file not found at {pokedex_path}", file=sys.stderr)
            return pd.DataFrame()
        main_df = pd.read_csv(pokedex_path)
        print(f"Loaded {len(main_df)} entries from main pokedex.")
    except Exception as e:
        print(f"Error loading main pokedex: {e}", file=sys.stderr)
        return pd.DataFrame()
    
    # Load alternative pokedex for additional info
    try:
        if os.path.exists(pokedex_other_path):
            other_df = pd.read_csv(pokedex_other_path)
            print(f"Loaded {len(other_df)} entries from alternative pokedex.")
        else:
            other_df = pd.DataFrame()
    except Exception as e:
        print(f"Error loading alternative pokedex: {e}", file=sys.stderr)
        other_df = pd.DataFrame()
    
    # Load poke corpus for descriptions
    try:
        if os.path.exists(poke_corpus_path):
            corpus_df = pd.read_csv(poke_corpus_path)
            print(f"Loaded {len(corpus_df)} entries from poke corpus.")
        else:
            corpus_df = pd.DataFrame()
    except Exception as e:
        print(f"Error loading poke corpus: {e}", file=sys.stderr)
        corpus_df = pd.DataFrame()
    
    # Filter for Generation 1 Pokemon (IDs 1-151)
    gen1_df = main_df[
        (main_df['pokedex_number'] <= 151) & 
        (main_df['generation'] == 1)
    ].copy()
    
    # Create enhanced dataframe with standardized columns
    enhanced_pokemon = []
    
    for _, pokemon in gen1_df.iterrows():
        # Get additional info from other sources
        other_info = None
        if not other_df.empty:
            other_match = other_df[other_df['id'] == pokemon['pokedex_number']]
            if not other_match.empty:
                other_info = other_match.iloc[0]
        
        # Get corpus info
        corpus_info = ""
        if not corpus_df.empty:
            corpus_match = corpus_df[
                corpus_df['pokemon_info'].str.contains(
                    pokemon['name'], case=False, na=False
                )
            ]
            if not corpus_match.empty:
                corpus_info = corpus_match.iloc[0]['pokemon_info']
        
        # Create enhanced Pokemon entry
        enhanced_entry = {
            'id': int(pokemon['pokedex_number']),
            'name': pokemon['name'].title(),
            'japanese_name': pokemon.get('japanese_name', ''),
            'species': pokemon.get('species', ''),
            'generation': pokemon.get('generation', 1),
            'primary_type': pokemon['type_1'],
            'secondary_type': pokemon['type_2'] if pd.notna(pokemon['type_2']) else None,
            'height_m': float(pokemon['height_m']),
            'weight_kg': float(pokemon['weight_kg']),
            'hp': int(pokemon['hp']),
            'attack': int(pokemon['attack']),
            'defense': int(pokemon['defense']),
            'special_attack': int(pokemon['sp_attack']),
            'special_defense': int(pokemon['sp_defense']),
            'speed': int(pokemon['speed']),
            'total_points': int(pokemon['total_points']),
            'catch_rate': float(pokemon['catch_rate']) if pd.notna(pokemon['catch_rate']) else 0,
            'base_friendship': float(pokemon['base_friendship']) if pd.notna(pokemon['base_friendship']) else 0,
            'base_experience': float(pokemon['base_experience']) if pd.notna(pokemon['base_experience']) else 0,
            'growth_rate': pokemon.get('growth_rate', ''),
            'egg_type_1': pokemon.get('egg_type_1', ''),
            'egg_type_2': pokemon.get('egg_type_2', '') if pd.notna(pokemon.get('egg_type_2')) else None,
            'percentage_male': float(pokemon['percentage_male']) if pd.notna(pokemon['percentage_male']) else 50.0,
            'abilities': [
                ability for ability in [
                    pokemon.get('ability_1'), 
                    pokemon.get('ability_2'),
                    pokemon.get('ability_hidden')
                ] if pd.notna(ability)
            ],
            'ability_descriptions': {
                pokemon.get('ability_1'): pokemon.get('ability_1_description') 
                if pd.notna(pokemon.get('ability_1_description')) else '',
                pokemon.get('ability_2'): pokemon.get('ability_2_description') 
                if pd.notna(pokemon.get('ability_2_description')) else '',
                pokemon.get('ability_hidden'): pokemon.get('ability_hidden_description') 
                if pd.notna(pokemon.get('ability_hidden_description')) else ''
            },
            'smogon_description': pokemon.get('smogon_description', '') if pd.notna(pokemon.get('smogon_description')) else '',
            'bulbapedia_description': pokemon.get('bulba_description', '') if pd.notna(pokemon.get('bulba_description')) else '',
            'additional_info': other_info['info'] if other_info is not None and 'info' in other_info else '',
            'corpus_info': corpus_info,
            'sprite_url': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon['pokedex_number']}.png"
        }
        
        enhanced_pokemon.append(enhanced_entry)
    
    df = pd.DataFrame(enhanced_pokemon)
    print(f"Enhanced data processing complete. Created {len(df)} Pokemon entries.")
    return df

def fetch_all_pokemon(limit: int = 151) -> pd.DataFrame:
    """
    Loads Pokemon data from local CSV files instead of API.
    
    Args:
        limit (int): The number of Pokémon to load (e.g., 151 for Gen 1).
        
    Returns:
        pd.DataFrame: A DataFrame containing all Pokemon data from local sources.
    """
    print(f"Loading data for {limit} Pokémon from local CSV files...")
    
    # Load enhanced data from CSV files
    df = load_enhanced_pokemon_data()
    
    if df.empty:
        print("No Pokémon data was loaded. Returning empty DataFrame.", file=sys.stderr)
        return pd.DataFrame()
    
    # Filter to requested limit
    df = df[df['id'] <= limit]
    
    # Ensure consistent column order for compatibility
    columns_order = [
        'id', 'name', 'japanese_name', 'species', 'generation',
        'primary_type', 'secondary_type', 'height_m', 'weight_kg', 
        'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed',
        'total_points', 'catch_rate', 'base_friendship', 'base_experience',
        'growth_rate', 'egg_type_1', 'egg_type_2', 'percentage_male',
        'abilities', 'ability_descriptions', 'smogon_description', 
        'bulbapedia_description', 'additional_info', 'corpus_info', 'sprite_url'
    ]
    
    # Ensure all expected columns exist
    for col in columns_order:
        if col not in df.columns:
            df[col] = None
            
    df = df[columns_order]
    return df

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    # e.g., python utils/data_extractor.py
    data = fetch_all_pokemon(limit=10)
    print("Test fetch successful:")
    print(data.head())