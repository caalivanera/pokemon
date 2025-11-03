"""
Download Pokemon Variant and Mega Evolution Sprites
Downloads sprites for all Pokemon variants including:
- Mega Evolutions
- Regional Forms (Alolan, Galarian, Hisuian, Paldean)
- Gigantamax Forms
- Other alternate forms

Sprites are downloaded from PokeAPI and saved to assets/sprites/
"""

import requests
import pandas as pd
from pathlib import Path
import time
from typing import List, Dict

# Configuration
ASSETS_DIR = Path("assets/sprites")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# PokeAPI base URLs (use home sprites which include variants)
POKEAPI_SPRITE_BASE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home"

# Variant mappings for PokeAPI
VARIANT_MAPPINGS = {
    # Mega Evolutions
    "Mega Venusaur": "3-mega",
    "Mega Charizard X": "6-mega-x",
    "Mega Charizard Y": "6-mega-y",
    "Mega Blastoise": "9-mega",
    "Mega Alakazam": "65-mega",
    "Mega Gengar": "94-mega",
    "Mega Kangaskhan": "115-mega",
    "Mega Pinsir": "127-mega",
    "Mega Gyarados": "130-mega",
    "Mega Aerodactyl": "142-mega",
    "Mega Mewtwo X": "150-mega-x",
    "Mega Mewtwo Y": "150-mega-y",
    "Mega Ampharos": "181-mega",
    "Mega Scizor": "212-mega",
    "Mega Heracross": "214-mega",
    "Mega Houndoom": "229-mega",
    "Mega Tyranitar": "248-mega",
    "Mega Blaziken": "257-mega",
    "Mega Gardevoir": "282-mega",
    "Mega Mawile": "303-mega",
    "Mega Aggron": "306-mega",
    "Mega Medicham": "308-mega",
    "Mega Manectric": "310-mega",
    "Mega Banette": "354-mega",
    "Mega Absol": "359-mega",
    "Mega Garchomp": "445-mega",
    "Mega Lucario": "448-mega",
    "Mega Abomasnow": "460-mega",
    "Mega Beedrill": "15-mega",
    "Mega Pidgeot": "18-mega",
    "Mega Slowbro": "80-mega",
    "Mega Steelix": "208-mega",
    "Mega Sceptile": "254-mega",
    "Mega Swampert": "260-mega",
    "Mega Sableye": "302-mega",
    "Mega Sharpedo": "319-mega",
    "Mega Camerupt": "323-mega",
    "Mega Altaria": "334-mega",
    "Mega Glalie": "362-mega",
    "Mega Salamence": "373-mega",
    "Mega Metagross": "376-mega",
    "Mega Latias": "380-mega",
    "Mega Latios": "381-mega",
    "Mega Rayquaza": "384-mega",
    "Mega Lopunny": "428-mega",
    "Mega Gallade": "475-mega",
    "Mega Audino": "531-mega",
    "Mega Diancie": "719-mega",
    
    # Alolan Forms
    "Alolan Rattata": "19-alola",
    "Alolan Raticate": "20-alola",
    "Alolan Raichu": "26-alola",
    "Alolan Sandshrew": "27-alola",
    "Alolan Sandslash": "28-alola",
    "Alolan Vulpix": "37-alola",
    "Alolan Ninetales": "38-alola",
    "Alolan Diglett": "50-alola",
    "Alolan Dugtrio": "51-alola",
    "Alolan Meowth": "52-alola",
    "Alolan Persian": "53-alola",
    "Alolan Geodude": "74-alola",
    "Alolan Graveler": "75-alola",
    "Alolan Golem": "76-alola",
    "Alolan Grimer": "88-alola",
    "Alolan Muk": "89-alola",
    "Alolan Exeggutor": "103-alola",
    "Alolan Marowak": "105-alola",
    
    # Galarian Forms
    "Galarian Meowth": "52-galar",
    "Galarian Ponyta": "77-galar",
    "Galarian Rapidash": "78-galar",
    "Galarian Slowpoke": "79-galar",
    "Galarian Slowbro": "80-galar",
    "Galarian Farfetch'd": "83-galar",
    "Galarian Weezing": "110-galar",
    "Galarian Mr. Mime": "122-galar",
    "Galarian Articuno": "144-galar",
    "Galarian Zapdos": "145-galar",
    "Galarian Moltres": "146-galar",
    "Galarian Corsola": "222-galar",
    "Galarian Zigzagoon": "263-galar",
    "Galarian Linoone": "264-galar",
    "Galarian Darumaka": "554-galar",
    "Galarian Darmanitan": "555-galar",
    "Galarian Yamask": "562-galar",
    "Galarian Stunfisk": "618-galar",
    "Galarian Slowking": "199-galar",
    
    # Hisuian Forms
    "Hisuian Growlithe": "58-hisui",
    "Hisuian Arcanine": "59-hisui",
    "Hisuian Voltorb": "100-hisui",
    "Hisuian Electrode": "101-hisui",
    "Hisuian Typhlosion": "157-hisui",
    "Hisuian Qwilfish": "211-hisui",
    "Hisuian Sneasel": "215-hisui",
    "Hisuian Samurott": "503-hisui",
    "Hisuian Lilligant": "549-hisui",
    "Hisuian Zorua": "570-hisui",
    "Hisuian Zoroark": "571-hisui",
    "Hisuian Braviary": "628-hisui",
    "Hisuian Sliggoo": "705-hisui",
    "Hisuian Goodra": "706-hisui",
    "Hisuian Avalugg": "713-hisui",
    "Hisuian Decidueye": "724-hisui",
}


