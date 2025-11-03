"""
Download Missing Pokemon Sprites
Downloads the 39 missing variant sprites and adds animated/shiny sprites
"""

import requests
from pathlib import Path
import json
import time
from PIL import Image
import io

print("="*70)
print("🎨 DOWNLOADING MISSING POKEMON SPRITES")
print("="*70)

# Load the asset verification report
with open('data/asset_verification_report.json', 'r') as f:
    report = json.load(f)

SPRITES_DIR = Path("assets/sprites")
ANIMATED_DIR = SPRITES_DIR / "animated"
SHINY_DIR = SPRITES_DIR / "shiny"

# Ensure directories exist
SPRITES_DIR.mkdir(parents=True, exist_ok=True)
ANIMATED_DIR.mkdir(parents=True, exist_ok=True)
SHINY_DIR.mkdir(parents=True, exist_ok=True)

# PokéAPI base URL
POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"

def download_sprite(url, save_path):
    """Download a sprite from URL and save to path"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            img.save(save_path)
            return True
        return False
    except Exception as e:
        print(f"      Error: {e}")
        return False

def get_pokemon_sprites(pokemon_id, variant=None):
    """Get sprite URLs for a Pokemon from PokéAPI"""
    try:
        # Build URL
        if variant:
            # Try variant-specific endpoint
            variant_name = variant.lower().replace(' ', '-')
            url = f"{POKEAPI_BASE}/{pokemon_id}-{variant_name}"
        else:
            url = f"{POKEAPI_BASE}/{pokemon_id}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            sprites = data.get('sprites', {})
            
            return {
                'front_default': sprites.get('front_default'),
                'front_shiny': sprites.get('front_shiny'),
                'animated': sprites.get('versions', {}).get('generation-v', {})
                           .get('black-white', {}).get('animated', {})
                           .get('front_default')
            }
        return None
    except Exception as e:
        print(f"      API Error: {e}")
        return None

print("\n📥 Downloading missing static sprites...")

missing_static = report['missing_details']['static']
downloaded = 0
failed = 0

# Parse missing sprite entries
for entry in missing_static:
    if 'TBA' not in entry:
        continue
    
    # Extract Pokemon number and form
    parts = entry.split(' - ')[0]  # Get "#052 Alolan Meowth"
    
    # Extract dex number
    dex_match = parts.split('#')[1].split(' ')[0]
    dex_num = int(dex_match)
    
    # Extract form name
    form_parts = parts.split(' ', 1)
    if len(form_parts) > 1:
        form_name = form_parts[1]
    else:
        form_name = None
    
    print(f"\n   Downloading #{dex_num:03d} {form_name}...")
    
    # Determine variant type for API
    variant = None
    if form_name:
        if 'Mega' in form_name:
            variant = 'mega'
        elif 'Alolan' in form_name:
            variant = 'alola'
        elif 'Galarian' in form_name:
            variant = 'galar'
        elif 'Hisuian' in form_name:
            variant = 'hisui'
        elif 'Paldean' in form_name:
            variant = 'paldea'
    
    # Get sprite URLs
    sprite_data = get_pokemon_sprites(dex_num, variant)
    
    if sprite_data and sprite_data['front_default']:
        # Download static sprite
        save_path = SPRITES_DIR / f"{dex_num:03d}_{variant}.png"
        if download_sprite(sprite_data['front_default'], save_path):
            print(f"      ✅ Static sprite downloaded")
            downloaded += 1
        else:
            print(f"      ❌ Failed to download")
            failed += 1
        
        # Download shiny sprite if available
        if sprite_data['front_shiny']:
            shiny_path = SHINY_DIR / f"{dex_num:03d}_{variant}.png"
            if download_sprite(sprite_data['front_shiny'], shiny_path):
                print(f"      ✅ Shiny sprite downloaded")
        
        # Download animated sprite if available
        if sprite_data['animated']:
            animated_path = ANIMATED_DIR / f"{dex_num:03d}_{variant}.gif"
            if download_sprite(sprite_data['animated'], animated_path):
                print(f"      ✅ Animated sprite downloaded")
        
        time.sleep(0.5)  # Rate limiting
    else:
        print(f"      ⚠️  Sprite not available in PokéAPI")
        failed += 1

print(f"\n📊 Static Sprites Download Results:")
print(f"   ✅ Downloaded: {downloaded}")
print(f"   ❌ Failed: {failed}")

# Download base Pokemon animated and shiny sprites
print("\n📥 Downloading animated sprites for base Pokemon (Gen 1-5)...")

import pandas as pd
df = pd.read_csv('data/national_dex_with_variants.csv')
base_pokemon = df[df['variant_type'] == 'base']

animated_count = 0
shiny_count = 0

for _, row in base_pokemon.iterrows():
    dex_num = int(row['pokedex_number'])
    
    # Only download for Gen 1-5 (up to #649)
    if dex_num > 649:
        continue
    
    # Check if already exists
    animated_path = ANIMATED_DIR / f"{dex_num:03d}.gif"
    shiny_path = SHINY_DIR / f"{dex_num:03d}.png"
    
    if not animated_path.exists() or not shiny_path.exists():
        sprite_data = get_pokemon_sprites(dex_num)
        
        if sprite_data:
            # Download animated
            if not animated_path.exists() and sprite_data.get('animated'):
                if download_sprite(sprite_data['animated'], animated_path):
                    animated_count += 1
            
            # Download shiny
            if not shiny_path.exists() and sprite_data.get('front_shiny'):
                if download_sprite(sprite_data['front_shiny'], shiny_path):
                    shiny_count += 1
        
        time.sleep(0.5)  # Rate limiting
    
    if dex_num % 50 == 0:
        print(f"   Progress: {dex_num}/649...")

print(f"\n📊 Additional Downloads:")
print(f"   🎬 Animated sprites: {animated_count}")
print(f"   ✨ Shiny sprites: {shiny_count}")

print("\n" + "="*70)
print("✅ DOWNLOAD COMPLETE!")
print("="*70)

print("\nRun verify_all_assets.py to see updated coverage statistics.")
