"""
Script to add all regional forms and Mega forms from Pokemon Legends Z-A
to the National Dex dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Regional Forms Data
HISUIAN_FORMS = [
    # Pokedex#, Name, Type1, Type2, HP, Atk, Def, SpA, SpD, Spe
    (58, "Hisuian Growlithe", "Fire", "Rock", 60, 75, 45, 65, 50, 55),
    (59, "Hisuian Arcanine", "Fire", "Rock", 95, 115, 80, 95, 80, 90),
    (100, "Hisuian Voltorb", "Electric", "Grass", 40, 30, 50, 55, 55, 100),
    (101, "Hisuian Electrode", "Electric", "Grass", 60, 50, 70, 80, 80, 150),
    (157, "Hisuian Typhlosion", "Fire", "Ghost", 73, 84, 78, 119, 85, 95),
    (211, "Hisuian Qwilfish", "Dark", "Poison", 65, 95, 85, 55, 55, 85),
    (215, "Hisuian Sneasel", "Fighting", "Poison", 55, 95, 55, 35, 75, 115),
    (503, "Hisuian Samurott", "Water", "Dark", 90, 108, 80, 100, 65, 85),
    (549, "Hisuian Lilligant", "Grass", "Fighting", 70, 105, 75, 50, 75, 105),
    (550, "Hisuian Basculin", "Water", None, 120, 112, 65, 80, 75, 78),
    (554, "Hisuian Zorua", "Normal", "Ghost", 35, 60, 40, 85, 40, 70),
    (555, "Hisuian Zoroark", "Normal", "Ghost", 55, 100, 60, 125, 60, 110),
    (570, "Hisuian Braviary", "Psychic", "Flying", 110, 83, 70, 112, 70, 65),
    (571, "Hisuian Sliggoo", "Steel", "Dragon", 58, 75, 83, 83, 113, 40),
    (706, "Hisuian Goodra", "Steel", "Dragon", 80, 100, 100, 110, 150, 60),
    (713, "Hisuian Avalugg", "Ice", "Rock", 95, 127, 184, 34, 36, 38),
    (724, "Hisuian Decidueye", "Grass", "Fighting", 88, 112, 80, 95, 95, 60),
]

PALDEAN_FORMS = [
    # Paldean Tauros forms
    (128, "Paldean Tauros (Combat)", "Fighting", None, 75, 110, 105, 30, 70, 100),
    (128, "Paldean Tauros (Blaze)", "Fighting", "Fire", 75, 110, 105, 30, 70, 100),
    (128, "Paldean Tauros (Aqua)", "Fighting", "Water", 75, 110, 105, 30, 70, 100),
    (194, "Paldean Wooper", "Poison", "Ground", 55, 45, 45, 25, 25, 15),
]

# New Mega Forms from Pokemon Legends Z-A (announced/leaked)
LEGENDS_ZA_MEGA_FORMS = [
    # These are the confirmed/speculated new Mega forms for Legends Z-A
    # Based on Kalos starters and Zygarde
    (652, "Mega Chesnaught", "Grass", "Fighting", 88, 127, 132, 74, 85, 64),
    (655, "Mega Delphox", "Fire", "Psychic", 75, 89, 92, 144, 120, 114),
    (658, "Mega Greninja", "Water", "Dark", 72, 115, 77, 153, 81, 142),  # Battle Bond evolution
    (700, "Mega Sylveon", "Fairy", None, 95, 85, 85, 140, 150, 80),
    (718, "Mega Zygarde", "Dragon", "Ground", 108, 120, 141, 101, 105, 105),
    # Additional speculated Kalos Megas
    (663, "Mega Talonflame", "Fire", "Flying", 78, 111, 91, 104, 89, 146),
    (687, "Mega Malamar", "Dark", "Psychic", 86, 132, 108, 108, 90, 83),
    (697, "Mega Tyrantrum", "Rock", "Dragon", 82, 141, 139, 89, 109, 81),
    (699, "Mega Aurorus", "Rock", "Ice", 123, 97, 92, 129, 105, 68),
    (706, "Mega Goodra", "Dragon", None, 90, 110, 90, 150, 170, 80),
]

# Complete list of existing Mega forms (for reference/validation)
EXISTING_MEGA_FORMS = [
    "Mega Venusaur", "Mega Charizard X", "Mega Charizard Y", "Mega Blastoise",
    "Mega Beedrill", "Mega Pidgeot", "Mega Alakazam", "Mega Slowbro",
    "Mega Gengar", "Mega Kangaskhan", "Mega Pinsir", "Mega Gyarados",
    "Mega Aerodactyl", "Mega Mewtwo X", "Mega Mewtwo Y", "Mega Ampharos",
    "Mega Steelix", "Mega Scizor", "Mega Heracross", "Mega Houndoom",
    "Mega Tyranitar", "Mega Sceptile", "Mega Blaziken", "Mega Swampert",
    "Mega Gardevoir", "Mega Sableye", "Mega Mawile", "Mega Aggron",
    "Mega Medicham", "Mega Manectric", "Mega Sharpedo", "Mega Camerupt",
    "Mega Altaria", "Mega Banette", "Mega Absol", "Mega Glalie",
    "Mega Salamence", "Mega Metagross", "Mega Latias", "Mega Latios",
    "Mega Rayquaza", "Mega Lopunny", "Mega Garchomp", "Mega Lucario",
    "Mega Abomasnow", "Mega Gallade", "Mega Audino", "Mega Diancie",
]


def load_current_national_dex(data_dir: Path) -> pd.DataFrame:
    """Load the current national dex CSV."""
    csv_path = data_dir / 'national_dex.csv'
    df = pd.read_csv(csv_path)
    print(f"📊 Current National Dex: {len(df)} entries")
    return df


def create_regional_form_entry(base_row: pd.Series, form_data: tuple) -> pd.Series:
    """Create a new row for a regional form based on a base Pokemon."""
    new_row = base_row.copy()
    
    pokedex_num, name, type1, type2, hp, atk, defe, spa, spd, spe = form_data
    
    # Update identifying information
    new_row['name'] = name
    new_row['type_1'] = type1
    new_row['type_2'] = type2 if type2 else np.nan
    new_row['type_number'] = 2 if type2 else 1
    
    # Update base stats
    new_row['hp'] = hp
    new_row['attack'] = atk
    new_row['defense'] = defe
    new_row['sp_attack'] = spa
    new_row['sp_defense'] = spd
    new_row['speed'] = spe
    new_row['total_points'] = hp + atk + defe + spa + spd + spe
    
    # Mark as regional variant
    new_row['status'] = 'Regional Variant'
    
    return new_row


def create_mega_form_entry(base_row: pd.Series, form_data: tuple) -> pd.Series:
    """Create a new row for a Mega Evolution."""
    new_row = base_row.copy()
    
    pokedex_num, name, type1, type2, hp, atk, defe, spa, spd, spe = form_data
    
    # Update identifying information
    new_row['name'] = name
    new_row['type_1'] = type1
    new_row['type_2'] = type2 if type2 else np.nan
    new_row['type_number'] = 2 if type2 else 1
    
    # Update base stats (Mega evolutions get +100 BST)
    new_row['hp'] = hp
    new_row['attack'] = atk
    new_row['defense'] = defe
    new_row['sp_attack'] = spa
    new_row['sp_defense'] = spd
    new_row['speed'] = spe
    new_row['total_points'] = hp + atk + defe + spa + spd + spe
    
    # Mark as Mega Evolution
    new_row['status'] = 'Mega Evolution'
    new_row['is_legendary'] = False  # Megas aren't legendary
    
    return new_row


def add_forms_to_national_dex(df: pd.DataFrame) -> pd.DataFrame:
    """Add all regional forms and new Mega forms to the National Dex."""
    new_rows = []
    
    print("\n🔧 Adding Hisuian forms...")
    for form_data in HISUIAN_FORMS:
        pokedex_num = form_data[0]
        # Find base Pokemon
        base_pokemon = df[df['pokedex_number'] == pokedex_num]
        if not base_pokemon.empty:
            new_row = create_regional_form_entry(base_pokemon.iloc[0], form_data)
            new_rows.append(new_row)
            print(f"  ✅ Added {form_data[1]}")
        else:
            print(f"  ⚠️ Base Pokemon #{pokedex_num} not found for {form_data[1]}")
    
    print("\n🔧 Adding Paldean forms...")
    for form_data in PALDEAN_FORMS:
        pokedex_num = form_data[0]
        # Find base Pokemon
        base_pokemon = df[df['pokedex_number'] == pokedex_num]
        if not base_pokemon.empty:
            new_row = create_regional_form_entry(base_pokemon.iloc[0], form_data)
            new_rows.append(new_row)
            print(f"  ✅ Added {form_data[1]}")
        else:
            print(f"  ⚠️ Base Pokemon #{pokedex_num} not found for {form_data[1]}")
    
    print("\n🔧 Adding new Mega forms from Legends Z-A...")
    for form_data in LEGENDS_ZA_MEGA_FORMS:
        pokedex_num = form_data[0]
        # Find base Pokemon
        base_pokemon = df[df['pokedex_number'] == pokedex_num]
        if not base_pokemon.empty:
            new_row = create_mega_form_entry(base_pokemon.iloc[0], form_data)
            new_rows.append(new_row)
            print(f"  ✅ Added {form_data[1]}")
        else:
            print(f"  ⚠️ Base Pokemon #{pokedex_num} not found for {form_data[1]}")
    
    # Combine original and new rows
    if new_rows:
        new_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
        print(f"\n✅ Added {len(new_rows)} new forms!")
        print(f"📊 New total: {len(new_df)} entries")
        return new_df
    else:
        print("\n⚠️ No new forms were added")
        return df


def recalculate_derived_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Recalculate percentiles and derived stats for all Pokemon."""
    print("\n📊 Recalculating derived statistics...")
    
    # Recalculate percentiles
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_points']
    for stat in stats:
        if stat in df.columns:
            df[f'{stat}_percentile'] = df[stat].rank(pct=True) * 100
    
    # Recalculate other derived stats
    df['physical_special_ratio'] = df['attack'] / (df['sp_attack'] + 1)
    df['offensive_rating'] = (df['attack'] + df['sp_attack']) / 2
    df['defensive_rating'] = (df['defense'] + df['sp_defense']) / 2
    
    print("✅ Derived statistics recalculated")
    return df


