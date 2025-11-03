"""
Verify national_dex.csv integrity and completeness
"""

import pandas as pd
from pathlib import Path

CSV_PATH = Path("data/national_dex.csv")

def verify_dataset():
    """Run comprehensive verification checks"""
    print("=" * 80)
    print("NATIONAL DEX DATASET VERIFICATION")
    print("=" * 80 + "\n")
    
    # Load CSV
    df = pd.read_csv(CSV_PATH)
    
    print(f"Dataset Overview:")
    print(f"  Total Pokemon: {len(df)}")
    print(f"  Total Columns: {len(df.columns)}")
    print(f"  Min Pokemon ID: #{df['pokedex_number'].min()}")
    print(f"  Max Pokemon ID: #{df['pokedex_number'].max()}")
    
    # Check for expected 1025 Pokemon
    print(f"\n✓ Contains all 1025 Pokemon: {len(df) == 1025}")
    
    # Check for duplicates
    duplicates = df[df.duplicated(subset=['pokedex_number'], keep=False)]
    print(f"✓ No duplicates: {len(duplicates) == 0}")
    
    # Check for missing IDs
    expected_ids = set(range(1, 1026))
    actual_ids = set(df['pokedex_number'].unique())
    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids
    
    if missing:
        print(f"\n⚠ Missing Pokemon IDs: {sorted(missing)}")
    else:
        print("✓ All Pokemon IDs from 1 to 1025 present")
    
    if extra:
        print(f"\n⚠ Extra Pokemon IDs: {sorted(extra)}")
    
    # Check for missing values in critical columns
    print("\nMissing Values Analysis:")
    critical_cols = ['name', 'type_1', 'hp', 'attack', 'defense', 
                     'sp_attack', 'sp_defense', 'speed', 'total_points']
    
    for col in critical_cols:
        if col in df.columns:
            missing_count = df[col].isna().sum()
            print(f"  {col}: {missing_count} missing")
    
    # Generation distribution
    print("\nPokemon by Generation:")
    if 'generation' in df.columns:
        gen_counts = df['generation'].value_counts().sort_index()
        for gen, count in gen_counts.items():
            print(f"  Gen {int(gen)}: {count} Pokemon")
    
    # Type distribution
    print("\nTop 10 Primary Types:")
    if 'type_1' in df.columns:
        type_counts = df['type_1'].value_counts().head(10)
        for type_name, count in type_counts.items():
            print(f"  {type_name}: {count}")
    
    # Stat ranges
    print("\nStat Ranges:")
    stat_cols = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_points']
    for col in stat_cols:
        if col in df.columns:
            print(f"  {col}: {df[col].min()}-{df[col].max()}")
    
    # Check new Pokemon from Gen 6-9
    print("\nNew Pokemon Added (Gen 6-9):")
    if 'generation' in df.columns:
        for gen in [6, 7, 8, 9]:
            gen_pokemon = df[df['generation'] == gen]
            print(f"  Gen {gen}: {len(gen_pokemon)} Pokemon")
            if len(gen_pokemon) > 0:
                sample = gen_pokemon.head(3)
                for _, pkmn in sample.iterrows():
                    print(f"    #{int(pkmn['pokedex_number'])}: {pkmn['name']}")
    
    # Overall assessment
    print("\n" + "=" * 80)
    all_good = (
        len(df) == 1025 and 
        len(duplicates) == 0 and 
        len(missing) == 0 and 
        len(extra) == 0
    )
    
    if all_good:
        print("✓ VERIFICATION PASSED: Dataset is complete and valid!")
    else:
        print("⚠ VERIFICATION ISSUES: Please review the problems above")
    print("=" * 80)

if __name__ == "__main__":
    verify_dataset()
