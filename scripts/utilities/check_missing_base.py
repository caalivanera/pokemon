"""Check for Pokemon missing base forms"""
import pandas as pd

df = pd.read_csv('data/national_dex_with_variants.csv')

print("Pokemon Missing Base Forms:")
print("=" * 50)

pokemon_groups = df.groupby('pokedex_number')
missing_base = []

for num, group in pokemon_groups:
    base_forms = group[group['variant_type'] == 'base']
    if len(base_forms) == 0:
        pokemon_name = group.iloc[0]['name']
        forms = ', '.join(group['variant_type'].unique())
        missing_base.append((num, pokemon_name, forms))

if missing_base:
    for num, name, forms in missing_base[:30]:
        print(f"#{num:03d} {name:20s} - Has: {forms}")
    if len(missing_base) > 30:
        print(f"\n... and {len(missing_base) - 30} more")
    print(f"\nTotal missing: {len(missing_base)}")
else:
    print("✅ All Pokemon have base forms!")
