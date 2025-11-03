"""
Comprehensive Pokemon Sprite Downloader
Downloads all sprites for base Pokemon and variants from PokeAPI

Features:
- Base Pokemon sprites (static PNG)
- Variant sprites (Mega, Regional, Gigantamax)
- Shiny variants for all forms
- Animated GIF sprites (Gen 5 style)
- Progress tracking with resume capability
- Rate limiting to respect API
- Fallback sources
"""

import requests
import pandas as pd
from pathlib import Path
import time
import json
from typing import Dict, List, Tuple, Optional
import logging

# Setup logging with UTF-8 encoding for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sprite_download.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Fix console encoding for Windows
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# ==================== CONFIGURATION ====================

# API Endpoints
POKEAPI_BASE = "https://pokeapi.co/api/v2"
SPRITE_SOURCES = {
    'official_artwork': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png',
    'official_artwork_shiny': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{id}.png',
    'home': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{id}.png',
    'home_shiny': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/{id}.png',
    'animated': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{id}.gif',
    'animated_shiny': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/shiny/{id}.gif',
}

# Directories
BASE_DIR = Path(__file__).parent
SPRITES_DIR = BASE_DIR / 'assets' / 'sprites'
ANIMATED_DIR = BASE_DIR / 'assets' / 'animated'
ICONS_DIR = BASE_DIR / 'assets' / 'icons'

# Progress tracking
PROGRESS_FILE = BASE_DIR / 'download_progress.json'

# Rate limiting
RATE_LIMIT_DELAY = 0.5  # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 15

# ==================== VARIANT MAPPINGS ====================

# PokeAPI uses specific IDs for variants
# Format: pokemon_name: pokeapi_id
POKEAPI_VARIANT_IDS = {
    # Mega Evolutions
    'venusaur-mega': 10033,
    'charizard-mega-x': 10034,
    'charizard-mega-y': 10035,
    'blastoise-mega': 10036,
    'alakazam-mega': 10037,
    'gengar-mega': 10038,
    'kangaskhan-mega': 10039,
    'pinsir-mega': 10040,
    'gyarados-mega': 10041,
    'aerodactyl-mega': 10042,
    'mewtwo-mega-x': 10043,
    'mewtwo-mega-y': 10044,
    'ampharos-mega': 10045,
    'scizor-mega': 10046,
    'heracross-mega': 10047,
    'houndoom-mega': 10048,
    'tyranitar-mega': 10049,
    'blaziken-mega': 10050,
    'gardevoir-mega': 10051,
    'mawile-mega': 10052,
    'aggron-mega': 10053,
    'medicham-mega': 10054,
    'manectric-mega': 10055,
    'banette-mega': 10056,
    'absol-mega': 10057,
    'garchomp-mega': 10058,
    'lucario-mega': 10059,
    'abomasnow-mega': 10060,
    'sceptile-mega': 10065,
    'swampert-mega': 10064,
    'sableye-mega': 10066,
    'sharpedo-mega': 10070,
    'camerupt-mega': 10087,
    'altaria-mega': 10067,
    'glalie-mega': 10068,
    'salamence-mega': 10069,
    'metagross-mega': 10071,
    'latias-mega': 10072,
    'latios-mega': 10073,
    'rayquaza-mega': 10079,
    'lopunny-mega': 10088,
    'gallade-mega': 10068,
    'audino-mega': 10069,
    'diancie-mega': 10101,
    'pidgeot-mega': 10073,
    'beedrill-mega': 10090,
    'slowbro-mega': 10071,
    'steelix-mega': 10072,
    
    # Alolan Forms
    'rattata-alola': 10091,
    'raticate-alola': 10092,
    'raichu-alola': 10100,
    'sandshrew-alola': 10103,
    'sandslash-alola': 10104,
    'vulpix-alola': 10105,
    'ninetales-alola': 10106,
    'diglett-alola': 10107,
    'dugtrio-alola': 10108,
    'meowth-alola': 10109,
    'persian-alola': 10110,
    'geodude-alola': 10111,
    'graveler-alola': 10112,
    'golem-alola': 10113,
    'grimer-alola': 10114,
    'muk-alola': 10115,
    'exeggutor-alola': 10116,
    'marowak-alola': 10117,
    
    # Galarian Forms
    'meowth-galar': 10161,
    'ponyta-galar': 10162,
    'rapidash-galar': 10163,
    'slowpoke-galar': 10164,
    'slowbro-galar': 10165,
    'farfetchd-galar': 10166,
    'weezing-galar': 10167,
    'mr-mime-galar': 10168,
    'articuno-galar': 10169,
    'zapdos-galar': 10170,
    'moltres-galar': 10171,
    'slowking-galar': 10172,
    'corsola-galar': 10173,
    'zigzagoon-galar': 10174,
    'linoone-galar': 10175,
    'darumaka-galar': 10176,
    'darmanitan-galar': 10177,
    'yamask-galar': 10178,
    'stunfisk-galar': 10179,
    
    # Gigantamax (special case - use base ID with gmax flag)
    # These don't have separate sprite IDs in standard PokeAPI
}

