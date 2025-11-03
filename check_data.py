import pandas as pd

# Check national_dex.csv
print("=== national_dex.csv ===")
df1 = pd.read_csv('data/national_dex.csv')
print(f"Total rows: {len(df1)}")
if 'pokedex_number' in df1.columns:
    print(f"Max Pokedex #: {df1['pokedex_number'].max()}")
    print(f"Unique Pokemon: {df1['pokedex_number'].nunique()}")
print(f"Columns: {list(df1.columns)}")

print("\n=== national_dex_backup.csv ===")
df2 = pd.read_csv('data/national_dex_backup.csv')
print(f"Total rows: {len(df2)}")
if 'pokedex_number' in df2.columns:
    print(f"Max Pokedex #: {df2['pokedex_number'].max()}")
    print(f"Unique Pokemon: {df2['pokedex_number'].nunique()}")
print(f"Columns: {list(df2.columns)}")

print("\n=== pokemon.csv ===")
df3 = pd.read_csv('data/pokemon.csv')
print(f"Total rows: {len(df3)}")
print(f"Columns: {list(df3.columns)}")
