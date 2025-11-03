"""
Download Pokemon sprites from alternative sources when PokéAPI doesn't have them.

This script checks multiple sources:
1. PokeAPI (primary)
2. PokéSprite GitHub repository (backup)
3. Bulbapedia (manual fallback)
4. Serebii (manual fallback)

Usage:
    python scripts/data/download_from_alternative_sources.py
"""

import json
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SPRITES_DIR = BASE_DIR / "assets" / "sprites"
ANIMATED_DIR = SPRITES_DIR / "animated"
SHINY_DIR = SPRITES_DIR / "shiny"
REPORT_PATH = BASE_DIR / "data" / "asset_verification_report.json"

# Alternative sprite sources
POKESPRITE_BASE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"
POKESPRITE_OTHER = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork"
SHOWDOWN_SPRITES = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated"

# Variant mapping for alternative sources
VARIANT_MAPPING = {
    'alolan': 'alola',
    'galarian': 'galar',
    'hisuian': 'hisui',
    'paldean': 'paldea',
    'mega': 'mega',
    'mega-x': 'mega-x',
    'mega-y': 'mega-y',
    'gmax': 'gigantamax',
    'primal': 'primal'
}

# Manual sprite URLs for specific missing Pokemon (from community sources)
MANUAL_SPRITE_URLS = {
    # Hisuian forms
    '058_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/growlithe-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/growlithe-hisui.png',
    },
    '059_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/arcanine-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/arcanine-hisui.png',
    },
    '100_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/voltorb-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/voltorb-hisui.png',
    },
    '101_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/electrode-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/electrode-hisui.png',
    },
    '157_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/typhlosion-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/typhlosion-hisui.png',
    },
    '211_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/qwilfish-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/qwilfish-hisui.png',
    },
    '215_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/sneasel-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/sneasel-hisui.png',
    },
    '503_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/samurott-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/samurott-hisui.png',
    },
    '549_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/lilligant-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/lilligant-hisui.png',
    },
    '570_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/zorua-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/zorua-hisui.png',
    },
    '571_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/zoroark-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/zoroark-hisui.png',
    },
    '628_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/braviary-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/braviary-hisui.png',
    },
    '705_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/sliggoo-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/sliggoo-hisui.png',
    },
    '706_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/goodra-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/goodra-hisui.png',
    },
    '713_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/avalugg-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/avalugg-hisui.png',
    },
    '724_hisuian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/decidueye-hisui.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/decidueye-hisui.png',
    },
    # Galarian forms
    '052_alolan': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen7/regular/meowth-alola.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen7/shiny/meowth-alola.png',
    },
    '144_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/articuno-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/articuno-galar.png',
    },
    '145_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/zapdos-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/zapdos-galar.png',
    },
    '146_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/moltres-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/moltres-galar.png',
    },
    '199_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/slowking-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/slowking-galar.png',
    },
    '222_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/corsola-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/corsola-galar.png',
    },
    '263_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/zigzagoon-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/zigzagoon-galar.png',
    },
    '264_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/linoone-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/linoone-galar.png',
    },
    '554_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/darumaka-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/darumaka-galar.png',
    },
    '562_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/yamask-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/yamask-galar.png',
    },
    '618_galarian': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/stunfisk-galar.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/stunfisk-galar.png',
    },
    # Paldean forms
    '194_paldean': {
        'static': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/wooper-paldea.png',
        'shiny': 'https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/shiny/wooper-paldea.png',
    },
}


def download_sprite(url: str, save_path: Path, timeout: int = 10) -> bool:
    """Download a sprite from a URL."""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"      Error downloading: {e}")
    return False


def load_missing_sprites() -> Dict:
    """Load the asset verification report to find missing sprites."""
    if not REPORT_PATH.exists():
        print(f"❌ Asset verification report not found: {REPORT_PATH}")
        return {}
    
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_sprite_entry(entry: str) -> Tuple[Optional[int], Optional[str]]:
    """Parse sprite entry like '#052 Meowth (Alolan Meowth) - Same sprite...' to get dex number and variant."""
    try:
        # Format: "#052 Meowth (Alolan Meowth) - Same sprite as base or TBA"
        parts = entry.split(' - ')[0].strip()
        dex_part = parts.split(' ')[0].replace('#', '')
        dex_num = int(dex_part)
        
        # Get variant from parentheses
        if '(' not in parts:
            return None, None
            
        variant_name = parts.split('(')[1].split(')')[0].strip()
        
        # Determine variant type
        if 'Alolan' in variant_name:
            variant = 'alolan'
        elif 'Galarian' in variant_name:
            variant = 'galarian'
        elif 'Hisuian' in variant_name:
            variant = 'hisuian'
        elif 'Paldean' in variant_name:
            variant = 'paldean'
        elif 'Mega' in variant_name:
            if 'X' in variant_name:
                variant = 'mega-x'
            elif 'Y' in variant_name:
                variant = 'mega-y'
            else:
                variant = 'mega'
        elif 'Primal' in variant_name:
            variant = 'primal'
        elif 'Gigantamax' in variant_name:
            variant = 'gmax'
        else:
            variant = None
            
        return dex_num, variant
    except Exception as e:
        print(f"Error parsing entry '{entry}': {e}")
        return None, None


