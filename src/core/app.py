"""
Enhanced Pokémon Dashboard - Comprehensive Statistics & Competitive Analysis
Version 5.4.2 - Utility System (Error Logging, Data Validation, Backups, Performance)
Latest Update: November 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
from PIL import Image
import io
import base64
import sys

# Add features directory to path
features_path = Path(__file__).parent.parent / "features"
sys.path.insert(0, str(features_path))

# Add utils directory to path
utils_path = Path(__file__).parent.parent / "utils"
sys.path.insert(0, str(utils_path))

# Import feature modules
from dark_mode import dark_mode_toggle, apply_dark_mode, get_theme_colors
from type_calculator import display_type_calculator
from team_builder import display_team_builder
from advanced_search import create_advanced_filters, quick_search_bar, display_filter_summary
from variant_stats import display_variant_statistics

# Import utility modules
try:
    from error_logger import get_error_logger, log_error
    from data_validator import DataValidator
    from backup_manager import BackupManager
    from performance_profiler import get_profiler, profile
    UTILS_AVAILABLE = True
except ImportError as e:
    UTILS_AVAILABLE = False
    print(f"Warning: Utility modules not available: {e}")

# Initialize utilities if available
if UTILS_AVAILABLE:
    error_logger = get_error_logger()
    profiler = get_profiler()

# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="National Pokédex Dashboard - Enhanced",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DATA LOADING ====================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_main_dataset():
    """Load the enhanced National Dex CSV with variants - 1,130 entries (1,025 base + 105 variants)"""
    try:
        if UTILS_AVAILABLE:
            profiler.start_timer('load_main_dataset')
        
        # Try new variant CSV first
        variant_csv_path = Path("data/national_dex_with_variants.csv")
        if variant_csv_path.exists():
            df = pd.read_csv(variant_csv_path)
            # Add variant support columns if missing
            if 'variant_type' not in df.columns:
                df['variant_type'] = 'base'
            if 'base_pokemon_id' not in df.columns:
                df['base_pokemon_id'] = df['pokedex_number']
            
            if UTILS_AVAILABLE:
                profiler.end_timer('load_main_dataset', {'rows': len(df)})
            return df
        
        # Fallback to original CSV
        csv_path = Path("data/national_dex.csv")
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            # Add variant columns for compatibility
            df['variant_type'] = 'base'
            df['base_pokemon_id'] = df['pokedex_number']
            if len(df) < 1025:
                st.warning(f"⚠️ Data may be outdated. Expected 1025 Pokemon, found {len(df)}")
            
            if UTILS_AVAILABLE:
                profiler.end_timer('load_main_dataset', {'rows': len(df)})
            return df
        
        if UTILS_AVAILABLE:
            profiler.end_timer('load_main_dataset', {'status': 'failed'})
        return None
    
    except Exception as e:
        if UTILS_AVAILABLE:
            log_error(e, context={'function': 'load_main_dataset'}, severity='CRITICAL')
        st.error(f"Error loading dataset: {e}")
        return None

@st.cache_data
def load_competitive_data():
    """Load competitive data (IVs, EVs, Natures)"""
    json_path = Path("data/competitive/competitive_data.json")
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    return None

@st.cache_data
def load_natures():
    """Load nature information"""
    json_path = Path("data/competitive/natures_reference.json")
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

@st.cache_data
def load_game_data():
    """Load comprehensive game data"""
    json_path = Path("data/enhanced/comprehensive_game_data.json")
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    return None

def load_sprite(pokemon_id, sprite_type='official', use_animated=False, variant_type='base', shiny=False):
    """
    Load Pokemon sprite image or animation with variant support
    
    Args:
        pokemon_id: Pokemon ID number
        sprite_type: 'official', 'icon', or 'animated'
        use_animated: If True, tries to load GIF animation first
        variant_type: 'base', 'mega', 'mega-x', 'mega-y', 'alolan', 'galarian', 'gigantamax', etc.
        shiny: If True, loads shiny variant
    
    Returns:
        tuple: (content, is_gif) - content is either Image or file path
    """
    # Build filename based on variant and shiny
    if variant_type != 'base':
        variant_suffix = variant_type.replace('-', '_')
        base_filename = f"{pokemon_id:03d}_{variant_suffix}"
    else:
        base_filename = f"{pokemon_id:03d}"
    
    if shiny:
        base_filename += "_shiny"
    
    # Try animated GIF first if requested
    if use_animated or sprite_type == 'animated':
        animated_dir = Path("assets/sprites/animated")
        gif_path = animated_dir / f"{base_filename}.gif"
        if gif_path.exists():
            return (str(gif_path), True)
    
    # Determine directory based on type and shiny
    if sprite_type == 'icon':
        sprite_dir = Path("assets/icons")
    elif shiny:
        sprite_dir = Path("assets/sprites/shiny")
        # Remove _shiny suffix since it's already in the directory
        base_filename = base_filename.replace("_shiny", "")
    else:  # official
        sprite_dir = Path("assets/sprites")
    
    # Try to find PNG sprite with exact filename
    png_path = sprite_dir / f"{base_filename}.png"
    if png_path.exists():
        try:
            return (Image.open(png_path), False)
        except Exception:
            pass
    
    # Fallback: Try base sprite if variant not found
    if variant_type != 'base':
        fallback_path = sprite_dir / f"{pokemon_id:03d}.png"
        if fallback_path.exists():
            try:
                return (Image.open(fallback_path), False)
            except Exception:
                pass
    
    # Final fallback: Try to load from PokeAPI URL directly
    try:
        import requests
        response = requests.get(
            f"https://raw.githubusercontent.com/PokeAPI/sprites/master/"
            f"sprites/pokemon/other/official-artwork/{pokemon_id}.png",
            timeout=5
        )
        if response.status_code == 200:
            return (Image.open(io.BytesIO(response.content)), False)
    except Exception:
        pass
    
    return (None, False)


def display_sprite(sprite_data, width=None, use_container_width=False):
    """
    Display sprite - handles both static PNG and animated GIF
    
    Args:
        sprite_data: tuple (content, is_gif) from load_sprite()
        width: Width in pixels for static images
        use_container_width: Use container width for static images
    """
    if sprite_data[0] is None:
        st.write("🎮 No sprite available")
        return
    
    content, is_gif = sprite_data
    
    if is_gif:
        # Display animated GIF using HTML
        with open(content, "rb") as f:
            gif_data = f.read()
            gif_b64 = io.BytesIO(gif_data)
            import base64
            gif_encoded = base64.b64encode(gif_data).decode()
            
        style = f"width: {width}px;" if width else "width: 100%;"
        st.markdown(
            f'<img src="data:image/gif;base64,{gif_encoded}" '
            f'style="{style}" alt="Pokemon sprite">',
            unsafe_allow_html=True
        )
    else:
        # Display static PNG
        if width:
            st.image(content, width=width)
        elif use_container_width:
            st.image(content, use_container_width=True)
        else:
            st.image(content)

# ==================== HELPER FUNCTIONS ====================

def get_pokemon_variants(df, base_pokemon_id):
    """Get all variant forms of a Pokemon"""
    if 'base_pokemon_id' not in df.columns:
        return []
    
    # Get all forms with matching base_pokemon_id (including base form)
    variants = df[df['base_pokemon_id'] == base_pokemon_id].copy()
    
    # Sort: base first, then mega, then others
    variant_order = {'base': 0, 'mega': 1, 'mega-x': 2, 'mega-y': 3, 
                     'alolan': 4, 'galarian': 5, 'hisuian': 6, 
                     'paldean': 7, 'gigantamax': 8}
    
    if 'variant_type' in variants.columns:
        variants['sort_order'] = variants['variant_type'].map(
            lambda x: variant_order.get(x, 99)
        )
        variants = variants.sort_values('sort_order')
    
    return variants.to_dict('records')


@st.cache_data
def get_type_color(type_name):
    """Get color for Pokemon type - Cached for performance"""
    colors = {
        'Normal': '#A8A878', 'Fire': '#F08030', 'Water': '#6890F0',
        'Electric': '#F8D030', 'Grass': '#78C850', 'Ice': '#98D8D8',
        'Fighting': '#C03028', 'Poison': '#A040A0', 'Ground': '#E0C068',
        'Flying': '#A890F0', 'Psychic': '#F85888', 'Bug': '#A8B820',
        'Rock': '#B8A038', 'Ghost': '#705898', 'Dragon': '#7038F8',
        'Dark': '#705848', 'Steel': '#B8B8D0', 'Fairy': '#EE99AC'
    }
    return colors.get(type_name, '#777777')

def display_pokemon_card(pokemon, show_sprite=True, use_animated=True, shiny=False):
    """Display a Pokemon card with sprite and info, supporting variants"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if show_sprite:
            pokemon_id = int(pokemon['pokedex_number'])
            variant_type = pokemon.get('variant_type', 'base')
            sprite_data = load_sprite(
                pokemon_id, 
                use_animated=use_animated,
                variant_type=variant_type,
                shiny=shiny
            )
            if sprite_data[0] is not None:
                display_sprite(sprite_data, width=150)
            else:
                st.write("🎮 No sprite")
    
    with col2:
        poke_num = int(pokemon['pokedex_number'])
        poke_name = pokemon['name']
        
        # Show form name if it's a variant
        if 'form_name' in pokemon and pd.notna(pokemon['form_name']):
            variant_badge = "✨" if shiny else ""
            st.markdown(f"### #{poke_num:04d} {variant_badge}{pokemon['form_name']}")
        else:
            st.markdown(f"### #{poke_num:04d} {poke_name}")
        
        # Type badges
        type1 = pokemon["type_1"]
        type_color1 = get_type_color(type1)
        type_html = (
            f'<span class="type-badge" '
            f'style="background-color: {type_color1}">{type1}</span>'
        )
        
        if pd.notna(pokemon.get('type_2')) and pokemon.get('type_2'):
            type2 = pokemon["type_2"]
            type_color2 = get_type_color(type2)
            type_html += (
                f'<span class="type-badge" '
                f'style="background-color: {type_color2}">{type2}</span>'
            )
        st.markdown(type_html, unsafe_allow_html=True)
        
        # Stats
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("HP", int(pokemon.get('hp', 0)))
        with col_b:
            st.metric("Attack", int(pokemon.get('attack', 0)))
        with col_c:
            st.metric("Defense", int(pokemon.get('defense', 0)))

