"""
Team Builder Feature
Build Pokemon teams with type coverage analysis and stat tracking
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict
from .type_calculator import get_pokemon_weaknesses, get_offensive_coverage


class PokemonTeam:
    """Pokemon Team with coverage analysis"""
    
    def __init__(self):
        self.team = []
        self.max_size = 6
    
    def add_pokemon(self, pokemon: dict) -> bool:
        """Add a Pokemon to the team"""
        if len(self.team) >= self.max_size:
            return False
        if any(p['pokedex_number'] == pokemon['pokedex_number'] for p in self.team):
            return False
        self.team.append(pokemon)
        return True
    
    def remove_pokemon(self, index: int):
        """Remove a Pokemon from the team by index"""
        if 0 <= index < len(self.team):
            self.team.pop(index)
    
    def clear_team(self):
        """Clear all Pokemon from team"""
        self.team = []
    
    def get_size(self) -> int:
        """Get current team size"""
        return len(self.team)
    
    def is_full(self) -> bool:
        """Check if team is full"""
        return len(self.team) >= self.max_size
    
    def get_team_types(self) -> List[str]:
        """Get all unique types in the team"""
        types = set()
        for pokemon in self.team:
            types.add(pokemon['type_1'])
            if pd.notna(pokemon.get('type_2')):
                types.add(pokemon['type_2'])
        return list(types)
    
    def calculate_team_coverage(self) -> Dict:
        """Calculate offensive and defensive coverage for the team"""
        # Offensive coverage (what types the team can hit super effectively)
        offensive_hits = set()
        offensive_weak = set()
        
        # Defensive weaknesses (what types the team is weak to)
        defensive_weak = {}  # type -> count
        defensive_resist = {}  # type -> count
        defensive_immune = {}  # type -> count
        
        for pokemon in self.team:
            types = [pokemon['type_1']]
            if pd.notna(pokemon.get('type_2')):
                types.append(pokemon['type_2'])
            
            # Offensive coverage
            coverage = get_offensive_coverage(types)
            offensive_hits.update(coverage['super_effective'])
            offensive_weak.update(coverage['not_effective'] + coverage['no_effect'])
            
            # Defensive coverage
            weaknesses = get_pokemon_weaknesses(types)
            for wtype in weaknesses['weak'] + weaknesses['very_weak']:
                defensive_weak[wtype] = defensive_weak.get(wtype, 0) + 1
            for rtype in weaknesses['resistant'] + weaknesses['very_resistant']:
                defensive_resist[rtype] = defensive_resist.get(rtype, 0) + 1
            for itype in weaknesses['immune']:
                defensive_immune[itype] = defensive_immune.get(itype, 0) + 1
        
        return {
            'offensive_coverage': list(offensive_hits),
            'offensive_count': len(offensive_hits),
            'offensive_weak': list(offensive_weak),
            'defensive_weaknesses': defensive_weak,
            'defensive_resistances': defensive_resist,
            'defensive_immunities': defensive_immune,
            'total_weaknesses': sum(defensive_weak.values()),
            'total_resistances': sum(defensive_resist.values())
        }
    
    def get_team_stats(self) -> Dict:
        """Calculate average team stats"""
        if not self.team:
            return {}
        
        stats = {
            'hp': 0, 'attack': 0, 'defense': 0,
            'sp_attack': 0, 'sp_defense': 0, 'speed': 0,
            'total_points': 0
        }
        
        for pokemon in self.team:
            stats['hp'] += pokemon.get('hp', 0)
            stats['attack'] += pokemon.get('attack', 0)
            stats['defense'] += pokemon.get('defense', 0)
            stats['sp_attack'] += pokemon.get('sp_attack', 0)
            stats['sp_defense'] += pokemon.get('sp_defense', 0)
            stats['speed'] += pokemon.get('speed', 0)
            stats['total_points'] += pokemon.get('total_points', 0)
        
        team_size = len(self.team)
        return {k: round(v / team_size, 1) for k, v in stats.items()}


def display_team_builder(df: pd.DataFrame):
    """Display the team builder interface"""
    st.markdown("### 👥 Pokemon Team Builder")
    st.markdown("Build your perfect team with type coverage analysis")
    
    # Initialize team in session state
    if 'pokemon_team' not in st.session_state:
        st.session_state.pokemon_team = PokemonTeam()
    
    team = st.session_state.pokemon_team
    
    # Team management controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Team Size:** {team.get_size()}/6")
    
    with col2:
        if st.button("🗑️ Clear Team", use_container_width=True):
            team.clear_team()
            st.rerun()
    
    with col3:
        if st.button("💾 Export Team", use_container_width=True):
            export_team(team)
    
    # Add Pokemon selector
    st.markdown("#### ➕ Add Pokemon to Team")
    
    search_col, add_col = st.columns([3, 1])
    
    with search_col:
        search_query = st.text_input(
            "Search Pokemon by name or number",
            placeholder="e.g., Charizard or 006",
            label_visibility="collapsed"
        )
    
    # Filter Pokemon
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search_query, case=False, na=False) |
            filtered_df['pokedex_number'].astype(str).str.contains(search_query, na=False)
        ]
    
    # Select Pokemon to add
    if not filtered_df.empty:
        selected_pokemon = st.selectbox(
            "Select Pokemon",
            options=filtered_df.index,
            format_func=lambda x: f"#{filtered_df.loc[x, 'pokedex_number']:03d} - {filtered_df.loc[x, 'name']} ({filtered_df.loc[x, 'type_1']}{f'/{filtered_df.loc[x, \"type_2\"]}' if pd.notna(filtered_df.loc[x, 'type_2']) else ''})",
            label_visibility="collapsed"
        )
        
        with add_col:
            if st.button("➕ Add", use_container_width=True, disabled=team.is_full()):
                pokemon_data = filtered_df.loc[selected_pokemon].to_dict()
                if team.add_pokemon(pokemon_data):
                    st.success(f"Added {pokemon_data['name']}!")
                    st.rerun()
                else:
                    st.error("Pokemon already in team or team is full!")
    
    st.markdown("---")
    
    # Display current team
    if team.get_size() == 0:
        st.info("👆 Add Pokemon to your team to see coverage analysis")
        return
    
    st.markdown("#### 🎮 Your Team")
    
    # Display team members in columns
    cols = st.columns(min(3, team.get_size()))
    for i, pokemon in enumerate(team.team):
        with cols[i % 3]:
            display_team_pokemon_card(pokemon, i, team)
    
    st.markdown("---")
    
    # Team statistics
    st.markdown("#### 📊 Team Statistics")
    
    stats_cols = st.columns(2)
    
    with stats_cols[0]:
        st.markdown("##### Average Stats")
        avg_stats = team.get_team_stats()
        if avg_stats:
            # Create radar chart
            fig = create_stats_radar(avg_stats)
            st.plotly_chart(fig, use_container_width=True)
    
    with stats_cols[1]:
        st.markdown("##### Stat Distribution")
        if avg_stats:
            for stat, value in avg_stats.items():
                if stat != 'total_points':
                    st.metric(
                        label=stat.replace('_', ' ').title(),
                        value=f"{value:.1f}"
                    )
    
    # Type coverage analysis
    st.markdown("---")
    st.markdown("#### ⚔️ Type Coverage Analysis")
    
    coverage = team.calculate_team_coverage()
    
    cov_cols = st.columns(3)
    
    with cov_cols[0]:
        st.markdown("##### 🎯 Offensive Coverage")
        st.metric(
            "Types Hit Super Effectively",
            f"{coverage['offensive_count']}/18"
        )
        if coverage['offensive_coverage']:
            st.success(f"**Can Hit:** {', '.join(sorted(coverage['offensive_coverage']))}")
        if coverage['offensive_weak']:
            st.warning(f"**Struggles Against:** {', '.join(sorted(coverage['offensive_weak']))}")
    
    with cov_cols[1]:
        st.markdown("##### 🛡️ Defensive Resistances")
        st.metric(
            "Total Resistances",
            coverage['total_resistances']
        )
        if coverage['defensive_resistances']:
            resist_list = sorted(
                coverage['defensive_resistances'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            resist_text = ', '.join([f"{t} (x{c})" for t, c in resist_list])
            st.info(f"**Resists:** {resist_text}")
    
    with cov_cols[2]:
        st.markdown("##### ⚠️ Team Weaknesses")
        st.metric(
            "Total Weaknesses",
            coverage['total_weaknesses'],
            delta=None
        )
        if coverage['defensive_weaknesses']:
            weak_list = sorted(
                coverage['defensive_weaknesses'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            weak_text = ', '.join([f"{t} (x{c})" for t, c in weak_list])
            st.error(f"**Weak To:** {weak_text}")
    
    # Coverage heatmap
    st.markdown("---")
    st.markdown("#### 🔥 Coverage Heatmap")
    display_coverage_heatmap(team)


def display_team_pokemon_card(pokemon: dict, index: int, team: PokemonTeam):
    """Display a Pokemon card in the team"""
    with st.container():
        st.markdown(f"""
        <div style='
            padding: 1rem;
            border: 2px solid #374151;
            border-radius: 12px;
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
            margin-bottom: 1rem;
        '>
            <h4>#{pokemon['pokedex_number']:03d} {pokemon['name']}</h4>
            <p><strong>Type:</strong> {pokemon['type_1']}{f"/{pokemon['type_2']}" if pd.notna(pokemon.get('type_2')) else ""}</p>
            <p><strong>BST:</strong> {pokemon.get('total_points', 0)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🗑️ Remove", key=f"remove_{index}", use_container_width=True):
            team.remove_pokemon(index)
            st.rerun()


def create_stats_radar(stats: Dict) -> go.Figure:
    """Create a radar chart for team stats"""
    categories = ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']
    values = [
        stats['hp'],
        stats['attack'],
        stats['defense'],
        stats['sp_attack'],
        stats['sp_defense'],
        stats['speed']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Team Average',
        line=dict(color='#22c55e', width=2),
        fillcolor='rgba(34, 197, 94, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 150]
            )
        ),
        showlegend=False,
        height=400
    )
    
    return fig


