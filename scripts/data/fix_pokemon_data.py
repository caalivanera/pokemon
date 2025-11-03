"""
Fix Pokemon Data Issues
- Correct Pokemon names (remove Mega/Gigantamax from base names)
- Fix evolution chains (Ivysaur -> Venusaur, not Mega Venusaur)
- Update sprite paths for variants
- Add TBA for missing sprites
- Ensure proper variant_type classification
"""

import pandas as pd
import os
from pathlib import Path

# File paths
DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "national_dex_with_variants.csv"
BACKUP_FILE = DATA_DIR / "national_dex_with_variants_backup.csv"
ASSETS_DIR = Path("assets")

def check_sprite_exists(sprite_path):
    """Check if a sprite file exists"""
    if pd.isna(sprite_path) or sprite_path == '':
        return False
    return Path(sprite_path).exists()

def get_correct_sprite_path(pokemon_id, variant_type, sprite_type='static'):
    """
    Generate correct sprite path based on Pokemon ID and variant
    
    Args:
        pokemon_id: Pokemon dex number
        variant_type: base, mega, alolan, galarian, hisuian, paldean, gmax, etc.
        sprite_type: static, animated, shiny
    """
    base_path = "assets/sprites"
    
    # Format pokemon_id with leading zeros (001, 002, etc.)
    pid = str(pokemon_id).zfill(3)
    
    if variant_type == 'base' or pd.isna(variant_type):
        # Base form sprites
        if sprite_type == 'static':
            path = f"{base_path}/{pid}.png"
        elif sprite_type == 'animated':
            path = f"{base_path}/animated/{pid}.gif"
        elif sprite_type == 'shiny':
            path = f"{base_path}/shiny/{pid}.png"
    else:
        # Variant sprites
        variant_suffix = variant_type.lower().replace(' ', '_')
        if sprite_type == 'static':
            path = f"{base_path}/{pid}_{variant_suffix}.png"
        elif sprite_type == 'animated':
            path = f"{base_path}/animated/{pid}_{variant_suffix}.gif"
        elif sprite_type == 'shiny':
            path = f"{base_path}/shiny/{pid}_{variant_suffix}.png"
    
    # Check if file exists, return TBA if not
    if Path(path).exists():
        return path
    else:
        return "TBA"

def fix_pokemon_names(df):
    """
    Fix Pokemon names - remove Mega/Gigantamax/Regional prefixes
    These should be in form_name instead
    """
    print("\n🔧 Fixing Pokemon names...")
    
    # Track changes
    changes = []
    
    for idx, row in df.iterrows():
        original_name = row['name']
        fixed_name = original_name
        variant_type = row.get('variant_type', 'base')
        
        # Remove Mega prefix
        if original_name.startswith('Mega '):
            fixed_name = original_name.replace('Mega ', '')
            if pd.isna(variant_type) or variant_type == 'base':
                df.at[idx, 'variant_type'] = 'mega'
                df.at[idx, 'form_name'] = f"Mega {fixed_name}"
            changes.append(f"  {original_name} → {fixed_name} (Mega form)")
        
        # Remove Gigantamax prefix
        elif original_name.startswith('Gigantamax '):
            fixed_name = original_name.replace('Gigantamax ', '')
            if pd.isna(variant_type) or variant_type == 'base':
                df.at[idx, 'variant_type'] = 'gmax'
                df.at[idx, 'form_name'] = f"Gigantamax {fixed_name}"
            changes.append(f"  {original_name} → {fixed_name} (Gigantamax form)")
        
        # Remove regional prefixes
        for region in ['Alolan', 'Galarian', 'Hisuian', 'Paldean']:
            if original_name.startswith(f'{region} '):
                fixed_name = original_name.replace(f'{region} ', '')
                if pd.isna(variant_type) or variant_type == 'base':
                    df.at[idx, 'variant_type'] = region.lower()
                    df.at[idx, 'form_name'] = f"{region} {fixed_name}"
                changes.append(f"  {original_name} → {fixed_name} ({region} form)")
                break
        
        if fixed_name != original_name:
            df.at[idx, 'name'] = fixed_name
    
    print(f"  ✅ Fixed {len(changes)} names")
    if changes:
        for change in changes[:10]:  # Show first 10
            print(change)
        if len(changes) > 10:
            print(f"  ... and {len(changes) - 10} more")
    
    return df

