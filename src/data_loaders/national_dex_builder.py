"""
National Dex Data Consolidator
Combines all CSV data sources into a comprehensive Pokemon National Dex dataset
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import json


class NationalDexBuilder:
    """Builds a comprehensive National Pokedex from multiple data sources."""
    
    def __init__(self, data_dir: str = None):
        """Initialize the National Dex Builder."""
        if data_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            data_dir = os.path.join(project_root, 'data')
        
        self.data_dir = Path(data_dir)
        self.national_dex = None
        
    def load_main_pokedex(self) -> pd.DataFrame:
        """Load the main comprehensive pokedex CSV."""
        print("Loading main pokedex data...")
        path = self.data_dir / 'pokedex.csv'
        df = pd.read_csv(path)
        
        # Clean up unnamed index column
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        
        print(f"✅ Loaded {len(df)} Pokemon from main pokedex")
        return df
    
    def load_alternate_pokedex(self) -> pd.DataFrame:
        """Load alternate pokedex version for additional info."""
        print("Loading alternate pokedex data...")
        path = self.data_dir / 'pokedex_otherVer.csv'
        df = pd.read_csv(path)
        
        # Rename columns to match main schema
        column_mapping = {
            'id': 'alt_id',
            'name': 'alt_name',
            'height': 'alt_height',
            'weight': 'alt_weight',
            'hp': 'alt_hp',
            'attack': 'alt_attack',
            'defense': 'alt_defense',
            's_attack': 'alt_sp_attack',
            's_defense': 'alt_sp_defense',
            'speed': 'alt_speed',
            'type': 'alt_type',
            'evo_set': 'evolution_chain',
            'info': 'alternate_info'
        }
        df = df.rename(columns=column_mapping)
        
        print(f"✅ Loaded {len(df)} Pokemon from alternate pokedex")
        return df
    
    def load_corpus_data(self) -> pd.DataFrame:
        """Load Pokemon corpus descriptions."""
        print("Loading Pokemon corpus data...")
        path = self.data_dir / 'poke_corpus.csv'
        df = pd.read_csv(path)
        
        # Clean up unnamed index column
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        
        df = df.rename(columns={'pokemon_info': 'corpus_description'})
        
        print(f"✅ Loaded {len(df)} corpus entries")
        return df
    
    def merge_datasets(self, main_df: pd.DataFrame, alt_df: pd.DataFrame, 
                      corpus_df: pd.DataFrame) -> pd.DataFrame:
        """Merge all datasets into comprehensive national dex."""
        print("\n🔄 Merging datasets...")
        
        # Start with main dataset
        national_dex = main_df.copy()
        
        # Add corpus descriptions (by index - they align with pokedex numbers)
        if len(corpus_df) > 0:
            national_dex['corpus_description'] = corpus_df['corpus_description'].values[:len(national_dex)]
        
        # Merge alternate data by name (fuzzy matching)
        if len(alt_df) > 0:
            # Clean names for matching
            alt_df['clean_name'] = alt_df['alt_name'].str.lower().str.strip()
            national_dex['clean_name'] = national_dex['name'].str.lower().str.strip()
            
            # Merge on cleaned names
            national_dex = national_dex.merge(
                alt_df,
                on='clean_name',
                how='left',
                suffixes=('', '_alt_source')
            )
            
            # Drop temporary clean name column
            national_dex = national_dex.drop('clean_name', axis=1)
        
        print(f"✅ Merged data: {len(national_dex)} Pokemon in National Dex")
        return national_dex
    
    def calculate_derived_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate additional statistical metrics."""
        print("\n📊 Calculating derived statistics...")
        
        # Base stat total (if not already present)
        if 'total_points' not in df.columns:
            df['total_points'] = (
                df['hp'] + df['attack'] + df['defense'] + 
                df['sp_attack'] + df['sp_defense'] + df['speed']
            )
        
        # Statistical percentiles for each stat
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_points']
        for stat in stats:
            if stat in df.columns:
                df[f'{stat}_percentile'] = df[stat].rank(pct=True) * 100
        
        # Physical vs Special bias
        df['physical_special_ratio'] = df['attack'] / (df['sp_attack'] + 1)  # +1 to avoid div by zero
        df['offensive_rating'] = (df['attack'] + df['sp_attack']) / 2
        df['defensive_rating'] = (df['defense'] + df['sp_defense']) / 2
        
        # BMI calculation (for fun)
        df['bmi'] = df['weight_kg'] / ((df['height_m'] ** 2) + 0.01)  # +0.01 to avoid div by zero
        
        # Speed tier classification
        df['speed_tier'] = pd.cut(
            df['speed'],
            bins=[0, 50, 80, 110, 150, 300],
            labels=['Very Slow', 'Slow', 'Average', 'Fast', 'Very Fast']
        )
        
        # BST tier classification
        df['bst_tier'] = pd.cut(
            df['total_points'],
            bins=[0, 300, 400, 500, 600, 1000],
            labels=['Very Low', 'Low', 'Average', 'High', 'Legendary']
        )
        
        # Type effectiveness summary
        type_effectiveness_cols = [col for col in df.columns if col.startswith('against_')]
        if type_effectiveness_cols:
            df['resistances_count'] = (df[type_effectiveness_cols] < 1).sum(axis=1)
            df['weaknesses_count'] = (df[type_effectiveness_cols] > 1).sum(axis=1)
            df['immunities_count'] = (df[type_effectiveness_cols] == 0).sum(axis=1)
            df['defensive_score'] = df['resistances_count'] - df['weaknesses_count'] + (df['immunities_count'] * 2)
        
        print("✅ Calculated derived statistics")
        return df
    
    def add_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add metadata and categorizations."""
        print("\n🏷️ Adding metadata and categorizations...")
        
        # Is Legendary/Mythical classification
        legendary_names = [
            'Articuno', 'Zapdos', 'Moltres', 'Mewtwo', 'Mew',
            'Raikou', 'Entei', 'Suicune', 'Lugia', 'Ho-Oh', 'Celebi',
            'Regirock', 'Regice', 'Registeel', 'Latias', 'Latios', 'Kyogre', 
            'Groudon', 'Rayquaza', 'Jirachi', 'Deoxys'
        ]
        df['is_legendary'] = df['name'].isin(legendary_names)
        
        # Starter Pokemon
        starter_numbers = [1, 4, 7, 152, 155, 158, 252, 255, 258, 387, 390, 393]
        df['is_starter'] = df['pokedex_number'].isin(starter_numbers)
        
        # Pseudo-legendary (BST 600, 3-stage evolution)
        df['is_pseudo_legendary'] = (df['total_points'] >= 600) & (df['total_points'] < 700) & (~df['is_legendary'])
        
        # Single vs Dual type
        df['type_count'] = df['type_2'].notna().astype(int) + 1
        df['is_dual_type'] = df['type_2'].notna()
        
        # Create combined type string
        df['full_type'] = df.apply(
            lambda row: f"{row['type_1']}/{row['type_2']}" if pd.notna(row['type_2']) else row['type_1'],
            axis=1
        )
        
        # Size categories
        df['size_category'] = pd.cut(
            df['height_m'],
            bins=[0, 0.5, 1.0, 2.0, 5.0, 100],
            labels=['Tiny', 'Small', 'Medium', 'Large', 'Huge']
        )
        
        df['weight_category'] = pd.cut(
            df['weight_kg'],
            bins=[0, 10, 50, 100, 200, 10000],
            labels=['Very Light', 'Light', 'Medium', 'Heavy', 'Very Heavy']
        )
        
        print("✅ Added metadata and categorizations")
        return df
    
    def build_national_dex(self) -> pd.DataFrame:
        """Build the complete National Pokedex."""
        print("=" * 60)
        print("🔨 Building National Pokedex")
        print("=" * 60)
        
        # Load all data sources
        main_df = self.load_main_pokedex()
        alt_df = self.load_alternate_pokedex()
        corpus_df = self.load_corpus_data()
        
        # Merge datasets
        national_dex = self.merge_datasets(main_df, alt_df, corpus_df)
        
        # Calculate derived statistics
        national_dex = self.calculate_derived_stats(national_dex)
        
        # Add metadata
        national_dex = self.add_metadata(national_dex)
        
        # Sort by pokedex number
        national_dex = national_dex.sort_values('pokedex_number').reset_index(drop=True)
        
        self.national_dex = national_dex
        
        print("\n" + "=" * 60)
        print("✅ National Pokedex Build Complete!")
        print("=" * 60)
        print(f"📊 Total Pokemon: {len(national_dex)}")
        print(f"📊 Total Columns: {len(national_dex.columns)}")
        print(f"📊 Generations: {national_dex['generation'].nunique()}")
        print(f"📊 Unique Types: {national_dex['type_1'].nunique()}")
        print(f"📊 Legendary Pokemon: {national_dex['is_legendary'].sum()}")
        
        return national_dex
    
    def save_national_dex(self, output_path: str = None):
        """Save the National Dex to CSV."""
        if self.national_dex is None:
            raise ValueError("National Dex not built yet. Run build_national_dex() first.")
        
        if output_path is None:
            output_path = self.data_dir / 'national_dex.csv'
        
        self.national_dex.to_csv(output_path, index=False)
        print(f"\n💾 National Dex saved to: {output_path}")
        print(f"📊 File size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
    
    def generate_data_dictionary(self) -> Dict[str, Any]:
        """Generate a data dictionary for the National Dex."""
        if self.national_dex is None:
            raise ValueError("National Dex not built yet. Run build_national_dex() first.")
        
        data_dict = {
            'dataset_name': 'Pokemon National Dex',
            'total_records': len(self.national_dex),
            'total_columns': len(self.national_dex.columns),
            'columns': {}
        }
        
        # Column descriptions
        column_descriptions = {
            'pokedex_number': 'National Pokedex number',
            'name': 'Pokemon name',
            'japanese_name': 'Japanese name',
            'generation': 'Generation introduced',
            'type_1': 'Primary type',
            'type_2': 'Secondary type (if dual-type)',
            'full_type': 'Combined type string',
            'height_m': 'Height in meters',
            'weight_kg': 'Weight in kilograms',
            'hp': 'Base HP stat',
            'attack': 'Base Attack stat',
            'defense': 'Base Defense stat',
            'sp_attack': 'Base Special Attack stat',
            'sp_defense': 'Base Special Defense stat',
            'speed': 'Base Speed stat',
            'total_points': 'Base Stat Total (BST)',
            'catch_rate': 'Catch rate (0-255)',
            'base_friendship': 'Base friendship value',
            'is_legendary': 'Whether Pokemon is legendary',
            'is_starter': 'Whether Pokemon is a starter',
            'is_pseudo_legendary': 'Whether Pokemon is pseudo-legendary',
            'speed_tier': 'Speed classification',
            'bst_tier': 'BST tier classification',
            'offensive_rating': 'Average offensive stat',
            'defensive_rating': 'Average defensive stat',
            'resistances_count': 'Number of type resistances',
            'weaknesses_count': 'Number of type weaknesses',
            'immunities_count': 'Number of type immunities'
        }
        
        for col in self.national_dex.columns:
            col_info = {
                'dtype': str(self.national_dex[col].dtype),
                'non_null_count': int(self.national_dex[col].notna().sum()),
                'null_count': int(self.national_dex[col].isna().sum()),
                'description': column_descriptions.get(col, 'No description available')
            }
            
            # Add statistics for numeric columns
            if pd.api.types.is_numeric_dtype(self.national_dex[col]):
                col_info['min'] = float(self.national_dex[col].min())
                col_info['max'] = float(self.national_dex[col].max())
                col_info['mean'] = float(self.national_dex[col].mean())
                col_info['median'] = float(self.national_dex[col].median())
            
            # Add unique values for categorical columns
            elif self.national_dex[col].nunique() < 50:
                col_info['unique_values'] = self.national_dex[col].value_counts().to_dict()
            
            data_dict['columns'][col] = col_info
        
        return data_dict
    
    def save_data_dictionary(self, output_path: str = None):
        """Save data dictionary to JSON."""
        data_dict = self.generate_data_dictionary()
        
        if output_path is None:
            output_path = self.data_dir / 'national_dex_dictionary.json'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
        
        print(f"📖 Data dictionary saved to: {output_path}")


def main():
    """Main execution function."""
    # Initialize builder
    builder = NationalDexBuilder()
    
    # Build National Dex
    national_dex = builder.build_national_dex()
    
    # Save to CSV
    builder.save_national_dex()
    
    # Save data dictionary
    builder.save_data_dictionary()
    
    print("\n✨ National Dex creation complete!")
    print("\n📊 Sample data:")
    print(national_dex[['pokedex_number', 'name', 'type_1', 'type_2', 'total_points', 'bst_tier']].head(10))
    
    return national_dex


if __name__ == '__main__':
    national_dex = main()
