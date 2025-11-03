"""
Pokemon Moveset Database Generator
Creates a comprehensive moveset database for Pokemon analysis
"""
import json
import random
import pandas as pd

class MovesetDatabaseGenerator:
    """Generates comprehensive Pokemon moveset data"""
    
    def __init__(self):
        # Move database organized by type
        self.moves_by_type = {
            'Fire': [
                {'name': 'Flamethrower', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Fire Blast', 'power': 110, 'accuracy': 85, 'category': 'Special'},
                {'name': 'Heat Wave', 'power': 95, 'accuracy': 90, 'category': 'Special'},
                {'name': 'Flare Blitz', 'power': 120, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Fire Punch', 'power': 75, 'accuracy': 100, 'category': 'Physical'},
            ],
            'Water': [
                {'name': 'Hydro Pump', 'power': 110, 'accuracy': 80, 'category': 'Special'},
                {'name': 'Scald', 'power': 80, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Surf', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Waterfall', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Aqua Jet', 'power': 40, 'accuracy': 100, 'category': 'Physical'},
            ],
            'Grass': [
                {'name': 'Energy Ball', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Giga Drain', 'power': 75, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Leaf Storm', 'power': 130, 'accuracy': 90, 'category': 'Special'},
                {'name': 'Wood Hammer', 'power': 120, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Seed Bomb', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
            ],
            'Electric': [
                {'name': 'Thunderbolt', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Thunder', 'power': 110, 'accuracy': 70, 'category': 'Special'},
                {'name': 'Volt Switch', 'power': 70, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Wild Charge', 'power': 90, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Thunder Punch', 'power': 75, 'accuracy': 100, 'category': 'Physical'},
            ],
            'Dragon': [
                {'name': 'Draco Meteor', 'power': 130, 'accuracy': 90, 'category': 'Special'},
                {'name': 'Dragon Pulse', 'power': 85, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Outrage', 'power': 120, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Dragon Claw', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Dragon Dance', 'power': 0, 'accuracy': 100, 'category': 'Status'},
            ],
            'Normal': [
                {'name': 'Hyper Voice', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Body Slam', 'power': 85, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Facade', 'power': 70, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Quick Attack', 'power': 40, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Protect', 'power': 0, 'accuracy': 100, 'category': 'Status'},
            ],
            'Fighting': [
                {'name': 'Close Combat', 'power': 120, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Drain Punch', 'power': 75, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Mach Punch', 'power': 40, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Focus Blast', 'power': 120, 'accuracy': 70, 'category': 'Special'},
                {'name': 'Superpower', 'power': 120, 'accuracy': 100, 'category': 'Physical'},
            ],
            'Psychic': [
                {'name': 'Psychic', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Psyshock', 'power': 80, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Zen Headbutt', 'power': 80, 'accuracy': 90, 'category': 'Physical'},
                {'name': 'Psybeam', 'power': 65, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Calm Mind', 'power': 0, 'accuracy': 100, 'category': 'Status'},
            ],
            'Dark': [
                {'name': 'Knock Off', 'power': 65, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Dark Pulse', 'power': 80, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Sucker Punch', 'power': 70, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Crunch', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Foul Play', 'power': 95, 'accuracy': 100, 'category': 'Physical'},
            ],
            'Steel': [
                {'name': 'Iron Head', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Flash Cannon', 'power': 80, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Meteor Mash', 'power': 90, 'accuracy': 90, 'category': 'Physical'},
                {'name': 'Bullet Punch', 'power': 40, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Steel Beam', 'power': 140, 'accuracy': 95, 'category': 'Special'},
            ],
            'Ice': [
                {'name': 'Ice Beam', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Blizzard', 'power': 110, 'accuracy': 70, 'category': 'Special'},
                {'name': 'Ice Shard', 'power': 40, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Icicle Crash', 'power': 85, 'accuracy': 90, 'category': 'Physical'},
                {'name': 'Freeze-Dry', 'power': 70, 'accuracy': 100, 'category': 'Special'},
            ],
            'Fairy': [
                {'name': 'Moonblast', 'power': 95, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Dazzling Gleam', 'power': 80, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Play Rough', 'power': 90, 'accuracy': 90, 'category': 'Physical'},
                {'name': 'Draining Kiss', 'power': 50, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Spirit Break', 'power': 75, 'accuracy': 100, 'category': 'Physical'},
            ],
            'Ghost': [
                {'name': 'Shadow Ball', 'power': 80, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Shadow Claw', 'power': 70, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Shadow Sneak', 'power': 40, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Phantom Force', 'power': 90, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Hex', 'power': 65, 'accuracy': 100, 'category': 'Special'},
            ],
            'Rock': [
                {'name': 'Stone Edge', 'power': 100, 'accuracy': 80, 'category': 'Physical'},
                {'name': 'Rock Slide', 'power': 75, 'accuracy': 90, 'category': 'Physical'},
                {'name': 'Stealth Rock', 'power': 0, 'accuracy': 100, 'category': 'Status'},
                {'name': 'Head Smash', 'power': 150, 'accuracy': 80, 'category': 'Physical'},
                {'name': 'Power Gem', 'power': 80, 'accuracy': 100, 'category': 'Special'},
            ],
            'Ground': [
                {'name': 'Earthquake', 'power': 100, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Earth Power', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Stomping Tantrum', 'power': 75, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Dig', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Bulldoze', 'power': 60, 'accuracy': 100, 'category': 'Physical'},
            ],
            'Flying': [
                {'name': 'Brave Bird', 'power': 120, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Hurricane', 'power': 110, 'accuracy': 70, 'category': 'Special'},
                {'name': 'Air Slash', 'power': 75, 'accuracy': 95, 'category': 'Special'},
                {'name': 'Acrobatics', 'power': 55, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Roost', 'power': 0, 'accuracy': 100, 'category': 'Status'},
            ],
            'Poison': [
                {'name': 'Sludge Bomb', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'Gunk Shot', 'power': 120, 'accuracy': 80, 'category': 'Physical'},
                {'name': 'Poison Jab', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Toxic', 'power': 0, 'accuracy': 90, 'category': 'Status'},
                {'name': 'Sludge Wave', 'power': 95, 'accuracy': 100, 'category': 'Special'},
            ],
            'Bug': [
                {'name': 'Bug Buzz', 'power': 90, 'accuracy': 100, 'category': 'Special'},
                {'name': 'U-turn', 'power': 70, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'X-Scissor', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'Leech Life', 'power': 80, 'accuracy': 100, 'category': 'Physical'},
                {'name': 'First Impression', 'power': 90, 'accuracy': 100, 'category': 'Physical'},
            ],
        }
        
        # Universal utility moves
        self.utility_moves = [
            {'name': 'Protect', 'power': 0, 'accuracy': 100, 'category': 'Status', 'type': 'Normal'},
            {'name': 'Substitute', 'power': 0, 'accuracy': 100, 'category': 'Status', 'type': 'Normal'},
            {'name': 'Toxic', 'power': 0, 'accuracy': 90, 'category': 'Status', 'type': 'Poison'},
            {'name': 'Will-O-Wisp', 'power': 0, 'accuracy': 85, 'category': 'Status', 'type': 'Fire'},
            {'name': 'Thunder Wave', 'power': 0, 'accuracy': 90, 'category': 'Status', 'type': 'Electric'},
            {'name': 'Stealth Rock', 'power': 0, 'accuracy': 100, 'category': 'Status', 'type': 'Rock'},
            {'name': 'Defog', 'power': 0, 'accuracy': 100, 'category': 'Status', 'type': 'Flying'},
            {'name': 'Roost', 'power': 0, 'accuracy': 100, 'category': 'Status', 'type': 'Flying'},
            {'name': 'Recover', 'power': 0, 'accuracy': 100, 'category': 'Status', 'type': 'Normal'},
            {'name': 'Taunt', 'power': 0, 'accuracy': 100, 'category': 'Status', 'type': 'Dark'},
        ]
    
    def generate_moveset(self, pokemon_types):
        """Generate a realistic moveset for a Pokemon based on its types"""
        moveset = []
        
        # Add STAB moves (Same Type Attack Bonus)
        for poke_type in pokemon_types:
            if poke_type and poke_type in self.moves_by_type:
                type_moves = self.moves_by_type[poke_type]
                # Add 1-2 moves of this type
                num_moves = random.randint(1, 2)
                moveset.extend(random.sample(type_moves, min(num_moves, len(type_moves))))
        
        # Add coverage/utility moves
        remaining_slots = 4 - len(moveset)
        if remaining_slots > 0:
            moveset.extend(random.sample(self.utility_moves, min(remaining_slots, len(self.utility_moves))))
        
        # Ensure exactly 4 moves
        moveset = moveset[:4]
        
        return moveset
    
    def create_moveset_database(self, pokemon_df):
        """
        Create comprehensive moveset database for all Pokemon
        
        Args:
            pokemon_df: Main Pokemon DataFrame
            
        Returns:
            Dictionary with moveset data
        """
        moveset_db = {}
        
        for _, pokemon in pokemon_df.iterrows():
            pokemon_id = int(pokemon['Dex No'])
            pokemon_name = pokemon['Name']
            type1 = pokemon.get('Type 1', 'Normal')
            type2 = pokemon.get('Type 2', None)
            
            types = [type1] if pd.isna(type2) else [type1, type2]
            
            # Generate moveset
            moveset = self.generate_moveset(types)
            
            moveset_db[pokemon_id] = {
                'pokemon_id': pokemon_id,
                'name': pokemon_name,
                'types': types,
                'moveset': [
                    {
                        'name': move['name'],
                        'type': move.get('type', types[0]),
                        'category': move['category'],
                        'power': move['power'],
                        'accuracy': move['accuracy'],
                        'learn_method': random.choice(['level-up', 'tm', 'tutor', 'egg'])
                    }
                    for move in moveset
                ]
            }
        
        return moveset_db
    
    def save_moveset_database(self, moveset_db):
        """Save moveset database to JSON"""
        output_path = 'data/moves/pokemon_movesets.json'
        
        with open(output_path, 'w') as f:
            json.dump(moveset_db, f, indent=2)
        
        print(f"✅ Saved moveset database: {output_path}")
        print(f"   Total Pokemon: {len(moveset_db)}")
        
        # Calculate statistics
        total_moves = sum(len(data['moveset']) for data in moveset_db.values())
        avg_moves = total_moves / len(moveset_db)
        
        print(f"   Total moves: {total_moves}")
        print(f"   Average moves per Pokemon: {avg_moves:.1f}")
        
        return output_path

def main():
    """Main execution"""
    print("🎮 Pokemon Moveset Database Generator")
    print("=" * 60)
    
    # Load Pokemon data
    print("\n1. Loading Pokemon data...")
    try:
        pokemon_df = pd.read_csv('data/pokemon.csv')
        print(f"   ✅ Loaded {len(pokemon_df)} Pokemon")
    except FileNotFoundError:
        print("   ❌ pokemon.csv not found")
        return
    
    # Generate moveset database
    print("\n2. Generating moveset database...")
    generator = MovesetDatabaseGenerator()
    moveset_db = generator.create_moveset_database(pokemon_df)
    print(f"   ✅ Generated movesets for {len(moveset_db)} Pokemon")
    
    # Save database
    print("\n3. Saving moveset database...")
    output_path = generator.save_moveset_database(moveset_db)
    
    # Show sample
    print("\n📋 Sample Moveset (Charizard):")
    if '6' in moveset_db:  # Charizard is #6
        charizard = moveset_db['6']
        print(f"   Pokemon: {charizard['name']}")
        print(f"   Types: {', '.join(charizard['types'])}")
        print("   Moves:")
        for move in charizard['moveset']:
            print(f"     - {move['name']} ({move['type']}, {move['category']})")
            print(f"       Power: {move['power']}, Accuracy: {move['accuracy']}%")
    
    print("\n✅ Moveset database generation complete!")
    print(f"📁 Output: {output_path}")

if __name__ == "__main__":
    main()
