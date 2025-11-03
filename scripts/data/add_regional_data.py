"""
Add Regional Grouping to Pokemon Dataset
Author: Copilot
Date: November 4, 2025

This script adds regional information (Kanto, Johto, etc.) to the national dex CSV
based on Pokedex number ranges.
"""

import pandas as pd
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "national_dex_with_variants.csv"

# Regional groupings based on National Dex number ranges
REGIONAL_MAPPING = {
    # Kanto (Gen 1): #001-#151
    "Kanto": (1, 151),
    # Johto (Gen 2): #152-#251
    "Johto": (152, 251),
    # Hoenn (Gen 3): #252-#386
    "Hoenn": (252, 386),
    # Sinnoh (Gen 4): #387-#493
    "Sinnoh": (387, 493),
    # Unova (Gen 5): #494-#649
    "Unova": (494, 649),
    # Kalos (Gen 6): #650-#721
    "Kalos": (650, 721),
    # Alola (Gen 7): #722-#809
    "Alola": (722, 809),
    # Galar (Gen 8): #810-#905
    "Galar": (810, 905),
    # Paldea (Gen 9): #906-#1025
    "Paldea": (906, 1025),
}

# Regional evolution methods (region-specific)
REGIONAL_EVOLUTION_METHODS = {
    "Kanto": ["Level up", "Stone evolution", "Trade", "Friendship"],
    "Johto": ["Level up", "Stone evolution", "Trade", "Friendship", "Time-based"],
    "Hoenn": ["Level up", "Stone evolution", "Trade", "Friendship", "Beauty", "Weather-based"],
    "Sinnoh": ["Level up", "Stone evolution", "Trade", "Friendship", "Location-based", "Time-based"],
    "Unova": ["Level up", "Stone evolution", "Trade", "Friendship", "Item", "Season-based"],
    "Kalos": ["Level up", "Stone evolution", "Trade", "Friendship", "Affection"],
    "Alola": ["Level up", "Stone evolution", "Trade", "Friendship", "Time-based", "Location-based"],
    "Galar": ["Level up", "Stone evolution", "Trade", "Friendship", "Location-based"],
    "Paldea": ["Level up", "Stone evolution", "Trade", "Friendship", "Collection-based"],
}

# Regional variant information
REGIONAL_VARIANTS = {
    "Alolan": ["Rattata", "Raticate", "Raichu", "Sandshrew", "Sandslash", "Vulpix", "Ninetales",
               "Diglett", "Dugtrio", "Meowth", "Persian", "Geodude", "Graveler", "Golem",
               "Grimer", "Muk", "Exeggutor", "Marowak"],
    "Galarian": ["Meowth", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Farfetch'd", "Weezing",
                 "Mr. Mime", "Articuno", "Zapdos", "Moltres", "Slowking", "Corsola", "Zigzagoon",
                 "Linoone", "Darumaka", "Darmanitan", "Yamask", "Stunfisk"],
    "Hisuian": ["Growlithe", "Arcanine", "Voltorb", "Electrode", "Typhlosion", "Qwilfish",
                "Sneasel", "Samurott", "Lilligant", "Zorua", "Zoroark", "Braviary",
                "Sliggoo", "Goodra", "Avalugg", "Decidueye"],
    "Paldean": ["Tauros", "Wooper"]
}


def get_region_from_dex_number(dex_num):
    """Determine region based on Pokedex number."""
    for region, (start, end) in REGIONAL_MAPPING.items():
        if start <= dex_num <= end:
            return region
    return "Unknown"


def get_region_from_variant(variant_name):
    """Determine region based on variant name."""
    variant_lower = variant_name.lower() if pd.notna(variant_name) else ""
    
    if "alolan" in variant_lower or "alola" in variant_lower:
        return "Alola"
    elif "galarian" in variant_lower or "galar" in variant_lower:
        return "Galar"
    elif "hisuian" in variant_lower or "hisui" in variant_lower:
        return "Hisui (Sinnoh ancient)"
    elif "paldean" in variant_lower or "paldea" in variant_lower:
        return "Paldea"
    
    return None


def add_regional_data():
    """Add regional columns to the dataset."""
    print("="*80)
    print("🗺️  ADDING REGIONAL GROUPING TO POKEMON DATASET")
    print("="*80)
    
    # Load CSV
    print(f"\n📂 Loading CSV: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, encoding='utf-8')
    print(f"✅ Loaded {len(df)} Pokemon forms")
    
    # Add region column
    print("\n🌍 Calculating regions...")
    df['region'] = df['pokedex_number'].apply(get_region_from_dex_number)
    
    # For regional variants, override with variant region
    print("🔄 Processing regional variants...")
    for idx, row in df.iterrows():
        variant_region = get_region_from_variant(row.get('variant_type', ''))
        if variant_region:
            df.at[idx, 'region_variant'] = variant_region
        else:
            df.at[idx, 'region_variant'] = df.at[idx, 'region']
    
    # Add regional Pokedex number (placeholder - would need actual data)
    df['regional_dex_number'] = df['pokedex_number']  # Simplified
    
    # Add evolution method (simplified based on generation)
    print("⚡ Adding evolution methods...")
    df['available_evolution_methods'] = df['region'].apply(
        lambda r: ", ".join(REGIONAL_EVOLUTION_METHODS.get(r, ["Level up"]))
    )
    
    # Add generation debut info
    df['debut_generation'] = df['generation']
    df['is_regional_variant'] = df['variant_type'].apply(
        lambda v: "Yes" if pd.notna(v) and any(
            reg in str(v).lower() for reg in ['alolan', 'galarian', 'hisuian', 'paldean']
        ) else "No"
    )
    
    # Statistics
    print("\n" + "="*80)
    print("📊 REGIONAL DISTRIBUTION")
    print("="*80)
    
    region_counts = df['region'].value_counts().sort_index()
    for region, count in region_counts.items():
        print(f"  {region:15} {count:4} Pokemon")
    
    # Regional variants
    print("\n🌟 Regional Variants:")
    variant_counts = df[df['is_regional_variant'] == "Yes"].groupby('region_variant').size()
    for region, count in variant_counts.items():
        print(f"  {region:15} {count:4} variants")
    
    # Save updated CSV
    backup_path = CSV_PATH.with_suffix('.backup.csv')
    print(f"\n💾 Creating backup: {backup_path}")
    df.to_csv(backup_path, index=False, encoding='utf-8')
    
    print(f"💾 Saving updated CSV: {CSV_PATH}")
    df.to_csv(CSV_PATH, index=False, encoding='utf-8')
    
    print("\n✅ Regional data added successfully!")
    print(f"📊 New columns: region, region_variant, regional_dex_number, available_evolution_methods,")
    print(f"                debut_generation, is_regional_variant")
    print("="*80)
    
    return df


if __name__ == "__main__":
    add_regional_data()
