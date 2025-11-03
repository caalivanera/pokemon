import streamlit as st
import pandas as pd
import os
from pathlib import Path
import sys
import requests
from urllib.parse import quote

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from src.data_loaders.data_extractor import (
    fetch_all_pokemon,
    load_pokemon_glossary
)
from src.data_loaders.yaml_loader import PokemonDataLoader

# --- Configuration ---
st.set_page_config(
    page_title="National Pokédex - Premium Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Constants ---
DATA_DIR = Path(parent_dir) / 'data'
NATIONAL_DEX_FILE = DATA_DIR / 'national_dex.csv'
LEGACY_DATA_FILE = 'pokemon_enhanced_data.csv'
POKEMON_LIMIT = 151

# Generation/Region mappings
GENERATION_RANGES = {
    "Generation I (Kanto)": (1, 151),
    "Generation II (Johto)": (152, 251),
    "Generation III (Hoenn)": (252, 386),
    "Generation IV (Sinnoh)": (387, 493),
    "Generation V (Unova)": (494, 649),
    "Generation VI (Kalos)": (650, 721),
    "Generation VII (Alola)": (722, 809),
    "Generation VIII (Galar)": (810, 905),
    "Generation IX (Paldea)": (906, 1025)
}

# Type colors for badges
TYPE_COLORS = {
    'normal': '#A8A878', 'fire': '#F08030', 'water': '#6890F0',
    'electric': '#F8D030', 'grass': '#78C850', 'ice': '#98D8D8',
    'fighting': '#C03028', 'poison': '#A040A0', 'ground': '#E0C068',
    'flying': '#A890F0', 'psychic': '#F85888', 'bug': '#A8B820',
    'rock': '#B8A038', 'ghost': '#705898', 'dragon': '#7038F8',
    'dark': '#705848', 'steel': '#B8B8D0', 'fairy': '#EE99AC'
}

# --- Helper Functions ---
def get_pokemon_sprite_url(pokemon_id: int, name: str = "", 
                          high_quality: bool = True) -> str:
    """Generate high-quality Pokemon sprite URL from PokeAPI"""
    clean_name = name.lower().replace(" ", "-").replace("'", "")
    
    # Handle regional forms
    if "alolan" in clean_name:
        form_name = clean_name.replace("alolan-", "") + "-alola"
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{form_name}.png"
    elif "galarian" in clean_name:
        form_name = clean_name.replace("galarian-", "") + "-galar"
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{form_name}.png"
    elif "hisuian" in clean_name:
        form_name = clean_name.replace("hisuian-", "") + "-hisui"
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{form_name}.png"
    elif "paldean" in clean_name:
        form_name = clean_name.replace("paldean-", "") + "-paldea"
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{form_name}.png"
    elif "mega" in clean_name:
        base_name = clean_name.replace("mega-", "").replace("-x", "").replace("-y", "")
        if "-x" in clean_name:
            form_name = f"{base_name}-mega-x"
        elif "-y" in clean_name:
            form_name = f"{base_name}-mega-y"
        else:
            form_name = f"{base_name}-mega"
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{form_name}.png"
    
    # Use high-quality official artwork or HOME sprites
    if high_quality:
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    else:
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"


def inject_premium_css():
    """Inject Netflix/Nintendo-quality dark theme CSS"""
    st.markdown("""
    <style>
        /* Dark Theme with Green Accent */
        :root {
            --netflix-black: #141414;
            --netflix-dark: #1F1F1F;
            --netflix-red: #10B981;
            --pokemon-green: #10B981;
            --netflix-white: #FFFFFF;
            --text-primary: #E5E5E5;
            --text-secondary: #B3B3B3;
            --hover-bg: #2F2F2F;
        }
        
        /* Main app dark background */
        .stApp {
            background-color: var(--netflix-black);
            color: var(--text-primary);
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Sticky animated header */
        .sticky-header {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: linear-gradient(180deg, #141414 0%, rgba(20,20,20,0.95) 100%);
            backdrop-filter: blur(10px);
            padding: 20px 0;
            border-bottom: 2px solid var(--netflix-red);
            animation: slideDown 0.3s ease-out;
        }
        
        @keyframes slideDown {
            from {
                transform: translateY(-100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        /* Floating animation for sprites */
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-15px);
            }
        }
        
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0) scale(1);
            }
            25% {
                transform: translateY(-10px) scale(1.02);
            }
            75% {
                transform: translateY(-5px) scale(0.98);
            }
        }
        
        /* Pokemon card styling - Netflix style */
        .pokemon-card {
            background: var(--netflix-dark);
            border-radius: 12px;
            padding: 15px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }
        
        .pokemon-card:hover {
            transform: scale(1.05) translateY(-5px);
            border-color: var(--pokemon-green);
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
            z-index: 10;
        }
        
        .pokemon-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.1), transparent);
            transition: left 0.4s;
        }
        
        .pokemon-card:hover::before {
            left: 100%;
        }
        
        /* Sprite animations */
        .pokemon-sprite {
            width: 100%;
            height: 200px;
            object-fit: contain;
            filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.5));
            transition: transform 0.2s ease;
            animation: float 3s ease-in-out infinite;
        }
        
        .pokemon-card:hover .pokemon-sprite {
            animation: bounce 0.6s ease-in-out;
            transform: scale(1.1) rotateY(15deg);
        }
        
        /* TBA placeholder styling */
        .tba-placeholder {
            width: 100%;
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #1F1F1F 0%, #2F2F2F 100%);
            border-radius: 12px;
            border: 2px dashed var(--pokemon-green);
            color: var(--pokemon-green);
            font-size: 48px;
            font-weight: bold;
            letter-spacing: 8px;
            text-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
        }
        
        /* Type badges */
        .type-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            margin: 2px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.5px;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: var(--netflix-dark);
            padding: 8px;
            border-radius: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: transparent;
            border-radius: 8px;
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0 24px;
            transition: all 0.15s;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: var(--hover-bg);
            color: var(--text-primary);
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--netflix-red) !important;
            color: white !important;
        }
        
        /* Buttons */
        .stButton>button {
            background: var(--netflix-red);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 12px 24px;
            font-weight: bold;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stButton>button:hover {
            background: #059669;
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(16, 185, 129, 0.4);
        }
        
        /* Select boxes and inputs */
        .stSelectbox, .stMultiSelect, .stTextInput {
            color: var(--text-primary);
        }
        
        .stSelectbox>div>div, .stMultiSelect>div>div {
            background-color: var(--netflix-dark);
            border-color: #444;
            color: var(--text-primary);
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            color: var(--netflix-red);
            font-size: 28px;
            font-weight: bold;
        }
        
        [data-testid="stMetricLabel"] {
            color: var(--text-secondary);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Dataframes */
        .stDataFrame {
            background-color: var(--netflix-dark);
        }
        
        /* Sliders */
        .stSlider>div>div>div {
            background-color: var(--netflix-red);
        }
        
        /* Loading animation */
        .stSpinner>div {
            border-top-color: var(--netflix-red) !important;
        }
        
        /* Headings */
        h1, h2, h3 {
            color: var(--text-primary);
            font-weight: 700;
        }
        
        /* Grid layout for gallery */
        .pokemon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px 0;
        }
        
        /* Search bar */
        .search-container {
            position: relative;
            margin: 20px 0;
        }
        
        .search-container input {
            width: 100%;
            padding: 15px 50px 15px 20px;
            background: var(--netflix-dark);
            border: 2px solid #444;
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 16px;
            transition: all 0.2s;
        }
        
        .search-container input:focus {
            border-color: var(--pokemon-green);
            outline: none;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--netflix-black);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--pokemon-green);
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #059669;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .pokemon-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }
        }
    </style>
    """, unsafe_allow_html=True)


def get_generation_for_pokemon(pokedex_num: int) -> str:
    """Get generation name for a Pokemon based on Pokedex number"""
    for gen_name, (start, end) in GENERATION_RANGES.items():
        if start <= pokedex_num <= end:
            return gen_name
    return "Unknown"


def create_type_badge(type_name: str) -> str:
    """Create HTML for type badge with proper color"""
    color = TYPE_COLORS.get(type_name.lower(), '#777')
    return f'<span class="type-badge" style="background-color: {color}; color: white;">{type_name}</span>'


def create_pokemon_card_html(pokemon_data: pd.Series, sprite_url: str) -> str:
    """Create Netflix-style Pokemon card HTML with TBA placeholder for missing sprites"""
    type_badges = create_type_badge(pokemon_data['primary_type'])
    if pd.notna(pokemon_data.get('secondary_type')) and str(pokemon_data.get('secondary_type')) != 'nan':
        type_badges += ' ' + create_type_badge(pokemon_data['secondary_type'])
    
    # Check if sprite URL is valid or use TBA placeholder
    sprite_html = f"""
        <img src="{sprite_url}" 
             class="pokemon-sprite" 
             alt="{pokemon_data['name']}"
             onerror="this.onerror=null; this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div class="tba-placeholder" style="display: none;">TBA</div>
    """
    
    return f"""
    <div class="pokemon-card">
        {sprite_html}
        <h3 style="text-align: center; margin: 10px 0; color: var(--text-primary);">
            #{int(pokemon_data['pokedex_number'])} {pokemon_data['name']}
        </h3>
        <div style="text-align: center;">
            {type_badges}
        </div>
        <div style="margin-top: 10px; text-align: center; color: var(--text-secondary); font-size: 14px;">
            BST: {int(pokemon_data['total_points'])}
        </div>
    </div>
    """


# --- Data Loading ---
@st.cache_data(ttl=60*60*24)
def load_national_dex() -> pd.DataFrame:
    """Load comprehensive National Pokedex dataset"""
    if NATIONAL_DEX_FILE.exists():
        df = pd.read_csv(NATIONAL_DEX_FILE)
        
        # Add column aliases
        if 'type_1' in df.columns:
            df['primary_type'] = df['type_1']
        if 'type_2' in df.columns:
            df['secondary_type'] = df['type_2']
        if 'pokedex_number' in df.columns:
            df['id'] = df['pokedex_number']
        
        # Sort by Pokedex number by default
        df = df.sort_values('pokedex_number').reset_index(drop=True)
        
        # Add generation column
        df['generation'] = df['pokedex_number'].apply(get_generation_for_pokemon)
        
        # Add high-quality sprite URLs
        df['sprite_url_hq'] = df.apply(
            lambda row: get_pokemon_sprite_url(
                int(row['pokedex_number']),
                str(row['name']),
                high_quality=True
            ),
            axis=1
        )
        
        return df
    else:
        st.error("National Dex not found!")
        return pd.DataFrame()


@st.cache_data
def load_glossary() -> dict:
    """Load Pokemon glossary"""
    return load_pokemon_glossary()


@st.cache_data
def load_yaml_data() -> dict:
    """Load YAML data"""
    try:
        yaml_loader = PokemonDataLoader()
        return yaml_loader.load_all_yaml_data()
    except Exception:
        return {}


# Inject premium CSS
inject_premium_css()

# Load data
with st.spinner("Loading Pokemon data..."):
    df = load_national_dex()
    glossary = load_glossary()
    yaml_data = load_yaml_data()

if df is None or df.empty:
    st.error("Failed to load Pokemon data.")
    st.stop()

# --- Sticky Header ---
st.markdown("""
<div class="sticky-header">
    <div style="max-width: 1400px; margin: 0 auto; padding: 0 20px;">
        <h1 style="margin: 0; font-size: 42px; font-weight: 900; text-align: center;">
            <span style="color: var(--netflix-red);">⚡</span> 
            NATIONAL POKÉDEX
            <span style="color: var(--netflix-red);">⚡</span>
        </h1>
        <p style="text-align: center; color: var(--text-secondary); margin: 8px 0 0 0; font-size: 16px;">
            Explore all {len(df)} Pokemon • Premium Edition
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Main Tabbed Interface ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Gallery", 
    "🔍 Search & Filter", 
    "📊 Statistics", 
    "📚 Glossary",
    "⚙️ Settings"
])

# ===== TAB 1: GALLERY VIEW =====
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick filters
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        selected_gen = st.selectbox(
            "Filter by Generation",
            ["All Generations"] + list(GENERATION_RANGES.keys()),
            key="gallery_gen"
        )
    
    with col_filter2:
        all_types = sorted(pd.concat([df['primary_type'], df['secondary_type']]).dropna().unique())
        selected_type_filter = st.selectbox(
            "Filter by Type",
            ["All Types"] + all_types,
            key="gallery_type"
        )
    
    with col_filter3:
        search_query = st.text_input("🔍 Search Pokemon", placeholder="Enter name or number...", key="gallery_search")
    
    # Apply filters
    df_gallery = df.copy()
    
    if selected_gen != "All Generations":
        df_gallery = df_gallery[df_gallery['generation'] == selected_gen]
    
    if selected_type_filter != "All Types":
        df_gallery = df_gallery[
            (df_gallery['primary_type'] == selected_type_filter) |
            (df_gallery['secondary_type'] == selected_type_filter)
        ]
    
    if search_query:
        df_gallery = df_gallery[
            df_gallery['name'].str.contains(search_query, case=False, na=False) |
            df_gallery['pokedex_number'].astype(str).str.contains(search_query, na=False)
        ]
    
    st.markdown(f"<h3 style='color: var(--text-primary);'>Showing {len(df_gallery)} Pokemon</h3>", unsafe_allow_html=True)
    
    # Display Pokemon grid
    cols_per_row = 5
    rows = [df_gallery.iloc[i:i+cols_per_row] for i in range(0, len(df_gallery), cols_per_row)]
    
    for row_idx, row in enumerate(rows):
        cols = st.columns(cols_per_row)
        for col_idx, (pokemon_idx, pokemon) in enumerate(row.iterrows()):
            with cols[col_idx]:
                sprite_url = pokemon.get('sprite_url_hq', get_pokemon_sprite_url(
                    int(pokemon['pokedex_number']),
                    str(pokemon['name']),
                    high_quality=True
                ))
                st.markdown(create_pokemon_card_html(pokemon, sprite_url), unsafe_allow_html=True)
                if st.button(f"View Details", key=f"btn_gallery_{row_idx}_{col_idx}_{pokemon_idx}", use_container_width=True):
                    st.session_state['selected_pokemon'] = pokemon['name']
                    st.rerun()

# ===== TAB 2: SEARCH & FILTER =====
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Advanced search
    search_col1, search_col2 = st.columns([2, 1])
    
    with search_col1:
        search_name = st.text_input("🔍 Search by Name", placeholder="Enter Pokemon name...")
    
    with search_col2:
        search_id = st.number_input("🔢 Search by ID", min_value=1, max_value=len(df), value=1)
    
    # Filters
    st.markdown("### 🎯 Advanced Filters")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        gen_filter = st.multiselect(
            "Generation",
            list(GENERATION_RANGES.keys()),
            key="search_gen"
        )
    
    with filter_col2:
        type_filter = st.multiselect(
            "Type",
            sorted(pd.concat([df['primary_type'], df['secondary_type']]).dropna().unique()),
            key="search_type"
        )
    
    with filter_col3:
        bst_range = st.slider(
            "Base Stat Total",
            int(df['total_points'].min()),
            int(df['total_points'].max()),
            (int(df['total_points'].min()), int(df['total_points'].max()))
        )
    
    # Apply filters
    df_filtered = df.copy()
    
    if search_name:
        df_filtered = df_filtered[df_filtered['name'].str.contains(search_name, case=False, na=False)]
    
    if gen_filter:
        df_filtered = df_filtered[df_filtered['generation'].isin(gen_filter)]
    
    if type_filter:
        df_filtered = df_filtered[
            df_filtered['primary_type'].isin(type_filter) |
            df_filtered['secondary_type'].isin(type_filter)
        ]
    
    df_filtered = df_filtered[
        df_filtered['total_points'].between(bst_range[0], bst_range[1])
    ]
    
    st.markdown(f"### Found {len(df_filtered)} Pokemon")
    
    # Display results
    if len(df_filtered) > 0:
        selected_pokemon_name = st.selectbox(
            "Select a Pokemon to view details:",
            df_filtered['name'].tolist()
        )
        
        if selected_pokemon_name:
            pokemon_data = df_filtered[df_filtered['name'] == selected_pokemon_name].iloc[0]
            
            # Pokemon detail view
            detail_col1, detail_col2, detail_col3 = st.columns([1, 2, 1])
            
            with detail_col1:
                sprite_url = pokemon_data.get('sprite_url_hq', get_pokemon_sprite_url(
                    int(pokemon_data['pokedex_number']),
                    str(pokemon_data['name']),
                    high_quality=True
                ))
                st.image(sprite_url, use_column_width=True)
                
                type_badges = create_type_badge(pokemon_data['primary_type'])
                if pd.notna(pokemon_data.get('secondary_type')):
                    type_badges += ' ' + create_type_badge(pokemon_data['secondary_type'])
                st.markdown(type_badges, unsafe_allow_html=True)
            
            with detail_col2:
                st.markdown(f"## #{int(pokemon_data['pokedex_number'])} {pokemon_data['name']}")
                st.markdown(f"**Species:** {pokemon_data['species']}")
                st.markdown(f"**Generation:** {pokemon_data['generation']}")
                st.markdown(f"**Height:** {pokemon_data['height_m']} m | **Weight:** {pokemon_data['weight_kg']} kg")
                
                # Abilities
                st.markdown("**Abilities:**")
                for i in range(1, 4):
                    ability_col = f'ability_{i}' if i < 3 else 'ability_hidden'
                    if ability_col in pokemon_data.index:
                        ability = pokemon_data.get(ability_col)
                        if pd.notna(ability) and str(ability) != 'nan':
                            hidden_label = " (Hidden)" if ability_col == 'ability_hidden' else ""
                            st.markdown(f"• {ability}{hidden_label}")
            
            with detail_col3:
                st.metric("Total BST", int(pokemon_data['total_points']))
                st.metric("Catch Rate", f"{float(pokemon_data['catch_rate']):.0f}%")
                st.metric("Base EXP", f"{float(pokemon_data['base_experience']):.0f}")
            
            # Base stats
            st.markdown("### 📊 Base Stats")
            stats_data = {
                'HP': pokemon_data['hp'],
                'Attack': pokemon_data['attack'],
                'Defense': pokemon_data['defense'],
                'Sp. Atk': pokemon_data['sp_attack'],
                'Sp. Def': pokemon_data['sp_defense'],
                'Speed': pokemon_data['speed']
            }
            
            stats_col1, stats_col2 = st.columns(2)
            
            with stats_col1:
                for stat_name, stat_value in list(stats_data.items())[:3]:
                    st.metric(stat_name, int(stat_value))
            
            with stats_col2:
                for stat_name, stat_value in list(stats_data.items())[3:]:
                    st.metric(stat_name, int(stat_value))

# ===== TAB 3: STATISTICS =====
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 📈 Pokemon Statistics & Analytics")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric("Total Pokemon", len(df))
    
    with stats_col2:
        st.metric("Generations", len(GENERATION_RANGES))
    
    with stats_col3:
        st.metric("Unique Types", len(TYPE_COLORS))
    
    with stats_col4:
        avg_bst = df['total_points'].mean()
        st.metric("Avg BST", f"{avg_bst:.0f}")
    
    # Distribution by generation
    st.markdown("### Pokemon by Generation")
    gen_counts = df['generation'].value_counts().sort_index()
    st.bar_chart(gen_counts)
    
    # Top 10 highest BST
    st.markdown("### 🏆 Top 10 Highest Base Stat Total")
    top_10 = df.nlargest(10, 'total_points')[['pokedex_number', 'name', 'primary_type', 'secondary_type', 'total_points']]
    st.dataframe(top_10, use_container_width=True, hide_index=True)
    
    # Type distribution
    st.markdown("### Pokemon by Primary Type")
    type_counts = df['primary_type'].value_counts()
    st.bar_chart(type_counts)

# ===== TAB 4: GLOSSARY =====
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 📚 Pokemon Glossary")
    st.markdown("Comprehensive dictionary of Pokemon terms and concepts.")
    
    if glossary:
        glossary_search = st.text_input("🔍 Search glossary", placeholder="Enter term...", key="glossary_search_main")
        
        if glossary_search:
            matching_terms = {k: v for k, v in glossary.items()
                            if glossary_search.lower() in k.lower() or glossary_search.lower() in v.lower()}
            
            if matching_terms:
                for term, definition in matching_terms.items():
                    with st.expander(f"**{term}**"):
                        st.write(definition)
            else:
                st.warning("No matching terms found.")
        else:
            # Display all terms
            st.markdown(f"**{len(glossary)} terms available**")
            for term, definition in sorted(glossary.items())[:20]:  # Show first 20
                with st.expander(f"**{term}**"):
                    st.write(definition)
            
            if len(glossary) > 20:
                st.info(f"Showing 20 of {len(glossary)} terms. Use search to find specific terms.")
    else:
        st.warning("Glossary data not available.")

# ===== TAB 5: SETTINGS =====
with tab5:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## ⚙️ Application Settings")
    
    st.markdown("### Display Options")
    display_mode = st.radio("Gallery View Mode", ["Grid", "List"], horizontal=True)
    
    st.markdown("### Data Management")
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.success("Cache cleared! Reloading data...")
        st.rerun()
    
    if st.button("💾 Export All Data"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"national_dex_complete_{len(df)}_pokemon.csv",
            mime="text/csv"
        )
    
    st.markdown("### About")
    st.info("""
    **National Pokédex - Premium Edition**
    
    Version: 2.0
    - 🎨 Netflix-inspired dark theme
    - 📊 1,076 Pokemon with comprehensive data
    - 🖼️ High-quality official artwork
    - 🔍 Advanced search and filtering
    - 📈 Statistics and analytics
    
    Built with Streamlit • Data from PokeAPI
    """)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 40px 20px; border-top: 2px solid var(--netflix-dark);">
    <p style="color: var(--text-secondary); margin: 0;">
        © 2025 National Pokédex Premium Edition • 
        Built with ❤️ by Charles Alivanera • 
        Data from <a href="https://pokeapi.co" style="color: var(--netflix-red);">PokeAPI</a>
    </p>
</div>
""", unsafe_allow_html=True)
