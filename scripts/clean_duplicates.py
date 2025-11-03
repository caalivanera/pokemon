"""
Clean duplicate Pokemon from national_dex.csv
"""

import pandas as pd
from pathlib import Path

CSV_PATH = Path("data/national_dex.csv")

def clean_duplicates():
    """Remove duplicate Pokemon entries"""
    print("=" * 80)
    print("CLEANING DUPLICATE POKEMON")
    print("=" * 80 + "\n")
    
    # Load CSV
    df = pd.read_csv(CSV_PATH)
    print(f"Original dataset: {len(df)} rows")
    
    # Check for duplicates by pokedex_number
    duplicates = df[df.duplicated(subset=['pokedex_number'], keep=False)]
    if len(duplicates) > 0:
        print(f"\n⚠ Found {len(duplicates)} duplicate rows")
        print(f"Duplicate Pokemon IDs: {sorted(duplicates['pokedex_number'].unique())}")
        
        # Show a few examples
        if len(duplicates) > 0:
            print("\nExample duplicates:")
            sample_id = duplicates['pokedex_number'].iloc[0]
            sample_dups = df[df['pokedex_number'] == sample_id]
            print(f"  Pokemon #{sample_id}:")
            for idx, row in sample_dups.iterrows():
                print(f"    Row {idx}: {row['name']} - {row['type_1']}")
    
    # Remove duplicates, keeping the last occurrence
    # (newer fetched data)
    df_clean = df.drop_duplicates(subset=['pokedex_number'], keep='last')
    
    print(f"\n✓ Cleaned dataset: {len(df_clean)} rows")
    print(f"✓ Removed {len(df) - len(df_clean)} duplicate rows")
    
    # Sort by pokedex_number
    df_clean = df_clean.sort_values('pokedex_number').reset_index(drop=True)
    
    # Verify we have all Pokemon from 1 to 1025
    expected_ids = set(range(1, 1026))
    actual_ids = set(df_clean['pokedex_number'].unique())
    
    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids
    
    if missing:
        print(f"\n⚠ Missing Pokemon IDs: {sorted(missing)}")
    if extra:
        print(f"\n⚠ Extra Pokemon IDs: {sorted(extra)}")
    
    if not missing and not extra and len(df_clean) == 1025:
        print("\n✓ SUCCESS: Dataset contains exactly all 1025 unique Pokemon!")
    
    # Save cleaned CSV
    df_clean.to_csv(CSV_PATH, index=False, encoding='utf-8')
    print(f"\n✓ Saved cleaned CSV to {CSV_PATH}")
    
    # Show final stats
    print("\n" + "=" * 80)
    print("CLEANUP COMPLETE!")
    print("=" * 80)
    print(f"Total Pokemon: {len(df_clean)}")
    print(f"Min ID: #{df_clean['pokedex_number'].min()}")
    print(f"Max ID: #{df_clean['pokedex_number'].max()}")
    print("=" * 80)

if __name__ == "__main__":
    clean_duplicates()
