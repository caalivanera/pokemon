"""
Variant Statistics Dashboard
Comprehensive analysis of Pokemon variants, regional forms, and special forms
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List


def display_variant_statistics(df: pd.DataFrame):
    """
    Display comprehensive variant statistics dashboard
    
    Args:
        df: DataFrame with Pokemon data including variant information
    """
    st.markdown("### 📊 Variant Statistics Dashboard")
    st.markdown("Comprehensive analysis of all Pokemon variants, regional forms, and special transformations")
    
    # Check if variant data exists
    if 'variant_type' not in df.columns:
        st.error("⚠️ Variant data not found in dataset. Please ensure variant_type column exists.")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        base_count = len(df[df['variant_type'] == 'base'])
        st.metric("Base Forms", base_count)
    
    with col2:
        variant_count = len(df[df['variant_type'] != 'base'])
        st.metric("Variant Forms", variant_count)
    
    with col3:
        total_forms = len(df)
        st.metric("Total Forms", total_forms)
    
    with col4:
        variant_percentage = (variant_count / total_forms * 100) if total_forms > 0 else 0
        st.metric("Variant %", f"{variant_percentage:.1f}%")
    
    st.markdown("---")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Distribution",
        "🔄 Type Changes",
        "📈 Stat Comparisons",
        "⚡ Mega Evolution",
        "💎 Special Forms"
    ])
    
    # TAB 1: Variant Distribution
    with tab1:
        st.markdown("#### Variant Type Distribution")
        
        variant_counts = df['variant_type'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = px.pie(
                values=variant_counts.values,
                names=variant_counts.index,
                title="Variant Type Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart
            fig_bar = px.bar(
                x=variant_counts.index,
                y=variant_counts.values,
                title="Variant Type Counts",
                labels={'x': 'Variant Type', 'y': 'Count'},
                color=variant_counts.values,
                color_continuous_scale='Viridis'
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detailed breakdown table
        st.markdown("#### Detailed Breakdown")
        
        breakdown_data = []
        for variant_type in variant_counts.index:
            count = variant_counts[variant_type]
            percentage = (count / len(df) * 100)
            breakdown_data.append({
                'Variant Type': variant_type.title(),
                'Count': count,
                'Percentage': f"{percentage:.2f}%"
            })
        
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    
    # TAB 2: Type Changes
    with tab2:
        st.markdown("#### Type Changes in Variants")
        st.markdown("Analysis of how Pokemon types change in different forms")
        
        # Get Pokemon with variants
        base_pokemon = df[df['variant_type'] == 'base'].copy()
        variant_pokemon = df[df['variant_type'] != 'base'].copy()
        
        if len(variant_pokemon) > 0:
            # Find type changes
            type_changes = []
            
            for idx, variant in variant_pokemon.iterrows():
                # Try to find base form
                base_match = base_pokemon[
                    base_pokemon['pokedex_number'] == variant['pokedex_number']
                ]
                
                if not base_match.empty:
                    base = base_match.iloc[0]
                    base_types = f"{base['type_1']}" + (f"/{base['type_2']}" if pd.notna(base.get('type_2')) else "")
                    variant_types = f"{variant['type_1']}" + (f"/{variant['type_2']}" if pd.notna(variant.get('type_2')) else "")
                    
                    if base_types != variant_types:
                        type_changes.append({
                            'Pokemon': variant['name'],
                            'Variant Type': variant['variant_type'].title(),
                            'Base Types': base_types,
                            'Variant Types': variant_types
                        })
            
            if type_changes:
                st.markdown(f"**Found {len(type_changes)} Pokemon with type changes**")
                
                type_change_df = pd.DataFrame(type_changes)
                st.dataframe(type_change_df, use_container_width=True, hide_index=True)
                
                # Type change frequency
                st.markdown("#### Most Common Type Changes")
                
                type_change_freq = {}
                for change in type_changes:
                    key = f"{change['Base Types']} → {change['Variant Types']}"
                    type_change_freq[key] = type_change_freq.get(key, 0) + 1
                
                fig_freq = px.bar(
                    x=list(type_change_freq.keys()),
                    y=list(type_change_freq.values()),
                    title="Type Change Frequency",
                    labels={'x': 'Type Change', 'y': 'Count'},
                    color=list(type_change_freq.values()),
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_freq, use_container_width=True)
            else:
                st.info("No type changes found in variant forms")
        else:
            st.info("No variant forms available for type change analysis")
    
    # TAB 3: Stat Comparisons
    with tab3:
        st.markdown("#### Base Stat Comparisons")
        st.markdown("Compare stats between base forms and variants")
        
        # Select Pokemon with variants for comparison
        pokemon_with_variants = df[df['variant_type'] != 'base']['pokedex_number'].unique()
        
        if len(pokemon_with_variants) > 0:
            # Create comparison selector
            selected_number = st.selectbox(
                "Select Pokemon to Compare",
                options=sorted(pokemon_with_variants),
                format_func=lambda x: f"#{x:03d}"
            )
            
            # Get all forms of selected Pokemon
            all_forms = df[df['pokedex_number'] == selected_number].copy()
            
            if len(all_forms) > 1:
                st.markdown(f"#### {all_forms.iloc[0]['name']} - All Forms")
                
                # Stat columns
                stat_cols = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_points']
                
                # Create comparison data
                comparison_data = []
                for _, form in all_forms.iterrows():
                    form_data = {
                        'Form': form.get('form_name', form['variant_type'].title()),
                        'Type': f"{form['type_1']}" + (f"/{form['type_2']}" if pd.notna(form.get('type_2')) else "")
                    }
                    for stat in stat_cols:
                        if stat in form:
                            form_data[stat.replace('_', ' ').title()] = form[stat]
                    comparison_data.append(form_data)
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                
                # Radar chart comparison
                st.markdown("#### Stat Radar Comparison")
                
                fig_radar = go.Figure()
                
                stat_names = ['HP', 'Attack', 'Defense', 'Sp Attack', 'Sp Defense', 'Speed']
                
                for _, form in all_forms.iterrows():
                    values = [
                        form['hp'], form['attack'], form['defense'],
                        form['sp_attack'], form['sp_defense'], form['speed']
                    ]
                    values.append(values[0])  # Close the radar
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values,
                        theta=stat_names + [stat_names[0]],
                        fill='toself',
                        name=form.get('form_name', form['variant_type'].title())
                    ))
                
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 200])),
                    showlegend=True,
                    title="Stat Comparison Radar Chart"
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
                
                # Stat difference analysis
                st.markdown("#### Stat Differences from Base")
                
                base_form = all_forms[all_forms['variant_type'] == 'base']
                if not base_form.empty:
                    base_stats = base_form.iloc[0]
                    
                    diff_data = []
                    for _, variant in all_forms[all_forms['variant_type'] != 'base'].iterrows():
                        diff_row = {
                            'Form': variant.get('form_name', variant['variant_type'].title())
                        }
                        for stat in ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']:
                            diff = variant[stat] - base_stats[stat]
                            diff_row[stat.replace('_', ' ').title()] = f"{diff:+d}"
                        diff_row['Total'] = f"{variant['total_points'] - base_stats['total_points']:+d}"
                        diff_data.append(diff_row)
                    
                    if diff_data:
                        diff_df = pd.DataFrame(diff_data)
                        st.dataframe(diff_df, use_container_width=True, hide_index=True)
            else:
                st.info("Selected Pokemon has only one form")
        else:
            st.info("No Pokemon with multiple forms found")
    
    # TAB 4: Mega Evolution Analysis
    with tab4:
        st.markdown("#### Mega Evolution Analysis")
        
        mega_pokemon = df[df['variant_type'].str.contains('mega', case=False, na=False)]
        
        if len(mega_pokemon) > 0:
            st.markdown(f"**Total Mega Evolutions: {len(mega_pokemon)}**")
            
            # Mega evolution stat boosts
            st.markdown("#### Average Stat Boosts")
            
            mega_base_pairs = []
            for _, mega in mega_pokemon.iterrows():
                base = df[(df['pokedex_number'] == mega['pokedex_number']) & 
                         (df['variant_type'] == 'base')]
                if not base.empty:
                    mega_base_pairs.append({
                        'mega': mega,
                        'base': base.iloc[0]
                    })
            
            if mega_base_pairs:
                stat_boosts = {
                    'HP': [], 'Attack': [], 'Defense': [],
                    'Sp. Attack': [], 'Sp. Defense': [], 'Speed': [], 'BST': []
                }
                
                for pair in mega_base_pairs:
                    mega, base = pair['mega'], pair['base']
                    stat_boosts['HP'].append(mega['hp'] - base['hp'])
                    stat_boosts['Attack'].append(mega['attack'] - base['attack'])
                    stat_boosts['Defense'].append(mega['defense'] - base['defense'])
                    stat_boosts['Sp. Attack'].append(mega['sp_attack'] - base['sp_attack'])
                    stat_boosts['Sp. Defense'].append(mega['sp_defense'] - base['sp_defense'])
                    stat_boosts['Speed'].append(mega['speed'] - base['speed'])
                    stat_boosts['BST'].append(mega['total_points'] - base['total_points'])
                
                avg_boosts = {stat: sum(boosts) / len(boosts) for stat, boosts in stat_boosts.items()}
                
                fig_boosts = px.bar(
                    x=list(avg_boosts.keys()),
                    y=list(avg_boosts.values()),
                    title="Average Stat Boosts in Mega Evolution",
                    labels={'x': 'Stat', 'y': 'Average Boost'},
                    color=list(avg_boosts.values()),
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig_boosts, use_container_width=True)
                
                # BST distribution
                st.markdown("#### Base Stat Total Distribution")
                
                mega_bst = mega_pokemon['total_points'].tolist()
                
                fig_hist = px.histogram(
                    x=mega_bst,
                    nbins=20,
                    title="Mega Evolution BST Distribution",
                    labels={'x': 'Base Stat Total', 'y': 'Count'},
                    color_discrete_sequence=['#FF6B6B']
                )
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # Top Mega Evolutions
                st.markdown("#### Top 10 Mega Evolutions by BST")
                
                top_megas = mega_pokemon.nlargest(10, 'total_points')[
                    ['name', 'variant_type', 'total_points', 'type_1', 'type_2']
                ].copy()
                top_megas.columns = ['Pokemon', 'Mega Type', 'BST', 'Type 1', 'Type 2']
                
                st.dataframe(top_megas, use_container_width=True, hide_index=True)
        else:
            st.info("No Mega Evolution data available")
    
    # TAB 5: Special Forms
    with tab5:
        st.markdown("#### Special Forms Analysis")
        st.markdown("Regional forms, Gigantamax, and other special variants")
        
        # Regional forms
        regional_forms = df[df['variant_type'].str.contains('alolan|galarian|hisuian|paldean', case=False, na=False)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Regional Forms")
            if len(regional_forms) > 0:
                regional_counts = regional_forms['variant_type'].value_counts()
                
                fig_regional = px.pie(
                    values=regional_counts.values,
                    names=[name.title() for name in regional_counts.index],
                    title=f"Regional Forms ({len(regional_forms)} total)",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig_regional, use_container_width=True)
            else:
                st.info("No regional forms found")
        
        with col2:
            st.markdown("##### Gigantamax Forms")
            gmax_forms = df[df['variant_type'].str.contains('gigantamax', case=False, na=False)]
            
            if len(gmax_forms) > 0:
                st.metric("Total G-Max Forms", len(gmax_forms))
                
                # List G-Max Pokemon
                gmax_list = gmax_forms[['name', 'total_points']].copy()
                gmax_list.columns = ['Pokemon', 'BST']
                gmax_list = gmax_list.sort_values('BST', ascending=False)
                
                st.dataframe(gmax_list, use_container_width=True, hide_index=True)
            else:
                st.info("No Gigantamax forms found")
        
        # Other special forms
        st.markdown("##### Other Special Forms")
        
        special_types = df['variant_type'].unique()
        other_forms = [
            vtype for vtype in special_types 
            if vtype not in ['base'] and 
            not any(keyword in vtype.lower() for keyword in ['mega', 'alolan', 'galarian', 'hisuian', 'paldean', 'gigantamax'])
        ]
        
        if other_forms:
            for form_type in other_forms:
                form_count = len(df[df['variant_type'] == form_type])
                st.markdown(f"- **{form_type.title()}**: {form_count} forms")
        else:
            st.info("No other special forms found")


def get_variant_summary(df: pd.DataFrame) -> Dict:
    """
    Get summary statistics for variants
    
    Args:
        df: DataFrame with Pokemon data
        
    Returns:
        Dictionary with variant summary statistics
    """
    if 'variant_type' not in df.columns:
        return {}
    
    summary = {
        'total_forms': len(df),
        'base_forms': len(df[df['variant_type'] == 'base']),
        'variant_forms': len(df[df['variant_type'] != 'base']),
        'variant_types': df['variant_type'].nunique(),
        'variant_percentage': (len(df[df['variant_type'] != 'base']) / len(df) * 100) if len(df) > 0 else 0
    }
    
    return summary
