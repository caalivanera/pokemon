"""
Complete Sprite Downloader - ALL 1025 Pokemon
Downloads both static PNG and animated GIF sprites
Version 2.0
"""

import requests
import os
from pathlib import Path
import time
from PIL import Image
import io

# Create directories
SPRITES_DIR = Path("assets/sprites")
ICONS_DIR = Path("assets/icons")
ANIMATED_DIR = Path("assets/animated")

SPRITES_DIR.mkdir(parents=True, exist_ok=True)
ICONS_DIR.mkdir(parents=True, exist_ok=True)
ANIMATED_DIR.mkdir(parents=True, exist_ok=True)

def download_sprite(pokemon_id: int, sprite_type: str, output_dir: Path) -> bool:
    """
    Download a sprite from PokeAPI
    
    sprite_type can be:
    - 'official-artwork': High-res official artwork (PNG)
    - 'front_default': Main sprite (PNG)
    - 'front_animated': Animated GIF
    """
    try:
        # Get Pokemon data
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        if response.status_code != 200:
            print(f"❌ Pokemon #{pokemon_id} not found")
            return False
        
        data = response.json()
        pokemon_name = data['name']
        
        # Get sprite URL based on type
        if sprite_type == 'official-artwork':
            sprite_url = data['sprites']['other']['official-artwork']['front_default']
        elif sprite_type == 'front_animated':
            sprite_url = data['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
            if not sprite_url:
                # Fallback to static if no animation
                sprite_url = data['sprites']['front_default']
        else:
            sprite_url = data['sprites'].get(sprite_type)
        
        if not sprite_url:
            print(f"⚠️  No {sprite_type} sprite for #{pokemon_id:04d} {pokemon_name}")
            return False
        
        # Download sprite
        img_response = requests.get(sprite_url)
        if img_response.status_code != 200:
            print(f"❌ Failed to download sprite for #{pokemon_id:04d}")
            return False
        
        # Determine file extension
        extension = '.gif' if 'animated' in sprite_type or sprite_url.endswith('.gif') else '.png'
        
        # Save sprite
        filename = f"{pokemon_id:04d}_{pokemon_name}{extension}"
        filepath = output_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(img_response.content)
        
        print(f"✅ Downloaded {sprite_type}: #{pokemon_id:04d} {pokemon_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading #{pokemon_id}: {e}")
        return False

def check_existing_sprites():
    """Check which sprites we already have"""
    existing_sprites = set()
    existing_icons = set()
    existing_animated = set()
    
    for file in SPRITES_DIR.glob("*.png"):
        pokemon_id = int(file.stem.split('_')[0])
        existing_sprites.add(pokemon_id)
    
    for file in ICONS_DIR.glob("*.png"):
        pokemon_id = int(file.stem.split('_')[0])
        existing_icons.add(pokemon_id)
    
    for file in ANIMATED_DIR.glob("*.gif"):
        pokemon_id = int(file.stem.split('_')[0])
        existing_animated.add(pokemon_id)
    
    return existing_sprites, existing_icons, existing_animated

def main():
    print("="*60)
    print("🎮 COMPLETE POKEMON SPRITE DOWNLOADER")
    print("="*60)
    print()
    
    # Check existing sprites
    print("📊 Checking existing sprites...")
    existing_sprites, existing_icons, existing_animated = check_existing_sprites()
    
    print(f"✅ Found {len(existing_sprites)} official artwork sprites")
    print(f"✅ Found {len(existing_icons)} icon sprites")
    print(f"✅ Found {len(existing_animated)} animated sprites")
    print()
    
    # Determine what to download
    missing_sprites = set(range(1, 1026)) - existing_sprites
    missing_icons = set(range(1, 1026)) - existing_icons
    missing_animated = set(range(1, 1026)) - existing_animated
    
    print(f"📥 Need to download:")
    print(f"   - {len(missing_sprites)} official artwork sprites")
    print(f"   - {len(missing_icons)} icon sprites")
    print(f"   - {len(missing_animated)} animated sprites")
    print()
    
    if not (missing_sprites or missing_icons or missing_animated):
        print("✅ All sprites already downloaded!")
        return
    
    input("Press Enter to start downloading...")
    print()
    
    # Download missing official artwork
    if missing_sprites:
        print("📥 Downloading official artwork sprites...")
        print("-"*60)
        success_count = 0
        for pokemon_id in sorted(missing_sprites):
            if download_sprite(pokemon_id, 'official-artwork', SPRITES_DIR):
                success_count += 1
            time.sleep(0.1)  # Rate limiting
            
            if pokemon_id % 50 == 0:
                print(f"   Progress: {pokemon_id}/1025")
        
        print(f"✅ Downloaded {success_count} official artwork sprites")
        print()
    
    # Download missing icons (front_default)
    if missing_icons:
        print("📥 Downloading icon sprites...")
        print("-"*60)
        success_count = 0
        for pokemon_id in sorted(missing_icons):
            if download_sprite(pokemon_id, 'front_default', ICONS_DIR):
                success_count += 1
            time.sleep(0.1)  # Rate limiting
            
            if pokemon_id % 50 == 0:
                print(f"   Progress: {pokemon_id}/1025")
        
        print(f"✅ Downloaded {success_count} icon sprites")
        print()
    
    # Download animated sprites
    if missing_animated:
        print("📥 Downloading animated sprites...")
        print("-"*60)
        success_count = 0
        for pokemon_id in sorted(missing_animated):
            if download_sprite(pokemon_id, 'front_animated', ANIMATED_DIR):
                success_count += 1
            time.sleep(0.1)  # Rate limiting
            
            if pokemon_id % 50 == 0:
                print(f"   Progress: {pokemon_id}/1025")
        
        print(f"✅ Downloaded {success_count} animated sprites")
        print()
    
    # Final summary
    print("="*60)
    print("📊 DOWNLOAD COMPLETE")
    print("="*60)
    
    final_sprites, final_icons, final_animated = check_existing_sprites()
    
    print(f"✅ Official Artwork: {len(final_sprites)}/1025")
    print(f"✅ Icon Sprites: {len(final_icons)}/1025")
    print(f"✅ Animated Sprites: {len(final_animated)}/1025")
    print()
    print("🎉 All sprite downloads complete!")

if __name__ == "__main__":
    main()
