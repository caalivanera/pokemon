"""
Type Effectiveness Calculator
Calculate type matchups, weaknesses, resistances, and immunities
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Tuple

# Complete type effectiveness chart
TYPE_CHART = {
    'Normal': {
        'weak_to': ['Fighting'],
        'resistant_to': [],
        'immune_to': ['Ghost'],
        'super_effective': [],
        'not_effective': ['Rock', 'Steel'],
        'no_effect': ['Ghost']
    },
    'Fire': {
        'weak_to': ['Water', 'Ground', 'Rock'],
        'resistant_to': ['Fire', 'Grass', 'Ice', 'Bug', 'Steel', 'Fairy'],
        'immune_to': [],
        'super_effective': ['Grass', 'Ice', 'Bug', 'Steel'],
        'not_effective': ['Fire', 'Water', 'Rock', 'Dragon'],
        'no_effect': []
    },
    'Water': {
        'weak_to': ['Electric', 'Grass'],
        'resistant_to': ['Fire', 'Water', 'Ice', 'Steel'],
        'immune_to': [],
        'super_effective': ['Fire', 'Ground', 'Rock'],
        'not_effective': ['Water', 'Grass', 'Dragon'],
        'no_effect': []
    },
    'Electric': {
        'weak_to': ['Ground'],
        'resistant_to': ['Electric', 'Flying', 'Steel'],
        'immune_to': [],
        'super_effective': ['Water', 'Flying'],
        'not_effective': ['Electric', 'Grass', 'Dragon'],
        'no_effect': ['Ground']
    },
    'Grass': {
        'weak_to': ['Fire', 'Ice', 'Poison', 'Flying', 'Bug'],
        'resistant_to': ['Water', 'Electric', 'Grass', 'Ground'],
        'immune_to': [],
        'super_effective': ['Water', 'Ground', 'Rock'],
        'not_effective': ['Fire', 'Grass', 'Poison', 'Flying', 'Bug', 'Dragon', 'Steel'],
        'no_effect': []
    },
    'Ice': {
        'weak_to': ['Fire', 'Fighting', 'Rock', 'Steel'],
        'resistant_to': ['Ice'],
        'immune_to': [],
        'super_effective': ['Grass', 'Ground', 'Flying', 'Dragon'],
        'not_effective': ['Fire', 'Water', 'Ice', 'Steel'],
        'no_effect': []
    },
    'Fighting': {
        'weak_to': ['Flying', 'Psychic', 'Fairy'],
        'resistant_to': ['Bug', 'Rock', 'Dark'],
        'immune_to': [],
        'super_effective': ['Normal', 'Ice', 'Rock', 'Dark', 'Steel'],
        'not_effective': ['Poison', 'Flying', 'Psychic', 'Bug', 'Fairy'],
        'no_effect': ['Ghost']
    },
    'Poison': {
        'weak_to': ['Ground', 'Psychic'],
        'resistant_to': ['Grass', 'Fighting', 'Poison', 'Bug', 'Fairy'],
        'immune_to': [],
        'super_effective': ['Grass', 'Fairy'],
        'not_effective': ['Poison', 'Ground', 'Rock', 'Ghost'],
        'no_effect': ['Steel']
    },
    'Ground': {
        'weak_to': ['Water', 'Grass', 'Ice'],
        'resistant_to': ['Poison', 'Rock'],
        'immune_to': ['Electric'],
        'super_effective': ['Fire', 'Electric', 'Poison', 'Rock', 'Steel'],
        'not_effective': ['Grass', 'Bug'],
        'no_effect': ['Flying']
    },
    'Flying': {
        'weak_to': ['Electric', 'Ice', 'Rock'],
        'resistant_to': ['Grass', 'Fighting', 'Bug'],
        'immune_to': ['Ground'],
        'super_effective': ['Grass', 'Fighting', 'Bug'],
        'not_effective': ['Electric', 'Rock', 'Steel'],
        'no_effect': []
    },
    'Psychic': {
        'weak_to': ['Bug', 'Ghost', 'Dark'],
        'resistant_to': ['Fighting', 'Psychic'],
        'immune_to': [],
        'super_effective': ['Fighting', 'Poison'],
        'not_effective': ['Psychic', 'Steel'],
        'no_effect': ['Dark']
    },
    'Bug': {
        'weak_to': ['Fire', 'Flying', 'Rock'],
        'resistant_to': ['Grass', 'Fighting', 'Ground'],
        'immune_to': [],
        'super_effective': ['Grass', 'Psychic', 'Dark'],
        'not_effective': ['Fire', 'Fighting', 'Poison', 'Flying', 'Ghost', 'Steel', 'Fairy'],
        'no_effect': []
    },
    'Rock': {
        'weak_to': ['Water', 'Grass', 'Fighting', 'Ground', 'Steel'],
        'resistant_to': ['Normal', 'Fire', 'Poison', 'Flying'],
        'immune_to': [],
        'super_effective': ['Fire', 'Ice', 'Flying', 'Bug'],
        'not_effective': ['Fighting', 'Ground', 'Steel'],
        'no_effect': []
    },
    'Ghost': {
        'weak_to': ['Ghost', 'Dark'],
        'resistant_to': ['Poison', 'Bug'],
        'immune_to': ['Normal', 'Fighting'],
        'super_effective': ['Psychic', 'Ghost'],
        'not_effective': ['Dark'],
        'no_effect': ['Normal']
    },
    'Dragon': {
        'weak_to': ['Ice', 'Dragon', 'Fairy'],
        'resistant_to': ['Fire', 'Water', 'Electric', 'Grass'],
        'immune_to': [],
        'super_effective': ['Dragon'],
        'not_effective': ['Steel'],
        'no_effect': ['Fairy']
    },
    'Dark': {
        'weak_to': ['Fighting', 'Bug', 'Fairy'],
        'resistant_to': ['Ghost', 'Dark'],
        'immune_to': ['Psychic'],
        'super_effective': ['Psychic', 'Ghost'],
        'not_effective': ['Fighting', 'Dark', 'Fairy'],
        'no_effect': []
    },
    'Steel': {
        'weak_to': ['Fire', 'Fighting', 'Ground'],
        'resistant_to': ['Normal', 'Grass', 'Ice', 'Flying', 'Psychic', 'Bug', 'Rock', 'Dragon', 'Steel', 'Fairy'],
        'immune_to': ['Poison'],
        'super_effective': ['Ice', 'Rock', 'Fairy'],
        'not_effective': ['Fire', 'Water', 'Electric', 'Steel'],
        'no_effect': []
    },
    'Fairy': {
        'weak_to': ['Poison', 'Steel'],
        'resistant_to': ['Fighting', 'Bug', 'Dark'],
        'immune_to': ['Dragon'],
        'super_effective': ['Fighting', 'Dragon', 'Dark'],
        'not_effective': ['Fire', 'Poison', 'Steel'],
        'no_effect': []
    }
}


def calculate_type_effectiveness(attacking_type: str, defending_types: List[str]) -> float:
    """
    Calculate the effectiveness multiplier for an attack
    
    Args:
        attacking_type: The type of the attacking move
        defending_types: List of defending Pokemon's types (1 or 2 types)
    
    Returns:
        float: Damage multiplier (0.0, 0.25, 0.5, 1.0, 2.0, or 4.0)
    """
    if attacking_type not in TYPE_CHART:
        return 1.0
    
    multiplier = 1.0
    attack_data = TYPE_CHART[attacking_type]
    
    for def_type in defending_types:
        if def_type in attack_data['no_effect']:
            multiplier *= 0.0
        elif def_type in attack_data['super_effective']:
            multiplier *= 2.0
        elif def_type in attack_data['not_effective']:
            multiplier *= 0.5
    
    return multiplier


def get_pokemon_weaknesses(types: List[str]) -> Dict[str, List[str]]:
    """
    Calculate all weaknesses, resistances, and immunities for a Pokemon
    
    Args:
        types: List of Pokemon's types (1 or 2 types)
    
    Returns:
        dict: Dictionary with multipliers and lists of types
    """
    # Calculate multipliers for all types
    multipliers = {}
    for attack_type in TYPE_CHART.keys():
        multipliers[attack_type] = calculate_type_effectiveness(attack_type, types)
    
    # Categorize by multiplier
    result = {
        'immune': [],        # 0x
        'very_resistant': [], # 0.25x
        'resistant': [],     # 0.5x
        'neutral': [],       # 1x
        'weak': [],          # 2x
        'very_weak': []      # 4x
    }
    
    for type_name, mult in multipliers.items():
        if mult == 0.0:
            result['immune'].append(type_name)
        elif mult == 0.25:
            result['very_resistant'].append(type_name)
        elif mult == 0.5:
            result['resistant'].append(type_name)
        elif mult == 1.0:
            result['neutral'].append(type_name)
        elif mult == 2.0:
            result['weak'].append(type_name)
        elif mult == 4.0:
            result['very_weak'].append(type_name)
    
    return result


def display_type_calculator():
    """Display the type effectiveness calculator interface"""
    st.markdown("### ⚔️ Type Effectiveness Calculator")
    st.markdown("Calculate damage multipliers and analyze type matchups")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Attacking Type")
        attacking_type = st.selectbox(
            "Select attacking move type",
            options=list(TYPE_CHART.keys()),
            help="Choose the type of the move being used"
        )
        
        st.markdown(f"**{attacking_type} Type Moves:**")
        attack_data = TYPE_CHART[attacking_type]
        
        if attack_data['super_effective']:
            st.success(f"✅ **Super Effective (2x):** {', '.join(attack_data['super_effective'])}")
        
        if attack_data['not_effective']:
            st.warning(f"⚠️ **Not Very Effective (0.5x):** {', '.join(attack_data['not_effective'])}")
        
        if attack_data['no_effect']:
            st.error(f"❌ **No Effect (0x):** {', '.join(attack_data['no_effect'])}")
    
    with col2:
        st.markdown("#### Defending Pokemon")
        defending_type1 = st.selectbox(
            "Primary Type",
            options=list(TYPE_CHART.keys()),
            help="Choose the defending Pokemon's primary type"
        )
        
        has_second_type = st.checkbox("Has Second Type?", value=False)
        defending_type2 = None
        
        if has_second_type:
            defending_type2 = st.selectbox(
                "Secondary Type",
                options=[t for t in TYPE_CHART.keys() if t != defending_type1],
                help="Choose the defending Pokemon's secondary type"
            )
        
        # Calculate effectiveness
        defending_types = [defending_type1]
        if defending_type2:
            defending_types.append(defending_type2)
        
        multiplier = calculate_type_effectiveness(attacking_type, defending_types)
        
        # Display result
        st.markdown("---")
        st.markdown("#### 🎯 Damage Multiplier")
        
        if multiplier == 0.0:
            st.error(f"# ❌ {multiplier}x - NO EFFECT!")
        elif multiplier < 0.5:
            st.info(f"# 🛡️ {multiplier}x - Very Resistant")
        elif multiplier < 1.0:
            st.warning(f"# 🛡️ {multiplier}x - Resistant")
        elif multiplier == 1.0:
            st.info(f"# ⚖️ {multiplier}x - Neutral")
        elif multiplier == 2.0:
            st.success(f"# ⚡ {multiplier}x - Super Effective!")
        elif multiplier > 2.0:
            st.success(f"# 💥 {multiplier}x - EXTREMELY EFFECTIVE!")
    
    # Full type coverage analysis
    st.markdown("---")
    st.markdown("#### 📊 Complete Type Coverage Analysis")
    
    defending_types_display = [defending_type1]
    if defending_type2:
        defending_types_display.append(defending_type2)
    
    weaknesses = get_pokemon_weaknesses(defending_types_display)
    
    coverage_cols = st.columns(3)
    
    with coverage_cols[0]:
        st.markdown("##### 🛡️ Defensive Strengths")
        if weaknesses['immune']:
            st.success(f"**Immune (0x):** {', '.join(weaknesses['immune'])}")
        if weaknesses['very_resistant']:
            st.info(f"**Very Resistant (0.25x):** {', '.join(weaknesses['very_resistant'])}")
        if weaknesses['resistant']:
            st.info(f"**Resistant (0.5x):** {', '.join(weaknesses['resistant'])}")
    
    with coverage_cols[1]:
        st.markdown("##### ⚖️ Neutral")
        if weaknesses['neutral']:
            st.write(f"**Neutral (1x):** {len(weaknesses['neutral'])} types")
            with st.expander("View all neutral types"):
                st.write(', '.join(weaknesses['neutral']))
    
    with coverage_cols[2]:
        st.markdown("##### ⚠️ Weaknesses")
        if weaknesses['weak']:
            st.warning(f"**Weak (2x):** {', '.join(weaknesses['weak'])}")
        if weaknesses['very_weak']:
            st.error(f"**Very Weak (4x):** {', '.join(weaknesses['very_weak'])}")
    
    # Create visual coverage matrix
    st.markdown("---")
    st.markdown("#### 🔥 Type Coverage Heatmap")
    
    # Create matrix data
    all_types = list(TYPE_CHART.keys())
    matrix_data = []
    
    for def_type in all_types:
        row = []
        for atk_type in all_types:
            mult = calculate_type_effectiveness(atk_type, [def_type])
            row.append(mult)
        matrix_data.append(row)
    
    # Create DataFrame
    coverage_df = pd.DataFrame(
        matrix_data,
        index=all_types,
        columns=all_types
    )
    
    # Display heatmap
    import plotly.express as px
    fig = px.imshow(
        coverage_df,
        labels=dict(x="Attacking Type", y="Defending Type", color="Multiplier"),
        x=all_types,
        y=all_types,
        color_continuous_scale=[
            [0.0, '#1e293b'],   # Immune (0x)
            [0.25, '#475569'],  # Very Resistant (0.25x)
            [0.375, '#64748b'], # Resistant (0.5x)
            [0.5, '#94a3b8'],   # Neutral (1x)
            [0.75, '#fbbf24'],  # Weak (2x)
            [1.0, '#ef4444']    # Very Weak (4x)
        ],
        text_auto=True
    )
    
    fig.update_layout(
        title="Complete Type Effectiveness Matrix",
        height=700,
        xaxis={'side': 'top'},
        font=dict(size=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def get_offensive_coverage(types: List[str]) -> Dict[str, int]:
    """
    Calculate what types a Pokemon can hit super effectively
    
    Args:
        types: List of Pokemon's types
    
    Returns:
        dict: Counts of types that can be hit at each multiplier
    """
    coverage = {
        'super_effective': set(),
        'neutral': set(),
        'not_effective': set(),
        'no_effect': set()
    }
    
    for poke_type in types:
        if poke_type in TYPE_CHART:
            data = TYPE_CHART[poke_type]
            coverage['super_effective'].update(data['super_effective'])
            coverage['not_effective'].update(data['not_effective'])
            coverage['no_effect'].update(data['no_effect'])
    
    # Calculate neutral (types not in other categories)
    all_types = set(TYPE_CHART.keys())
    coverage['neutral'] = all_types - coverage['super_effective'] - coverage['not_effective'] - coverage['no_effect']
    
    # Convert sets to lists and return counts
    return {
        'super_effective': list(coverage['super_effective']),
        'super_effective_count': len(coverage['super_effective']),
        'neutral': list(coverage['neutral']),
        'neutral_count': len(coverage['neutral']),
        'not_effective': list(coverage['not_effective']),
        'not_effective_count': len(coverage['not_effective']),
        'no_effect': list(coverage['no_effect']),
        'no_effect_count': len(coverage['no_effect'])
    }
