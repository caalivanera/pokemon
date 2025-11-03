"""
Similar Pokemon Finder
ML-based recommendation system to find similar Pokemon
Version 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Tuple
import plotly.graph_objects as go


def calculate_stat_similarity(pokemon1: pd.Series, pokemon2: pd.Series) -> float:
    """
    Calculate statistical similarity using Euclidean distance
    
    Args:
        pokemon1: First Pokemon data
        pokemon2: Second Pokemon data
        
    Returns:
        Similarity score (0-100, higher is more similar)
    """
    stat_cols = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    
    # Get stats for both Pokemon
    stats1 = [pokemon1[col] for col in stat_cols if col in pokemon1.index]
    stats2 = [pokemon2[col] for col in stat_cols if col in pokemon2.index]
    
    if len(stats1) != 6 or len(stats2) != 6:
        return 0.0
    
    # Calculate Euclidean distance
    distance = np.sqrt(sum((s1 - s2) ** 2 for s1, s2 in zip(stats1, stats2)))
    
    # Normalize to 0-100 scale (max distance ~500 for stats)
    # Lower distance = higher similarity
    similarity = max(0, 100 - (distance / 5))
    
    return similarity


def calculate_type_similarity(pokemon1: pd.Series, pokemon2: pd.Series) -> float:
    """
    Calculate type similarity
    
    Args:
        pokemon1: First Pokemon data
        pokemon2: Second Pokemon data
        
    Returns:
        Type similarity score (0-100)
    """
    types1 = {pokemon1['type1']}
    if pd.notna(pokemon1.get('type2')):
        types1.add(pokemon1['type2'])
    
    types2 = {pokemon2['type1']}
    if pd.notna(pokemon2.get('type2')):
        types2.add(pokemon2['type2'])
    
    # Jaccard similarity: intersection / union
    intersection = len(types1 & types2)
    union = len(types1 | types2)
    
    if union == 0:
        return 0.0
    
    return (intersection / union) * 100


def calculate_role_similarity(pokemon1: pd.Series, pokemon2: pd.Series) -> float:
    """
    Calculate role/archetype similarity based on stat distribution
    
    Args:
        pokemon1: First Pokemon data
        pokemon2: Second Pokemon data
        
    Returns:
        Role similarity score (0-100)
    """
    # Define roles based on highest stats
    def get_role(poke: pd.Series) -> str:
        if 'attack' not in poke.index:
            return "unknown"
        
        # Physical attacker
        if poke['attack'] > poke['sp_attack'] and poke['attack'] > poke['defense']:
            return "physical_attacker"
        # Special attacker
        elif poke['sp_attack'] > poke['attack'] and poke['sp_attack'] > poke['sp_defense']:
            return "special_attacker"
        # Physical wall
        elif poke['defense'] > poke['attack'] and poke['defense'] > poke['hp']:
            return "physical_wall"
        # Special wall
        elif poke['sp_defense'] > poke['sp_attack'] and poke['sp_defense'] > poke['hp']:
            return "special_wall"
        # Tank
        elif poke['hp'] > 100:
            return "tank"
        # Fast
        elif poke['speed'] > 100:
            return "speedster"
        # Balanced
        else:
            return "balanced"
    
    role1 = get_role(pokemon1)
    role2 = get_role(pokemon2)
    
    return 100.0 if role1 == role2 else 50.0


def find_similar_pokemon(
    df: pd.DataFrame,
    target_pokemon: pd.Series,
    top_n: int = 10,
    stat_weight: float = 0.6,
    type_weight: float = 0.3,
    role_weight: float = 0.1
) -> List[Tuple[pd.Series, float]]:
    """
    Find most similar Pokemon using weighted similarity metrics
    
    Args:
        df: Pokemon DataFrame
        target_pokemon: Target Pokemon to find similar ones for
        top_n: Number of similar Pokemon to return
        stat_weight: Weight for statistical similarity (0-1)
        type_weight: Weight for type similarity (0-1)
        role_weight: Weight for role similarity (0-1)
        
    Returns:
        List of tuples (pokemon_data, similarity_score) sorted by similarity
    """
    similarities = []
    target_id = target_pokemon['pokedex_number']
    
    for idx, pokemon in df.iterrows():
        # Skip the target Pokemon itself
        if pokemon['pokedex_number'] == target_id:
            continue
        
        # Calculate individual similarities
        stat_sim = calculate_stat_similarity(target_pokemon, pokemon)
        type_sim = calculate_type_similarity(target_pokemon, pokemon)
        role_sim = calculate_role_similarity(target_pokemon, pokemon)
        
        # Weighted overall similarity
        overall_sim = (
            stat_sim * stat_weight +
            type_sim * type_weight +
            role_sim * role_weight
        )
        
        similarities.append((pokemon, overall_sim, stat_sim, type_sim, role_sim))
    
    # Sort by overall similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N with all similarity components
    return similarities[:top_n]


def create_similarity_radar_chart(
    target: pd.Series,
    similar: pd.Series,
    similarity_score: float
) -> go.Figure:
    """
    Create a radar chart comparing stats of two Pokemon
    
    Args:
        target: Target Pokemon data
        similar: Similar Pokemon data
        similarity_score: Overall similarity score
        
    Returns:
        Plotly Figure object
    """
    stat_names = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    stat_cols = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    
    target_stats = [target[col] for col in stat_cols]
    similar_stats = [similar[col] for col in stat_cols]
    
    fig = go.Figure()
    
    # Target Pokemon trace
    fig.add_trace(go.Scatterpolar(
        r=target_stats,
        theta=stat_names,
        fill='toself',
        name=target['name'].title(),
        line=dict(color='#22c55e', width=2),
        fillcolor='rgba(34, 197, 94, 0.2)'
    ))
    
    # Similar Pokemon trace
    fig.add_trace(go.Scatterpolar(
        r=similar_stats,
        theta=stat_names,
        fill='toself',
        name=similar['name'].title(),
        line=dict(color='#3b82f6', width=2),
        fillcolor='rgba(59, 130, 246, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 255])
        ),
        showlegend=True,
        title=f"Stat Comparison (Similarity: {similarity_score:.1f}%)",
        height=400
    )
    
    return fig


def display_similar_pokemon_tab(df: pd.DataFrame):
    """
    Display the Similar Pokemon Finder tab
    
    Args:
        df: Main Pokemon DataFrame
    """
    st.markdown("### 🔍 Similar Pokemon Finder")
    st.caption("Find Pokemon with similar stats, types, and battle roles using ML algorithms")
    
    # Pokemon selector
    pokemon_list = sorted(df['name'].str.lower().unique())
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_pokemon_name = st.selectbox(
            "Select a Pokemon",
            pokemon_list,
            format_func=lambda x: x.title(),
            key="similar_pokemon_selector"
        )
    
    with col2:
        top_n = st.slider("Number of results", 3, 20, 10, key="similar_top_n")
    
    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        st.markdown("**Similarity Weights** (must sum to 1.0)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            stat_weight = st.slider("Stat Similarity", 0.0, 1.0, 0.6, 0.1)
        with col2:
            type_weight = st.slider("Type Similarity", 0.0, 1.0, 0.3, 0.1)
        with col3:
            role_weight = st.slider("Role Similarity", 0.0, 1.0, 0.1, 0.1)
        
        # Normalize weights
        total = stat_weight + type_weight + role_weight
        if total > 0:
            stat_weight /= total
            type_weight /= total
            role_weight /= total
    
    if selected_pokemon_name:
        # Get target Pokemon
        target_mask = df['name'].str.lower() == selected_pokemon_name.lower()
        if target_mask.sum() == 0:
            st.error("Pokemon not found")
            return
        
        target_pokemon = df[target_mask].iloc[0]
        
        # Find similar Pokemon
        with st.spinner("🔍 Analyzing Pokemon database..."):
            similar_pokemon = find_similar_pokemon(
                df, target_pokemon, top_n,
                stat_weight, type_weight, role_weight
            )
        
        # Display target Pokemon info
        st.markdown("---")
        st.markdown(f"### 🎯 Target: #{target_pokemon['pokedex_number']:04d} {target_pokemon['name'].title()}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            types = [target_pokemon['type1']]
            if pd.notna(target_pokemon.get('type2')):
                types.append(target_pokemon['type2'])
            st.markdown("**Types:** " + " / ".join([t.title() for t in types]))
        with col2:
            if 'total' in target_pokemon.index:
                st.markdown(f"**Total Stats:** {target_pokemon['total']}")
        with col3:
            st.markdown(f"**Generation:** {target_pokemon.get('generation', 'N/A')}")
        
        # Display results
        st.markdown("---")
        st.markdown(f"### 📊 Top {top_n} Most Similar Pokemon")
        
        for idx, (pokemon, overall_sim, stat_sim, type_sim, role_sim) in enumerate(similar_pokemon, 1):
            with st.expander(
                f"#{idx} - {pokemon['name'].title()} "
                f"(Similarity: {overall_sim:.1f}%)",
                expanded=(idx <= 3)
            ):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Pokemon info
                    st.markdown(f"**#{pokemon['pokedex_number']:04d} {pokemon['name'].title()}**")
                    
                    types = [pokemon['type1']]
                    if pd.notna(pokemon.get('type2')):
                        types.append(pokemon['type2'])
                    st.markdown("**Types:** " + " / ".join([t.title() for t in types]))
                    
                    if 'total' in pokemon.index:
                        st.markdown(f"**Total Stats:** {pokemon['total']}")
                    
                    # Similarity breakdown
                    st.markdown("---")
                    st.markdown("**Similarity Breakdown:**")
                    st.progress(overall_sim / 100, text=f"Overall: {overall_sim:.1f}%")
                    st.progress(stat_sim / 100, text=f"Stats: {stat_sim:.1f}%")
                    st.progress(type_sim / 100, text=f"Types: {type_sim:.1f}%")
                    st.progress(role_sim / 100, text=f"Role: {role_sim:.1f}%")
                
                with col2:
                    # Radar chart
                    fig = create_similarity_radar_chart(
                        target_pokemon, pokemon, overall_sim
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.markdown("---")
        st.markdown("### 📈 Analysis Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_similarity = sum(sim[1] for sim in similar_pokemon) / len(similar_pokemon)
            st.metric("Average Similarity", f"{avg_similarity:.1f}%")
        
        with col2:
            same_type_count = sum(
                1 for poke, *_ in similar_pokemon 
                if poke['type1'] == target_pokemon['type1']
            )
            st.metric("Same Primary Type", f"{same_type_count}/{top_n}")
        
        with col3:
            if similar_pokemon:
                best_match = similar_pokemon[0]
                st.metric("Best Match", best_match[0]['name'].title())


def render_quick_similarity_widget(df: pd.DataFrame, pokemon_name: str):
    """
    Render a compact widget showing top 3 similar Pokemon
    
    Args:
        df: Pokemon DataFrame
        pokemon_name: Pokemon name to find similar ones for
    """
    target_mask = df['name'].str.lower() == pokemon_name.lower()
    if target_mask.sum() == 0:
        return
    
    target_pokemon = df[target_mask].iloc[0]
    similar = find_similar_pokemon(df, target_pokemon, top_n=3)
    
    st.markdown("#### 🔍 Similar Pokemon:")
    for pokemon, score, _, _, _ in similar:
        st.markdown(
            f"- **{pokemon['name'].title()}** "
            f"(#{pokemon['pokedex_number']:04d}) - "
            f"{score:.0f}% similar"
        )
