"""
Merge base forms from national_dex.csv with variants in national_dex_with_variants.csv
This will ensure all Pokemon have proper base forms and variants
"""

import pandas as pd
from pathlib import Path

# Load both datasets
print("Loading datasets...")
base_df = pd.read_csv('data/national_dex.csv')
variants_df = pd.read_csv('data/national_dex_with_variants.csv')

print(f"Base dataset: {len(base_df)} entries")
print(f"Variants dataset: {len(variants_df)} entries")

# Check what's in base dataset
print(f"\nBase dataset has Venusaur #3: {len(base_df[base_df['pokedex_number'] == 3]) > 0}")
print("First 5 entries:")
print(base_df.head(5)[['pokedex_number', 'name', 'type_1', 'type_2']])

# Check variants dataset
print(f"\nVariants dataset - Pokemon #3 entries:")
venusaur_variants = variants_df[variants_df['pokedex_number'] == 3]
print(venusaur_variants[['pokedex_number', 'name', 'variant_type', 'form_name']])