# ==================== UTILITY FUNCTIONS ====================

def create_directories():
    """Ensure all required directories exist"""
    SPRITES_DIR.mkdir(parents=True, exist_ok=True)
    ANIMATED_DIR.mkdir(parents=True, exist_ok=True)
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"✓ Created directories: {SPRITES_DIR}, {ANIMATED_DIR}")


def load_progress() -> Dict:
    """Load download progress from file"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {
        'base_sprites': [],
        'variant_sprites': [],
        'shiny_sprites': [],
        'animated_sprites': [],
        'failed': []
    }


def save_progress(progress: Dict):
    """Save download progress to file"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def download_image(url: str, save_path: Path, retries: int = MAX_RETRIES) -> bool:
    """
    Download image from URL with retry logic
    
    Args:
        url: Image URL
        save_path: Path to save image
        retries: Number of retry attempts
        
    Returns:
        True if successful, False otherwise
    """
    if save_path.exists():
        logger.debug(f"⏭️  Skipping (already exists): {save_path.name}")
        return True
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"✓ Downloaded: {save_path.name}")
                time.sleep(RATE_LIMIT_DELAY)
                return True
            elif response.status_code == 404:
                logger.warning(f"✗ Not found (404): {url}")
                return False
            else:
                logger.warning(f"⚠️  HTTP {response.status_code}: {url}")
        except requests.exceptions.Timeout:
            logger.warning(f"⏱️  Timeout (attempt {attempt + 1}/{retries}): {url}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️  Error (attempt {attempt + 1}/{retries}): {e}")
        
        if attempt < retries - 1:
            time.sleep(RATE_LIMIT_DELAY * 2)  # Longer delay on retry
    
    return False


# ==================== MAIN DOWNLOAD FUNCTIONS ====================

def download_base_sprites(df: pd.DataFrame, progress: Dict) -> Tuple[int, int]:
    """
    Download static sprites for base Pokemon
    
    Returns:
        (success_count, failure_count)
    """
    logger.info("\n" + "="*60)
    logger.info("📥 DOWNLOADING BASE POKEMON SPRITES")
    logger.info("="*60)
    
    success = 0
    failed = 0
    
    base_pokemon = df[df['variant_type'] == 'base']
    total = len(base_pokemon)
    
    for idx, row in base_pokemon.iterrows():
        dex_num = int(row['pokedex_number'])
        filename = f"{dex_num:03d}.png"
        save_path = SPRITES_DIR / filename
        
        # Check if already downloaded
        if filename in progress['base_sprites']:
            logger.debug(f"⏭️  [{idx+1}/{total}] Already downloaded: {filename}")
            success += 1
            continue
        
        logger.info(f"[{idx+1}/{total}] Downloading: {row['name']} ({dex_num})")
        
        # Try official artwork first, then home
        url_artwork = SPRITE_SOURCES['official_artwork'].format(id=dex_num)
        url_home = SPRITE_SOURCES['home'].format(id=dex_num)
        
        if download_image(url_artwork, save_path):
            progress['base_sprites'].append(filename)
            success += 1
        elif download_image(url_home, save_path):
            progress['base_sprites'].append(filename)
            success += 1
        else:
            logger.error(f"✗ Failed: {row['name']}")
            progress['failed'].append({
                'type': 'base',
                'name': row['name'],
                'id': dex_num
            })
            failed += 1
        
        # Save progress every 50 downloads
        if (idx + 1) % 50 == 0:
            save_progress(progress)
            logger.info(f"💾 Progress saved: {success}/{total} completed")
    
    save_progress(progress)
    logger.info(f"\n✅ Base sprites: {success} successful, {failed} failed")
    return success, failed


