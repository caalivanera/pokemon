"""
Quick diagnostic to check what version and data we have
"""
import pandas as pd
from pathlib import Path

print("=" * 60)
print("DASHBOARD VERSION CHECK")
print("=" * 60)

# Check enhanced_dashboard.py version
with open('enhanced_dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[:10]):
        if 'Version' in line:
            print(f"\n📌 Dashboard Version: {line.strip()}")
            break

# Check data files
print("\n📊 DATA FILES:")
print("-" * 60)

# Check national_dex.csv
csv_path = Path("data/national_dex.csv")
if csv_path.exists():
    df = pd.read_csv(csv_path)
    print(f"✅ national_dex.csv: {len(df)} Pokemon")
    print(f"   Max Pokedex #: {df['pokedex_number'].max()}")
    print(f"   Columns: {len(df.columns)}")
else:
    print("❌ national_dex.csv: NOT FOUND")

# Check game data
game_path = Path("data/enhanced/comprehensive_game_data.json")
if game_path.exists():
    import json
    with open(game_path, 'r', encoding='utf-8') as f:
        game_data = json.load(f)
    print(f"✅ comprehensive_game_data.json: {len(game_data)} entries")
else:
    print("❌ comprehensive_game_data.json: NOT FOUND")

# Check competitive data
comp_path = Path("data/competitive/competitive_data.json")
if comp_path.exists():
    with open(comp_path, 'r', encoding='utf-8') as f:
        comp_data = json.load(f)
    print(f"✅ competitive_data.json: {len(comp_data)} entries")
else:
    print("❌ competitive_data.json: NOT FOUND")

# Check theme
theme_path = Path(".streamlit/config.toml")
if theme_path.exists():
    with open(theme_path, 'r') as f:
        theme_content = f.read()
    if 'backgroundColor = "#0E1117"' in theme_content:
        print("\n🎨 THEME: DARK MODE ✅")
    elif 'backgroundColor = "#FFFFFF"' in theme_content:
        print("\n🎨 THEME: LIGHT MODE ⚠️")
    else:
        print("\n🎨 THEME: UNKNOWN")
else:
    print("\n🎨 THEME: config.toml NOT FOUND")

print("\n" + "=" * 60)
print("CHECK COMPLETE")
print("=" * 60)
