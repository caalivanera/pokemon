"""
Download Pokemon Type Icons and Create Color Mapping
Author: Copilot
Date: November 4, 2025

This script downloads official Pokemon type icons from multiple sources
and creates a comprehensive color mapping for all 18 Pokemon types.
"""

import os
import json
import time
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
TYPES_DIR = PROJECT_ROOT / "assets" / "types"
DATA_DIR = PROJECT_ROOT / "data"

# Ensure directories exist
TYPES_DIR.mkdir(parents=True, exist_ok=True)

# Pokemon type data with official colors
POKEMON_TYPES = {
    "normal": {
        "color": "#A8A878",
        "color_dark": "#6D6D4E",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/normal.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/1.png"
        ]
    },
    "fire": {
        "color": "#F08030",
        "color_dark": "#9C531F",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/fire.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/10.png"
        ]
    },
    "water": {
        "color": "#6890F0",
        "color_dark": "#445E9C",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/water.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/11.png"
        ]
    },
    "electric": {
        "color": "#F8D030",
        "color_dark": "#A1871F",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/electric.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/13.png"
        ]
    },
    "grass": {
        "color": "#78C850",
        "color_dark": "#4E8234",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/grass.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/12.png"
        ]
    },
    "ice": {
        "color": "#98D8D8",
        "color_dark": "#638D8D",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/ice.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/15.png"
        ]
    },
    "fighting": {
        "color": "#C03028",
        "color_dark": "#7D1F1A",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/fighting.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/2.png"
        ]
    },
    "poison": {
        "color": "#A040A0",
        "color_dark": "#682A68",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/poison.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/4.png"
        ]
    },
    "ground": {
        "color": "#E0C068",
        "color_dark": "#927D44",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/ground.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/5.png"
        ]
    },
    "flying": {
        "color": "#A890F0",
        "color_dark": "#6D5E9C",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/flying.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/3.png"
        ]
    },
    "psychic": {
        "color": "#F85888",
        "color_dark": "#A13959",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/psychic.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/14.png"
        ]
    },
    "bug": {
        "color": "#A8B820",
        "color_dark": "#6D7815",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/bug.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/7.png"
        ]
    },
    "rock": {
        "color": "#B8A038",
        "color_dark": "#786824",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/rock.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/6.png"
        ]
    },
    "ghost": {
        "color": "#705898",
        "color_dark": "#493963",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/ghost.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/8.png"
        ]
    },
    "dragon": {
        "color": "#7038F8",
        "color_dark": "#4924A1",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/dragon.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/16.png"
        ]
    },
    "dark": {
        "color": "#705848",
        "color_dark": "#49392F",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/dark.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/17.png"
        ]
    },
    "steel": {
        "color": "#B8B8D0",
        "color_dark": "#787887",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/steel.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/9.png"
        ]
    },
    "fairy": {
        "color": "#EE99AC",
        "color_dark": "#9B6470",
        "icon_sources": [
            "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/type/fairy.png",
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/18.png"
        ]
    }
}


def download_image(url, save_path, timeout=10, resize=None):
    """Download an image from URL and optionally resize it."""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Resize if requested
            if resize:
                img = img.resize(resize, Image.Resampling.LANCZOS)
            
            # Save
            img.save(save_path, 'PNG', optimize=True)
            return True
    except Exception as e:
        print(f"  ❌ Failed to download from {url}: {e}")
    return False


def download_type_icon(type_name, type_data):
    """Download type icon from multiple sources with fallbacks."""
    # Try each source
    for i, source_url in enumerate(type_data['icon_sources']):
        # Original size
        original_path = TYPES_DIR / f"{type_name}.png"
        if download_image(source_url, original_path):
            print(f"  ✅ Downloaded {type_name} icon (original)")
            
            # Create multiple sizes
            try:
                # 32x32 (small)
                small_path = TYPES_DIR / f"{type_name}_32.png"
                download_image(source_url, small_path, resize=(32, 32))
                print(f"  ✅ Created {type_name} icon (32x32)")
                
                # 64x64 (medium)
                medium_path = TYPES_DIR / f"{type_name}_64.png"
                download_image(source_url, medium_path, resize=(64, 64))
                print(f"  ✅ Created {type_name} icon (64x64)")
                
                # 128x128 (large)
                large_path = TYPES_DIR / f"{type_name}_128.png"
                download_image(source_url, large_path, resize=(128, 128))
                print(f"  ✅ Created {type_name} icon (128x128)")
                
                return True
            except Exception as e:
                print(f"  ⚠️  Error creating sized icons: {e}")
                return True  # Original was downloaded at least
        
        # Try next source
        if i < len(type_data['icon_sources']) - 1:
            print(f"  ⚠️  Source {i+1} failed, trying source {i+2}...")
            time.sleep(0.3)
    
    return False


def create_color_mapping():
    """Create JSON file with type colors."""
    color_mapping = {}
    
    for type_name, type_data in POKEMON_TYPES.items():
        color_mapping[type_name] = {
            "name": type_name.capitalize(),
            "color": type_data["color"],
            "color_dark": type_data["color_dark"],
            "icon_path": f"assets/types/{type_name}.png",
            "icon_32": f"assets/types/{type_name}_32.png",
            "icon_64": f"assets/types/{type_name}_64.png",
            "icon_128": f"assets/types/{type_name}_128.png"
        }
    
    # Save to JSON
    json_path = DATA_DIR / "type_colors.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(color_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Color mapping saved to: {json_path}")
    return color_mapping


