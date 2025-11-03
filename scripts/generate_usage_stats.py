"""
Pokemon Usage Statistics Generator
Creates sample usage statistics data for competitive Pokemon
"""
import pandas as pd
import random
from datetime import datetime, timedelta

class UsageStatsGenerator:
    """Generates sample Pokemon usage statistics"""
    
    def __init__(self):
        self.tiers = ['OU', 'UU', 'RU', 'NU', 'Uber']
        self.months = self._generate_months(6)
        
    def _generate_months(self, count=6):
        """Generate last N months"""
        months = []
        current = datetime.now()
        for i in range(count):
            date = current - timedelta(days=30*i)
            months.append(date.strftime('%Y-%m'))
        return list(reversed(months))
    
    def generate_usage_stats(self, tier_df):
        """
        Generate monthly usage statistics for Pokemon
        
        Args:
            tier_df: DataFrame with pokemon tier data
            
        Returns:
            DataFrame with monthly usage stats
        """
        usage_records = []
        
        for _, pokemon in tier_df.iterrows():
            tier = pokemon['tier']
            base_usage = pokemon['usage_percent']
            
            # Generate monthly variations
            for month in self.months:
                # Add random variation (+/- 10%)
                variation = random.uniform(-10, 10)
                monthly_usage = max(0, base_usage + variation)
                
                usage_records.append({
                    'pokemon_id': pokemon['pokemon_id'],
                    'pokemon_name': pokemon['name'],
                    'tier': tier,
                    'month': month,
                    'usage_percent': round(monthly_usage, 2),
                    'rank': 0,  # Will calculate after
                    'battles': random.randint(10000, 100000)
                })
        
        usage_df = pd.DataFrame(usage_records)
        
        # Calculate ranks within each tier-month
        usage_df['rank'] = (
            usage_df.groupby(['tier', 'month'])['usage_percent']
            .rank(method='dense', ascending=False)
            .astype(int)
        )
        
        return usage_df
    
    def generate_move_usage(self, tier_df):
        """
        Generate popular move usage data
        
        Args:
            tier_df: DataFrame with pokemon tier data
            
        Returns:
            DataFrame with move usage stats
        """
        # Popular moves by type
        move_pool = {
            'Fire': ['Flamethrower', 'Fire Blast', 'Heat Wave', 'Flare Blitz'],
            'Water': ['Hydro Pump', 'Scald', 'Surf', 'Waterfall'],
            'Grass': ['Energy Ball', 'Giga Drain', 'Leaf Storm', 'Wood Hammer'],
            'Electric': ['Thunderbolt', 'Thunder', 'Volt Switch', 'Wild Charge'],
            'Psychic': ['Psychic', 'Psyshock', 'Psybeam', 'Zen Headbutt'],
            'Dragon': ['Dragon Claw', 'Draco Meteor', 'Outrage', 'Dragon Dance'],
            'Ice': ['Ice Beam', 'Blizzard', 'Ice Shard', 'Icicle Crash'],
            'Fighting': ['Close Combat', 'Drain Punch', 'Mach Punch', 'Superpower'],
            'Normal': ['Body Slam', 'Hyper Voice', 'Facade', 'Quick Attack'],
            'Dark': ['Knock Off', 'Dark Pulse', 'Sucker Punch', 'Crunch'],
            'Steel': ['Iron Head', 'Flash Cannon', 'Meteor Mash', 'Bullet Punch'],
            'Fairy': ['Moonblast', 'Dazzling Gleam', 'Play Rough', 'Draining Kiss'],
            'Ghost': ['Shadow Ball', 'Shadow Claw', 'Shadow Sneak', 'Phantom Force'],
            'Rock': ['Stone Edge', 'Rock Slide', 'Stealth Rock', 'Head Smash'],
            'Ground': ['Earthquake', 'Earth Power', 'Stomping Tantrum', 'Dig'],
            'Flying': ['Brave Bird', 'Hurricane', 'Air Slash', 'Acrobatics'],
            'Poison': ['Sludge Bomb', 'Gunk Shot', 'Poison Jab', 'Toxic'],
            'Bug': ['Bug Buzz', 'U-turn', 'X-Scissor', 'Leech Life'],
        }
        
        # Universal good moves
        universal_moves = [
            'Protect', 'Substitute', 'Toxic', 'Will-O-Wisp',
            'Stealth Rock', 'Rapid Spin', 'Defog', 'Roost',
            'Recover', 'Rest', 'Sleep Talk', 'Taunt'
        ]
        
        move_records = []
        
        for _, pokemon in tier_df.head(50).iterrows():  # Top 50 for sample
            pokemon_id = pokemon['pokemon_id']
            pokemon_name = pokemon['name']
            
            # Assign 4-6 moves per Pokemon
            num_moves = random.randint(4, 6)
            
            # Pick moves from pool
            all_moves = universal_moves + move_pool.get('Normal', [])
            selected_moves = random.sample(all_moves, min(num_moves, len(all_moves)))
            
            for i, move in enumerate(selected_moves):
                move_records.append({
                    'pokemon_id': pokemon_id,
                    'pokemon_name': pokemon_name,
                    'move_name': move,
                    'usage_percent': round(random.uniform(20, 95), 2),
                    'move_slot': i + 1
                })
        
        return pd.DataFrame(move_records)
    
    def generate_ability_usage(self, tier_df):
        """Generate ability usage data"""
        common_abilities = [
            'Intimidate', 'Levitate', 'Multiscale', 'Regenerator',
            'Magic Bounce', 'Prankster', 'Swift Swim', 'Drought',
            'Sand Stream', 'Drizzle', 'Pressure', 'Technician',
            'Huge Power', 'Speed Boost', 'Sturdy', 'Contrary'
        ]
        
        ability_records = []
        
        for _, pokemon in tier_df.head(50).iterrows():
            num_abilities = random.randint(1, 3)  # Hidden abilities
            
            for ability in random.sample(common_abilities, num_abilities):
                ability_records.append({
                    'pokemon_id': pokemon['pokemon_id'],
                    'pokemon_name': pokemon['name'],
                    'ability_name': ability,
                    'usage_percent': round(random.uniform(10, 90), 2)
                })
        
        return pd.DataFrame(ability_records)
    
    def save_all_stats(self, tier_df):
        """Generate and save all usage statistics"""
        print("📊 Generating usage statistics...")
        
        # Generate datasets
        print("\n1. Monthly usage trends...")
        usage_df = self.generate_usage_stats(tier_df)
        usage_df.to_csv('data/competitive/usage_stats.csv', index=False)
        print(f"   ✅ {len(usage_df)} usage records")
        
        print("\n2. Move usage data...")
        moves_df = self.generate_move_usage(tier_df)
        moves_df.to_csv('data/competitive/move_usage.csv', index=False)
        print(f"   ✅ {len(moves_df)} move records")
        
        print("\n3. Ability usage data...")
        abilities_df = self.generate_ability_usage(tier_df)
        abilities_df.to_csv('data/competitive/ability_usage.csv', index=False)
        print(f"   ✅ {len(abilities_df)} ability records")
        
        # Print summary
        print("\n📈 Usage Statistics Summary:")
        print(f"   - Months tracked: {len(self.months)}")
        print(f"   - Pokemon analyzed: {len(tier_df)}")
        print(f"   - Total usage records: {len(usage_df)}")
        print(f"   - Move combinations: {len(moves_df)}")
        print(f"   - Ability variations: {len(abilities_df)}")
        
        return usage_df, moves_df, abilities_df

def main():
    """Main execution"""
    print("🎮 Pokemon Usage Statistics Generator")
    print("=" * 60)
    
    # Load tier data
    print("\n1. Loading tier data...")
    try:
        tier_df = pd.read_csv('data/competitive/tier_data.csv')
        print(f"   ✅ Loaded {len(tier_df)} Pokemon")
    except FileNotFoundError:
        print("   ❌ tier_data.csv not found. Run collect_tier_data.py first.")
        return
    
    # Generate usage stats
    print("\n2. Generating usage statistics...")
    generator = UsageStatsGenerator()
    usage_df, moves_df, abilities_df = generator.save_all_stats(tier_df)
    
    # Show sample data
    print("\n📋 Sample Usage Trends (Top 5):")
    print(usage_df.head().to_string(index=False))
    
    print("\n📋 Sample Move Usage (Top 5):")
    print(moves_df.head().to_string(index=False))
    
    print("\n✅ Usage statistics generation complete!")
    print("📁 Output files:")
    print("   - data/competitive/usage_stats.csv")
    print("   - data/competitive/move_usage.csv")
    print("   - data/competitive/ability_usage.csv")

if __name__ == "__main__":
    main()
