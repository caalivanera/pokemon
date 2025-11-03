"""
Advanced Search and Filter Module
Comprehensive Pokemon filtering with BST range, ability, move search
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any


def create_advanced_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create advanced filter UI and return filtered DataFrame
    
    Args:
        df: Pokemon DataFrame
        
    Returns:
        Filtered DataFrame
    """
    st.markdown("### 🔍 Advanced Search & Filters")
    
    # Create filter tabs
    filter_tabs = st.tabs([
        "🔢 Stats & BST",
        "🎯 Type & Ability",
        "📊 Advanced",
        "💾 Saved Filters"
    ])
    
    # Tab 1: Stats & BST
    with filter_tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Base Stat Total (BST)")
            bst_range = st.slider(
                "BST Range",
                min_value=int(df['total_points'].min()),
                max_value=int(df['total_points'].max()),
                value=(
                    int(df['total_points'].min()),
                    int(df['total_points'].max())
                ),
                help="Filter Pokemon by total base stats"
            )
            
            st.markdown("#### HP Range")
            hp_range = st.slider(
                "HP",
                min_value=int(df['hp'].min()),
                max_value=int(df['hp'].max()),
                value=(int(df['hp'].min()), int(df['hp'].max()))
            )
        
        with col2:
            st.markdown("#### Attack Range")
            atk_range = st.slider(
                "Attack",
                min_value=int(df['attack'].min()),
                max_value=int(df['attack'].max()),
                value=(int(df['attack'].min()), int(df['attack'].max()))
            )
            
            st.markdown("#### Speed Range")
            spd_range = st.slider(
                "Speed",
                min_value=int(df['speed'].min()),
                max_value=int(df['speed'].max()),
                value=(int(df['speed'].min()), int(df['speed'].max()))
            )
        
        # Apply BST and stat filters
        df = df[
            (df['total_points'] >= bst_range[0]) &
            (df['total_points'] <= bst_range[1]) &
            (df['hp'] >= hp_range[0]) &
            (df['hp'] <= hp_range[1]) &
            (df['attack'] >= atk_range[0]) &
            (df['attack'] <= atk_range[1]) &
            (df['speed'] >= spd_range[0]) &
            (df['speed'] <= spd_range[1])
        ]
    
    # Tab 2: Type & Ability
    with filter_tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Type Filters")
            
            # Primary type filter
            type1_options = ['All'] + sorted(df['type_1'].unique().tolist())
            selected_type1 = st.selectbox(
                "Primary Type",
                options=type1_options,
                help="Filter by primary type"
            )
            
            if selected_type1 != 'All':
                df = df[df['type_1'] == selected_type1]
            
            # Secondary type filter
            type2_options = ['All'] + sorted(
                df['type_2'].dropna().unique().tolist()
            )
            selected_type2 = st.selectbox(
                "Secondary Type",
                options=type2_options,
                help="Filter by secondary type"
            )
            
            if selected_type2 != 'All':
                df = df[df['type_2'] == selected_type2]
            
            # Type combination filter
            has_dual_type = st.checkbox(
                "Only Dual-Type Pokemon",
                help="Show only Pokemon with two types"
            )
            if has_dual_type:
                df = df[df['type_2'].notna()]
        
        with col2:
            st.markdown("#### Ability Filters")
            
            # Ability search
            ability_search = st.text_input(
                "Search by Ability",
                placeholder="e.g., Levitate, Intimidate",
                help="Search for Pokemon with specific abilities"
            )
            
            if ability_search:
                ability_search_lower = ability_search.lower()
                df = df[
                    df['ability_1'].str.lower().str.contains(
                        ability_search_lower, na=False
                    ) |
                    df['ability_2'].fillna('').str.lower().str.contains(
                        ability_search_lower, na=False
                    ) |
                    df['hidden_ability'].fillna('').str.lower().str.contains(
                        ability_search_lower, na=False
                    )
                ]
            
            # Ability type
            ability_filter_type = st.radio(
                "Ability Type",
                options=['All', 'Has Hidden Ability', 'Single Ability'],
                horizontal=True
            )
            
            if ability_filter_type == 'Has Hidden Ability':
                df = df[df['hidden_ability'].notna()]
            elif ability_filter_type == 'Single Ability':
                df = df[df['ability_2'].isna()]
    
    # Tab 3: Advanced Filters
    with filter_tabs[2]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Generation & Region")
            
            # Generation filter
            gen_options = ['All'] + [
                f"Gen {i}" for i in range(1, 10)
            ]
            selected_gen = st.selectbox(
                "Generation",
                options=gen_options,
                help="Filter by Pokemon generation"
            )
            
            if selected_gen != 'All':
                gen_num = int(selected_gen.split()[1])
                # Define generation ranges
                gen_ranges = {
                    1: (1, 151),
                    2: (152, 251),
                    3: (252, 386),
                    4: (387, 493),
                    5: (494, 649),
                    6: (650, 721),
                    7: (722, 809),
                    8: (810, 905),
                    9: (906, 1025)
                }
                if gen_num in gen_ranges:
                    start, end = gen_ranges[gen_num]
                    df = df[
                        (df['pokedex_number'] >= start) &
                        (df['pokedex_number'] <= end)
                    ]
            
            # Variant filter
            if 'variant_type' in df.columns:
                variant_options = ['All'] + sorted(
                    df['variant_type'].unique().tolist()
                )
                selected_variant = st.multiselect(
                    "Variant Forms",
                    options=variant_options[1:],  # Exclude 'All'
                    help="Filter by variant type"
                )
                
                if selected_variant:
                    df = df[df['variant_type'].isin(selected_variant)]
        
        with col2:
            st.markdown("#### Stat Rankings")
            
            # Top performers filter
            stat_ranking = st.selectbox(
                "Show Top Performers in",
                options=[
                    'None',
                    'Total BST',
                    'HP',
                    'Attack',
                    'Defense',
                    'Sp. Attack',
                    'Sp. Defense',
                    'Speed'
                ],
                help="Filter for highest stat values"
            )
            
            if stat_ranking != 'None':
                top_n = st.slider(
                    "Top N Pokemon",
                    min_value=10,
                    max_value=100,
                    value=25,
                    step=5
                )
                
                stat_map = {
                    'Total BST': 'total_points',
                    'HP': 'hp',
                    'Attack': 'attack',
                    'Defense': 'defense',
                    'Sp. Attack': 'sp_attack',
                    'Sp. Defense': 'sp_defense',
                    'Speed': 'speed'
                }
                
                if stat_ranking in stat_map:
                    df = df.nlargest(top_n, stat_map[stat_ranking])
            
            # Legendary filter
            is_legendary = st.checkbox(
                "Only Legendary/Mythical",
                help="Show only legendary and mythical Pokemon"
            )
            
            if is_legendary:
                # Define legendary Pokemon BST threshold (typically >= 580)
                df = df[df['total_points'] >= 580]
    
    # Tab 4: Saved Filters
    with filter_tabs[3]:
        st.markdown("#### 💾 Saved Filter Presets")
        
        # Predefined filter presets
        presets = {
            "None": None,
            "Starter Pokemon": {
                'numbers': list(range(1, 10)) + list(range(152, 161)) +
                           list(range(252, 261)) + list(range(387, 396)) +
                           list(range(495, 504)) + list(range(650, 659)) +
                           list(range(722, 731)) + list(range(810, 819)) +
                           list(range(906, 915))
            },
            "Pseudo-Legendaries": {
                'bst_min': 600,
                'bst_max': 600,
                'has_evolution': True
            },
            "Fast Attackers": {
                'speed_min': 100,
                'attack_min': 100
            },
            "Tanks": {
                'hp_min': 100,
                'defense_min': 80,
                'sp_defense_min': 80
            },
            "Glass Cannons": {
                'attack_min': 110,
                'defense_max': 70
            }
        }
        
        selected_preset = st.selectbox(
            "Load Preset Filter",
            options=list(presets.keys()),
            help="Apply predefined filter combinations"
        )
        
        if selected_preset != "None" and presets[selected_preset]:
            preset_data = presets[selected_preset]
            
            if 'numbers' in preset_data:
                df = df[df['pokedex_number'].isin(preset_data['numbers'])]
            
            if 'bst_min' in preset_data:
                df = df[df['total_points'] >= preset_data['bst_min']]
            if 'bst_max' in preset_data:
                df = df[df['total_points'] <= preset_data['bst_max']]
            
            if 'speed_min' in preset_data:
                df = df[df['speed'] >= preset_data['speed_min']]
            if 'attack_min' in preset_data:
                df = df[df['attack'] >= preset_data['attack_min']]
            
            if 'hp_min' in preset_data:
                df = df[df['hp'] >= preset_data['hp_min']]
            if 'defense_min' in preset_data:
                df = df[df['defense'] >= preset_data['defense_min']]
            if 'sp_defense_min' in preset_data:
                df = df[df['sp_defense'] >= preset_data['sp_defense_min']]
            
            if 'defense_max' in preset_data:
                df = df[df['defense'] <= preset_data['defense_max']]
        
        st.info(f"**Results:** {len(df)} Pokemon match current filters")
    
    return df


def quick_search_bar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quick search bar for name and number
    
    Args:
        df: Pokemon DataFrame
        
    Returns:
        Filtered DataFrame
    """
    search_query = st.text_input(
        "🔍 Quick Search",
        placeholder="Search by name or number (e.g., Charizard, 006)",
        help="Type Pokemon name or Pokedex number"
    )
    
    if search_query:
        search_lower = search_query.lower().strip()
        df = df[
            df['name'].str.lower().str.contains(search_lower, na=False) |
            df['pokedex_number'].astype(str).str.contains(search_query, na=False)
        ]
    
    return df


def display_filter_summary(original_count: int, filtered_count: int):
    """
    Display filter results summary
    
    Args:
        original_count: Original number of Pokemon
        filtered_count: Filtered number of Pokemon
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Pokemon",
            original_count,
            help="Total Pokemon in database"
        )
    
    with col2:
        st.metric(
            "Filtered Results",
            filtered_count,
            delta=filtered_count - original_count,
            delta_color="normal",
            help="Pokemon matching current filters"
        )
    
    with col3:
        percentage = (filtered_count / original_count * 100) if original_count > 0 else 0
        st.metric(
            "Match Rate",
            f"{percentage:.1f}%",
            help="Percentage of Pokemon shown"
        )