def download_variant_sprites(df: pd.DataFrame, progress: Dict) -> Tuple[int, int]:
    """
    Download sprites for Pokemon variants (Mega, Regional, Gigantamax)
    
    Returns:
        (success_count, failure_count)
    """
    logger.info("\n" + "="*60)
    logger.info("🔥 DOWNLOADING VARIANT SPRITES")
    logger.info("="*60)
    
    success = 0
    failed = 0
    
    variants = df[df['variant_type'] != 'base']
    total = len(variants)
    
    for idx, row in variants.iterrows():
        base_id = int(row['base_pokemon_id'])
        variant_type = row['variant_type']
        form_name = row['form_name']
        
        # Generate filename
        variant_suffix = variant_type.replace('-', '_')
        filename = f"{base_id:03d}_{variant_suffix}.png"
        save_path = SPRITES_DIR / filename
        
        # Check if already downloaded
        if filename in progress['variant_sprites']:
            logger.debug(f"⏭️  [{idx+1}/{total}] Already downloaded: {filename}")
            success += 1
            continue
        
        logger.info(f"[{idx+1}/{total}] Downloading: {form_name}")
        
        # Try to find PokeAPI ID for this variant
        variant_key = None
        name_lower = form_name.lower().replace(' ', '-')
        
        # Try exact match
        if name_lower in POKEAPI_VARIANT_IDS:
            variant_key = name_lower
        else:
            # Try variations
            for key in POKEAPI_VARIANT_IDS.keys():
                if form_name.lower() in key or key in form_name.lower():
                    variant_key = key
                    break
        
        if variant_key:
            variant_id = POKEAPI_VARIANT_IDS[variant_key]
            url = SPRITE_SOURCES['official_artwork'].format(id=variant_id)
            
            if download_image(url, save_path):
                progress['variant_sprites'].append(filename)
                success += 1
                continue
        
        # Fallback: try constructing URL from base ID
        logger.warning(f"⚠️  No PokeAPI ID found for: {form_name}")
        logger.warning(f"    Using base sprite as placeholder")
        
        # Copy base sprite as placeholder
        base_sprite = SPRITES_DIR / f"{base_id:03d}.png"
        if base_sprite.exists():
            import shutil
            shutil.copy(base_sprite, save_path)
            logger.info(f"📋 Copied base sprite as placeholder: {filename}")
            progress['variant_sprites'].append(filename)
            success += 1
        else:
            logger.error(f"✗ Failed: {form_name} (no base sprite)")
            progress['failed'].append({
                'type': 'variant',
                'name': form_name,
                'id': base_id,
                'variant': variant_type
            })
            failed += 1
        
        # Save progress every 20 downloads
        if (idx + 1) % 20 == 0:
            save_progress(progress)
    
    save_progress(progress)
    logger.info(f"\n✅ Variant sprites: {success} successful, {failed} failed")
    return success, failed


def download_shiny_sprites(df: pd.DataFrame, progress: Dict) -> Tuple[int, int]:
    """
    Download shiny variants for all Pokemon
    
    Returns:
        (success_count, failure_count)
    """
    logger.info("\n" + "="*60)
    logger.info("✨ DOWNLOADING SHINY SPRITES")
    logger.info("="*60)
    
    success = 0
    failed = 0
    total = len(df)
    
    for idx, row in df.iterrows():
        dex_num = int(row['pokedex_number'])
        variant_type = row['variant_type']
        
        # Generate filename
        if variant_type == 'base':
            filename = f"{dex_num:03d}_shiny.png"
        else:
            variant_suffix = variant_type.replace('-', '_')
            filename = f"{dex_num:03d}_{variant_suffix}_shiny.png"
        
        save_path = SPRITES_DIR / filename
        
        # Check if already downloaded
        if filename in progress['shiny_sprites']:
            logger.debug(f"⏭️  [{idx+1}/{total}] Already downloaded: {filename}")
            success += 1
            continue
        
        logger.info(f"[{idx+1}/{total}] Downloading shiny: {row['name']}")
        
        # Try shiny official artwork
        url = SPRITE_SOURCES['official_artwork_shiny'].format(id=dex_num)
        
        if download_image(url, save_path):
            progress['shiny_sprites'].append(filename)
            success += 1
        else:
            # Try home shiny as fallback
            url_home = SPRITE_SOURCES['home_shiny'].format(id=dex_num)
            if download_image(url_home, save_path):
                progress['shiny_sprites'].append(filename)
                success += 1
            else:
                logger.warning(f"⚠️  Shiny not available: {row['name']}")
                failed += 1
        
        # Save progress every 100 downloads
        if (idx + 1) % 100 == 0:
            save_progress(progress)
            logger.info(f"💾 Progress saved: {success}/{total} completed")
    
    save_progress(progress)
    logger.info(f"\n✅ Shiny sprites: {success} successful, {failed} failed")
    return success, failed


