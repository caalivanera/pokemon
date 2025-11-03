"""
Sprite Comparison Tool
Provides side-by-side comparison of Pokemon sprites and stats
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import plotly.graph_objects as go


class SpriteComparison:
    """Tool for comparing Pokemon sprites and stats side-by-side"""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the sprite comparison tool"""
        self.data_dir = Path(data_dir)
        self.pokemon_data = None
        self.sprite_base_path = Path("assets/sprites")
        
    def load_data(self) -> bool:
        """Load Pokemon data"""
        try:
            csv_path = self.data_dir / "pokemon.csv"
            if csv_path.exists():
                self.pokemon_data = pd.read_csv(csv_path)
                return True
            else:
                st.error(f"Pokemon data not found at {csv_path}")
                return False
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return False
    
    def get_sprite_path(self, pokemon_name: str, sprite_type: str = "static") -> Optional[Path]:
        """Get the path to a Pokemon sprite"""
        # Clean the name for file path
        clean_name = pokemon_name.lower().replace(" ", "_").replace("'", "")
        
        if sprite_type == "static":
            sprite_path = self.sprite_base_path / "pokemon" / f"{clean_name}.png"
        elif sprite_type == "animated":
            sprite_path = self.sprite_base_path / "pokemon-animated" / f"{clean_name}.gif"
        elif sprite_type == "shiny":
            sprite_path = self.sprite_base_path / "pokemon-shiny" / f"{clean_name}.png"
        else:
            sprite_path = self.sprite_base_path / "pokemon" / f"{clean_name}.png"
        
        return sprite_path if sprite_path.exists() else None
    
    def get_stat_difference(self, base_stats: Dict, compare_stats: Dict) -> Dict[str, int]:
        """Calculate stat differences between two Pokemon"""
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        differences = {}
        
        for stat in stats:
            base_val = base_stats.get(stat, 0)
            comp_val = compare_stats.get(stat, 0)
            differences[stat] = comp_val - base_val
        
        return differences
    
    def render_pokemon_card(self, pokemon_row: pd.Series, show_differences: bool = False, 
                           base_pokemon: Optional[pd.Series] = None):
        """Render a Pokemon card with sprite and stats"""
        
        # Header with name and types
        st.markdown(f"### {pokemon_row['name']}")
        
        # Display types
        type1 = pokemon_row.get('type1', 'Unknown')
        type2 = pokemon_row.get('type2', None)
        
        type_cols = st.columns(2 if type2 and pd.notna(type2) else 1)
        with type_cols[0]:
            st.markdown(f"**Type:** {type1}")
        if type2 and pd.notna(type2):
            with type_cols[1]:
                st.markdown(f"**Type 2:** {type2}")
        
        # Display sprite
        sprite_path = self.get_sprite_path(pokemon_row['name'])
        if sprite_path and sprite_path.exists():
            st.image(str(sprite_path), width=200)
        else:
            st.info("Sprite not available")
        
        # Display stats
        st.markdown("**Base Stats:**")
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        
        for stat in stats:
            stat_value = pokemon_row.get(stat, 0)
            stat_name = stat.replace('_', ' ').title()
            
            if show_differences and base_pokemon is not None:
                base_value = base_pokemon.get(stat, 0)
                diff = stat_value - base_value
                
                if diff > 0:
                    st.markdown(f"**{stat_name}:** {stat_value} "
                              f"<span style='color: green;'>(+{diff})</span>", 
                              unsafe_allow_html=True)
                elif diff < 0:
                    st.markdown(f"**{stat_name}:** {stat_value} "
                              f"<span style='color: red;'>({diff})</span>", 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f"**{stat_name}:** {stat_value}")
            else:
                st.markdown(f"**{stat_name}:** {stat_value}")
        
        # Total stats
        total = sum([pokemon_row.get(stat, 0) for stat in stats])
        st.markdown(f"**Total BST:** {total}")
        
        # Abilities
        abilities = []
        for i in range(1, 4):
            ability = pokemon_row.get(f'ability{i}', None)
            if ability and pd.notna(ability):
                abilities.append(ability)
        
        if abilities:
            st.markdown(f"**Abilities:** {', '.join(abilities)}")
    
    def create_stat_radar_chart(self, pokemon_list: List[pd.Series]) -> go.Figure:
        """Create a radar chart comparing stats of multiple Pokemon"""
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        stat_labels = ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']
        
        fig = go.Figure()
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        for idx, pokemon in enumerate(pokemon_list):
            values = [pokemon.get(stat, 0) for stat in stats]
            values.append(values[0])  # Close the radar
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=stat_labels + [stat_labels[0]],
                fill='toself',
                name=pokemon['name'],
                line=dict(color=colors[idx % len(colors)])
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 255]
                )
            ),
            showlegend=True,
            title="Stat Comparison Radar Chart"
        )
        
        return fig
    
    def create_stat_bar_chart(self, pokemon_list: List[pd.Series]) -> go.Figure:
        """Create a bar chart comparing stats"""
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        stat_labels = ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']
        
        fig = go.Figure()
        
        for pokemon in pokemon_list:
            values = [pokemon.get(stat, 0) for stat in stats]
            fig.add_trace(go.Bar(
                name=pokemon['name'],
                x=stat_labels,
                y=values
            ))
        
        fig.update_layout(
            barmode='group',
            title="Stat Comparison",
            xaxis_title="Stat",
            yaxis_title="Value",
            yaxis=dict(range=[0, 255])
        )
        
        return fig
    
    def render_comparison_tool(self):
        """Render the main comparison interface"""
        st.title("🔍 Pokemon Sprite & Stat Comparison")
        st.markdown("Compare Pokemon side-by-side to analyze differences")
        
        if not self.load_data():
            return
        
        # Comparison mode selection
        st.markdown("---")
        comparison_mode = st.radio(
            "Comparison Mode:",
            ["Variant Comparison", "Custom Comparison", "Type Comparison"],
            horizontal=True
        )
        
        if comparison_mode == "Variant Comparison":
            self._render_variant_comparison()
        elif comparison_mode == "Custom Comparison":
            self._render_custom_comparison()
        else:
            self._render_type_comparison()
    
    def _render_variant_comparison(self):
        """Render variant comparison (base vs regional forms)"""
        st.markdown("### Compare Base Form with Regional Variants")
        
        # Get list of Pokemon with variants
        pokemon_with_variants = self.pokemon_data[
            self.pokemon_data['name'].str.contains('-', na=False)
        ]['name'].str.split('-').str[0].unique()
        
        selected_base = st.selectbox(
            "Select Pokemon:",
            sorted(pokemon_with_variants)
        )
        
        if selected_base:
            # Get base and all variants
            variants = self.pokemon_data[
                self.pokemon_data['name'].str.startswith(selected_base, na=False)
            ]
            
            st.markdown(f"**Found {len(variants)} form(s)**")
            
            # Display in columns
            cols = st.columns(min(len(variants), 4))
            variant_list = []
            
            for idx, (_, variant) in enumerate(variants.iterrows()):
                with cols[idx % 4]:
                    base_pokemon = variants.iloc[0] if idx > 0 else None
                    self.render_pokemon_card(variant, show_differences=(idx > 0), 
                                           base_pokemon=base_pokemon)
                    variant_list.append(variant)
            
            # Show radar chart
            if len(variant_list) > 1:
                st.markdown("---")
                st.plotly_chart(self.create_stat_radar_chart(variant_list), 
                              use_container_width=True)
    
    def _render_custom_comparison(self):
        """Render custom Pokemon comparison"""
        st.markdown("### Compare Any Pokemon")
        
        num_pokemon = st.slider("Number of Pokemon to compare:", 2, 6, 3)
        
        pokemon_names = sorted(self.pokemon_data['name'].unique())
        selected_pokemon = []
        
        cols = st.columns(num_pokemon)
        for i in range(num_pokemon):
            with cols[i]:
                selected = st.selectbox(
                    f"Pokemon {i+1}:",
                    pokemon_names,
                    key=f"compare_{i}"
                )
                selected_pokemon.append(selected)
        
        if st.button("Compare", type="primary"):
            # Get Pokemon data
            pokemon_list = []
            display_cols = st.columns(num_pokemon)
            
            for idx, name in enumerate(selected_pokemon):
                pokemon_row = self.pokemon_data[
                    self.pokemon_data['name'] == name
                ].iloc[0]
                pokemon_list.append(pokemon_row)
                
                with display_cols[idx]:
                    self.render_pokemon_card(pokemon_row)
            
            # Show comparison charts
            st.markdown("---")
            chart_type = st.radio("Chart Type:", ["Radar", "Bar"], horizontal=True)
            
            if chart_type == "Radar":
                st.plotly_chart(self.create_stat_radar_chart(pokemon_list), 
                              use_container_width=True)
            else:
                st.plotly_chart(self.create_stat_bar_chart(pokemon_list), 
                              use_container_width=True)
    
    def _render_type_comparison(self):
        """Render type-based comparison"""
        st.markdown("### Compare Pokemon by Type")
        
        all_types = sorted(self.pokemon_data['type1'].dropna().unique())
        
        col1, col2 = st.columns(2)
        with col1:
            selected_type = st.selectbox("Select Type:", all_types)
        
        with col2:
            sort_by = st.selectbox(
                "Sort by:", 
                ["Total", "HP", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]
            )
        
        if selected_type:
            # Get Pokemon of selected type
            type_pokemon = self.pokemon_data[
                (self.pokemon_data['type1'] == selected_type) | 
                (self.pokemon_data['type2'] == selected_type)
            ].copy()
            
            # Calculate total and sort
            stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
            type_pokemon['total'] = type_pokemon[stats].sum(axis=1)
            
            sort_column = sort_by.lower().replace(' ', '_').replace('.', '')
            type_pokemon = type_pokemon.sort_values(
                by=sort_column if sort_column != 'total' else 'total', 
                ascending=False
            )
            
            # Show top 6
            st.markdown(f"**Top 6 {selected_type}-type Pokemon by {sort_by}**")
            
            top_6 = type_pokemon.head(6)
            cols = st.columns(3)
            
            for idx, (_, pokemon) in enumerate(top_6.iterrows()):
                with cols[idx % 3]:
                    self.render_pokemon_card(pokemon)
            
            # Show radar comparison
            if len(top_6) >= 2:
                st.markdown("---")
                st.plotly_chart(
                    self.create_stat_radar_chart(list(top_6.itertuples(index=False))), 
                    use_container_width=True
                )


def main():
    """Main function for standalone testing"""
    st.set_page_config(page_title="Pokemon Sprite Comparison", layout="wide")
    
    comparison = SpriteComparison()
    comparison.render_comparison_tool()


if __name__ == "__main__":
    main()
