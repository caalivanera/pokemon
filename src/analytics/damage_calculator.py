"""
Pokemon Damage Calculator
Implements exact damage formula from Pokemon games
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Optional, Tuple
import math


class DamageCalculator:
    """Calculate exact Pokemon battle damage"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.load_data()
        self.load_type_chart()
    
    def load_data(self):
        """Load Pokemon and move data"""
        try:
            self.pokemon_data = pd.read_csv(self.data_dir / "pokemon.csv")
            
            # Load moveset database
            moveset_path = self.data_dir / "moves" / "pokemon_movesets.json"
            with open(moveset_path, 'r') as f:
                self.movesets = json.load(f)
            
            print("✅ Data loaded successfully")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.movesets = {}
    
    def load_type_chart(self):
        """Load type effectiveness chart"""
        # Complete 18x18 type effectiveness matrix
        self.type_chart = {
            'Normal': {'Rock': 0.5, 'Ghost': 0, 'Steel': 0.5},
            'Fire': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2.0, 'Ice': 2.0, 
                    'Bug': 2.0, 'Rock': 0.5, 'Dragon': 0.5, 'Steel': 2.0},
            'Water': {'Fire': 2.0, 'Water': 0.5, 'Grass': 0.5, 'Ground': 2.0,
                     'Rock': 2.0, 'Dragon': 0.5},
            'Electric': {'Water': 2.0, 'Electric': 0.5, 'Grass': 0.5, 
                        'Ground': 0, 'Flying': 2.0, 'Dragon': 0.5},
            'Grass': {'Fire': 0.5, 'Water': 2.0, 'Grass': 0.5, 'Poison': 0.5,
                     'Ground': 2.0, 'Flying': 0.5, 'Bug': 0.5, 'Rock': 2.0,
                     'Dragon': 0.5, 'Steel': 0.5},
            'Ice': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2.0, 'Ice': 0.5,
                   'Ground': 2.0, 'Flying': 2.0, 'Dragon': 2.0, 'Steel': 0.5},
            'Fighting': {'Normal': 2.0, 'Ice': 2.0, 'Poison': 0.5, 
                        'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 
                        'Rock': 2.0, 'Ghost': 0, 'Dark': 2.0, 'Steel': 2.0,
                        'Fairy': 0.5},
            'Poison': {'Grass': 2.0, 'Poison': 0.5, 'Ground': 0.5, 
                      'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0, 'Fairy': 2.0},
            'Ground': {'Fire': 2.0, 'Electric': 2.0, 'Grass': 0.5, 
                      'Poison': 2.0, 'Flying': 0, 'Bug': 0.5, 'Rock': 2.0,
                      'Steel': 2.0},
            'Flying': {'Electric': 0.5, 'Grass': 2.0, 'Fighting': 2.0,
                      'Bug': 2.0, 'Rock': 0.5, 'Steel': 0.5},
            'Psychic': {'Fighting': 2.0, 'Poison': 2.0, 'Psychic': 0.5,
                       'Dark': 0, 'Steel': 0.5},
            'Bug': {'Fire': 0.5, 'Grass': 2.0, 'Fighting': 0.5, 'Poison': 0.5,
                   'Flying': 0.5, 'Psychic': 2.0, 'Ghost': 0.5, 'Dark': 2.0,
                   'Steel': 0.5, 'Fairy': 0.5},
            'Rock': {'Fire': 2.0, 'Ice': 2.0, 'Fighting': 0.5, 'Ground': 0.5,
                    'Flying': 2.0, 'Bug': 2.0, 'Steel': 0.5},
            'Ghost': {'Normal': 0, 'Psychic': 2.0, 'Ghost': 2.0, 'Dark': 0.5},
            'Dragon': {'Dragon': 2.0, 'Steel': 0.5, 'Fairy': 0},
            'Dark': {'Fighting': 0.5, 'Psychic': 2.0, 'Ghost': 2.0,
                    'Dark': 0.5, 'Fairy': 0.5},
            'Steel': {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Ice': 2.0,
                     'Rock': 2.0, 'Steel': 0.5, 'Fairy': 2.0},
            'Fairy': {'Fire': 0.5, 'Fighting': 2.0, 'Poison': 0.5, 
                     'Dragon': 2.0, 'Dark': 2.0, 'Steel': 0.5}
        }
    
    def get_type_effectiveness(self, attack_type: str, 
                               defend_types: list) -> float:
        """Calculate type effectiveness multiplier"""
        multiplier = 1.0
        
        for defend_type in defend_types:
            if attack_type in self.type_chart:
                multiplier *= self.type_chart[attack_type].get(defend_type, 1.0)
        
        return multiplier
    
    def calculate_damage(self, attacker: Dict, defender: Dict, 
                        move: Dict, modifiers: Dict) -> Dict:
        """
        Calculate damage using Gen 5+ formula
        
        Damage = ((2 * Level / 5 + 2) * Power * A/D / 50 + 2) * Modifiers
        """
        level = attacker.get('level', 100)
        power = move.get('power', 0)
        
        if power == 0:
            return {
                'damage': 0,
                'min_damage': 0,
                'max_damage': 0,
                'percentage': "0%",
                'effectiveness': "Status Move"
            }
        
        # Determine if Physical or Special
        category = move.get('category', 'Physical')
        
        if category == 'Physical':
            attack_stat = attacker.get('attack', 100)
            defense_stat = defender.get('defense', 100)
        else:  # Special
            attack_stat = attacker.get('sp_attack', 100)
            defense_stat = defender.get('sp_defense', 100)
        
        # Apply stat modifiers (boosts/drops from -6 to +6)
        attack_boost = modifiers.get('attack_boost', 0)
        defense_boost = modifiers.get('defense_boost', 0)
        
        attack_multiplier = self._get_stat_multiplier(attack_boost)
        defense_multiplier = self._get_stat_multiplier(defense_boost)
        
        attack_stat = int(attack_stat * attack_multiplier)
        defense_stat = int(defense_stat * defense_multiplier)
        
        # Base damage calculation
        damage = ((2 * level / 5 + 2) * power * attack_stat / defense_stat) / 50 + 2
        
        # Apply STAB (Same Type Attack Bonus)
        attacker_types = [attacker.get('type_1'), attacker.get('type_2')]
        move_type = move.get('type', 'Normal')
        
        if move_type in attacker_types:
            damage *= modifiers.get('stab', 1.5)
        
        # Type effectiveness
        defender_types = [t for t in [defender.get('type_1'), 
                                      defender.get('type_2')] if t]
        effectiveness = self.get_type_effectiveness(move_type, defender_types)
        damage *= effectiveness
        
        # Weather modifier
        damage *= modifiers.get('weather', 1.0)
        
        # Item modifier
        damage *= modifiers.get('item', 1.0)
        
        # Ability modifier
        damage *= modifiers.get('ability', 1.0)
        
        # Critical hit
        if modifiers.get('critical', False):
            damage *= 1.5
        
        # Random factor (0.85 to 1.0)
        min_damage = int(damage * 0.85)
        max_damage = int(damage * 1.0)
        avg_damage = int((min_damage + max_damage) / 2)
        
        # Calculate percentage of defender's HP
        defender_hp = defender.get('hp', 100)
        percentage = (avg_damage / defender_hp) * 100
        
        # Effectiveness description
        if effectiveness == 0:
            eff_text = "No Effect"
        elif effectiveness < 0.5:
            eff_text = "Not Very Effective (0.25x)"
        elif effectiveness == 0.5:
            eff_text = "Not Very Effective (0.5x)"
        elif effectiveness == 1.0:
            eff_text = "Neutral"
        elif effectiveness == 2.0:
            eff_text = "Super Effective! (2x)"
        else:
            eff_text = "Super Effective! (4x)"
        
        return {
            'damage': avg_damage,
            'min_damage': min_damage,
            'max_damage': max_damage,
            'percentage': f"{percentage:.1f}%",
            'effectiveness': eff_text,
            'type_multiplier': effectiveness,
            'ohko': avg_damage >= defender_hp,
            'twoko': (avg_damage * 2) >= defender_hp
        }
    
    def _get_stat_multiplier(self, boost: int) -> float:
        """Convert stat boost/drop to multiplier"""
        if boost >= 0:
            return (2 + boost) / 2
        else:
            return 2 / (2 - boost)
    
    def render_calculator(self):
        """Render the damage calculator interface"""
        st.title("⚔️ Pokemon Damage Calculator")
        st.markdown("*Calculate exact damage between any two Pokemon*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔴 Attacker")
            attacker = self._render_pokemon_selector("attacker")
            move = self._render_move_selector(attacker)
        
        with col2:
            st.subheader("🔵 Defender")
            defender = self._render_pokemon_selector("defender")
        
        st.divider()
        
        # Modifiers
        st.subheader("⚙️ Battle Conditions")
        modifiers = self._render_modifiers()
        
        st.divider()
        
        # Calculate button
        if st.button("⚔️ Calculate Damage", type="primary", 
                     use_container_width=True):
            if attacker and defender and move:
                result = self.calculate_damage(attacker, defender, 
                                               move, modifiers)
                self._display_results(result, attacker, defender, move)
            else:
                st.error("Please select attacker, defender, and move")
    
    def _render_pokemon_selector(self, key: str) -> Optional[Dict]:
        """Render Pokemon selection interface"""
        pokemon_names = sorted(self.pokemon_data['name'].unique())
        
        selected = st.selectbox(
            "Select Pokemon",
            pokemon_names,
            key=f"{key}_pokemon"
        )
        
        if selected:
            pokemon = self.pokemon_data[
                self.pokemon_data['name'] == selected
            ].iloc[0].to_dict()
            
            # Display stats
            with st.expander("📊 View Stats"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("HP", pokemon['hp'])
                    st.metric("Attack", pokemon['attack'])
                
                with col2:
                    st.metric("Defense", pokemon['defense'])
                    st.metric("Sp. Atk", pokemon['sp_attack'])
                
                with col3:
                    st.metric("Sp. Def", pokemon['sp_defense'])
                    st.metric("Speed", pokemon['speed'])
                
                st.write(f"**Type:** {pokemon['type_1']}" + 
                        (f"/{pokemon['type_2']}" if pd.notna(pokemon.get('type_2')) 
                         else ""))
            
            # Level
            pokemon['level'] = st.number_input(
                "Level",
                min_value=1,
                max_value=100,
                value=100,
                key=f"{key}_level"
            )
            
            return pokemon
        
        return None
    
    def _render_move_selector(self, attacker: Optional[Dict]) -> Optional[Dict]:
        """Render move selection interface"""
        if not attacker:
            st.info("Select an attacker first")
            return None
        
        pokemon_name = attacker['name']
        
        # Get moves for this Pokemon
        pokemon_moves = []
        if pokemon_name in self.movesets:
            pokemon_moves = self.movesets[pokemon_name].get('moves', [])
        
        if not pokemon_moves:
            st.warning("No moveset data available")
            return None
        
        move_names = [m['name'] for m in pokemon_moves]
        
        selected_move = st.selectbox(
            "Select Move",
            move_names,
            key="attacker_move"
        )
        
        if selected_move:
            move = next((m for m in pokemon_moves if m['name'] == selected_move),
                       None)
            
            if move:
                with st.expander("ℹ️ Move Details"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Type:** {move.get('type', 'Unknown')}")
                        st.write(f"**Category:** {move.get('category', 'Unknown')}")
                    
                    with col2:
                        st.write(f"**Power:** {move.get('power', 0)}")
                        st.write(f"**Accuracy:** {move.get('accuracy', 0)}")
                
                return move
        
        return None
    
    def _render_modifiers(self) -> Dict:
        """Render battle modifier options"""
        col1, col2, col3 = st.columns(3)
        
        modifiers = {}
        
        with col1:
            st.markdown("**Stat Boosts**")
            modifiers['attack_boost'] = st.slider(
                "Attack Boost",
                min_value=-6,
                max_value=6,
                value=0,
                help="Stat stages from moves like Swords Dance"
            )
            
            modifiers['defense_boost'] = st.slider(
                "Defense Boost",
                min_value=-6,
                max_value=6,
                value=0
            )
        
        with col2:
            st.markdown("**Battle Effects**")
            modifiers['critical'] = st.checkbox("Critical Hit")
            
            weather = st.selectbox(
                "Weather",
                ["None", "Sun", "Rain", "Sand", "Hail", "Snow"]
            )
            
            # Weather modifiers (simplified)
            weather_mods = {
                "Sun": 1.5,  # Fire boost
                "Rain": 1.5,  # Water boost
                "None": 1.0
            }
            modifiers['weather'] = weather_mods.get(weather, 1.0)
        
        with col3:
            st.markdown("**Items & Abilities**")
            
            item = st.selectbox(
                "Held Item",
                ["None", "Life Orb", "Choice Band", "Choice Specs"]
            )
            
            item_mods = {
                "Life Orb": 1.3,
                "Choice Band": 1.5,
                "Choice Specs": 1.5,
                "None": 1.0
            }
            modifiers['item'] = item_mods.get(item, 1.0)
            
            modifiers['ability'] = st.number_input(
                "Ability Modifier",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.25,
                help="e.g., 1.5 for Adaptability, 1.3 for Technician"
            )
        
        return modifiers
    
    def _display_results(self, result: Dict, attacker: Dict, 
                        defender: Dict, move: Dict):
        """Display calculation results"""
        st.success("✅ Damage Calculated!")
        
        # Main damage display
        st.markdown(f"## {result['damage']} Damage")
        st.markdown(f"**Range:** {result['min_damage']} - {result['max_damage']}")
        st.markdown(f"**{result['percentage']} of defender's HP**")
        
        # Effectiveness
        if result['type_multiplier'] == 0:
            st.error(f"❌ {result['effectiveness']}")
        elif result['type_multiplier'] >= 2.0:
            st.success(f"✅ {result['effectiveness']}")
        elif result['type_multiplier'] < 1.0:
            st.warning(f"⚠️ {result['effectiveness']}")
        else:
            st.info(f"ℹ️ {result['effectiveness']}")
        
        # KO prediction
        col1, col2 = st.columns(2)
        
        with col1:
            if result['ohko']:
                st.success("💥 **OHKO** (One-Hit KO)")
            else:
                st.info(f"Requires multiple hits")
        
        with col2:
            if result['twoko']:
                st.success("💥 **2HKO** (Two-Hit KO)")
        
        # Detailed breakdown
        with st.expander("📊 Detailed Breakdown"):
            st.write(f"**Attacker:** {attacker['name']} (Lv. {attacker['level']})")
            st.write(f"**Defender:** {defender['name']} (Lv. {defender['level']})")
            st.write(f"**Move:** {move['name']} ({move['type']})")
            st.write(f"**Base Power:** {move.get('power', 0)}")
            st.write(f"**Type Multiplier:** {result['type_multiplier']}x")


def main():
    """Main function for standalone testing"""
    st.set_page_config(
        page_title="Damage Calculator",
        layout="wide",
        page_icon="⚔️"
    )
    
    calculator = DamageCalculator()
    calculator.render_calculator()


if __name__ == "__main__":
    main()