def fix_evolution_chains(df):
    """
    Fix evolution chains - ensure base forms evolve to base forms, not variants
    Example: Ivysaur should evolve to Venusaur, not Mega Venusaur
    """
    print("\n🔧 Fixing evolution chains...")
    
    # This would require parsing and fixing the evolution_chain column
    # For now, we'll log entries that need manual review
    print("  ℹ️  Evolution chain fixes require manual review of evolution_chain column")
    print("  📝 Recommendation: Update evolution_chain to reference base forms only")
    
    return df

def fix_sprite_paths(df):
    """
    Update sprite paths for all Pokemon and variants
    Add TBA for missing sprites
    """
    print("\n🔧 Fixing sprite paths...")
    
    fixed_count = 0
    tba_count = 0
    
    for idx, row in df.iterrows():
        pokemon_id = int(row['pokedex_number'])
        variant_type = row.get('variant_type', 'base')
        
        # Fix static sprite path
        static_path = get_correct_sprite_path(pokemon_id, variant_type, 'static')
        df.at[idx, 'sprite_path_static'] = static_path
        if static_path == 'TBA':
            tba_count += 1
        else:
            fixed_count += 1
        
        # Fix animated sprite path
        animated_path = get_correct_sprite_path(pokemon_id, variant_type, 'animated')
        df.at[idx, 'sprite_path_animated'] = animated_path
        
        # Fix shiny sprite path
        shiny_path = get_correct_sprite_path(pokemon_id, variant_type, 'shiny')
        df.at[idx, 'sprite_path_shiny'] = shiny_path
    
    print(f"  ✅ Updated {fixed_count} sprite paths")
    print(f"  ⚠️  {tba_count} sprites marked as TBA (missing)")
    
    return df

def verify_variants(df):
    """
    Verify that variants have correct entries
    Example: Abomasnow (base) and Mega Abomasnow should have different sprites
    """
    print("\n🔍 Verifying variants...")
    
    # Group by pokedex_number to check variants
    variant_issues = []
    
    for dex_num, group in df.groupby('pokedex_number'):
        if len(group) > 1:
            base_forms = group[group['variant_type'] == 'base']
            variants = group[group['variant_type'] != 'base']
            
            if len(base_forms) == 0:
                variant_issues.append(f"  ⚠️  #{dex_num}: No base form found!")
            
            # Check if variants have different sprite paths than base
            if len(base_forms) > 0 and len(variants) > 0:
                base_sprite = base_forms.iloc[0]['sprite_path_static']
                for _, variant in variants.iterrows():
                    if variant['sprite_path_static'] == base_sprite:
                        variant_name = variant['name']
                        form = variant.get('form_name', 'Unknown form')
                        variant_issues.append(
                            f"  ⚠️  #{dex_num} {variant_name} ({form}): Uses same sprite as base form"
                        )
    
    if variant_issues:
        print(f"  Found {len(variant_issues)} variant issues:")
        for issue in variant_issues[:10]:
            print(issue)
        if len(variant_issues) > 10:
            print(f"  ... and {len(variant_issues) - 10} more")
    else:
        print("  ✅ All variants look correct")
    
    return df

def main():
    """Main execution"""
    print("=" * 70)
    print("🔧 POKEMON DATA FIX SCRIPT")
    print("=" * 70)
    
    # Load data
    print(f"\n📂 Loading data from {CSV_FILE}...")
    if not CSV_FILE.exists():
        print(f"  ❌ Error: {CSV_FILE} not found!")
        return
    
    df = pd.read_csv(CSV_FILE)
    print(f"  ✅ Loaded {len(df)} entries")
    
    # Create backup
    print(f"\n💾 Creating backup at {BACKUP_FILE}...")
    df.to_csv(BACKUP_FILE, index=False)
    print("  ✅ Backup created")
    
    # Apply fixes
    df = fix_pokemon_names(df)
    df = fix_evolution_chains(df)
    df = fix_sprite_paths(df)
    df = verify_variants(df)
    
    # Save fixed data
    print(f"\n💾 Saving fixed data to {CSV_FILE}...")
    df.to_csv(CSV_FILE, index=False)
    print("  ✅ Data saved")
    
    print("\n" + "=" * 70)
    print("✅ DATA FIX COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  Total entries: {len(df)}")
    print(f"  Unique Pokemon: {df['pokedex_number'].nunique()}")
    print(f"  Base forms: {len(df[df['variant_type'] == 'base'])}")
    print(f"  Variants: {len(df[df['variant_type'] != 'base'])}")
    print(f"\n💡 Next steps:")
    print(f"  1. Review the backup file: {BACKUP_FILE}")
    print(f"  2. Check TBA sprites and download missing ones")
    print(f"  3. Manually review evolution_chain column")
    print(f"  4. Test the dashboard to ensure sprites display correctly")

if __name__ == "__main__":
    main()