def create_stat_distribution_chart(df, stat_name):
    """Create an interactive distribution chart for a stat"""
    fig = px.histogram(
        df, 
        x=stat_name,
        nbins=50,
        title=f'{stat_name.title()} Distribution Across All Pokémon',
        labels={stat_name: stat_name.title()},
        color_discrete_sequence=['#ff6b6b']
    )
    fig.update_layout(
        showlegend=False,
        height=400,
        hovermode='x unified'
    )
    return fig

def create_type_effectiveness_heatmap(pokemon):
    """Create type effectiveness heatmap for a Pokemon"""
    types = [
        'normal', 'fire', 'water', 'electric', 'grass', 'ice',
        'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
        'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'
    ]
    
    effectiveness = []
    for t in types:
        col_name = f'against_{t}'
        if col_name in pokemon:
            effectiveness.append(pokemon[col_name])
        else:
            effectiveness.append(1.0)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=[effectiveness],
        x=[t.title() for t in types],
        y=['Defensive'],
        colorscale=[
            [0, '#00ff00'],  # Immune (0x)
            [0.25, '#90EE90'],  # Resistant (0.25x, 0.5x)
            [0.5, '#FFFF00'],  # Normal (1x)
            [0.75, '#FFA500'],  # Weak (2x)
            [1, '#FF0000']  # Very Weak (4x)
        ],
        text=[[f'{e}x' for e in effectiveness]],
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Multiplier")
    ))
    
    fig.update_layout(
        title='Type Effectiveness (Defensive)',
        height=200,
        xaxis_title='Attacking Type',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

# ==================== MAIN APP ====================

def main():
    """Main application logic"""
    
    # Apply custom CSS styling
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .main-header {
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(135deg, #22c55e 0%, #10b981 25%, #14b8a6 50%, #06b6d4 75%, #22c55e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradient 3s ease infinite;
            margin-bottom: 1rem;
            text-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .stat-card {
            background: linear-gradient(135deg, #374151 0%, #1F2937 100%);
            padding: 1.8rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            box-shadow: 0 8px 16px rgba(31, 41, 55, 0.4);
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(31, 41, 55, 0.6);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        /* Hide metric delta indicators */
        .stat-card [data-testid="stMetricDelta"] {
            display: none !important;
        }
        
        .stat-card div[data-testid="metric-container"] > div:last-child {
            display: none !important;
        }
        
        /* Enhanced Tab Spacing */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            padding: 0.5rem 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(34, 197, 94, 0.1);
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #22c55e 0%, #10b981 100%);
            color: white !important;
        }
        
        .pokemon-card {
            border: 2px solid #374151;
            border-radius: 16px;
            padding: 1.5rem;
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        
        .pokemon-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(34, 197, 94, 0.3);
            border-color: #22c55e;
        }
        
        .type-badge {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 24px;
            font-weight: 700;
            margin: 0.3rem;
            font-size: 0.9rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transition: transform 0.2s;
        }
        
        .type-badge:hover {
            transform: scale(1.1);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
            padding: 12px;
            border-radius: 16px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 56px;
            padding: 0 24px;
            font-weight: 700;
            border-radius: 12px;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(34, 197, 94, 0.1);
            border-color: #22c55e;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #22c55e 0%, #10b981 100%);
            color: white !important;
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
        }
        
        .randomizer-button {
            background: linear-gradient(135deg, #22c55e 0%, #10b981 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            border: none;
            font-size: 1.1rem;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .randomizer-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(34, 197, 94, 0.4);
        }
        
        .game-container {
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            border: 2px solid #22c55e;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">⚡ National Pokédex Dashboard ⚡</h1>', unsafe_allow_html=True)
    st.markdown("### Version 5.4.2 - Enhanced System with Utilities & Admin Dashboard")
    st.caption("🔥 NEW: Admin Utilities | Error Logging | Backups | Performance Monitoring | Data Validation")
    
    # Startup validation (non-blocking)
    if UTILS_AVAILABLE:
        validator = DataValidator()
        with st.spinner("� Validating data files..."):
            validation_results = validator.validate_all_data_files()
            
            # Show warnings for any issues (non-blocking)
            if 'files' in validation_results:
                for result in validation_results['files']:
                    if not result.get('valid', True):
                        st.warning(f"⚠️ Data validation warning in {result.get('file', 'unknown')}: "
                                 f"{result.get('error', 'Unknown issue')}")
    
    # Load data
    df = load_main_dataset()
    comp_df = load_competitive_data()
    natures = load_natures()
    
    if df is None:
        st.error("❌ Could not load Pokemon data. Please ensure data/national_dex.csv exists.")
        st.info("💡 Try refreshing the page or clearing the cache.")
        if UTILS_AVAILABLE:
            log_error(
                ValueError("Failed to load main dataset"),
                context={'function': 'main', 'data_file': 'national_dex.csv'},
                severity='CRITICAL'
            )
        return
    
    # Display actual data count
    st.sidebar.info(f"📊 **Loaded {len(df)} Pokémon** | v5.0.0")
    
    # Sidebar - Dark Mode & Global Filters
    with st.sidebar:
        # Dark Mode Toggle (NEW in v5.0.0!)
        st.markdown("### 🌙 Theme")
        dark_mode = dark_mode_toggle()
        apply_dark_mode(dark_mode)
        
        st.markdown("---")
        
        st.header("🔍 Filters")
        
        # Cache management
        if st.button("🔄 Clear Cache & Reload Data", help="Clear cached data and reload from source"):
            st.cache_data.clear()
            st.rerun()
        
        # Animation toggle
        st.subheader("🎬 Display Options")
        use_animations = st.checkbox(
            "Enable Animated Sprites",
            value=True,
            help="Show moving GIF sprites when available"
        )
        
        # Shiny mode toggle
        shiny_mode = st.checkbox(
            "✨ Shiny Mode",
            value=False,
            help="Display shiny variants of all Pokemon"
        )
        
        st.markdown("---")
        
        # Variant filter (NEW!)
        st.subheader("🔥 Variant Forms")
        variant_options = ["Base Forms", "Mega Evolution", "Regional Forms", "Gigantamax"]
        selected_variants = st.multiselect(
            "Show Forms",
            options=variant_options,
            default=["Base Forms"],
            help="Filter by Pokemon form types"
        )
        
        st.markdown("---")
        
        # Generation filter
        generations = ["All"] + [f"Gen {i}" for i in range(1, 10)]
        selected_gen = st.selectbox("Generation", generations)
        
        # Type filter
        all_types = sorted(df['type_1'].dropna().unique())
        selected_types = st.multiselect("Primary Type", all_types)
        
        # Status filter
        statuses = ["All", "Normal", "Legendary", "Mythical"]
        selected_status = st.selectbox("Status", statuses)
        
        # Stat range filters
        st.subheader("Stat Ranges")
        min_bst = st.slider("Min Base Stat Total", 0, 800, 0)
        max_bst = st.slider("Max Base Stat Total", 0, 800, 800)
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply variant filter (NEW!)
        if selected_variants:
            variant_filter = []
            if "Base Forms" in selected_variants:
                variant_filter.append('base')
            if "Mega Evolution" in selected_variants:
                variant_filter.extend(['mega', 'mega-x', 'mega-y'])
            if "Regional Forms" in selected_variants:
                variant_filter.extend(['alolan', 'galarian', 'hisuian', 'paldean'])
            if "Gigantamax" in selected_variants:
                variant_filter.append('gigantamax')
            
            if variant_filter and 'variant_type' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['variant_type'].isin(variant_filter)]
        
        if selected_gen != "All":
            gen_num = int(selected_gen.split()[1])
            filtered_df = filtered_df[filtered_df['generation'] == gen_num]
        
        if selected_types:
            filtered_df = filtered_df[filtered_df['type_1'].isin(selected_types)]
        
        if selected_status != "All":
            filtered_df = filtered_df[filtered_df['status'] == selected_status]
        
        filtered_df = filtered_df[
            (filtered_df['total_points'] >= min_bst) &
            (filtered_df['total_points'] <= max_bst)
        ]
        
        st.markdown(f"**{len(filtered_df)}** Pokémon match filters")
    
    # Main Tabs (v5.4.2 - Added Admin Utilities)
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18 = st.tabs([
        "📊 Overview",
        "🔍 Pokémon Search",
        "⚔️ Competitive Analysis",
        "📈 Statistics & Trends",
        "🎨 Type Analysis",
        "🧬 Evolution & Forms",
        "🎮 By Game",
        "🎨 Sprite Gallery",
        "⚡ Type Calculator",
        "👥 Team Builder",
        "📊 Variant Statistics",
        "🏆 Legacy Team Builder",
        "📊 Meta Analytics",
        "⚔️ Damage Calculator",
        "🤖 Team Recommender",
        "🔍 Sprite Comparison",
        "📤 Advanced Export",
        "🛠️ Admin Utilities"
    ])
    
    # ==================== TAB 1: OVERVIEW ====================
    with tab1:
        # Hero Section with Gradient
        st.markdown("""
            <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%); 
                        padding: 3rem 2rem; border-radius: 20px; margin-bottom: 2rem;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.3);">
                <h1 style="text-align: center; color: white; font-size: 3rem; margin-bottom: 1rem;">
                    ⚡ National Pokédex Dashboard
                </h1>
                <p style="text-align: center; color: rgba(255,255,255,0.9); font-size: 1.2rem;">
                    Complete Database of All 1,194 Pokémon Forms • Generations I-IX
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Key Statistics Grid - Redesigned
        st.markdown("### 📊 Dataset Statistics")
        
        # Row 1: Main Stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            padding: 2rem; border-radius: 16px; text-align: center;
                            box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎮</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: white;">{}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 1rem;">Total Pokémon</div>
                </div>
            """.format(len(df)), unsafe_allow_html=True)
        
        with col2:
            generations = df['generation'].nunique()
            st.markdown("""
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
                            padding: 2rem; border-radius: 16px; text-align: center;
                            box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🌍</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: white;">{}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 1rem;">Generations</div>
                </div>
            """.format(generations), unsafe_allow_html=True)
        
        with col3:
            variant_count = len(df[df['variant_type'] != 'base']) if 'variant_type' in df.columns else 0
            st.markdown("""
                <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
                            padding: 2rem; border-radius: 16px; text-align: center;
                            box-shadow: 0 8px 16px rgba(139, 92, 246, 0.3);">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">✨</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: white;">{}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 1rem;">Variant Forms</div>
                </div>
            """.format(variant_count), unsafe_allow_html=True)
        
        with col4:
            total_types = df['type_1'].nunique()
            st.markdown("""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                            padding: 2rem; border-radius: 16px; text-align: center;
                            box-shadow: 0 8px 16px rgba(245, 158, 11, 0.3);">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎨</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: white;">{}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 1rem;">Unique Types</div>
                </div>
            """.format(total_types), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 2: Special Categories
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            legendary_count = len(df[df['status'] == 'Legendary'])
            st.markdown("""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
                            padding: 1.5rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 6px 12px rgba(239, 68, 68, 0.3);">
                    <div style="font-size: 2rem;">👑</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: white;">{}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">Legendary</div>
                </div>
            """.format(legendary_count), unsafe_allow_html=True)
        
        with col6:
            mythical_count = len(df[df['status'] == 'Mythical'])
            st.markdown("""
                <div style="background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
                            padding: 1.5rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 6px 12px rgba(236, 72, 153, 0.3);">
                    <div style="font-size: 2rem;">🌟</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: white;">{}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">Mythical</div>
                </div>
            """.format(mythical_count), unsafe_allow_html=True)
        
        with col7:
            mega_count = len(df[df['variant_type'].str.contains('mega', case=False, na=False)]) if 'variant_type' in df.columns else 0
            st.markdown("""
                <div style="background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
                            padding: 1.5rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 6px 12px rgba(6, 182, 212, 0.3);">
                    <div style="font-size: 2rem;">💎</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: white;">{}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">Mega Forms</div>
                </div>
            """.format(mega_count), unsafe_allow_html=True)
        
        with col8:
            regions = df['region'].nunique() if 'region' in df.columns else 9
            st.markdown("""
                <div style="background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
                            padding: 1.5rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 6px 12px rgba(20, 184, 166, 0.3);">
                    <div style="font-size: 2rem;">🗺️</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: white;">{}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">Regions</div>
                </div>
            """.format(regions), unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # POKEMON RANDOMIZER
        st.subheader("🎲 Pokémon Randomizer")
        col_random1, col_random2, col_random3 = st.columns([2, 1, 2])
        
        with col_random2:
            if st.button("🎲 Generate Random Pokémon", use_container_width=True):
                random_pokemon = df.sample(1).iloc[0]
                st.session_state['random_pokemon'] = random_pokemon
        
        if 'random_pokemon' in st.session_state:
            random_poke = st.session_state['random_pokemon']
            st.markdown('<div class="game-container">', unsafe_allow_html=True)
            
            col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
            
            # Left column - Sprite
            with col_r1:
                poke_id = int(random_poke['pokedex_number'])
                sprite_data = load_sprite(poke_id, use_animated=use_animations)
                display_sprite(sprite_data, width=200)
            
            # Middle column - Basic info and stats
            with col_r2:
                st.markdown(
                    f"<h2 style='text-align: center;'>#{poke_id:04d} {random_poke['name']}</h2>",
                    unsafe_allow_html=True
                )
                
                # Types
                type1 = random_poke["type_1"]
                type_color1 = get_type_color(type1)
                type_html = (
                    f'<div style="text-align: center;">'
                    f'<span class="type-badge" style="background-color: {type_color1}">{type1}</span>'
                )
                
                if pd.notna(random_poke.get('type_2')) and random_poke.get('type_2'):
                    type2 = random_poke["type_2"]
                    type_color2 = get_type_color(type2)
                    type_html += f'<span class="type-badge" style="background-color: {type_color2}">{type2}</span>'
                
                type_html += '</div>'
                st.markdown(type_html, unsafe_allow_html=True)
                
                st.markdown(f"**Generation:** {int(random_poke['generation'])}")
                st.markdown(f"**Species:** {random_poke.get('species', 'Unknown')}")
                
                # Base Stats
                st.markdown("#### 📊 Base Stats")
                stats_col1, stats_col2 = st.columns(2)
                with stats_col1:
                    st.metric("HP", int(random_poke['hp']))
                    st.metric("Attack", int(random_poke['attack']))
                    st.metric("Defense", int(random_poke['defense']))
                with stats_col2:
                    st.metric("Sp. Atk", int(random_poke['sp_attack']))
                    st.metric("Sp. Def", int(random_poke['sp_defense']))
                    st.metric("Speed", int(random_poke['speed']))
                
                st.markdown(f"**Total BST:** {int(random_poke['total_points'])}")
            
            # Right column - Additional info
            with col_r3:
                st.markdown("#### 🎮 Info")
                
                # Abilities
                abilities = []
                if pd.notna(random_poke.get('ability_1')):
                    abilities.append(random_poke['ability_1'])
                if pd.notna(random_poke.get('ability_2')):
                    abilities.append(random_poke['ability_2'])
                if pd.notna(random_poke.get('ability_hidden')):
                    abilities.append(f"{random_poke['ability_hidden']} (H)")
                
                if abilities:
                    st.markdown(f"**Abilities:**")
                    for ability in abilities:
                        st.caption(f"• {ability}")
                
                # Evolution chain
                if pd.notna(random_poke.get('evolution_chain')):
                    evo_chain_id = random_poke['evolution_chain']
                    chain_members = df[df['evolution_chain'] == evo_chain_id]['name'].tolist()
                    if len(chain_members) > 1:
                        st.markdown(f"**Evolution:**")
                        st.caption(f"{' → '.join(chain_members)}")
                
                # Physical characteristics
                st.markdown(f"**Height:** {random_poke.get('height_m', 'N/A')} m")
                st.markdown(f"**Weight:** {random_poke.get('weight_kg', 'N/A')} kg")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # POKEMON GUESSING GAME
        st.subheader("🎮 Who's That Pokémon?")
        
        if 'game_pokemon' not in st.session_state:
            st.session_state['game_pokemon'] = None
            st.session_state['game_revealed'] = False
            st.session_state['game_score'] = 0
            st.session_state['game_attempts'] = 0
        
        col_game1, col_game2 = st.columns([1, 2])
        
        with col_game1:
            if st.button("🎮 Start New Game", use_container_width=True):
                st.session_state['game_pokemon'] = df.sample(1).iloc[0]
                st.session_state['game_revealed'] = False
            
            if st.button("🔄 Reset Score", use_container_width=True):
                st.session_state['game_score'] = 0
                st.session_state['game_attempts'] = 0
                st.success("Score reset!")
        
        with col_game2:
            st.markdown(
                f"**Score:** {st.session_state['game_score']} / {st.session_state['game_attempts']}"
            )
        
        if st.session_state['game_pokemon'] is not None:
            game_poke = st.session_state['game_pokemon']
            
            st.markdown('<div class="game-container">', unsafe_allow_html=True)
            
            if not st.session_state['game_revealed']:
                col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
                with col_g2:
                    poke_id = int(game_poke['pokedex_number'])
                    sprite_data = load_sprite(poke_id, use_animated=False)
                    
                    if sprite_data[0] is not None:
                        content, is_gif = sprite_data
                        if not is_gif:
                            try:
                                from PIL import ImageOps, ImageEnhance, ImageDraw
                                # Create a proper silhouette
                                img = content.convert("RGBA")
                                # Create black silhouette from alpha channel
                                silhouette = Image.new("RGBA", img.size, (0, 0, 0, 0))
                                draw = ImageDraw.Draw(silhouette)
                                # Use alpha channel to create black silhouette
                                for x in range(img.width):
                                    for y in range(img.height):
                                        r, g, b, a = img.getpixel((x, y))
                                        if a > 50:  # If not transparent
                                            silhouette.putpixel((x, y), (0, 0, 0, 255))
                                st.image(silhouette, width=250)
                            except Exception as e:
                                st.warning(f"Could not create silhouette. Error: {e}")
                                # Fallback: show a placeholder
                                st.markdown("### 🎮 **WHO'S THAT POKEMON?**")
                        else:
                            st.warning("Animated sprites not supported for quiz")
                    else:
                        st.error("Could not load Pokemon sprite")
                    
                    st.markdown("### Guess the Pokémon!")
                    
                    guess = st.text_input(
                        "Enter Pokémon name:",
                        key="guess_input"
                    )
                    
                    if st.button("✅ Submit Guess"):
                        st.session_state['game_attempts'] += 1
                        if guess.lower().strip() == game_poke['name'].lower().strip():
                            st.session_state['game_score'] += 1
                            st.session_state['game_revealed'] = True
                            st.success("🎉 Correct!")
                            st.balloons()
                        else:
                            st.error(f"❌ Wrong! Try again or reveal the answer.")
                    
                    if st.button("👁️ Reveal"):
                        st.session_state['game_revealed'] = True
                        st.info(f"It was {game_poke['name']}!")
            else:
                col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
                with col_g2:
                    poke_id = int(game_poke['pokedex_number'])
                    sprite_data = load_sprite(poke_id, use_animated=use_animations)
                    display_sprite(sprite_data, width=250)
                    
                    st.markdown(
                        f"<h2 style='text-align: center;'>#{poke_id:04d} {game_poke['name']}</h2>",
                        unsafe_allow_html=True
                    )
                    
                    st.info("Click 'Start New Game' to play again!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ===== ENHANCED DATA VISUALIZATIONS =====
        st.markdown("### 📈 Dataset Analytics & Visualizations")
        
        # Row 1: Regional & Type Distribution
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Regional Distribution (if region data exists)
            if 'region' in df.columns and df['region'].notna().any():
                region_counts = df['region'].value_counts().sort_index()
                fig = px.bar(
                    x=region_counts.index,
                    y=region_counts.values,
                    title='🗺️ Pokémon Distribution by Region',
                    labels={'x': 'Region', 'y': 'Number of Pokémon'},
                    color=region_counts.values,
                    color_continuous_scale=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'],
                    text=region_counts.values
                )
                fig.update_traces(textposition='outside', textfont_size=12)
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    xaxis_title="Region",
                    yaxis_title="Count",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True, key="overview_region_bar")
            else:
                # Pokemon by Generation as fallback
                gen_counts = df.groupby('generation').size().reset_index(name='count')
                fig = px.bar(
                    gen_counts,
                    x='generation',
                    y='count',
                    title='🎮 Pokémon Count by Generation',
                    labels={'generation': 'Generation', 'count': 'Number of Pokémon'},
                    color='count',
                    color_continuous_scale='viridis',
                    text='count'
                )
                fig.update_traces(textposition='outside', textfont_size=12)
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True, key="overview_gen_bar")
        
        with viz_col2:
            # Type Distribution - Pie Chart
            type_counts = df['type_1'].value_counts()
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title='🎨 Primary Type Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=10
            )
            fig.update_layout(
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )
            st.plotly_chart(fig, use_container_width=True, key="overview_type_pie")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 2: Generation Timeline & Top Types
        viz_col3, viz_col4 = st.columns(2)
        
        with viz_col3:
            # Generation Timeline with Cumulative Count
            gen_counts = df.groupby('generation').size().reset_index(name='count')
            gen_counts['cumulative'] = gen_counts['count'].cumsum()
            
            fig = px.area(
                gen_counts,
                x='generation',
                y='cumulative',
                title='📊 Cumulative Pokémon Count by Generation',
                labels={'generation': 'Generation', 'cumulative': 'Total Pokémon'},
                color_discrete_sequence=['#22c55e']
            )
            fig.add_scatter(
                x=gen_counts['generation'],
                y=gen_counts['count'],
                mode='markers+lines',
                name='Per Generation',
                marker=dict(size=10, color='#3b82f6'),
                line=dict(color='#3b82f6', width=2)
            )
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True, key="overview_gen_timeline")
        
        with viz_col4:
            # Top 10 Types - Horizontal Bar
            type_counts_top = df['type_1'].value_counts().head(10)
            fig = px.bar(
                x=type_counts_top.values,
                y=type_counts_top.index,
                orientation='h',
                title='🏆 Top 10 Primary Types',
                labels={'x': 'Count', 'y': 'Type'},
                color=type_counts_top.values,
                color_continuous_scale='plasma',
                text=type_counts_top.values
            )
            fig.update_traces(textposition='outside', textfont_size=12)
            fig.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True, key="overview_type_bar")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 3: Base Stat Total Distribution
        st.markdown("### 💪 Base Stat Total (BST) Distribution")
        fig = create_stat_distribution_chart(df, 'total_points')
        st.plotly_chart(fig, use_container_width=True, key="overview_bst_dist")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Asset Coverage Section
        st.markdown("### 🖼️ Asset Coverage Statistics")
        
        asset_col1, asset_col2, asset_col3 = st.columns(3)
        
        # Count available sprites
        total_pokemon = len(df)
        sprites_with_paths = df['sprite_path'].notna().sum() if 'sprite_path' in df.columns else 0
        shiny_with_paths = df['shiny_path'].notna().sum() if 'shiny_path' in df.columns else 0
        
        sprite_coverage = (sprites_with_paths / total_pokemon * 100) if total_pokemon > 0 else 0
        shiny_coverage = (shiny_with_paths / total_pokemon * 100) if total_pokemon > 0 else 0
        
        with asset_col1:
            st.markdown(f"""
                <div style="padding: 1.5rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎨</div>
                    <div style="font-size: 2rem; font-weight: bold; color: white;">{sprite_coverage:.1f}%</div>
                    <div style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">Regular Sprites</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{sprites_with_paths:,} / {total_pokemon:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with asset_col2:
            st.markdown(f"""
                <div style="padding: 1.5rem; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                            border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">✨</div>
                    <div style="font-size: 2rem; font-weight: bold; color: white;">{shiny_coverage:.1f}%</div>
                    <div style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">Shiny Sprites</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{shiny_with_paths:,} / {total_pokemon:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with asset_col3:
            # Type icons (18 types * 4 sizes = 72 files)
            type_icon_count = 72
            expected_type_icons = 72
            type_icon_coverage = (type_icon_count / expected_type_icons * 100)
            
            st.markdown(f"""
                <div style="padding: 1.5rem; background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
                            border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🏷️</div>
                    <div style="font-size: 2rem; font-weight: bold; color: white;">{type_icon_coverage:.0f}%</div>
                    <div style="color: rgba(255,255,255,0.9); margin-top: 0.5rem;">Type Icons</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{type_icon_count} / {expected_type_icons}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # ==================== TAB 2: POKEMON SEARCH ====================
    with tab2:
        st.header("🔍 Pokémon Search & Details")
        
        # Quick search bar (NEW v5.0.0)
        search_filtered_df = quick_search_bar(filtered_df)
        
        # Advanced filters (NEW v5.0.0)
        with st.expander("🔧 Advanced Filters & Presets", expanded=False):
            search_filtered_df = create_advanced_filters(search_filtered_df)
            display_filter_summary(len(filtered_df), len(search_filtered_df))
        
        st.markdown("---")
        
        # Enhanced Dynamic Search Interface
        st.markdown("### 🔍 Dynamic Pokemon Search")
        st.caption("🎯 Type to see instant results with sprites and stats")
        
        search_col1, search_col2, search_col3 = st.columns([3, 2, 1])
        
        with search_col1:
            search_query = st.text_input(
                "Search Pokemon",
                placeholder="🔎 Start typing: Pikachu, Charizard, 25, Fire, Dragon...",
                help="Search by name, number, type, or generation",
                label_visibility="collapsed"
            )
        
        with search_col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Pokédex #", "Name", "Total Stats", "HP", "Attack", "Defense"],
                label_visibility="collapsed"
            )
        
        with search_col3:
            results_limit = st.selectbox(
                "Results",
                [10, 20, 50, 100],
                index=1,
                label_visibility="collapsed"
            )
        
        # Display filtered Pokemon (use advanced filtered data)
        display_df = search_filtered_df.copy()
        
        # Enhanced search: Support name, number, type, and generation
        if search_query:
            search_lower = search_query.lower().strip()
            display_df = display_df[
                display_df['name'].str.contains(search_query, case=False, na=False) |
                display_df['pokedex_number'].astype(str).str.contains(search_query, na=False) |
                display_df['type_1'].str.contains(search_query, case=False, na=False) |
                display_df['type_2'].astype(str).str.contains(search_query, case=False, na=False) |
                display_df['generation'].astype(str).str.contains(search_query, na=False)
            ]
        
        # Sort
        sort_mapping = {
            "Pokédex #": "pokedex_number",
            "Name": "name",
            "Total Stats": "total_points",
            "HP": "hp",
            "Attack": "attack",
            "Defense": "defense"
        }
        display_df = display_df.sort_values(sort_mapping[sort_by]).reset_index(drop=True)
        
        # Dynamic results display with enhanced UI
        if search_query and len(display_df) > 0:
            st.success(f"✅ Found **{len(display_df)}** Pokemon matching '{search_query}'")
        elif search_query and len(display_df) == 0:
            st.warning(f"⚠️ No Pokemon found for '{search_query}'. Try a different search term.")
        else:
            st.info(f"📊 Showing **{len(display_df)}** Pokemon (filtered by advanced options)")
        
        # Pagination with dynamic limits
        items_per_page = results_limit
        total_pages = max(1, (len(display_df) - 1) // items_per_page + 1)
        page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            help=f"Navigate through {total_pages} pages of results"
        )
        
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        # Display Pokemon cards
        for idx in range(start_idx, min(end_idx, len(display_df))):
            pokemon = display_df.iloc[idx]
            
            poke_num = int(pokemon['pokedex_number'])
            poke_name = pokemon['name']
            base_id = int(pokemon.get('base_pokemon_id', poke_num))
            
            # Get all variants of this Pokemon
            variants = get_pokemon_variants(df, base_id)
            
            # Create type text for expander title
            type1 = pokemon["type_1"]
            type_text = f"[{type1}"
            
            if pd.notna(pokemon.get('type_2')) and pokemon.get('type_2'):
                type2 = pokemon["type_2"]
                type_text += f"/{type2}"
            type_text += "]"
            
            with st.expander(f"#{poke_num:04d} - {poke_name} {type_text}", expanded=False):
                # Show variant tabs if multiple forms exist
                if len(variants) > 1:
                    variant_tabs = st.tabs([
                        v.get('form_name', v['name']) if pd.notna(v.get('form_name')) 
                        else v['name'] for v in variants
                    ])
                    
                    for tab_idx, variant in enumerate(variants):
                        with variant_tabs[tab_idx]:
                            display_pokemon_card(variant, use_animated=use_animations, shiny=shiny_mode)
                            
                            # Show variant-specific info
                            if variant.get('variant_type') != 'base':
                                st.info(f"**Form:** {variant.get('form_name', 'Unknown')}")
                                if pd.notna(variant.get('mega_stone')):
                                    st.write(f"🔮 **Mega Stone:** {variant['mega_stone']}")
                                if pd.notna(variant.get('gmax_move')):
                                    st.write(f"⚡ **G-Max Move:** {variant['gmax_move']}")
                else:
                    display_pokemon_card(pokemon, use_animated=use_animations, shiny=shiny_mode)
                
                # Additional details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Basic Info")
                    st.write(f"**Generation:** {int(pokemon['generation'])}")
                    st.write(f"**Status:** {pokemon['status']}")
                    st.write(f"**Species:** {pokemon.get('species', 'N/A')}")
                    st.write(f"**Height:** {pokemon.get('height_m', 'N/A')} m")
                    st.write(f"**Weight:** {pokemon.get('weight_kg', 'N/A')} kg")
                
                with col2:
                    st.subheader("Abilities")
                    if pd.notna(pokemon.get('ability_1')):
                        st.write(f"• {pokemon['ability_1']}")
                    if pd.notna(pokemon.get('ability_2')):
                        st.write(f"• {pokemon['ability_2']}")
                    if pd.notna(pokemon.get('ability_hidden')):
                        st.write(f"• **Hidden:** {pokemon['ability_hidden']}")
                
                # Type Effectiveness
                st.subheader("Type Effectiveness")
                fig = create_type_effectiveness_heatmap(pokemon)
                st.plotly_chart(fig, use_container_width=True, key=f"type_eff_{idx}")
    
    # ==================== TAB 3: COMPETITIVE ANALYSIS ====================
    with tab3:
        st.header("⚔️ Competitive Battle Analysis")
        
        if comp_df is not None:
            st.success(f"✅ Competitive data loaded for {len(comp_df)} Pokémon")
            
            # Competitive tier distribution
            col1, col2 = st.columns(2)
            
            with col1:
                tier_counts = comp_df['competitive_tier'].value_counts()
                fig = px.pie(
                    values=tier_counts.values,
                    names=tier_counts.index,
                    title='Competitive Tier Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True, key="comp_tier_chart")
            
            with col2:
                role_counts = comp_df['optimal_role'].value_counts()
                fig = px.bar(
                    x=role_counts.index,
                    y=role_counts.values,
                    title='Optimal Role Distribution',
                    labels={'x': 'Role', 'y': 'Count'},
                    color=role_counts.values,
                    color_continuous_scale='sunset'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True, key="comp_role_bar")
            
            # Pokemon selector for detailed analysis
            st.subheader("Detailed Competitive Analysis")
            selected_pokemon_name = st.selectbox(
                "Select a Pokémon",
                options=sorted(df['name'].tolist())
            )
            
            # Get Pokemon data
            pokemon_base = df[df['name'] == selected_pokemon_name].iloc[0]
            
            # Safely get competitive data if available
            comp_data = comp_df[comp_df['name'] == selected_pokemon_name]
            if len(comp_data) > 0:
                pokemon_comp = comp_data.iloc[0]
            else:
                pokemon_comp = pokemon_base  # Fallback to base data
            
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                pokemon_id = int(pokemon_base['pokedex_number'])
                sprite_data = load_sprite(pokemon_id, use_animated=use_animations)
                display_sprite(sprite_data, width=200)
                st.markdown(f"### {pokemon_base['name']}")
                
                # Safely display competitive info (may not be available for all Pokemon)
                if 'competitive_tier' in pokemon_comp and pd.notna(pokemon_comp.get('competitive_tier')):
                    st.markdown(f"**Tier:** {pokemon_comp['competitive_tier']}")
                else:
                    st.markdown("**Tier:** Not Ranked")
                
                if 'optimal_role' in pokemon_comp and pd.notna(pokemon_comp.get('optimal_role')):
                    st.markdown(f"**Role:** {pokemon_comp['optimal_role']}")
                else:
                    st.markdown("**Role:** N/A")
                
                if 'optimal_nature' in pokemon_comp and pd.notna(pokemon_comp.get('optimal_nature')):
                    st.markdown(f"**Nature:** {pokemon_comp['optimal_nature']}")
                else:
                    st.markdown("**Nature:** N/A")
            
            with col2:
                st.subheader("Optimal EV Spread")
                
                # Check if competitive data has EV spread info
                if 'optimal_ev_spread' in pokemon_comp and pokemon_comp['optimal_ev_spread'] is not None:
                    ev_spread = pokemon_comp['optimal_ev_spread']
                    ev_df = pd.DataFrame({
                        'Stat': ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
                        'EVs': [
                            ev_spread['hp'],
                            ev_spread['attack'],
                            ev_spread['defense'],
                            ev_spread['sp_attack'],
                            ev_spread['sp_defense'],
                            ev_spread['speed']
                        ]
                    })
                    
                    fig = px.bar(
                        ev_df,
                        x='Stat',
                        y='EVs',
                        title='Recommended EV Distribution',
                        color='EVs',
                        color_continuous_scale='blues'
                    )
                    fig.update_layout(showlegend=False, height=300)
                    st.plotly_chart(fig, use_container_width=True, key="comp_ev_bar")
                else:
                    st.info("No competitive EV spread data available for this Pokémon.")
            
            with col3:
                st.subheader("Stats at Level 100")
                
                # Check if competitive data has optimal stats
                if 'optimal_stats_lv100' in pokemon_comp and pokemon_comp['optimal_stats_lv100'] is not None:
                    optimal_stats = pokemon_comp['optimal_stats_lv100']
                    stats_df = pd.DataFrame({
                        'Stat': list(optimal_stats.keys()),
                        'Value': list(optimal_stats.values())
                    })
                    
                    fig = px.bar(
                        stats_df,
                        x='Stat',
                        y='Value',
                        title='Optimal Stats (31 IVs, Optimal EVs & Nature)',
                        color='Value',
                        color_continuous_scale='reds'
                    )
                    fig.update_layout(showlegend=False, height=300)
                    st.plotly_chart(fig, use_container_width=True, key="comp_stats_bar")
                else:
                    st.info("No competitive stats data available for this Pokémon.")
            
            # Nature information
            if natures:
                with st.expander("📖 Nature Guide", expanded=False):
                    st.subheader("All 25 Natures")
                    
                    nature_data = []
                    for nature_name, nature_info in natures.items():
                        increases = nature_info.get('increases', 'None')
                        decreases = nature_info.get('decreases', 'None')
                        nature_data.append({
                            'Nature': nature_name,
                            'Increases': increases if increases else 'None',
                            'Decreases': decreases if decreases else 'None'
                        })
                    
                    nature_df = pd.DataFrame(nature_data)
                    st.dataframe(nature_df, use_container_width=True, height=400)
        
        else:
            st.warning("⚠️ Competitive data not yet loaded. Run `python scripts/fetch_competitive_data.py` to generate competitive analysis.")
    
    # ==================== TAB 4: STATISTICS & TRENDS ====================
    with tab4:
        st.header("📈 Statistics & Trends Analysis")
        
        # Stat correlations
        st.subheader("Stat Correlations")
        stats_cols = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        corr_matrix = df[stats_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            x=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            y=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            color_continuous_scale='RdBu',
            aspect="auto",
            title="Stat Correlation Matrix"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True, key="stats_corr_matrix")
        
        # Scatter plots
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Attack vs Defense")
            fig = px.scatter(
                df,
                x='attack',
                y='defense',
                color='type_1',
                size='total_points',
                hover_data=['name'],
                title='Attack vs Defense by Type',
                labels={'attack': 'Attack', 'defense': 'Defense'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="stats_atk_def_scatter")
        
        with col2:
            st.subheader("Speed vs Total Stats")
            fig = px.scatter(
                df,
                x='speed',
                y='total_points',
                color='generation',
                hover_data=['name'],
                title='Speed vs Base Stat Total',
                labels={'speed': 'Speed', 'total_points': 'BST'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="stats_speed_bst_scatter")
        
        # Average stats by generation
        st.subheader("Average Stats by Generation")
        gen_stats = df.groupby('generation')[stats_cols].mean().reset_index()
        gen_stats_melted = gen_stats.melt(id_vars='generation', var_name='Stat', value_name='Average')
        
        fig = px.line(
            gen_stats_melted,
            x='generation',
            y='Average',
            color='Stat',
            markers=True,
            title='Average Stats Trend Across Generations'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True, key="stats_gen_trend_line")
    
    # ==================== TAB 5: TYPE ANALYSIS ====================
    with tab5:
        st.header("🎨 Type Analysis & Matchups")
        
        # Type combination analysis
        st.subheader("Type Combinations")
        
        df['type_combo'] = df.apply(
            lambda x: f"{x['type_1']}/{x['type_2']}" if pd.notna(x.get('type_2')) and x.get('type_2') else x['type_1'],
            axis=1
        )
        
        type_combo_counts = df['type_combo'].value_counts().head(20)
        
        fig = px.bar(
            x=type_combo_counts.index,
            y=type_combo_counts.values,
            title='Top 20 Type Combinations',
            labels={'x': 'Type Combination', 'y': 'Count'},
            color=type_combo_counts.values,
            color_continuous_scale='rainbow'
        )
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True, key="type_combo_bar")
        
        # Average stats by type
        st.subheader("Average Stats by Primary Type")
        type_stats = df.groupby('type_1')[stats_cols + ['total_points']].mean().round(1)
        type_stats = type_stats.sort_values('total_points', ascending=False)
        
        st.dataframe(
            type_stats.style.background_gradient(cmap='YlOrRd', axis=0),
            use_container_width=True,
            height=400
        )
    
    # ==================== TAB 6: EVOLUTION & FORMS ====================
    with tab6:
        st.header("🧬 Evolution & Forms")
        
        # Load main data with all forms
        if df is not None:
            st.success(f"✅ Data loaded for {len(df)} Pokémon (including forms & variants)")
            
            # Search for Pokemon (case-insensitive)
            evo_search = st.text_input(
                "Search Pokémon for evolution info",
                placeholder="e.g., Bulbasaur, Eevee, Charizard, Pikachu",
                help="Search is case-insensitive. Try 'char' or 'EEVEE' or 'pikachu'"
            )
            
            if evo_search:
                # Find matching Pokemon (case-insensitive search)
                search_lower = evo_search.lower().strip()
                matching = df[
                    df['name'].str.lower().str.contains(search_lower, na=False)
                ]
                
                if len(matching) > 0:
                    st.info(f"Found {len(matching)} Pokémon matching '{evo_search}'")
                    
                    for idx, pokemon in matching.iterrows():
                        # Check if this Pokemon has alternate forms
                        alt_name = pokemon.get('alt_name', '')
                        form_indicator = " 🔀" if pd.notna(alt_name) and alt_name.lower() != pokemon['name'].lower() else ""
                        
                        with st.expander(
                            f"#{int(pokemon['pokedex_number'])} {pokemon['name']}{form_indicator}",
                            expanded=len(matching) <= 3  # Auto-expand if 3 or fewer results
                        ):
                            col1, col2, col3 = st.columns([1, 2, 1])
                            
                            with col1:
                                poke_id = int(pokemon['pokedex_number'])
                                sprite_data = load_sprite(poke_id, use_animated=use_animations)
                                display_sprite(sprite_data, width=150)
                                
                                # Show types with colored badges
                                type1_color = get_type_color(pokemon["type_1"])
                                type_html = (
                                    f'<span style="background-color: {type1_color}; '
                                    f'color: white; padding: 5px 10px; border-radius: 5px; '
                                    f'margin: 2px; display: inline-block;">'
                                    f'{pokemon["type_1"]}</span>'
                                )
                                if pd.notna(pokemon.get("type_2")):
                                    type2_color = get_type_color(pokemon["type_2"])
                                    type_html += (
                                        f' <span style="background-color: {type2_color}; '
                                        f'color: white; padding: 5px 10px; border-radius: 5px; '
                                        f'margin: 2px; display: inline-block;">'
                                        f'{pokemon["type_2"]}</span>'
                                    )
                                st.markdown(type_html, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown(f"### {pokemon['name']}")
                                st.markdown(f"**Pokédex #:** {int(pokemon['pokedex_number'])}")
                                st.markdown(f"**Generation:** {int(pokemon['generation'])}")
                                st.markdown(f"**Species:** {pokemon.get('species', 'Unknown')}")
                                
                                # Show alternate form info
                                if pd.notna(alt_name) and alt_name.lower() != pokemon['name'].lower():
                                    st.markdown(f"**Alternate Form:** {alt_name}")
                                    if pd.notna(pokemon.get('alternate_info')):
                                        st.caption(pokemon['alternate_info'])
                                
                                # Evolution chain info
                                if pd.notna(pokemon.get('evolution_chain')):
                                    evo_chain_id = pokemon['evolution_chain']
                                    # Find all Pokemon in same evolution chain
                                    chain_members = df[df['evolution_chain'] == evo_chain_id]['name'].tolist()
                                    if len(chain_members) > 1:
                                        st.markdown(f"**Evolution Chain:** {' → '.join(chain_members)}")
                                    else:
                                        st.markdown("**Evolution:** Does not evolve")
                                else:
                                    st.markdown("**Evolution:** No evolution data")
                            
                            with col3:
                                st.markdown("#### Base Stats")
                                st.metric("HP", int(pokemon.get('hp', 0)))
                                st.metric("Attack", int(pokemon.get('attack', 0)))
                                st.metric("Defense", int(pokemon.get('defense', 0)))
                                st.metric("Sp. Atk", int(pokemon.get('sp_attack', 0)))
                                st.metric("Sp. Def", int(pokemon.get('sp_defense', 0)))
                                st.metric("Speed", int(pokemon.get('speed', 0)))
                                st.metric("Total", int(pokemon.get('total_points', 0)))
                            
                            # Show abilities
                            abilities = []
                            if pd.notna(pokemon.get('ability_1')):
                                abilities.append(pokemon['ability_1'])
                            if pd.notna(pokemon.get('ability_2')):
                                abilities.append(pokemon['ability_2'])
                            if pd.notna(pokemon.get('ability_hidden')):
                                abilities.append(f"{pokemon['ability_hidden']} (Hidden)")
                            
                            if abilities:
                                st.markdown(f"**Abilities:** {', '.join(abilities)}")
                            
                            # Show description if available
                            if pd.notna(pokemon.get('description')):
                                with st.expander("📖 Description"):
                                    st.write(pokemon['description'])
                else:
                    st.warning(f"No Pokémon found matching '{evo_search}'. Try a different search term.")
            else:
                st.info("👆 Enter a Pokémon name to view evolution & form details")
                st.caption("💡 The search is case-insensitive - try 'PIKACHU', 'eevee', or 'Charizard'")
        else:
            st.error("⏳ Data not loaded. Please check the data files.")
    
    # ==================== TAB 7: BY GAME ====================
    with tab7:
        st.header("🎮 Pokémon by Game")
        st.subheader("Filter Pokémon by their game of origin and availability")
        
        import yaml
        
        # Load games data
        games_path = Path("data/games.yaml")
        if games_path.exists():
            with open(games_path, 'r', encoding='utf-8') as f:
                games_data = yaml.safe_load(f)
            
            # Create game selector
            game_list = [(k, v['name']) for k, v in games_data.items()]
            game_names = [g[1] for g in game_list]
            
            selected_game = st.selectbox(
                "Select a Pokémon Game",
                options=game_names,
                help="Choose a game to see which Pokémon are available"
            )
            
            # Find the game key
            game_key = next((k for k, v in games_data.items() if v['name'] == selected_game), None)
            
            if game_key:
                game_info = games_data[game_key]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"### {game_info['name']}")
                    st.markdown(f"**Release Group:** {game_info['release']}")
                
                with col2:
                    # Determine generation from release
                    release_to_gen = {
                        'red-blue': 1, 'yellow': 1,
                        'gold-silver': 2, 'crystal': 2,
                        'ruby-sapphire': 3, 'firered-leafgreen': 3, 'emerald': 3,
                        'diamond-pearl': 4, 'platinum': 4, 'heartgold-soulsilver': 4,
                        'black-white': 5, 'black-white-2': 5,
                        'x-y': 6, 'omega-ruby-alpha-sapphire': 6,
                        'sun-moon': 7, 'ultra-sun-ultra-moon': 7, 'lets-go-pikachu-eevee': 7,
                        'sword-shield': 8, 'brilliant-diamond-shining-pearl': 8, 'legends-arceus': 8,
                        'scarlet-violet': 9, 'legends-z-a': 9
                    }
                    
                    game_gen = release_to_gen.get(game_info['release'], 0)
                    st.markdown(f"**Generation:** {game_gen}")
                
                st.markdown("---")
                
                # Filter Pokemon available in this game (up to that generation)
                if game_gen > 0:
                    game_pokemon = df[df['generation'] <= game_gen]
                    
                    st.success(f"✅ {len(game_pokemon)} Pokémon available in {game_info['name']}")
                    
                    # Display stats
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Pokémon", len(game_pokemon))
                    
                    with col2:
                        game_types = game_pokemon['type_1'].nunique()
                        st.metric("Types", game_types)
                    
                    with col3:
                        game_legendaries = len(game_pokemon[game_pokemon['status'] == 'Legendary'])
                        st.metric("Legendary", game_legendaries)
                    
                    # Type distribution in this game
                    st.subheader(f"Type Distribution in {game_info['name']}")
                    type_counts = game_pokemon['type_1'].value_counts().head(10)
                    
                    fig = px.bar(
                        x=type_counts.index,
                        y=type_counts.values,
                        title=f'Top 10 Types in {game_info['name']}',
                        labels={'x': 'Type', 'y': 'Count'},
                        color=type_counts.values,
                        color_continuous_scale='viridis'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True, key="game_type_bar")
                    
                    # Searchable list
                    st.subheader("Pokémon List")
                    
                    game_search = st.text_input(
                        "Search in this game's Pokédex",
                        placeholder="Search by name or number..."
                    )
                    
                    display_game_df = game_pokemon.copy()
                    if game_search:
                        display_game_df = display_game_df[
                            display_game_df['name'].str.contains(game_search, case=False, na=False) |
                            display_game_df['pokedex_number'].astype(str).str.contains(game_search, na=False)
                        ]
                    
                    # Show data table
                    st.dataframe(
                        display_game_df[[
                            'pokedex_number', 'name', 'type_1', 'type_2',
                            'total_points', 'generation', 'status'
                        ]].rename(columns={
                            'pokedex_number': 'Dex #',
                            'name': 'Name',
                            'type_1': 'Type 1',
                            'type_2': 'Type 2',
                            'total_points': 'BST',
                            'generation': 'Gen',
                            'status': 'Status'
                        }),
                        use_container_width=True,
                        height=400
                    )
        else:
            st.error("❌ Games data file not found. Please ensure data/games.yaml exists.")
    
    # ==================== TAB 8: SPRITE GALLERY ====================
    with tab8:
        st.header("🎨 Sprite Gallery")
        st.caption("Browse all Pokemon sprites with filters applied from sidebar")
        
        # Gallery controls
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 1, 1])
        with col_ctrl1:
            gallery_limit = st.slider(
                "Sprites to display",
                min_value=60,
                max_value=min(len(filtered_df), 1025),
                value=min(120, len(filtered_df)),
                step=60,
                help="Adjust number of sprites shown (more may slow loading)"
            )
        with col_ctrl2:
            sprites_per_row = st.selectbox(
                "Sprites per row",
                options=[4, 6, 8, 10],
                index=1
            )
        with col_ctrl3:
            show_names = st.checkbox("Show names", value=True)
        
        # Use filtered_df so filters apply
        display_df = filtered_df.head(gallery_limit).reset_index(drop=True)
        
        if len(filtered_df) == 0:
            st.warning("No Pokemon match the selected filters. Try adjusting your filters in the sidebar.")
        else:
            st.info(f"**Showing {len(display_df)} of {len(filtered_df)} Pokemon** (filtered results)")
            
            # Grid display of sprites with pagination
            for i in range(0, len(display_df), sprites_per_row):
                cols = st.columns(sprites_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(display_df):
                        pokemon = display_df.iloc[i + j]
                        with col:
                            pokemon_id = int(pokemon['pokedex_number'])
                            variant_type = pokemon.get('variant_type', 'base')
                            
                            # Show variant badge
                            badge = ""
                            if variant_type != 'base':
                                if 'mega' in variant_type:
                                    badge = "🔥"
                                elif variant_type in ['alolan', 'galarian', 'hisuian']:
                                    badge = "🌍"
                                elif variant_type == 'gigantamax':
                                    badge = "⚡"
                            
                            if shiny_mode:
                                badge += "✨"
                            
                            # Always use static PNG sprites in gallery for consistency
                            sprite_data = load_sprite(
                                pokemon_id,
                                use_animated=False,  # Force static sprites in gallery
                                variant_type=variant_type,
                                shiny=shiny_mode
                            )
                            display_sprite(sprite_data, use_container_width=True)
                            
                            if show_names:
                                display_name = pokemon.get('form_name', pokemon['name']) if pd.notna(pokemon.get('form_name')) else pokemon['name']
                                st.markdown(
                                    f"<div style='text-align: center; font-size: 0.75rem;'>"
                                    f"#{int(pokemon['pokedex_number']):04d} {badge}<br>"
                                    f"<b>{display_name}</b>"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )
    
    # ==================== TAB 9: TYPE CALCULATOR (NEW v5.0.0) ====================
    with tab9:
        st.header("⚡ Type Effectiveness Calculator")
        st.markdown("Calculate damage multipliers and analyze type matchups")
        display_type_calculator()
    
    # ==================== TAB 10: TEAM BUILDER (NEW v5.0.0) ====================
    with tab10:
        st.header("👥 Advanced Team Builder")
        st.markdown("Build and analyze 6-Pokémon teams with coverage analysis")
        display_team_builder(filtered_df)
    
    # ==================== TAB 11: VARIANT STATISTICS (NEW v5.0.0) ====================
    with tab11:
        st.header("📊 Variant Statistics Dashboard")
        st.markdown("Comprehensive analysis of Pokemon variants and special forms")
        display_variant_statistics(filtered_df)
    
    # ==================== TAB 12: LEGACY TEAM BUILDER ====================
    with tab12:
        st.header("🏆 Team Builder")
        st.subheader("Build your competitive team")
        
        if 'team' not in st.session_state:
            st.session_state.team = []
        
        # Team member selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            pokemon_options = sorted(df['name'].tolist())
            selected_pokemon = st.selectbox(
                "Add Pokémon to team",
                options=pokemon_options,
                key='team_selector'
            )
        
        with col2:
            if st.button("➕ Add to Team") and len(st.session_state.team) < 6:
                if selected_pokemon not in st.session_state.team:
                    st.session_state.team.append(selected_pokemon)
                    st.success(f"Added {selected_pokemon}!")
                else:
                    st.warning(f"{selected_pokemon} is already in your team!")
            
            if st.button("🗑️ Clear Team"):
                st.session_state.team = []
                st.info("Team cleared!")
        
        # Display team
        if st.session_state.team:
            st.subheader(f"Your Team ({len(st.session_state.team)}/6)")
            
            team_cols = st.columns(6)
            for idx, pokemon_name in enumerate(st.session_state.team):
                with team_cols[idx]:
                    pokemon = df[df['name'] == pokemon_name].iloc[0]
                    pokemon_id = int(pokemon['pokedex_number'])
                    sprite_data = load_sprite(
                        pokemon_id,
                        use_animated=use_animations
                    )
                    display_sprite(sprite_data, use_container_width=True)
                    st.markdown(f"**{pokemon_name}**")
                    st.markdown(f"{pokemon['type_1']}")
                    
                    if st.button("❌", key=f"remove_{idx}"):
                        st.session_state.team.pop(idx)
                        st.rerun()
            
            # Team analysis
            st.subheader("Team Analysis")
            
            team_pokemon = df[df['name'].isin(st.session_state.team)]
            
            # Type coverage
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Type Coverage:**")
                all_team_types = list(team_pokemon['type_1']) + list(team_pokemon['type_2'].dropna())
                type_coverage = pd.Series(all_team_types).value_counts()
                
                fig = px.bar(
                    x=type_coverage.index,
                    y=type_coverage.values,
                    title='Type Distribution in Team',
                    labels={'x': 'Type', 'y': 'Count'}
                )
                st.plotly_chart(fig, use_container_width=True, key="team_type_dist")
            
            with col2:
                st.markdown("**Average Stats:**")
                avg_stats = team_pokemon[stats_cols].mean().round(1)
                
                fig = px.bar(
                    x=avg_stats.index,
                    y=avg_stats.values,
                    title='Team Average Stats',
                    labels={'x': 'Stat', 'y': 'Average Value'}
                )
                st.plotly_chart(fig, use_container_width=True, key="team_avg_stats")
        else:
            st.info("👆 Select Pokémon above to build your team!")
    
    # ==================== TAB 13: META ANALYTICS ====================
    with tab13:
        try:
            # Import analytics module
            import sys
            from pathlib import Path
            analytics_path = Path(__file__).parent.parent / "analytics"
            if str(analytics_path) not in sys.path:
                sys.path.insert(0, str(analytics_path))
            
            from meta_dashboard import MetaAnalyticsDashboard
            
            dashboard = MetaAnalyticsDashboard(data_dir="data")
            dashboard.render_dashboard()
        except Exception as e:
            st.error(f"Error loading Meta Analytics: {e}")
            st.info("This feature requires competitive data files.")
    
    # ==================== TAB 14: DAMAGE CALCULATOR ====================
    with tab14:
        try:
            from damage_calculator import DamageCalculator
            
            calculator = DamageCalculator(data_dir="data")
            calculator.render_calculator()
        except Exception as e:
            st.error(f"Error loading Damage Calculator: {e}")
            st.info("This feature requires moveset database.")
    
    # ==================== TAB 15: TEAM RECOMMENDER ====================
    with tab15:
        try:
            from team_recommender import TeamRecommender
            
            recommender = TeamRecommender(data_dir="data")
            recommender.render_recommender()
        except Exception as e:
            st.error(f"Error loading Team Recommender: {e}")
            st.info("This feature requires competitive data and moveset database.")
    
    # ==================== TAB 16: SPRITE COMPARISON ====================
    with tab16:
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "features"))
            from sprite_comparison import SpriteComparison
            
            comparison = SpriteComparison(data_dir="data")
            comparison.render_comparison_tool()
        except Exception as e:
            st.error(f"Error loading Sprite Comparison: {e}")
            st.info("This feature compares Pokemon sprites and stats side-by-side.")
    
    # ==================== TAB 17: ADVANCED EXPORT ====================
    with tab17:
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "features"))
            from advanced_export import AdvancedExporter
            
            st.title("📤 Advanced Export System")
            st.markdown("Export Pokemon data in multiple formats with customization options")
            
            exporter = AdvancedExporter()
            
            # Single dataset export
            st.markdown("---")
            st.markdown("### 📊 Export Current Dataset")
            exporter.render_export_interface(df, "pokemon_data")
            
            # Batch export option
            st.markdown("---")
            if st.checkbox("🔧 Enable Batch Export", help="Export multiple datasets at once"):
                # Prepare datasets for batch export
                batch_data = {
                    'pokemon_full': df,
                    'pokemon_base': df[df['is_default'] == True] if 'is_default' in df.columns else df,
                    'pokemon_stats': df[['name', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']],
                }
                
                exporter.render_batch_export_interface(batch_data)
                
        except Exception as e:
            st.error(f"Error loading Advanced Export: {e}")
            st.info("This feature provides advanced export capabilities.")
    
    # ==================== TAB 18: ADMIN UTILITIES ====================
    with tab18:
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "features"))
            from admin_utilities import render_admin_dashboard
            
            render_admin_dashboard()
        except Exception as e:
            st.error(f"Error loading Admin Utilities: {e}")
            st.info("This feature provides system management and monitoring tools.")
            if UTILS_AVAILABLE:
                log_error(e, context={'tab': 'admin_utilities'}, severity='ERROR')

# ==================== RUN APP ====================

if __name__ == "__main__":
    main()
