#!/usr/bin/env python3
"""
Test script for Enhanced Pokemon Dashboard
Tests the core functionality of the data extraction and loading.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.data_loaders.data_extractor import (
        fetch_all_pokemon,
        load_pokemon_glossary
    )
    print("✅ Successfully imported data extraction functions")
    
    # Test glossary loading
    print("\n📚 Testing glossary loading...")
    glossary = load_pokemon_glossary('../data/pokemon_glossary.csv')
    print(f"✅ Loaded {len(glossary)} glossary terms")
    
    # Test Pokemon data loading (limit to 10 for testing)
    print("\n🔄 Testing Pokemon data loading (first 10)...")
    df = fetch_all_pokemon(limit=10)
    
    if not df.empty:
        print(f"✅ Successfully loaded {len(df)} Pokemon entries")
        print(f"📊 Columns: {list(df.columns)}")
        print(f"🎯 Sample Pokemon: {df['name'].head().tolist()}")
        
        # Test basic stats
        print("\n📈 Sample stats:")
        print(f"   - Average BST: {df['total_points'].mean():.1f}")
        print(f"   - Highest Attack: {df['attack'].max()}")
        most_common = (df['primary_type'].mode().iloc[0]
                       if not df['primary_type'].mode().empty else 'N/A')
        print(f"   - Most common type: {most_common}")
        
        print("\n🎉 All tests passed! The enhanced dashboard is ready to run.")
        print("🚀 Run 'streamlit run app.py' to start the application.")
        
    else:
        print("❌ Failed to load Pokemon data")
        sys.exit(1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all required packages are installed:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    sys.exit(1)
