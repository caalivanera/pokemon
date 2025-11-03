import json

# Load and inspect the fetched data
with open('data/new_pokemon_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total Pokemon fetched: {len(data)}")
print(f"First Pokemon: {data[0]['name']} (#{data[0]['pokedex_number']})")
print(f"Last Pokemon: {data[-1]['name']} (#{data[-1]['pokedex_number']})")
print(f"\nFields per Pokemon: {len(data[0].keys())}")
print(f"\nSample fields:")
for key in list(data[0].keys())[:10]:
    print(f"  - {key}: {data[0][key]}")
