"""
AI-Powered Team Recommendation System
Suggests optimal Pokemon teams based on meta analysis
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Set
from collections import Counter
import random


class TeamRecommender:
    """Recommend optimal Pokemon teams"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.load_data()
        self.load_type_chart()
    
    def load_data(self):
        """Load all necessary data"""
        try:
            self.pokemon_data = pd.read_csv(self.data_dir / "pokemon.csv")
            self.tier_data = pd.read_csv(
                self.data_dir / "competitive" / "tier_data.csv"
            )
            self.usage_stats = pd.read_csv(
                self.data_dir / "competitive" / "usage_stats.csv"
            )
            
            # Load movesets
            moveset_path = self.data_dir / "moves" / "pokemon_movesets.json"
            with open(moveset_path, 'r') as f:
                self.movesets = json.load(f)
            
            print("✅ All data loaded")
        except Exception as e:
            print(f"❌ Error: {e}")
            self.movesets = {}
    
    def load_type_chart(self):
        """Load type effectiveness for coverage analysis"""
        self.weaknesses = {
            'Normal': ['Fighting'],
            'Fire': ['Water', 'Ground', 'Rock'],
            'Water': ['Electric', 'Grass'],
            'Electric': ['Ground'],
            'Grass': ['Fire', 'Ice', 'Poison', 'Flying', 'Bug'],
            'Ice': ['Fire', 'Fighting', 'Rock', 'Steel'],
            'Fighting': ['Flying', 'Psychic', 'Fairy'],
            'Poison': ['Ground', 'Psychic'],
            'Ground': ['Water', 'Grass', 'Ice'],
            'Flying': ['Electric', 'Ice', 'Rock'],
            'Psychic': ['Bug', 'Ghost', 'Dark'],
            'Bug': ['Fire', 'Flying', 'Rock'],
            'Rock': ['Water', 'Grass', 'Fighting', 'Ground', 'Steel'],
            'Ghost': ['Ghost', 'Dark'],
            'Dragon': ['Ice', 'Dragon', 'Fairy'],
            'Dark': ['Fighting', 'Bug', 'Fairy'],
            'Steel': ['Fire', 'Fighting', 'Ground'],
            'Fairy': ['Poison', 'Steel']
        }
        
        self.resistances = {
            'Normal': [],
            'Fire': ['Fire', 'Grass', 'Ice', 'Bug', 'Steel', 'Fairy'],
            'Water': ['Fire', 'Water', 'Ice', 'Steel'],
            'Electric': ['Electric', 'Flying', 'Steel'],
            'Grass': ['Water', 'Electric', 'Grass', 'Ground'],
            'Ice': ['Ice'],
            'Fighting': ['Bug', 'Rock', 'Dark'],
            'Poison': ['Grass', 'Fighting', 'Poison', 'Bug', 'Fairy'],
            'Ground': ['Poison', 'Rock'],
            'Flying': ['Grass', 'Fighting', 'Bug'],
            'Psychic': ['Fighting', 'Psychic'],
            'Bug': ['Grass', 'Fighting', 'Ground'],
            'Rock': ['Normal', 'Fire', 'Poison', 'Flying'],
            'Ghost': ['Poison', 'Bug'],
            'Dragon': ['Fire', 'Water', 'Electric', 'Grass'],
            'Dark': ['Ghost', 'Dark'],
            'Steel': ['Normal', 'Grass', 'Ice', 'Flying', 'Psychic', 
                     'Bug', 'Rock', 'Dragon', 'Steel', 'Fairy'],
            'Fairy': ['Fighting', 'Bug', 'Dark']
        }
    
    def analyze_team_coverage(self, team: List[str]) -> Dict:
        """Analyze type coverage and weaknesses"""
        if not team:
            return {}
        
        # Get Pokemon data for team
        team_df = self.pokemon_data[self.pokemon_data['name'].isin(team)]
        
        # Collect all types
        team_types = []
        for _, pokemon in team_df.iterrows():
            team_types.append(pokemon['type_1'])
            if pd.notna(pokemon.get('type_2')):
                team_types.append(pokemon['type_2'])
        
        # Analyze weaknesses
        all_weaknesses = []
        for _, pokemon in team_df.iterrows():
            types = [pokemon['type_1']]
            if pd.notna(pokemon.get('type_2')):
                types.append(pokemon['type_2'])
            
            for ptype in types:
                all_weaknesses.extend(self.weaknesses.get(ptype, []))
        
        weakness_counts = Counter(all_weaknesses)
        
        # Analyze resistances
        all_resistances = []
        for ptype in team_types:
            all_resistances.extend(self.resistances.get(ptype, []))
        
        resistance_counts = Counter(all_resistances)
        
        return {
            'team_types': team_types,
            'weaknesses': dict(weakness_counts),
            'resistances': dict(resistance_counts),
            'type_coverage': len(set(team_types))
        }
    
    def recommend_team(self, tier: str = 'OU', role_balance: bool = True,
                      seed_pokemon: List[str] = None) -> List[Dict]:
        """
        Recommend a 6-Pokemon team
        
        Args:
            tier: Competitive tier to build for
            role_balance: Balance roles (sweeper/tank/support)
            seed_pokemon: Start with these Pokemon
        """
        team = []
        
        # Get Pokemon from specified tier
        tier_pokemon = self.tier_data[self.tier_data['tier'] == tier]
        
        if tier_pokemon.empty:
            tier_pokemon = self.tier_data.head(100)
        
        # Merge with full Pokemon data
        available = self.pokemon_data[
            self.pokemon_data['name'].isin(tier_pokemon['pokemon'])
        ].copy()
        
        # Add seed Pokemon if provided
        if seed_pokemon:
            for pokemon in seed_pokemon:
                if pokemon in available['name'].values:
                    team.append(pokemon)
        
        # Build team to 6 Pokemon
        while len(team) < 6 and len(available) > 0:
            # Analyze current team
            coverage = self.analyze_team_coverage(team)
            
            # Score remaining Pokemon
            scores = []
            for _, pokemon in available.iterrows():
                if pokemon['name'] in team:
                    continue
                
                score = self._score_pokemon_for_team(
                    pokemon,
                    team,
                    coverage
                )
                scores.append((pokemon['name'], score))
            
            # Sort by score and pick best
            scores.sort(key=lambda x: x[1], reverse=True)
            
            if scores:
                best_pokemon = scores[0][0]
                team.append(best_pokemon)
        
        # Build detailed team info
        team_details = []
        for pokemon_name in team:
            pokemon = self.pokemon_data[
                self.pokemon_data['name'] == pokemon_name
            ].iloc[0]
            
            details = {
                'name': pokemon_name,
                'type_1': pokemon['type_1'],
                'type_2': pokemon.get('type_2'),
                'hp': pokemon['hp'],
                'attack': pokemon['attack'],
                'defense': pokemon['defense'],
                'sp_attack': pokemon['sp_attack'],
                'sp_defense': pokemon['sp_defense'],
                'speed': pokemon['speed'],
                'total': pokemon['total_points'],
                'role': self._determine_role(pokemon)
            }
            team_details.append(details)
        
        return team_details
    
    def _score_pokemon_for_team(self, pokemon: pd.Series, 
                                team: List[str], 
                                coverage: Dict) -> float:
        """Score how well a Pokemon fits the team"""
        score = 0.0
        
        # Base score from stats
        score += pokemon['total_points'] / 10
        
        # Type coverage bonus
        pokemon_types = [pokemon['type_1']]
        if pd.notna(pokemon.get('type_2')):
            pokemon_types.append(pokemon['type_2'])
        
        for ptype in pokemon_types:
            if ptype not in coverage.get('team_types', []):
                score += 50  # New type coverage
        
        # Weakness coverage bonus
        weaknesses = coverage.get('weaknesses', {})
        for ptype in pokemon_types:
            resistances = self.resistances.get(ptype, [])
            for weakness in weaknesses:
                if weakness in resistances:
                    score += 30  # Covers team weakness
        
        # Usage bonus (popular Pokemon)
        usage_data = self.usage_stats[
            self.usage_stats['pokemon'] == pokemon['name']
        ]
        if not usage_data.empty:
            avg_usage = usage_data['usage_percent'].mean()
            score += avg_usage * 5
        
        # Avoid duplicates
        if pokemon['name'] in team:
            score = 0
        
        return score
    
    def _determine_role(self, pokemon: pd.Series) -> str:
        """Determine Pokemon's role based on stats"""
        atk = pokemon['attack']
        sp_atk = pokemon['sp_attack']
        defense = pokemon['defense']
        sp_def = pokemon['sp_defense']
        hp = pokemon['hp']
        speed = pokemon['speed']
        
        # Physical Sweeper
        if atk >= 110 and speed >= 90:
            return "Physical Sweeper"
        
        # Special Sweeper
        if sp_atk >= 110 and speed >= 90:
            return "Special Sweeper"
        
        # Physical Tank
        if hp >= 90 and defense >= 90:
            return "Physical Tank"
        
        # Special Tank
        if hp >= 90 and sp_def >= 90:
            return "Special Tank"
        
        # Support
        if speed >= 80 and (defense + sp_def) >= 150:
            return "Support"
        
        # Balanced
        return "Balanced"
    
    def render_recommender(self):
        """Render the team recommender interface"""
        st.title("🤖 AI Team Recommender")
        st.markdown("*Get optimal Pokemon team suggestions*")
        
        # Configuration
        st.subheader("⚙️ Team Builder Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tier = st.selectbox(
                "Competitive Tier",
                ['AG', 'Uber', 'OU', 'UU', 'RU', 'NU', 'PU', 'ZU'],
                index=2
            )
        
        with col2:
            role_balance = st.checkbox(
                "Balance Team Roles",
                value=True,
                help="Ensure mix of sweepers, tanks, and support"
            )
        
        # Optional seed Pokemon
        st.subheader("🌱 Seed Pokemon (Optional)")
        st.markdown("*Start your team with specific Pokemon*")
        
        seed_pokemon = st.multiselect(
            "Select up to 3 Pokemon to start with",
            self.pokemon_data['name'].unique(),
            max_selections=3
        )
        
        st.divider()
        
        # Generate team button
        if st.button("🎲 Generate Team", type="primary", 
                     use_container_width=True):
            with st.spinner("Analyzing meta and building team..."):
                team = self.recommend_team(
                    tier=tier,
                    role_balance=role_balance,
                    seed_pokemon=seed_pokemon
                )
                
                if team:
                    st.session_state['recommended_team'] = team
                    st.success("✅ Team generated successfully!")
                else:
                    st.error("❌ Could not generate team")
        
        # Display team if generated
        if 'recommended_team' in st.session_state:
            team = st.session_state['recommended_team']
            self._display_team(team)
    
    def _display_team(self, team: List[Dict]):
        """Display the recommended team"""
        st.header("👥 Your Recommended Team")
        
        # Team overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_bst = sum(p['total'] for p in team) / len(team)
            st.metric("Average BST", f"{avg_bst:.0f}")
        
        with col2:
            types = set()
            for p in team:
                types.add(p['type_1'])
                if p['type_2']:
                    types.add(p['type_2'])
            st.metric("Type Coverage", len(types))
        
        with col3:
            roles = set(p['role'] for p in team)
            st.metric("Unique Roles", len(roles))
        
        st.divider()
        
        # Display each Pokemon
        for idx, pokemon in enumerate(team, 1):
            with st.expander(f"#{idx} - {pokemon['name']} ({pokemon['role']})"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    types_str = pokemon['type_1']
                    if pokemon['type_2']:
                        types_str += f" / {pokemon['type_2']}"
                    st.markdown(f"**Types:** {types_str}")
                    st.markdown(f"**BST:** {pokemon['total']}")
                    st.markdown(f"**Role:** {pokemon['role']}")
                
                with col2:
                    # Stats table
                    stats = {
                        'HP': pokemon['hp'],
                        'Attack': pokemon['attack'],
                        'Defense': pokemon['defense'],
                        'Sp. Atk': pokemon['sp_attack'],
                        'Sp. Def': pokemon['sp_defense'],
                        'Speed': pokemon['speed']
                    }
                    
                    st.dataframe(
                        pd.DataFrame([stats]),
                        use_container_width=True,
                        hide_index=True
                    )
        
        st.divider()
        
        # Team analysis
        st.subheader("📊 Team Analysis")
        
        team_names = [p['name'] for p in team]
        coverage = self.analyze_team_coverage(team_names)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**⚠️ Team Weaknesses**")
            weaknesses = coverage.get('weaknesses', {})
            
            if weaknesses:
                sorted_weak = sorted(
                    weaknesses.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                for wtype, count in sorted_weak[:5]:
                    st.write(f"- {wtype}: {count}x")
            else:
                st.success("No major weaknesses!")
        
        with col2:
            st.markdown("**✅ Team Resistances**")
            resistances = coverage.get('resistances', {})
            
            if resistances:
                sorted_res = sorted(
                    resistances.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                for rtype, count in sorted_res[:5]:
                    st.write(f"- {rtype}: {count}x")
        
        st.divider()
        
        # Export options
        st.subheader("💾 Export Team")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Copy Team (Text)"):
                team_text = "\n".join([
                    f"{i}. {p['name']} ({p['type_1']}"
                    f"{f'/{p["type_2"]}' if p['type_2'] else ''})"
                    for i, p in enumerate(team, 1)
                ])
                st.code(team_text)
        
        with col2:
            if st.button("📄 Export as JSON"):
                team_json = json.dumps(team, indent=2)
                st.download_button(
                    "Download JSON",
                    team_json,
                    file_name="pokemon_team.json",
                    mime="application/json"
                )


def main():
    """Main function for standalone testing"""
    st.set_page_config(
        page_title="Team Recommender",
        layout="wide",
        page_icon="🤖"
    )
    
    recommender = TeamRecommender()
    recommender.render_recommender()


if __name__ == "__main__":
    main()
