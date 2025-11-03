"""
Download high-quality Pokemon sprites from PokeAPI
Downloads official artwork (475x475 PNG) for all 1025 Pokemon
"""

import requests
import json
from pathlib import Path
import time
from typing import Optional

# Configuration
POKEAPI_SPRITES_BASE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"
OFFICIAL_ARTWORK_BASE = f"{POKEAPI_SPRITES_BASE}/other/official-artwork"
SPRITE_DIR = Path("assets/sprites")
ICON_DIR = Path("assets/icons")
JSON_PATH = Path("data/new_pokemon_data.json")
RATE_LIMIT = 0.2  # seconds between downloads

# Create directories
SPRITE_DIR.mkdir(parents=True, exist_ok=True)
ICON_DIR.mkdir(parents=True, exist_ok=True)


class SpriteDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pokemon-Dashboard-Sprite-Downloader/1.0'
        })
        self.success_count = 0
        self.fail_count = 0
    
    def download_sprite(
        self, 
        pokemon_id: int, 
        pokemon_name: str, 
        sprite_type: str = "official"
    ) -> bool:
        """Download a single sprite"""
        try:
            # Determine URL based on type
            if sprite_type == "official":
                url = f"{OFFICIAL_ARTWORK_BASE}/{pokemon_id}.png"
                output_dir = SPRITE_DIR
            else:
                url = f"{POKEAPI_SPRITES_BASE}/{pokemon_id}.png"
                output_dir = ICON_DIR
            
            # Clean Pokemon name for filename
            clean_name = pokemon_name.lower().replace(" ", "_")
            clean_name = clean_name.replace(".", "").replace("'", "")
            filename = f"{pokemon_id:04d}_{clean_name}.png"
            filepath = output_dir / filename
            
            # Skip if already exists
            if filepath.exists():
                print(f"  ✓ #{pokemon_id} {pokemon_name} (cached)")
                self.success_count += 1
                return True
            
            # Download
            print(f"  Downloading #{pokemon_id} {pokemon_name}...", end=" ")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Save
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print("✓")
            self.success_count += 1
            time.sleep(RATE_LIMIT)
            return True
            
        except Exception as e:
            print(f"✗ Error: {e}")
            self.fail_count += 1
            return False
    
    def download_all_from_json(self):
        """Download sprites for all Pokemon in the JSON file"""
        print("=" * 80)
        print("DOWNLOADING POKEMON SPRITES")
        print("=" * 80 + "\n")
        
        # Load Pokemon data
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            pokemon_list = json.load(f)
        
        print(f"Found {len(pokemon_list)} Pokemon in JSON")
        print(f"Output directory: {SPRITE_DIR}\n")
        
        # Download official artwork
        print("Downloading official artwork (475x475)...")
        for pkmn in pokemon_list:
            self.download_sprite(
                pkmn['pokedex_number'],
                pkmn['name'],
                "official"
            )
        
        # Download icons
        print("\nDownloading icons...")
        for pkmn in pokemon_list:
            self.download_sprite(
                pkmn['pokedex_number'],
                pkmn['name'],
                "icon"
            )
        
        # Summary
        print("\n" + "=" * 80)
        print("DOWNLOAD COMPLETE!")
        print("=" * 80)
        print(f"✓ Success: {self.success_count}")
        print(f"✗ Failed: {self.fail_count}")
        print(f"Total sprites: {self.success_count}")
        print("=" * 80)
    
    def download_all_pokemon(self, start_id: int = 1, end_id: int = 1025):
        """Download sprites for all Pokemon by ID range"""
        print("=" * 80)
        print("DOWNLOADING ALL POKEMON SPRITES")
        print("=" * 80 + "\n")
        
        print(f"Downloading Pokemon #{start_id} to #{end_id}")
        print(f"Output directory: {SPRITE_DIR}\n")
        
        for pokemon_id in range(start_id, end_id + 1):
            # Use ID as name for now
            name = f"pokemon_{pokemon_id}"
            
            # Download official artwork
            self.download_sprite(pokemon_id, name, "official")
            
            # Progress marker every 50
            if pokemon_id % 50 == 0:
                print(f"\n--- Progress: {pokemon_id}/{end_id} ---\n")
        
        # Summary
        print("\n" + "=" * 80)
        print("DOWNLOAD COMPLETE!")
        print("=" * 80)
        print(f"✓ Success: {self.success_count}")
        print(f"✗ Failed: {self.fail_count}")
        print("=" * 80)


def main():
    downloader = SpriteDownloader()
    
    # Try JSON first (has Pokemon names)
    if JSON_PATH.exists():
        print("Using Pokemon data from JSON file for accurate naming...\n")
        downloader.download_all_from_json()
    else:
        print("JSON not found, downloading by ID range...\n")
        downloader.download_all_pokemon(1, 1025)


if __name__ == "__main__":
    main()
