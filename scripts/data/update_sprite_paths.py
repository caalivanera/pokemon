"""
Update sprite paths in the dataset after downloading sprites from alternative sources.

This script scans the assets/sprites folders and updates the CSV to reflect
which sprites are actually available versus TBA.
"""

import pandas as pd
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "national_dex_with_variants.csv"
SPRITES_DIR = BASE_DIR / "assets" / "sprites"
ANIMATED_DIR = SPRITES_DIR / "animated"
SHINY_DIR = SPRITES_DIR / "shiny"


def update_sprite_paths():
    """Update sprite paths in CSV based on actual file existence."""
    print("=" * 70)
    print("🔄 UPDATING SPRITE PATHS IN DATASET")
    print("=" * 70)
    print()
    
    # Load dataset
    print("📂 Loading dataset...")
    df = pd.read_csv(DATA_FILE)
    print(f"   Loaded {len(df)} entries")
    print()
    
    # Statistics
    stats = {
        'static_updated': 0,
        'animated_updated': 0,
        'shiny_updated': 0,
        'total_checked': 0
    }
    
    print("🔍 Checking actual sprite file existence...")
    print()
    
    # Update each entry
    for idx, row in df.iterrows():
        stats['total_checked'] += 1
        dex_num = row['pokedex_number']
        variant_type = row['variant_type']
        
        # Determine file suffix
        if variant_type == 'base':
            suffix = ''
        else:
            suffix = f'_{variant_type}'
        
        # Check static sprite
        static_path_value = f"assets/sprites/{dex_num:03d}{suffix}.png"
        actual_static = SPRITES_DIR / f"{dex_num:03d}{suffix}.png"
        
        if actual_static.exists():
            if df.at[idx, 'sprite_path_static'] != static_path_value:
                df.at[idx, 'sprite_path_static'] = static_path_value
                stats['static_updated'] += 1
        else:
            if df.at[idx, 'sprite_path_static'] != 'TBA':
                df.at[idx, 'sprite_path_static'] = 'TBA'
        
        # Check animated sprite
        animated_path_value = f"assets/sprites/animated/{dex_num:03d}{suffix}.gif"
        actual_animated = ANIMATED_DIR / f"{dex_num:03d}{suffix}.gif"
        
        if actual_animated.exists():
            if df.at[idx, 'sprite_path_animated'] != animated_path_value:
                df.at[idx, 'sprite_path_animated'] = animated_path_value
                stats['animated_updated'] += 1
        else:
            if df.at[idx, 'sprite_path_animated'] != 'TBA':
                df.at[idx, 'sprite_path_animated'] = 'TBA'
        
        # Check shiny sprite
        shiny_path_value = f"assets/sprites/shiny/{dex_num:03d}{suffix}.png"
        actual_shiny = SHINY_DIR / f"{dex_num:03d}{suffix}.png"
        
        if actual_shiny.exists():
            if df.at[idx, 'sprite_path_shiny'] != shiny_path_value:
                df.at[idx, 'sprite_path_shiny'] = shiny_path_value
                stats['shiny_updated'] += 1
        else:
            if df.at[idx, 'sprite_path_shiny'] != 'TBA':
                df.at[idx, 'sprite_path_shiny'] = 'TBA'
    
    # Save updated dataset
    print("💾 Saving updated dataset...")
    df.to_csv(DATA_FILE, index=False)
    print(f"   Saved to: {DATA_FILE}")
    print()
    
    # Print statistics
    print("=" * 70)
    print("📊 UPDATE SUMMARY")
    print("=" * 70)
    print(f"   Total entries checked: {stats['total_checked']}")
    print(f"   Static sprite paths updated: {stats['static_updated']}")
    print(f"   Animated sprite paths updated: {stats['animated_updated']}")
    print(f"   Shiny sprite paths updated: {stats['shiny_updated']}")
    print()
    
    # Count current availability
    static_available = len(df[df['sprite_path_static'] != 'TBA'])
    animated_available = len(df[df['sprite_path_animated'] != 'TBA'])
    shiny_available = len(df[df['sprite_path_shiny'] != 'TBA'])
    
    print("📊 CURRENT SPRITE AVAILABILITY")
    print("=" * 70)
    print(f"   Static: {static_available}/{len(df)} ({static_available/len(df)*100:.1f}%)")
    print(f"   Animated: {animated_available}/{len(df)} ({animated_available/len(df)*100:.1f}%)")
    print(f"   Shiny: {shiny_available}/{len(df)} ({shiny_available/len(df)*100:.1f}%)")
    print()
    
    print("✅ SPRITE PATH UPDATE COMPLETE!")


if __name__ == "__main__":
    update_sprite_paths()
