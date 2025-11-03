"""
Merge new Pokemon data into national_dex.csv
"""

import json
import pandas as pd
from pathlib import Path
import shutil
from datetime import datetime

# Paths
JSON_PATH = Path("data/new_pokemon_data.json")
CSV_PATH = Path("data/national_dex.csv")
BACKUP_DIR = Path("data/backups")

def create_backup():
    """Create a timestamped backup of the CSV"""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"national_dex_backup_{timestamp}.csv"
    shutil.copy2(CSV_PATH, backup_path)
    print(f"✓ Backup created: {backup_path}")
    return backup_path

def load_json_data():
    """Load the fetched Pokemon data"""
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ Loaded {len(data)} new Pokemon from JSON")
    return data

def load_csv_data():
    """Load the existing CSV"""
    df = pd.read_csv(CSV_PATH)
    print(f"✓ Loaded existing CSV with {len(df)} Pokemon")
    return df

def merge_data(df_existing, new_pokemon_list):
    """Merge new Pokemon into existing DataFrame"""
    # Convert JSON list to DataFrame
    df_new = pd.DataFrame(new_pokemon_list)
    
    print(f"\nExisting CSV columns: {len(df_existing.columns)}")
    print(f"New data columns: {len(df_new.columns)}")
    
    # Check for missing columns in new data
    missing_cols = set(df_existing.columns) - set(df_new.columns)
    if missing_cols:
        print(f"\n⚠ Adding missing columns to new data: {len(missing_cols)}")
        for col in missing_cols:
            df_new[col] = ""
    
    # Check for new columns in fetched data
    new_cols = set(df_new.columns) - set(df_existing.columns)
    if new_cols:
        print(f"\n⚠ New columns found: {new_cols}")
        print("These will be added to the dataset")
        for col in new_cols:
            df_existing[col] = ""
    
    # Ensure column order matches
    df_new = df_new[df_existing.columns]
    
    # Concatenate
    df_merged = pd.concat([df_existing, df_new], ignore_index=True)
    
    print(f"\n✓ Merged dataset has {len(df_merged)} Pokemon")
    return df_merged

def save_updated_csv(df):
    """Save the updated CSV"""
    df.to_csv(CSV_PATH, index=False, encoding='utf-8')
    print(f"✓ Saved updated CSV to {CSV_PATH}")

def main():
    print("=" * 80)
    print("MERGING NEW POKEMON DATA INTO NATIONAL DEX")
    print("=" * 80 + "\n")
    
    # Create backup
    backup_path = create_backup()
    
    # Load data
    print("\nLoading data...")
    json_data = load_json_data()
    df_existing = load_csv_data()
    
    # Check current range
    current_max = df_existing['pokedex_number'].max()
    print(f"\nCurrent max Pokemon ID in CSV: #{current_max}")
    print(f"New Pokemon range: #{json_data[0]['pokedex_number']} to #{json_data[-1]['pokedex_number']}")
    
    # Merge
    print("\nMerging data...")
    df_merged = merge_data(df_existing, json_data)
    
    # Verify
    print("\nVerifying merged data...")
    new_max = df_merged['pokedex_number'].max()
    total_count = len(df_merged)
    
    print(f"  - Total Pokemon: {total_count}")
    print(f"  - Max Pokemon ID: #{new_max}")
    print(f"  - Expected: 1025")
    
    if new_max == 1025:
        print("  ✓ SUCCESS: Dataset now contains all 1025 Pokemon!")
    else:
        print(f"  ⚠ WARNING: Dataset max is {new_max}, expected 1025")
    
    # Save
    print("\nSaving updated CSV...")
    save_updated_csv(df_merged)
    
    # Final stats
    print("\n" + "=" * 80)
    print("MERGE COMPLETE!")
    print("=" * 80)
    print(f"Backup saved to: {backup_path}")
    print(f"Updated CSV: {CSV_PATH}")
    print(f"Total Pokemon in dataset: {total_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()
