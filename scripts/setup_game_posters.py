"""
Pokemon Game Poster Downloader
Downloads official game box art for all Pokemon generations
"""
import os
import requests
from pathlib import Path
import time

class GamePosterCollector:
    """Downloads and organizes Pokemon game box art"""
    
    def __init__(self, output_dir='assets/games'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Game metadata organized by generation
        self.games = {
            'gen_1': [
                {'name': 'Red', 'filename': 'pokemon_red.jpg', 'region': 'Kanto'},
                {'name': 'Blue', 'filename': 'pokemon_blue.jpg', 'region': 'Kanto'},
                {'name': 'Yellow', 'filename': 'pokemon_yellow.jpg', 'region': 'Kanto'},
            ],
            'gen_2': [
                {'name': 'Gold', 'filename': 'pokemon_gold.jpg', 'region': 'Johto'},
                {'name': 'Silver', 'filename': 'pokemon_silver.jpg', 'region': 'Johto'},
                {'name': 'Crystal', 'filename': 'pokemon_crystal.jpg', 'region': 'Johto'},
            ],
            'gen_3': [
                {'name': 'Ruby', 'filename': 'pokemon_ruby.jpg', 'region': 'Hoenn'},
                {'name': 'Sapphire', 'filename': 'pokemon_sapphire.jpg', 'region': 'Hoenn'},
                {'name': 'Emerald', 'filename': 'pokemon_emerald.jpg', 'region': 'Hoenn'},
                {'name': 'FireRed', 'filename': 'pokemon_firered.jpg', 'region': 'Kanto'},
                {'name': 'LeafGreen', 'filename': 'pokemon_leafgreen.jpg', 'region': 'Kanto'},
            ],
            'gen_4': [
                {'name': 'Diamond', 'filename': 'pokemon_diamond.jpg', 'region': 'Sinnoh'},
                {'name': 'Pearl', 'filename': 'pokemon_pearl.jpg', 'region': 'Sinnoh'},
                {'name': 'Platinum', 'filename': 'pokemon_platinum.jpg', 'region': 'Sinnoh'},
                {'name': 'HeartGold', 'filename': 'pokemon_heartgold.jpg', 'region': 'Johto'},
                {'name': 'SoulSilver', 'filename': 'pokemon_soulsilver.jpg', 'region': 'Johto'},
            ],
            'gen_5': [
                {'name': 'Black', 'filename': 'pokemon_black.jpg', 'region': 'Unova'},
                {'name': 'White', 'filename': 'pokemon_white.jpg', 'region': 'Unova'},
                {'name': 'Black 2', 'filename': 'pokemon_black2.jpg', 'region': 'Unova'},
                {'name': 'White 2', 'filename': 'pokemon_white2.jpg', 'region': 'Unova'},
            ],
            'gen_6': [
                {'name': 'X', 'filename': 'pokemon_x.jpg', 'region': 'Kalos'},
                {'name': 'Y', 'filename': 'pokemon_y.jpg', 'region': 'Kalos'},
                {'name': 'Omega Ruby', 'filename': 'pokemon_omega_ruby.jpg', 'region': 'Hoenn'},
                {'name': 'Alpha Sapphire', 'filename': 'pokemon_alpha_sapphire.jpg', 'region': 'Hoenn'},
            ],
            'gen_7': [
                {'name': 'Sun', 'filename': 'pokemon_sun.jpg', 'region': 'Alola'},
                {'name': 'Moon', 'filename': 'pokemon_moon.jpg', 'region': 'Alola'},
                {'name': 'Ultra Sun', 'filename': 'pokemon_ultra_sun.jpg', 'region': 'Alola'},
                {'name': 'Ultra Moon', 'filename': 'pokemon_ultra_moon.jpg', 'region': 'Alola'},
            ],
            'gen_8': [
                {'name': 'Sword', 'filename': 'pokemon_sword.jpg', 'region': 'Galar'},
                {'name': 'Shield', 'filename': 'pokemon_shield.jpg', 'region': 'Galar'},
            ],
            'gen_9': [
                {'name': 'Scarlet', 'filename': 'pokemon_scarlet.jpg', 'region': 'Paldea'},
                {'name': 'Violet', 'filename': 'pokemon_violet.jpg', 'region': 'Paldea'},
            ],
        }
    
    def create_placeholder_images(self):
        """
        Create placeholder text files instead of downloading images
        (For demonstration purposes - actual images would be too large)
        """
        print("🎨 Creating game poster directory structure...")
        
        total_games = 0
        for gen, games in self.games.items():
            gen_dir = self.output_dir / gen
            gen_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"\n📁 {gen.upper().replace('_', ' ')}:")
            for game in games:
                # Create a text placeholder file
                placeholder_path = gen_dir / game['filename'].replace('.jpg', '.txt')
                
                with open(placeholder_path, 'w') as f:
                    f.write(f"Pokemon {game['name']}\n")
                    f.write(f"Region: {game['region']}\n")
                    f.write(f"Generation: {gen}\n")
                    f.write(f"\nPlaceholder for game box art.\n")
                    f.write(f"In production, download official box art from:\n")
                    f.write(f"- Bulbapedia\n")
                    f.write(f"- Official Pokemon websites\n")
                    f.write(f"- Video game cover databases\n")
                
                print(f"  ✅ {game['name']} ({game['region']})")
                total_games += 1
        
        print(f"\n✅ Created structure for {total_games} games across 9 generations")
    
    def create_metadata_file(self):
        """Create a JSON metadata file with all game information"""
        import json
        
        metadata = {
            'total_games': sum(len(games) for games in self.games.values()),
            'generations': {}
        }
        
        for gen, games in self.games.items():
            gen_num = gen.split('_')[1]
            metadata['generations'][gen_num] = {
                'folder': gen,
                'game_count': len(games),
                'games': games
            }
        
        metadata_path = self.output_dir / 'games_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📄 Created metadata file: {metadata_path}")
    
    def print_download_instructions(self):
        """Print instructions for downloading actual game posters"""
        print("\n" + "="*60)
        print("📥 DOWNLOAD INSTRUCTIONS FOR ACTUAL GAME POSTERS")
        print("="*60)
        print("\nTo add actual game box art images:")
        print("\n1. Visit these sources:")
        print("   - https://bulbapedia.bulbagarden.net/")
        print("   - https://www.pokemon.com/")
        print("   - https://www.giantbomb.com/ (game covers)")
        print("   - https://www.mobygames.com/ (high-quality covers)")
        
        print("\n2. Download box art for each game:")
        total = sum(len(games) for games in self.games.values())
        print(f"   Total: {total} games across 9 generations")
        
        print("\n3. Recommended specs:")
        print("   - Format: JPG or PNG")
        print("   - Size: 300x300px (consistent dimensions)")
        print("   - Quality: High resolution for dashboard display")
        
        print("\n4. Save to generation folders:")
        for gen in self.games.keys():
            print(f"   - {self.output_dir / gen}/")
        
        print("\n5. Update dashboard code to display posters")
        print(f"   See: {self.output_dir / 'README.md'}")
        
        print("\n⏱️ Estimated time: 2-3 hours for all posters")
        print("="*60)

def main():
    """Main execution function"""
    print("🎮 Pokemon Game Poster Collection Setup")
    print("=" * 60)
    
    # Initialize collector
    collector = GamePosterCollector()
    
    # Create directory structure with placeholders
    print("\n1. Setting up directory structure...")
    collector.create_placeholder_images()
    
    # Create metadata file
    print("\n2. Creating metadata file...")
    collector.create_metadata_file()
    
    # Print download instructions
    collector.print_download_instructions()
    
    print("\n✅ Game poster setup complete!")
    print("📁 Directory: assets/games/")
    print("📄 Metadata: assets/games/games_metadata.json")
    print("\n💡 Note: Placeholder files created.")
    print("   Follow instructions above to download actual images.")

if __name__ == "__main__":
    main()
