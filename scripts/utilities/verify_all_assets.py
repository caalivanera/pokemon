"""
Comprehensive Asset Verification Script
Checks all Pokemon sprites, icons, and animated assets
"""

import pandas as pd
from pathlib import Path
import json

print("="*70)
print("🔍 POKEMON ASSET VERIFICATION")
print("="*70)

# Load dataset
df = pd.read_csv('data/national_dex_with_variants.csv')
print(f"\n📊 Checking {len(df)} Pokemon entries...")

# Define asset directories
ASSETS_DIR = Path("assets")
SPRITES_DIR = ASSETS_DIR / "sprites"
ANIMATED_DIR = SPRITES_DIR / "animated"
SHINY_DIR = SPRITES_DIR / "shiny"
ICONS_DIR = ASSETS_DIR / "icons"

# Results storage
results = {
    'static': {'found': [], 'missing': []},
    'animated': {'found': [], 'missing': []},
    'shiny': {'found': [], 'missing': []},
    'icons': {'found': [], 'missing': []}
}

variant_issues = []

print("\n🔍 Verifying sprites...")

for idx, row in df.iterrows():
    dex_num = int(row['pokedex_number'])
    name = row['name']
    variant_type = row.get('variant_type', 'base')
    form_name = row.get('form_name', name)
    
    pid = f"{dex_num:03d}"
    
    # Check static sprite
    static_path = row.get('sprite_path_static', '')
    if static_path and static_path != 'TBA':
        if Path(static_path).exists():
            results['static']['found'].append(f"#{pid} {form_name}")
        else:
            results['static']['missing'].append(f"#{pid} {form_name} - {static_path}")
    else:
        results['static']['missing'].append(f"#{pid} {form_name} - TBA")
    
    # Check animated sprite
    animated_path = row.get('sprite_path_animated', '')
    if animated_path and animated_path != 'TBA':
        if Path(animated_path).exists():
            results['animated']['found'].append(f"#{pid} {form_name}")
        else:
            results['animated']['missing'].append(f"#{pid} {form_name} - {animated_path}")
    else:
        results['animated']['missing'].append(f"#{pid} {form_name} - TBA")
    
    # Check shiny sprite
    shiny_path = row.get('sprite_path_shiny', '')
    if shiny_path and shiny_path != 'TBA':
        if Path(shiny_path).exists():
            results['shiny']['found'].append(f"#{pid} {form_name}")
        else:
            results['shiny']['missing'].append(f"#{pid} {form_name} - {shiny_path}")
    else:
        results['shiny']['missing'].append(f"#{pid} {form_name} - TBA")
    
    # Check icon
    icon_path = ICONS_DIR / f"{pid}.png"
    if icon_path.exists():
        results['icons']['found'].append(f"#{pid} {name}")
    else:
        results['icons']['missing'].append(f"#{pid} {name}")

# Check for duplicate sprites in variants
print("\n🔍 Checking variant sprite uniqueness...")

pokemon_groups = df.groupby('pokedex_number')
for dex_num, group in pokemon_groups:
    if len(group) > 1:
        # Get base form sprite
        base_forms = group[group['variant_type'] == 'base']
        if len(base_forms) > 0:
            base_sprite = base_forms.iloc[0]['sprite_path_static']
            
            # Check variants
            variants = group[group['variant_type'] != 'base']
            for _, variant in variants.iterrows():
                variant_sprite = variant['sprite_path_static']
                if variant_sprite == base_sprite or variant_sprite == 'TBA':
                    issue = (f"#{dex_num:03d} {variant['name']} "
                            f"({variant.get('form_name', 'Unknown')}) - "
                            f"Same sprite as base or TBA")
                    variant_issues.append(issue)

# Print results
print("\n" + "="*70)
print("📊 VERIFICATION RESULTS")
print("="*70)

print(f"\n📷 Static Sprites:")
print(f"   ✅ Found: {len(results['static']['found'])}")
print(f"   ❌ Missing: {len(results['static']['missing'])}")
if len(results['static']['missing']) > 0:
    print(f"\n   Missing sprites (first 20):")
    for sprite in results['static']['missing'][:20]:
        print(f"      {sprite}")
    if len(results['static']['missing']) > 20:
        print(f"      ... and {len(results['static']['missing']) - 20} more")

print(f"\n🎬 Animated Sprites:")
print(f"   ✅ Found: {len(results['animated']['found'])}")
print(f"   ❌ Missing: {len(results['animated']['missing'])}")

print(f"\n✨ Shiny Sprites:")
print(f"   ✅ Found: {len(results['shiny']['found'])}")
print(f"   ❌ Missing: {len(results['shiny']['missing'])}")

print(f"\n🎨 Icons:")
print(f"   ✅ Found: {len(results['icons']['found'])}")
print(f"   ❌ Missing: {len(results['icons']['missing'])}")

if variant_issues:
    print(f"\n⚠️  Variant Sprite Issues: {len(variant_issues)}")
    print(f"   First 10 issues:")
    for issue in variant_issues[:10]:
        print(f"      {issue}")
    if len(variant_issues) > 10:
        print(f"      ... and {len(variant_issues) - 10} more")
else:
    print(f"\n✅ All variants have unique sprites!")

# Calculate percentages
total_entries = len(df)
static_pct = (len(results['static']['found']) / total_entries) * 100
animated_pct = (len(results['animated']['found']) / total_entries) * 100
shiny_pct = (len(results['shiny']['found']) / total_entries) * 100
icons_pct = (len(results['icons']['found']) / total_entries) * 100

print(f"\n📊 Coverage:")
print(f"   Static: {static_pct:.1f}%")
print(f"   Animated: {animated_pct:.1f}%")
print(f"   Shiny: {shiny_pct:.1f}%")
print(f"   Icons: {icons_pct:.1f}%")

# Save detailed report
report = {
    'total_entries': total_entries,
    'static': {
        'found': len(results['static']['found']),
        'missing': len(results['static']['missing']),
        'percentage': static_pct
    },
    'animated': {
        'found': len(results['animated']['found']),
        'missing': len(results['animated']['missing']),
        'percentage': animated_pct
    },
    'shiny': {
        'found': len(results['shiny']['found']),
        'missing': len(results['shiny']['missing']),
        'percentage': shiny_pct
    },
    'icons': {
        'found': len(results['icons']['found']),
        'missing': len(results['icons']['missing']),
        'percentage': icons_pct
    },
    'variant_issues': variant_issues,
    'missing_details': {
        'static': results['static']['missing'],
        'animated': results['animated']['missing'],
        'shiny': results['shiny']['missing'],
        'icons': results['icons']['missing']
    }
}

report_path = 'data/asset_verification_report.json'
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

print(f"\n💾 Detailed report saved: {report_path}")
print("\n" + "="*70)
print("✅ VERIFICATION COMPLETE!")
print("="*70)