def download_animated_sprites(df: pd.DataFrame, progress: Dict) -> Tuple[int, int]:
    """
    Download animated GIF sprites (Gen 5 style)
    
    Returns:
        (success_count, failure_count)
    """
    logger.info("\n" + "="*60)
    logger.info("🎬 DOWNLOADING ANIMATED SPRITES")
    logger.info("="*60)
    
    success = 0
    failed = 0
    
    # Only download for base Pokemon (variants rarely have animations)
    base_pokemon = df[df['variant_type'] == 'base']
    total = len(base_pokemon)
    
    for idx, row in base_pokemon.iterrows():
        dex_num = int(row['pokedex_number'])
        filename = f"{dex_num:03d}.gif"
        save_path = ANIMATED_DIR / filename
        
        # Check if already downloaded
        if filename in progress['animated_sprites']:
            logger.debug(f"⏭️  [{idx+1}/{total}] Already downloaded: {filename}")
            success += 1
            continue
        
        logger.info(f"[{idx+1}/{total}] Downloading animated: {row['name']}")
        
        url = SPRITE_SOURCES['animated'].format(id=dex_num)
        
        if download_image(url, save_path):
            progress['animated_sprites'].append(filename)
            success += 1
        else:
            logger.warning(f"⚠️  Animated sprite not available: {row['name']}")
            failed += 1
        
        # Save progress every 100 downloads
        if (idx + 1) % 100 == 0:
            save_progress(progress)
            logger.info(f"💾 Progress saved: {success}/{total} completed")
    
    save_progress(progress)
    logger.info(f"\n✅ Animated sprites: {success} successful, {failed} failed")
    return success, failed


# ==================== MAIN EXECUTION ====================

def main():
    """Main execution function"""
    print("=" * 70)
    print("   COMPREHENSIVE POKEMON SPRITE DOWNLOADER")
    print("=" * 70)
    print()
    
    # Setup
    create_directories()
    progress = load_progress()
    
    # Load variant data
    logger.info("📂 Loading Pokemon data...")
    csv_path = BASE_DIR / 'data' / 'national_dex_with_variants.csv'
    df = pd.read_csv(csv_path)
    logger.info(f"✓ Loaded {len(df)} Pokemon entries")
    
    # Download sprites
    total_success = 0
    total_failed = 0
    
    # 1. Base sprites
    success, failed = download_base_sprites(df, progress)
    total_success += success
    total_failed += failed
    
    # 2. Variant sprites
    success, failed = download_variant_sprites(df, progress)
    total_success += success
    total_failed += failed
    
    # 3. Shiny sprites (optional - can be skipped for speed)
    print("\n" + "="*70)
    choice = input("Download shiny sprites? This will take a while. (y/n): ")
    if choice.lower() == 'y':
        success, failed = download_shiny_sprites(df, progress)
        total_success += success
        total_failed += failed
    
    # 4. Animated sprites (optional)
    print("\n" + "="*70)
    choice = input("Download animated sprites? This will take a while. (y/n): ")
    if choice.lower() == 'y':
        success, failed = download_animated_sprites(df, progress)
        total_success += success
        total_failed += failed
    
    # Final summary
    print("\n" + "=" * 70)
    print("   📊 DOWNLOAD SUMMARY")
    print("=" * 70)
    print(f"✅ Total successful: {total_success}")
    print(f"✗ Total failed: {total_failed}")
    print(f"📁 Base sprites: {len(progress['base_sprites'])}")
    print(f"🔥 Variant sprites: {len(progress['variant_sprites'])}")
    print(f"✨ Shiny sprites: {len(progress['shiny_sprites'])}")
    print(f"🎬 Animated sprites: {len(progress['animated_sprites'])}")
    
    if progress['failed']:
        print(f"\n⚠️  {len(progress['failed'])} failed downloads:")
        for fail in progress['failed'][:10]:  # Show first 10
            print(f"   - {fail['type']}: {fail['name']} (#{fail['id']})")
        if len(progress['failed']) > 10:
            print(f"   ... and {len(progress['failed']) - 10} more")
    
    print("\n✅ Download complete!")
    print(f"📊 Progress saved to: {PROGRESS_FILE}")
    print(f"📁 Sprites saved to: {SPRITES_DIR}")
    print(f"🎬 Animated saved to: {ANIMATED_DIR}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        print("Progress has been saved. Run again to resume.")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
