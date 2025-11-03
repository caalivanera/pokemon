"""
Rebuild Complete Pokemon Dataset with Base Forms and Variants
This script properly merges base Pokemon with their variant forms
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re

print("="*70)
print("🔧 POKEMON DATASET REBUILD - COMPLETE FIX")
print("="*70)

# Load the source dataset with proper structure
print("\n📂 Loading source data...")
pokemon_df = pd.read_csv('data/pokemon.csv')
print(f"   Loaded: {len(pokemon_df)} Pokemon entries from pokemon.csv")

# Load current variant dataset for reference
current_df = pd.read_csv('data/national_dex_with_variants.csv')
print(f"   Current dataset: {len(current_df)} entries")

# Create backup
backup_path = 'data/national_dex_with_variants_before_rebuild.csv'
current_df.to_csv(backup_path, index=False)
print(f"   ✅ Backup created: {backup_path}")

print("\n🔧 Processing Pokemon data...")

# Function to determine variant type
def get_variant_type(name, base_name):
    """Determine the variant type from Pokemon name"""
    if pd.isna(base_name) or base_name == name:
        return 'base'
    
    name_lower = name.lower()
    
    if 'mega' in name_lower:
        if 'x' in name_lower:
            return 'mega-x'
        elif 'y' in name_lower:
            return 'mega-y'
        return 'mega'
    elif 'gigantamax' in name_lower or 'gmax' in name_lower:
        return 'gmax'
    elif 'alolan' in name_lower:
        return 'alolan'
    elif 'galarian' in name_lower:
        return 'galarian'
    elif 'hisuian' in name_lower:
        return 'hisuian'
    elif 'paldean' in name_lower:
        return 'paldean'
    elif 'primal' in name_lower:
        return 'primal'
    else:
        return 'base'

# Function to clean Pokemon name (remove variant prefix)
def clean_pokemon_name(name):
    """Remove variant prefixes from Pokemon name"""
    name = str(name)
    prefixes = ['Mega ', 'Gigantamax ', 'Alolan ', 'Galarian ', 
                'Hisuian ', 'Paldean ', 'Primal ']
    
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name.replace(prefix, '', 1)
    
    # Also remove X/Y suffixes for Megas
    name = re.sub(r'\s+[XY]$', '', name)
    
    return name

# Function to get form name
def get_form_name(original_name, variant_type):
    """Get the proper form name for display"""
    if variant_type == 'base':
        return original_name
    
    # Extract the variant descriptor
    if 'Mega' in original_name:
        if original_name.endswith(' X'):
            return f"Mega {clean_pokemon_name(original_name)} X"
        elif original_name.endswith(' Y'):
            return f"Mega {clean_pokemon_name(original_name)} Y"
        return f"Mega {clean_pokemon_name(original_name)}"
    elif 'Gigantamax' in original_name:
        return f"Gigantamax {clean_pokemon_name(original_name)}"
    elif 'Alolan' in original_name:
        return f"Alolan {clean_pokemon_name(original_name)}"
    elif 'Galarian' in original_name:
        return f"Galarian {clean_pokemon_name(original_name)}"
    elif 'Hisuian' in original_name:
        return f"Hisuian {clean_pokemon_name(original_name)}"
    elif 'Paldean' in original_name:
        return f"Paldean {clean_pokemon_name(original_name)}"
    elif 'Primal' in original_name:
        return f"Primal {clean_pokemon_name(original_name)}"
    
    return original_name

# Function to get sprite path
def get_sprite_path(dex_num, variant_type, sprite_type='static'):
    """Generate sprite path based on Pokemon and variant"""
    base_path = "assets/sprites"
    pid = str(dex_num).zfill(3)
    
    if variant_type == 'base':
        if sprite_type == 'static':
            path = f"{base_path}/{pid}.png"
        elif sprite_type == 'animated':
            path = f"{base_path}/animated/{pid}.gif"
        elif sprite_type == 'shiny':
            path = f"{base_path}/shiny/{pid}.png"
    else:
        # Variant sprites
        variant_suffix = variant_type.replace('-', '_')
        if sprite_type == 'static':
            path = f"{base_path}/{pid}_{variant_suffix}.png"
        elif sprite_type == 'animated':
            path = f"{base_path}/animated/{pid}_{variant_suffix}.gif"
        elif sprite_type == 'shiny':
            path = f"{base_path}/shiny/{pid}_{variant_suffix}.png"
    
    # Check if file exists
    if Path(path).exists():
        return path
    return "TBA"

# Process each Pokemon entry
processed_data = []

for idx, row in pokemon_df.iterrows():
    dex_num = row['Dex No']
    original_name = row['Name']
    base_name = row.get('Base Name', original_name)
    
    # Determine variant type
    variant_type = get_variant_type(original_name, base_name)
    
    # Clean name
    clean_name = clean_pokemon_name(original_name)
    
    # Get form name
    form_name = get_form_name(original_name, variant_type)
    
    # Get sprite paths
    sprite_static = get_sprite_path(dex_num, variant_type, 'static')
    sprite_animated = get_sprite_path(dex_num, variant_type, 'animated')
    sprite_shiny = get_sprite_path(dex_num, variant_type, 'shiny')
    
    # Find matching entry in current dataset to preserve other columns
    match = current_df[
        (current_df['pokedex_number'] == dex_num) & 
        (current_df['name'] == clean_name)
    ]
    
    if len(match) > 0:
        # Use existing entry and update specific fields
        entry = match.iloc[0].to_dict()
    else:
        # Try to find base form match
        match_base = current_df[current_df['pokedex_number'] == dex_num]
        if len(match_base) > 0:
            entry = match_base.iloc[0].to_dict()
        else:
            # Create minimal entry
            entry = {col: np.nan for col in current_df.columns}
            entry['pokedex_number'] = dex_num
    
    # Update critical fields
    entry['name'] = clean_name
    entry['variant_type'] = variant_type
    entry['form_name'] = form_name
    entry['sprite_path_static'] = sprite_static
    entry['sprite_path_animated'] = sprite_animated
    entry['sprite_path_shiny'] = sprite_shiny
    entry['base_pokemon_id'] = dex_num if variant_type == 'base' else dex_num
    
    processed_data.append(entry)

# Create new DataFrame
new_df = pd.DataFrame(processed_data)

print(f"\n✅ Processed {len(new_df)} Pokemon entries")
print(f"   Base forms: {len(new_df[new_df['variant_type'] == 'base'])}")
print(f"   Variants: {len(new_df[new_df['variant_type'] != 'base'])}")

# Verify all Pokemon have base forms
print("\n🔍 Verifying base forms...")
missing_base = []
for dex_num in new_df['pokedex_number'].unique():
    pokemon_entries = new_df[new_df['pokedex_number'] == dex_num]
    base_entries = pokemon_entries[pokemon_entries['variant_type'] == 'base']
    
    if len(base_entries) == 0:
        pokemon_name = pokemon_entries.iloc[0]['name']
        missing_base.append(f"#{dex_num:03d} {pokemon_name}")

if missing_base:
    print(f"   ⚠️  {len(missing_base)} Pokemon still missing base forms:")
    for pokemon in missing_base[:10]:
        print(f"      {pokemon}")
    if len(missing_base) > 10:
        print(f"      ... and {len(missing_base) - 10} more")
else:
    print("   ✅ All Pokemon have base forms!")

# Check sprite availability
print("\n🖼️  Checking sprite availability...")
static_available = len(new_df[new_df['sprite_path_static'] != 'TBA'])
static_missing = len(new_df[new_df['sprite_path_static'] == 'TBA'])
print(f"   Static sprites: {static_available} available, {static_missing} TBA")

animated_available = len(new_df[new_df['sprite_path_animated'] != 'TBA'])
animated_missing = len(new_df[new_df['sprite_path_animated'] == 'TBA'])
print(f"   Animated sprites: {animated_available} available, {animated_missing} TBA")

# Save the new dataset
output_path = 'data/national_dex_with_variants.csv'
new_df.to_csv(output_path, index=False)
print(f"\n💾 Saved new dataset: {output_path}")

# Generate summary report
print("\n" + "="*70)
print("✅ REBUILD COMPLETE!")
print("="*70)
print(f"\n📊 Final Statistics:")
print(f"   Total entries: {len(new_df)}")
print(f"   Unique Pokemon: {new_df['pokedex_number'].nunique()}")
print(f"   Base forms: {len(new_df[new_df['variant_type'] == 'base'])}")
print(f"   Mega forms: {len(new_df[new_df['variant_type'].str.contains('mega', na=False)])}")
print(f"   Gigantamax forms: {len(new_df[new_df['variant_type'] == 'gmax'])}")
print(f"   Regional forms: {len(new_df[new_df['variant_type'].isin(['alolan', 'galarian', 'hisuian', 'paldean'])])}")

print(f"\n📁 Files:")
print(f"   Output: {output_path}")
print(f"   Backup: {backup_path}")

print(f"\n✅ Dataset ready for use!")