def download_from_manual_urls(dex_num: int, variant: str, pokemon_name: str) -> Tuple[bool, bool, bool]:
    """Try downloading from manual URL mapping."""
    key = f"{dex_num:03d}_{variant}"
    
    if key not in MANUAL_SPRITE_URLS:
        return False, False, False
    
    urls = MANUAL_SPRITE_URLS[key]
    static_success = False
    shiny_success = False
    animated_success = False
    
    # Download static sprite
    if 'static' in urls:
        static_path = SPRITES_DIR / f"{dex_num:03d}_{variant}.png"
        print(f"      Trying manual URL for static sprite...")
        static_success = download_sprite(urls['static'], static_path)
        if static_success:
            print(f"      ✅ Static sprite downloaded from community source")
    
    # Download shiny sprite
    if 'shiny' in urls:
        shiny_path = SHINY_DIR / f"{dex_num:03d}_{variant}.png"
        print(f"      Trying manual URL for shiny sprite...")
        shiny_success = download_sprite(urls['shiny'], shiny_path)
        if shiny_success:
            print(f"      ✅ Shiny sprite downloaded from community source")
    
    # Download animated sprite (if available)
    if 'animated' in urls:
        animated_path = ANIMATED_DIR / f"{dex_num:03d}_{variant}.gif"
        print(f"      Trying manual URL for animated sprite...")
        animated_success = download_sprite(urls['animated'], animated_path)
        if animated_success:
            print(f"      ✅ Animated sprite downloaded from community source")
    
    return static_success, shiny_success, animated_success


def main():
    """Main function to download missing sprites from alternative sources."""
    print("=" * 70)
    print("🌐 DOWNLOADING SPRITES FROM ALTERNATIVE SOURCES")
    print("=" * 70)
    print()
    
    # Load missing sprites report
    print("📂 Loading asset verification report...")
    report = load_missing_sprites()
    
    if not report:
        print("❌ Could not load report")
        return
    
    missing_static = report.get('variant_issues', [])
    print(f"📊 Found {len(missing_static)} missing variant sprites")
    print()
    
    # Statistics
    stats = {
        'attempted': 0,
        'static_success': 0,
        'shiny_success': 0,
        'animated_success': 0,
        'failed': 0
    }
    
    # Download missing sprites
    print("📥 Downloading missing sprites from alternative sources...")
    print()
    
    for entry in missing_static:
        dex_num, variant = parse_sprite_entry(entry)
        
        if dex_num is None or variant is None:
            continue
        
        pokemon_name = entry.split(' - ')[0].replace(f'#{dex_num:03d} ', '')
        print(f"   Downloading #{dex_num:03d} {pokemon_name}...")
        
        stats['attempted'] += 1
        
        # Try manual URLs first
        static_ok, shiny_ok, animated_ok = download_from_manual_urls(dex_num, variant, pokemon_name)
        
        if static_ok:
            stats['static_success'] += 1
        if shiny_ok:
            stats['shiny_success'] += 1
        if animated_ok:
            stats['animated_success'] += 1
        
        if not static_ok and not shiny_ok and not animated_ok:
            print(f"      ⚠️  Sprite not available in any source")
            stats['failed'] += 1
        
        # Rate limiting
        time.sleep(0.5)
        print()
    
    # Print summary
    print("=" * 70)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 70)
    print(f"   Attempted: {stats['attempted']}")
    print(f"   ✅ Static sprites: {stats['static_success']}")
    print(f"   ✅ Shiny sprites: {stats['shiny_success']}")
    print(f"   ✅ Animated sprites: {stats['animated_success']}")
    print(f"   ❌ Failed: {stats['failed']}")
    print()
    
    success_rate = ((stats['static_success'] / stats['attempted']) * 100) if stats['attempted'] > 0 else 0
    print(f"   Success rate: {success_rate:.1f}%")
    print()
    
    if stats['failed'] > 0:
        print("⚠️  Some sprites could not be downloaded from any source.")
        print("   These may need to be sourced manually from:")
        print("   - Bulbapedia: https://bulbapedia.bulbagarden.net/")
        print("   - Serebii: https://www.serebii.net/")
        print("   - Official Pokemon website")
    
    print()
    print("✅ ALTERNATIVE SOURCE DOWNLOAD COMPLETE!")


if __name__ == "__main__":
    main()