def main():
    """Main function to add all forms."""
    # Get data directory
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    data_dir = project_root / 'data'
    
    print("🎮 Pokemon Regional & Mega Forms Updater")
    print("=" * 60)
    
    # Load current national dex
    df = load_current_national_dex(data_dir)
    
    # Check current variants
    print(f"\n📋 Current variant counts:")
    print(f"  Hisuian: {len(df[df['name'].str.contains('Hisuian', na=False)])}")
    print(f"  Paldean: {len(df[df['name'].str.contains('Paldean', na=False)])}")
    print(f"  Alolan: {len(df[df['name'].str.contains('Alolan', na=False)])}")
    print(f"  Galarian: {len(df[df['name'].str.contains('Galarian', na=False)])}")
    print(f"  Mega: {len(df[df['name'].str.contains('Mega', na=False)])}")
    
    # Add new forms
    df_updated = add_forms_to_national_dex(df)
    
    # Recalculate derived stats
    df_updated = recalculate_derived_stats(df_updated)
    
    # Save updated dataset
    output_path = data_dir / 'national_dex.csv'
    backup_path = data_dir / 'national_dex_backup.csv'
    
    # Create backup
    print(f"\n💾 Creating backup: {backup_path}")
    df.to_csv(backup_path, index=False)
    
    # Save updated version
    print(f"💾 Saving updated National Dex: {output_path}")
    df_updated.to_csv(output_path, index=False)
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE! National Dex updated successfully!")
    print(f"📊 Final count: {len(df_updated)} Pokemon")
    print(f"🎯 Added: {len(df_updated) - len(df)} new forms")
    
    # Show final counts
    print(f"\n📋 Final variant counts:")
    print(f"  Hisuian: {len(df_updated[df_updated['name'].str.contains('Hisuian', na=False)])}")
    print(f"  Paldean: {len(df_updated[df_updated['name'].str.contains('Paldean', na=False)])}")
    print(f"  Alolan: {len(df_updated[df_updated['name'].str.contains('Alolan', na=False)])}")
    print(f"  Galarian: {len(df_updated[df_updated['name'].str.contains('Galarian', na=False)])}")
    print(f"  Mega: {len(df_updated[df_updated['name'].str.contains('Mega', na=False)])}")


if __name__ == "__main__":
    main()