def create_type_effectiveness_data():
    """Create type effectiveness (strengths/weaknesses) data."""
    # Type effectiveness matrix (attacking type -> defending type)
    effectiveness = {
        "normal": {
            "super_effective": [],
            "not_very_effective": ["rock", "steel"],
            "no_effect": ["ghost"]
        },
        "fire": {
            "super_effective": ["grass", "ice", "bug", "steel"],
            "not_very_effective": ["fire", "water", "rock", "dragon"],
            "no_effect": []
        },
        "water": {
            "super_effective": ["fire", "ground", "rock"],
            "not_very_effective": ["water", "grass", "dragon"],
            "no_effect": []
        },
        "electric": {
            "super_effective": ["water", "flying"],
            "not_very_effective": ["electric", "grass", "dragon"],
            "no_effect": ["ground"]
        },
        "grass": {
            "super_effective": ["water", "ground", "rock"],
            "not_very_effective": ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"],
            "no_effect": []
        },
        "ice": {
            "super_effective": ["grass", "ground", "flying", "dragon"],
            "not_very_effective": ["fire", "water", "ice", "steel"],
            "no_effect": []
        },
        "fighting": {
            "super_effective": ["normal", "ice", "rock", "dark", "steel"],
            "not_very_effective": ["poison", "flying", "psychic", "bug", "fairy"],
            "no_effect": ["ghost"]
        },
        "poison": {
            "super_effective": ["grass", "fairy"],
            "not_very_effective": ["poison", "ground", "rock", "ghost"],
            "no_effect": ["steel"]
        },
        "ground": {
            "super_effective": ["fire", "electric", "poison", "rock", "steel"],
            "not_very_effective": ["grass", "bug"],
            "no_effect": ["flying"]
        },
        "flying": {
            "super_effective": ["grass", "fighting", "bug"],
            "not_very_effective": ["electric", "rock", "steel"],
            "no_effect": []
        },
        "psychic": {
            "super_effective": ["fighting", "poison"],
            "not_very_effective": ["psychic", "steel"],
            "no_effect": ["dark"]
        },
        "bug": {
            "super_effective": ["grass", "psychic", "dark"],
            "not_very_effective": ["fire", "fighting", "poison", "flying", "ghost", "steel", "fairy"],
            "no_effect": []
        },
        "rock": {
            "super_effective": ["fire", "ice", "flying", "bug"],
            "not_very_effective": ["fighting", "ground", "steel"],
            "no_effect": []
        },
        "ghost": {
            "super_effective": ["psychic", "ghost"],
            "not_very_effective": ["dark"],
            "no_effect": ["normal"]
        },
        "dragon": {
            "super_effective": ["dragon"],
            "not_very_effective": ["steel"],
            "no_effect": ["fairy"]
        },
        "dark": {
            "super_effective": ["psychic", "ghost"],
            "not_very_effective": ["fighting", "dark", "fairy"],
            "no_effect": []
        },
        "steel": {
            "super_effective": ["ice", "rock", "fairy"],
            "not_very_effective": ["fire", "water", "electric", "steel"],
            "no_effect": []
        },
        "fairy": {
            "super_effective": ["fighting", "dragon", "dark"],
            "not_very_effective": ["fire", "poison", "steel"],
            "no_effect": []
        }
    }
    
    # Save to JSON
    json_path = DATA_DIR / "type_effectiveness.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(effectiveness, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Type effectiveness data saved to: {json_path}")
    return effectiveness


def main():
    """Main execution function."""
    print("=" * 80)
    print("🎨 POKEMON TYPE ICONS & COLOR MAPPING DOWNLOADER")
    print("=" * 80)
    print(f"\n📁 Assets directory: {TYPES_DIR}")
    print(f"📊 Types to download: {len(POKEMON_TYPES)}\n")
    
    # Statistics
    successful_downloads = 0
    failed_downloads = []
    
    # Download each type icon
    for type_name, type_data in POKEMON_TYPES.items():
        print(f"⬇️  Downloading {type_name.upper()} type icon...")
        
        if download_type_icon(type_name, type_data):
            successful_downloads += 1
        else:
            failed_downloads.append(type_name)
            print(f"  ❌ All sources failed for {type_name}")
        
        # Rate limiting
        time.sleep(0.3)
    
    # Create color mapping
    print("\n" + "=" * 80)
    print("🎨 Creating color mapping...")
    print("=" * 80)
    color_mapping = create_color_mapping()
    
    # Create type effectiveness data
    print("\n" + "=" * 80)
    print("⚔️  Creating type effectiveness data...")
    print("=" * 80)
    effectiveness = create_type_effectiveness_data()
    
    # Final statistics
    print("\n" + "=" * 80)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully downloaded: {successful_downloads}/{len(POKEMON_TYPES)} types")
    print(f"❌ Failed downloads: {len(failed_downloads)}")
    
    if failed_downloads:
        print(f"\nFailed types: {', '.join(failed_downloads)}")
    
    # File counts
    icon_files = list(TYPES_DIR.glob("*.png"))
    print(f"\n📁 Total icon files created: {len(icon_files)}")
    print(f"📄 Color mapping file: {DATA_DIR / 'type_colors.json'}")
    print(f"⚔️  Type effectiveness file: {DATA_DIR / 'type_effectiveness.json'}")
    
    print("\n✅ Type icons and color mapping complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