def display_coverage_heatmap(team: PokemonTeam):
    """Display type coverage heatmap for the team"""
    import plotly.express as px
    
    # Get all type matchups for team
    all_types = [
        'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
        'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug',
        'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'
    ]
    
    # Create matrix
    matrix_data = []
    for pokemon in team.team:
        types = [pokemon['type_1']]
        if pd.notna(pokemon.get('type_2')):
            types.append(pokemon['type_2'])
        
        coverage = get_offensive_coverage(types)
        row = [1 if t in coverage['super_effective'] else 0 for t in all_types]
        matrix_data.append(row)
    
    if not matrix_data:
        return
    
    # Create DataFrame
    df = pd.DataFrame(
        matrix_data,
        index=[f"#{p['pokedex_number']:03d} {p['name']}" for p in team.team],
        columns=all_types
    )
    
    # Create heatmap
    fig = px.imshow(
        df,
        labels=dict(x="Defending Type", y="Team Member", color="Coverage"),
        color_continuous_scale=['#1e293b', '#22c55e'],
        text_auto=False
    )
    
    fig.update_layout(
        title="Team Type Coverage (Green = Super Effective)",
        height=300 + (len(team.team) * 40)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def export_team(team: PokemonTeam):
    """Export team to JSON"""
    import json
    
    team_data = {
        'team_size': team.get_size(),
        'pokemon': [
            {
                'number': p['pokedex_number'],
                'name': p['name'],
                'type_1': p['type_1'],
                'type_2': p.get('type_2') if pd.notna(p.get('type_2')) else None,
                'hp': p.get('hp', 0),
                'attack': p.get('attack', 0),
                'defense': p.get('defense', 0),
                'sp_attack': p.get('sp_attack', 0),
                'sp_defense': p.get('sp_defense', 0),
                'speed': p.get('speed', 0),
                'total_points': p.get('total_points', 0)
            }
            for p in team.team
        ],
        'coverage': team.calculate_team_coverage()
    }
    
    json_str = json.dumps(team_data, indent=2)
    st.download_button(
        label="💾 Download Team JSON",
        data=json_str,
        file_name="pokemon_team.json",
        mime="application/json"
    )