def download_sprite(url: str, save_path: Path, pokemon_name: str) -> bool:
    """Download a sprite from URL and save to path"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            save_path.write_bytes(response.content)
            print(f"✓ Downloaded: {pokemon_name} ({save_path.name})")
            return True
        else:
            print(f"✗ Failed: {pokemon_name} (HTTP {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ Error downloading {pokemon_name}: {e}")
        return False


def download_variant_sprites():
    """Download all variant and mega evolution sprites"""
    print(f"Starting download of {len(VARIANT_MAPPINGS)} variant sprites...")
    print(f"Saving to: {ASSETS_DIR.absolute()}\n")
    
    success_count = 0
    failed_count = 0
    
    for variant_name, pokeapi_id in VARIANT_MAPPINGS.items():
        # Create filename from variant name
        filename = f"{pokeapi_id}.png"
        save_path = ASSETS_DIR / filename
        
        # Skip if already exists
        if save_path.exists():
            print(f"⊙ Exists: {variant_name} ({filename})")
            success_count += 1
            continue
        
        # Download from PokeAPI
        url = f"{POKEAPI_SPRITE_BASE}/{pokeapi_id}.png"
        
        if download_sprite(url, save_path, variant_name):
            success_count += 1
        else:
            failed_count += 1
        
        # Rate limiting
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print(f"Download Complete!")
    print(f"{'='*60}")
    print(f"✓ Successful: {success_count}")
    print(f"✗ Failed: {failed_count}")
    print(f"Total: {len(VARIANT_MAPPINGS)}")
    print(f"{'='*60}")


def verify_variant_data():
    """Verify variant entries exist in national_dex.csv"""
    try:
        df = pd.read_csv("data/national_dex.csv")
        
        print("\nVerifying variant data in national_dex.csv...")
        print(f"Total records: {len(df)}")
        
        # Count variants
        mega_count = df[df['name'].str.contains('Mega', na=False, case=False)].shape[0]
        alolan_count = df[df['name'].str.contains('Alolan', na=False, case=False)].shape[0]
        galarian_count = df[df['name'].str.contains('Galarian', na=False, case=False)].shape[0]
        hisuian_count = df[df['name'].str.contains('Hisuian', na=False, case=False)].shape[0]
        
        print(f"\nVariant counts in database:")
        print(f"  Mega Evolutions: {mega_count}")
        print(f"  Alolan Forms: {alolan_count}")
        print(f"  Galarian Forms: {galarian_count}")
        print(f"  Hisuian Forms: {hisuian_count}")
        print(f"  Total Variants: {mega_count + alolan_count + galarian_count + hisuian_count}")
        
        return True
    except Exception as e:
        print(f"Error verifying data: {e}")
        return False


def main():
    """Main execution function"""
    print("="*60)
    print("POKEMON VARIANT SPRITE DOWNLOADER")
    print("="*60)
    print()
    
    # Verify data first
    verify_variant_data()
    print()
    
    # Download sprites
    download_variant_sprites()
    
    print("\n✓ Script completed successfully!")
    print(f"Sprites saved to: {ASSETS_DIR.absolute()}")


if __name__ == "__main__":
    main()
