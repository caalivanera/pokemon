"""
Enhanced Interactive Pokemon Dashboard with National Dex
Features advanced analytics, correlations, and interactive visualizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from src.data_loaders.data_extractor import load_pokemon_glossary
from src.data_loaders.yaml_loader import PokemonDataLoader

# Page configuration
st.set_page_config(
    page_title="Pokemon National Dex Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .stat-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Constants
DATA_DIR = Path(parent_dir) / 'data'
NATIONAL_DEX_FILE = DATA_DIR / 'national_dex.csv'


@st.cache_data(ttl=60*60*24)
def load_national_dex() -> pd.DataFrame:
    """Load the National Pokedex dataset."""
    if NATIONAL_DEX_FILE.exists():
        st.success("✅ Loading National Pokedex...")
        df = pd.read_csv(NATIONAL_DEX_FILE)
        st.info(f"📊 Loaded {len(df)} Pokemon across {df['generation'].nunique()} generations")
        return df
    else:
        st.error("❌ National Dex not found! Please run national_dex_builder.py first.")
        st.stop()


@st.cache_data
def load_glossary() -> dict:
    """Load Pokemon glossary."""
    return load_pokemon_glossary()


@st.cache_data
def load_yaml_data() -> dict:
    """Load YAML data."""
    try:
        yaml_loader = PokemonDataLoader()
        yaml_data = yaml_loader.load_all_yaml_data()
        st.success(f"✅ Loaded {len(yaml_data)} YAML data files!")
        return yaml_data
    except Exception as e:
        st.warning(f"⚠️ YAML data not available: {e}")
        return {}


# Load data
df = load_national_dex()
glossary = load_glossary()
yaml_data = load_yaml_data()

# Header
st.markdown('<h1 class="main-header">⚡ Pokemon National Dex Dashboard ⚡</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi_256.png", width=200)
st.sidebar.title("🎮 Navigation & Filters")

# Navigation
page = st.sidebar.radio(
    "Select View",
    ["📊 Overview Analytics", "🔍 Advanced Filters", "📈 Statistical Analysis", 
     "🔗 Correlations", "🎯 Type Analysis", "⚔️ Battle Stats", "📖 Pokemon Details"]
)

st.sidebar.markdown("---")

# ===== OVERVIEW ANALYTICS PAGE =====
if page == "📊 Overview Analytics":
    st.header("📊 National Pokedex Overview")
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Pokemon", f"{len(df):,}")
    with col2:
        st.metric("Generations", df['generation'].nunique())
    with col3:
        st.metric("Types", df['type_1'].nunique())
    with col4:
        st.metric("Legendary", df['is_legendary'].sum())
    with col5:
        st.metric("Avg BST", f"{df['total_points'].mean():.0f}")
    
    st.markdown("---")
    
    # Two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎲 Pokemon by Generation")
        gen_counts = df['generation'].value_counts().sort_index()
        fig = px.bar(
            x=gen_counts.index,
            y=gen_counts.values,
            labels={'x': 'Generation', 'y': 'Number of Pokemon'},
            title='Pokemon Distribution Across Generations',
            color=gen_counts.values,
            color_continuous_scale='viridis'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎨 Pokemon by Primary Type")
        type_counts = df['type_1'].value_counts().head(10)
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title='Top 10 Primary Types'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Three-column layout for stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 BST Distribution")
        fig = px.histogram(
            df,
            x='total_points',
            nbins=50,
            title='Base Stat Total Distribution',
            labels={'total_points': 'Base Stat Total'},
            color_discrete_sequence=['#636EFA']
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Speed Distribution")
        fig = px.box(
            df,
            x='speed_tier',
            y='speed',
            title='Speed by Tier',
            color='speed_tier',
            labels={'speed': 'Speed Stat', 'speed_tier': 'Speed Tier'}
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.subheader("🏆 BST by Tier")
        bst_tier_avg = df.groupby('bst_tier')['total_points'].mean().sort_values()
        fig = px.bar(
            x=bst_tier_avg.index,
            y=bst_tier_avg.values,
            title='Average BST by Tier',
            labels={'x': 'BST Tier', 'y': 'Average BST'},
            color=bst_tier_avg.values,
            color_continuous_scale='reds'
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Legendary vs Non-Legendary comparison
    st.markdown("---")
    st.subheader("👑 Legendary vs Non-Legendary Pokemon")
    
    col1, col2 = st.columns(2)
    
    with col1:
        legendary_stats = df.groupby('is_legendary')[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].mean()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Non-Legendary',
            x=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            y=legendary_stats.loc[False].values,
            marker_color='#636EFA'
        ))
        fig.add_trace(go.Bar(
            name='Legendary',
            x=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            y=legendary_stats.loc[True].values,
            marker_color='#EF553B'
        ))
        fig.update_layout(
            title='Average Stats Comparison',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            df,
            x='offensive_rating',
            y='defensive_rating',
            color='is_legendary',
            size='total_points',
            hover_name='name',
            title='Offensive vs Defensive Rating',
            labels={
                'offensive_rating': 'Offensive Rating',
                'defensive_rating': 'Defensive Rating',
                'is_legendary': 'Legendary'
            },
            color_discrete_map={True: '#EF553B', False: '#636EFA'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ===== ADVANCED FILTERS PAGE =====
elif page == "🔍 Advanced Filters":
    st.header("🔍 Advanced Pokemon Filters")
    
    # Create filter columns
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        st.subheader("🎯 Basic Filters")
        
        # Generation filter
        gen_options = ['All'] + sorted(df['generation'].unique().tolist())
        selected_gen = st.selectbox("Generation", gen_options)
        
        # Type filter
        type_options = ['All'] + sorted(df['type_1'].unique().tolist())
        selected_type = st.multiselect("Primary Type", type_options, default=['All'])
        
        # Legendary filter
        legendary_filter = st.radio("Legendary Status", ['All', 'Legendary Only', 'Non-Legendary Only'])
    
    with filter_col2:
        st.subheader("📊 Stat Filters")
        
        bst_range = st.slider(
            "Base Stat Total",
            int(df['total_points'].min()),
            int(df['total_points'].max()),
            (int(df['total_points'].min()), int(df['total_points'].max()))
        )
        
        speed_range = st.slider(
            "Speed",
            int(df['speed'].min()),
            int(df['speed'].max()),
            (int(df['speed'].min()), int(df['speed'].max()))
        )
        
        attack_range = st.slider(
            "Attack",
            int(df['attack'].min()),
            int(df['attack'].max()),
            (int(df['attack'].min()), int(df['attack'].max()))
        )
    
    with filter_col3:
        st.subheader("🔢 Physical Attributes")
        
        height_range = st.slider(
            "Height (m)",
            float(df['height_m'].min()),
            float(df['height_m'].max()),
            (float(df['height_m'].min()), float(df['height_m'].max()))
        )
        
        weight_range = st.slider(
            "Weight (kg)",
            float(df['weight_kg'].min()),
            float(df['weight_kg'].max()),
            (float(df['weight_kg'].min()), float(df['weight_kg'].max()))
        )
        
        dual_type_filter = st.checkbox("Dual-Type Only", value=False)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_gen != 'All':
        filtered_df = filtered_df[filtered_df['generation'] == selected_gen]
    
    if 'All' not in selected_type and len(selected_type) > 0:
        filtered_df = filtered_df[filtered_df['type_1'].isin(selected_type)]
    
    if legendary_filter == 'Legendary Only':
        filtered_df = filtered_df[filtered_df['is_legendary'] == True]
    elif legendary_filter == 'Non-Legendary Only':
        filtered_df = filtered_df[filtered_df['is_legendary'] == False]
    
    filtered_df = filtered_df[
        (filtered_df['total_points'] >= bst_range[0]) &
        (filtered_df['total_points'] <= bst_range[1]) &
        (filtered_df['speed'] >= speed_range[0]) &
        (filtered_df['speed'] <= speed_range[1]) &
        (filtered_df['attack'] >= attack_range[0]) &
        (filtered_df['attack'] <= attack_range[1]) &
        (filtered_df['height_m'] >= height_range[0]) &
        (filtered_df['height_m'] <= height_range[1]) &
        (filtered_df['weight_kg'] >= weight_range[0]) &
        (filtered_df['weight_kg'] <= weight_range[1])
    ]
    
    if dual_type_filter:
        filtered_df = filtered_df[filtered_df['is_dual_type'] == True]
    
    # Display results
    st.markdown("---")
    st.subheader(f"📋 Filtered Results: {len(filtered_df)} Pokemon")
    
    if len(filtered_df) > 0:
        # Display options
        display_cols = st.multiselect(
            "Select columns to display",
            ['pokedex_number', 'name', 'type_1', 'type_2', 'total_points', 'hp', 'attack', 
             'defense', 'sp_attack', 'sp_defense', 'speed', 'height_m', 'weight_kg', 
             'is_legendary', 'generation', 'bst_tier', 'speed_tier'],
            default=['pokedex_number', 'name', 'type_1', 'type_2', 'total_points', 'bst_tier']
        )
        
        st.dataframe(filtered_df[display_cols], use_container_width=True, height=400)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_pokemon.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No Pokemon match the selected filters.")

# ===== STATISTICAL ANALYSIS PAGE =====
elif page == "📈 Statistical Analysis":
    st.header("📈 Statistical Analysis")
    
    # Stat selector
    stat_to_analyze = st.selectbox(
        "Select stat to analyze",
        ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_points',
         'height_m', 'weight_kg', 'offensive_rating', 'defensive_rating']
    )
    
    # Statistical summary
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Mean", f"{df[stat_to_analyze].mean():.2f}")
    with col2:
        st.metric("Median", f"{df[stat_to_analyze].median():.2f}")
    with col3:
        st.metric("Std Dev", f"{df[stat_to_analyze].std():.2f}")
    with col4:
        st.metric("Min", f"{df[stat_to_analyze].min():.2f}")
    with col5:
        st.metric("Max", f"{df[stat_to_analyze].max():.2f}")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution
        fig = px.histogram(
            df,
            x=stat_to_analyze,
            nbins=50,
            title=f'{stat_to_analyze.replace("_", " ").title()} Distribution',
            marginal="box"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # By type
        type_stats = df.groupby('type_1')[stat_to_analyze].mean().sort_values(ascending=False).head(15)
        fig = px.bar(
            x=type_stats.index,
            y=type_stats.values,
            title=f'Average {stat_to_analyze.replace("_", " ").title()} by Type (Top 15)',
            labels={'x': 'Type', 'y': f'Average {stat_to_analyze}'},
            color=type_stats.values,
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # By generation
    st.subheader(f"📊 {stat_to_analyze.replace('_', ' ').title()} Trends Across Generations")
    
    gen_stats = df.groupby('generation')[stat_to_analyze].agg(['mean', 'median', 'std']).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=gen_stats['generation'],
        y=gen_stats['mean'],
        mode='lines+markers',
        name='Mean',
        line=dict(color='#636EFA', width=3),
        marker=dict(size=10)
    ))
    fig.add_trace(go.Scatter(
        x=gen_stats['generation'],
        y=gen_stats['median'],
        mode='lines+markers',
        name='Median',
        line=dict(color='#EF553B', width=3),
        marker=dict(size=10)
    ))
    fig.update_layout(
        title=f'{stat_to_analyze.replace("_", " ").title()} Evolution Across Generations',
        xaxis_title='Generation',
        yaxis_title=stat_to_analyze.replace('_', ' ').title(),
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top performers
    st.subheader(f"🏆 Top 10 Pokemon by {stat_to_analyze.replace('_', ' ').title()}")
    top_pokemon = df.nlargest(10, stat_to_analyze)[['name', 'type_1', 'type_2', stat_to_analyze, 'total_points', 'generation']]
    st.dataframe(top_pokemon, use_container_width=True)

# ===== CORRELATIONS PAGE =====
elif page == "🔗 Correlations":
    st.header("🔗 Statistical Correlations")
    
    # Select stats for correlation
    stats_for_corr = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 
                      'total_points', 'height_m', 'weight_kg', 'catch_rate', 
                      'offensive_rating', 'defensive_rating']
    
    # Correlation matrix
    st.subheader("📊 Correlation Heatmap")
    corr_matrix = df[stats_for_corr].corr()
    
    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        color_continuous_scale='RdBu_r',
        aspect="auto",
        title="Correlation Matrix of Pokemon Stats"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot for custom correlation
    st.markdown("---")
    st.subheader("🔍 Custom Correlation Explorer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_stat = st.selectbox("X-axis stat", stats_for_corr, index=1)
    with col2:
        y_stat = st.selectbox("Y-axis stat", stats_for_corr, index=4)
    
    color_by = st.selectbox(
        "Color by",
        ['type_1', 'generation', 'is_legendary', 'bst_tier', 'speed_tier'],
        index=0
    )
    
    fig = px.scatter(
        df,
        x=x_stat,
        y=y_stat,
        color=color_by,
        hover_name='name',
        title=f'{x_stat.replace("_", " ").title()} vs {y_stat.replace("_", " ").title()}',
        trendline="ols",
        labels={x_stat: x_stat.replace('_', ' ').title(), y_stat: y_stat.replace('_', ' ').title()}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate correlation coefficient
    corr_coef = df[x_stat].corr(df[y_stat])
    st.info(f"📊 Pearson Correlation Coefficient: **{corr_coef:.4f}**")
    
    if abs(corr_coef) > 0.7:
        st.success("✅ Strong correlation detected!")
    elif abs(corr_coef) > 0.4:
        st.warning("⚠️ Moderate correlation detected.")
    else:
        st.error("❌ Weak or no correlation.")

# ===== TYPE ANALYSIS PAGE =====
elif page == "🎯 Type Analysis":
    st.header("🎯 Pokemon Type Analysis")
    
    # Type matchup effectiveness
    st.subheader("⚔️ Type Effectiveness Analysis")
    
    type_cols = [col for col in df.columns if col.startswith('against_')]
    
    if len(type_cols) > 0:
        # Select a type to analyze
        selected_type = st.selectbox("Select Primary Type to Analyze", sorted(df['type_1'].unique()))
        
        type_df = df[df['type_1'] == selected_type]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Pokemon with this type", len(type_df))
            st.metric("Average BST", f"{type_df['total_points'].mean():.0f}")
        
        with col2:
            st.metric("Avg Weaknesses", f"{type_df['weaknesses_count'].mean():.1f}")
            st.metric("Avg Resistances", f"{type_df['resistances_count'].mean():.1f}")
        
        with col3:
            st.metric("Avg Immunities", f"{type_df['immunities_count'].mean():.1f}")
            st.metric("Defensive Score", f"{type_df['defensive_score'].mean():.1f}")
        
        # Type effectiveness breakdown
        st.subheader("🛡️ Type Matchup Breakdown")
        
        effectiveness_data = []
        for col in type_cols:
            type_name = col.replace('against_', '').title()
            avg_effectiveness = type_df[col].mean()
            effectiveness_data.append({
                'Type': type_name,
                'Average Effectiveness': avg_effectiveness
            })
        
        eff_df = pd.DataFrame(effectiveness_data).sort_values('Average Effectiveness')
        
        fig = px.bar(
            eff_df,
            x='Average Effectiveness',
            y='Type',
            orientation='h',
            title=f'{selected_type} Type - Defensive Matchups',
            color='Average Effectiveness',
            color_continuous_scale=['green', 'yellow', 'red'],
            labels={'Average Effectiveness': 'Damage Multiplier'}
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Type distribution
        st.subheader("📊 Type Combination Analysis")
        
        type_combo_counts = df['full_type'].value_counts().head(20)
        
        fig = px.bar(
            x=type_combo_counts.values,
            y=type_combo_counts.index,
            orientation='h',
            title='Top 20 Most Common Type Combinations',
            labels={'x': 'Count', 'y': 'Type Combination'},
            color=type_combo_counts.values,
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Type effectiveness data not available in this dataset.")

# ===== BATTLE STATS PAGE =====
elif page == "⚔️ Battle Stats":
    st.header("⚔️ Battle Statistics & Meta Analysis")
    
    # Speed tiers
    st.subheader("⚡ Speed Tier Distribution")
    
    speed_tier_counts = df['speed_tier'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            values=speed_tier_counts.values,
            names=speed_tier_counts.index,
            title='Speed Tier Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average stats by speed tier
        speed_stats = df.groupby('speed_tier')[['attack', 'sp_attack', 'defense', 'sp_defense']].mean()
        
        fig = go.Figure()
        for stat in ['attack', 'sp_attack', 'defense', 'sp_defense']:
            fig.add_trace(go.Bar(
                name=stat.replace('_', ' ').title(),
                x=speed_stats.index,
                y=speed_stats[stat]
            ))
        
        fig.update_layout(
            title='Average Stats by Speed Tier',
            barmode='group',
            xaxis_title='Speed Tier',
            yaxis_title='Average Stat Value'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Offensive vs Defensive breakdown
    st.subheader("⚔️🛡️ Offensive vs Defensive Profiles")
    
    # Categorize Pokemon
    df['battle_style'] = 'Balanced'
    df.loc[df['physical_special_ratio'] > 1.5, 'battle_style'] = 'Physical Sweeper'
    df.loc[df['physical_special_ratio'] < 0.67, 'battle_style'] = 'Special Sweeper'
    df.loc[(df['offensive_rating'] < df['defensive_rating'] * 0.8), 'battle_style'] = 'Tank'
    df.loc[(df['offensive_rating'] > df['defensive_rating'] * 1.2) & (df['speed'] > 100), 'battle_style'] = 'Glass Cannon'
    
    battle_style_counts = df['battle_style'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            x=battle_style_counts.index,
            y=battle_style_counts.values,
            title='Pokemon by Battle Style',
            labels={'x': 'Battle Style', 'y': 'Count'},
            color=battle_style_counts.values,
            color_continuous_scale='plasma'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            df,
            x='offensive_rating',
            y='defensive_rating',
            color='battle_style',
            size='speed',
            hover_name='name',
            title='Battle Profile Scatter Plot',
            labels={
                'offensive_rating': 'Offensive Rating',
                'defensive_rating': 'Defensive Rating'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Best Pokemon by role
    st.subheader("🏆 Top Pokemon by Role")
    
    role = st.selectbox("Select Role", ['Physical Sweeper', 'Special Sweeper', 'Tank', 'Glass Cannon', 'Balanced'])
    
    role_df = df[df['battle_style'] == role].nlargest(10, 'total_points')
    
    display_cols = ['name', 'type_1', 'type_2', 'total_points', 'offensive_rating', 'defensive_rating', 'speed']
    st.dataframe(role_df[display_cols], use_container_width=True)

# ===== POKEMON DETAILS PAGE =====
elif page == "📖 Pokemon Details":
    st.header("📖 Pokemon Encyclopedia")
    
    # Search/select Pokemon
    search_method = st.radio("Search by", ["Name", "Pokedex Number"])
    
    if search_method == "Name":
        selected_pokemon = st.selectbox(
            "Select Pokemon",
            options=sorted(df['name'].unique())
        )
        pokemon_data = df[df['name'] == selected_pokemon].iloc[0]
    else:
        pokedex_num = st.number_input(
            "Enter Pokedex Number",
            min_value=int(df['pokedex_number'].min()),
            max_value=int(df['pokedex_number'].max()),
            value=1
        )
        pokemon_data = df[df['pokedex_number'] == pokedex_num].iloc[0]
    
    # Display Pokemon details
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.image(
            f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{int(pokemon_data['pokedex_number'])}.png",
            width=200
        )
    
    with col2:
        st.markdown(f"# {pokemon_data['name']}")
        st.markdown(f"**#  {int(pokemon_data['pokedex_number']):03d}**")
        st.markdown(f"**Type:** {pokemon_data['type_1']}" + (f" / {pokemon_data['type_2']}" if pd.notna(pokemon_data['type_2']) else ""))
        st.markdown(f"**Generation:** {int(pokemon_data['generation'])}")
        st.markdown(f"**Species:** {pokemon_data.get('species', 'N/A')}")
        
        if pokemon_data['is_legendary']:
            st.markdown("👑 **LEGENDARY POKEMON**")
        if pokemon_data['is_starter']:
            st.markdown("🔥 **STARTER POKEMON**")
        if pokemon_data['is_pseudo_legendary']:
            st.markdown("⭐ **PSEUDO-LEGENDARY**")
    
    with col3:
        st.metric("BST", int(pokemon_data['total_points']))
        st.metric("Height", f"{pokemon_data['height_m']:.2f} m")
        st.metric("Weight", f"{pokemon_data['weight_kg']:.2f} kg")
        st.metric("Catch Rate", int(pokemon_data['catch_rate']))
    
    # Base stats
    st.subheader("📊 Base Stats")
    
    stats_data = {
        'Stat': ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed'],
        'Value': [
            pokemon_data['hp'],
            pokemon_data['attack'],
            pokemon_data['defense'],
            pokemon_data['sp_attack'],
            pokemon_data['sp_defense'],
            pokemon_data['speed']
        ]
    }
    
    fig = px.bar(
        stats_data,
        x='Value',
        y='Stat',
        orientation='h',
        title=f"{pokemon_data['name']} Base Stats",
        color='Value',
        color_continuous_scale='viridis',
        text='Value'
    )
    fig.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Stat percentiles
    st.subheader("📈 Percentile Rankings")
    
    percentile_data = {
        'Stat': ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed', 'BST'],
        'Percentile': [
            pokemon_data.get('hp_percentile', 0),
            pokemon_data.get('attack_percentile', 0),
            pokemon_data.get('defense_percentile', 0),
            pokemon_data.get('sp_attack_percentile', 0),
            pokemon_data.get('sp_defense_percentile', 0),
            pokemon_data.get('speed_percentile', 0),
            pokemon_data.get('total_points_percentile', 0)
        ]
    }
    
    percentile_df = pd.DataFrame(percentile_data)
    
    fig = px.bar(
        percentile_df,
        x='Stat',
        y='Percentile',
        title=f"{pokemon_data['name']} Percentile Rankings (vs all Pokemon)",
        color='Percentile',
        color_continuous_scale='RdYlGn',
        text='Percentile'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(showlegend=False, height=350, yaxis_range=[0, 110])
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional info
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Battle Info")
        st.markdown(f"**BST Tier:** {pokemon_data['bst_tier']}")
        st.markdown(f"**Speed Tier:** {pokemon_data['speed_tier']}")
        st.markdown(f"**Offensive Rating:** {pokemon_data['offensive_rating']:.1f}")
        st.markdown(f"**Defensive Rating:** {pokemon_data['defensive_rating']:.1f}")
        st.markdown(f"**Battle Style:** {pokemon_data.get('battle_style', 'N/A')}")
    
    with col2:
        st.subheader("🛡️ Defensive Profile")
        st.markdown(f"**Resistances:** {int(pokemon_data.get('resistances_count', 0))}")
        st.markdown(f"**Weaknesses:** {int(pokemon_data.get('weaknesses_count', 0))}")
        st.markdown(f"**Immunities:** {int(pokemon_data.get('immunities_count', 0))}")
        st.markdown(f"**Defensive Score:** {pokemon_data.get('defensive_score', 0):.1f}")
    
    # Descriptions
    if pd.notna(pokemon_data.get('smogon_description')):
        st.subheader("📝 Smogon Description")
        st.write(pokemon_data['smogon_description'])
    
    if pd.notna(pokemon_data.get('bulba_description')):
        st.subheader("📝 Bulbapedia Description")
        st.write(pokemon_data['bulba_description'])
    
    if pd.notna(pokemon_data.get('corpus_description')):
        st.subheader("📝 Additional Information")
        st.write(pokemon_data['corpus_description'][:500] + "..." if len(str(pokemon_data['corpus_description'])) > 500 else pokemon_data['corpus_description'])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use filters to narrow down Pokemon based on your criteria!")
st.sidebar.markdown("**Data Source**: Pokemon National Dex (1045 Pokemon)")
