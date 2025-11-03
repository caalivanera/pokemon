import streamlit as st
import pandas as pd
import os
import re
import json
from pathlib import Path
import sys

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
    page_title="Enhanced Pokédex Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Constants ---
DATA_DIR = Path(parent_dir) / 'data'
NATIONAL_DEX_FILE = DATA_DIR / 'national_dex.csv'
LEGACY_DATA_FILE = 'pokemon_enhanced_data.csv'
POKEMON_LIMIT = 151  # Generation 1 (for legacy mode)

# --- Data Loading ---
@st.cache_data(ttl=60*60*24)  # Cache data for 24 hours
def load_national_dex() -> pd.DataFrame:
    """
    Loads the comprehensive National Pokedex dataset.
    This dataset combines all CSV sources with advanced analytics.
    """
    if NATIONAL_DEX_FILE.exists():
        st.success("✅ Loading National Pokedex (1076 Pokemon with all regional & Mega forms)...")
        df = pd.read_csv(NATIONAL_DEX_FILE)
        
        # Add column aliases for compatibility with app code
        if 'type_1' in df.columns:
            df['primary_type'] = df['type_1']
        if 'type_2' in df.columns:
            df['secondary_type'] = df['type_2']
        if 'pokedex_number' in df.columns:
            df['id'] = df['pokedex_number']
        
        # Count variants for display
        hisuian = len(df[df['name'].str.contains('Hisuian', na=False)])
        paldean = len(df[df['name'].str.contains('Paldean', na=False)])
        alolan = len(df[df['name'].str.contains('Alolan', na=False)])
        galarian = len(df[df['name'].str.contains('Galarian', na=False)])
        mega = len(df[df['name'].str.contains('Mega', na=False)])
        
        st.info(f"📊 Loaded {len(df)} Pokemon | Variants: {hisuian} Hisuian, {paldean} Paldean, {alolan} Alolan, {galarian} Galarian, {mega} Mega")
        return df
    else:
        st.error("❌ National Dex not found! Attempting fallback to legacy mode...")
        return load_legacy_data()

@st.cache_data(ttl=60*60*24)
def load_legacy_data() -> pd.DataFrame:
    """
    Legacy data loading function (Gen 1 only).
    Used as fallback if National Dex is not available.
    """
    file_path = LEGACY_DATA_FILE
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            if len(df) >= POKEMON_LIMIT:
                st.success("✅ Loaded cached Gen 1 Pokemon data!")
                return df
        except (pd.errors.EmptyDataError, KeyError):
            st.warning("⚠️ Cached data corrupted. Regenerating...")
    
    # Load enhanced data from multiple CSV sources
    with st.spinner(f"� Loading Gen 1 data for {POKEMON_LIMIT} Pokémon..."):
        try:
            df = fetch_all_pokemon(limit=POKEMON_LIMIT)
            if df is not None and not df.empty:
                df.to_csv(file_path, index=False)
                st.success("✅ Gen 1 Pokemon data loaded!")
                return df
            else:
                st.error("❌ Failed to load Pokemon data!")
                return pd.DataFrame()
        except Exception as e:
            st.error(f"❌ Error loading Pokemon data: {str(e)}")
            return pd.DataFrame()

@st.cache_data
def load_glossary() -> dict:
    """Load and cache the Pokemon glossary."""
    return load_pokemon_glossary()

@st.cache_data
def load_yaml_data() -> dict:
    """
    Load and cache YAML data from pokemondbgit folder.
    Includes: pokemon.yaml, moves.yaml, abilities.yaml, types.yaml,
    type-chart.yaml, items.yaml, locations.yaml, egg-groups.yaml,
    games.yaml, releases.yaml, pokemon-forms.yaml
    """
    try:
        yaml_loader = PokemonDataLoader()
        yaml_data = yaml_loader.load_all_yaml_data()
        st.success(f"✅ Loaded {len(yaml_data)} YAML data files!")
        return yaml_data
    except Exception as e:
        st.warning(f"⚠️ YAML data not available: {e}")
        return {}

# Load the data, glossary, and YAML enrichment
df = load_national_dex()
glossary = load_glossary()
yaml_data = load_yaml_data()

# Check if data loaded successfully
if df is None or df.empty:
    st.error("❌ Failed to load Pokemon data. Please check data files.")
    st.stop()

# --- Sidebar ---
logo_url = "https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi_256.png"
st.sidebar.image(logo_url, width=200)
st.sidebar.title("⚡ National Pokédex")

# Pokemon Glossary Section
with st.sidebar.expander("📚 Pokemon Glossary", expanded=False):
    if glossary:
        search_term = st.text_input("Search glossary terms:", key="glossary_search")
        if search_term:
            matching_terms = {k: v for k, v in glossary.items() 
                            if search_term.lower() in k.lower() or search_term.lower() in v.lower()}
            if matching_terms:
                for term, definition in matching_terms.items():
                    st.write(f"**{term}:** {definition[:200]}{'...' if len(definition) > 200 else ''}")
            else:
                st.write("No matching terms found.")
        else:
            st.write("💡 Search for Pokemon terms like 'Attack', 'Type', 'BST', etc.")
    else:
        st.write("Glossary not available")

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")

# Get unique types for the filter (handling different column name possibilities)
try:
    # Try common column name variations
    if 'primary_type' in df.columns and 'secondary_type' in df.columns:
        all_types = pd.concat([df['primary_type'], df['secondary_type']]).dropna().unique()
    elif 'type1' in df.columns and 'type2' in df.columns:
        all_types = pd.concat([df['type1'], df['type2']]).dropna().unique()
    elif 'type_1' in df.columns and 'type_2' in df.columns:
        all_types = pd.concat([df['type_1'], df['type_2']]).dropna().unique()
    elif 'Type 1' in df.columns and 'Type 2' in df.columns:
        all_types = pd.concat([df['Type 1'], df['Type 2']]).dropna().unique()
    else:
        st.warning(f"⚠️ Type columns not found. Available columns: {list(df.columns)}")
        all_types = []
    all_types = sorted(all_types) if len(all_types) > 0 else []
except Exception as e:
    st.error(f"Error getting types: {e}")
    all_types = []

# Type Filter
selected_types = st.sidebar.multiselect(
    "Filter by Type:",
    options=all_types,
    help="Select one or more types. Pokémon matching *any* selected type will be shown."
)

# Generation Filter (for future expansion)
selected_generation = st.sidebar.selectbox(
    "Generation:",
    options=[1],
    index=0,
    help="Currently showing Generation 1 (Kanto) Pokémon"
)

# Advanced Filters
with st.sidebar.expander("⚙️ Advanced Filters", expanded=True):
    # Stat Sliders
    st.write("**Base Stats Range:**")
    
    total_stats_range = st.slider(
        "Total Base Stat (BST):",
        min_value=int(df['total_points'].min()),
        max_value=int(df['total_points'].max()),
        value=(int(df['total_points'].min()), int(df['total_points'].max())),
        help="Filter by total base stat points"
    )
    
    hp_range = st.slider(
        "HP Range:",
        min_value=int(df['hp'].min()),
        max_value=int(df['hp'].max()),
        value=(int(df['hp'].min()), int(df['hp'].max()))
    )

    attack_range = st.slider(
        "Attack Range:",
        min_value=int(df['attack'].min()),
        max_value=int(df['attack'].max()),
        value=(int(df['attack'].min()), int(df['attack'].max()))
    )

    defense_range = st.slider(
        "Defense Range:",
        min_value=int(df['defense'].min()),
        max_value=int(df['defense'].max()),
        value=(int(df['defense'].min()), int(df['defense'].max()))
    )
    
    special_attack_range = st.slider(
        "Special Attack Range:",
        min_value=int(df['sp_attack'].min()),
        max_value=int(df['sp_attack'].max()),
        value=(int(df['sp_attack'].min()), int(df['sp_attack'].max()))
    )
    
    special_defense_range = st.slider(
        "Special Defense Range:",
        min_value=int(df['sp_defense'].min()),
        max_value=int(df['sp_defense'].max()),
        value=(int(df['sp_defense'].min()), int(df['sp_defense'].max()))
    )

    speed_range = st.slider(
        "Speed Range:",
        min_value=int(df['speed'].min()),
        max_value=int(df['speed'].max()),
        value=(int(df['speed'].min()), int(df['speed'].max()))
    )
    
    # Additional filters
    st.write("**Other Filters:**")
    
    height_range = st.slider(
        "Height (m):",
        min_value=float(df['height_m'].min()),
        max_value=float(df['height_m'].max()),
        value=(float(df['height_m'].min()), float(df['height_m'].max())),
        step=0.1
    )
    
    weight_range = st.slider(
        "Weight (kg):",
        min_value=float(df['weight_kg'].min()),
        max_value=float(df['weight_kg'].max()),
        value=(float(df['weight_kg'].min()), float(df['weight_kg'].max())),
        step=0.1
    )

# --- Filtering Logic ---
df_filtered = df.copy()

# Apply Type filter (logical OR)
if selected_types:
    df_filtered = df_filtered[
        (df_filtered['primary_type'].isin(selected_types)) |
        (df_filtered['secondary_type'].isin(selected_types))
    ]

# Apply all stat filters (logical AND)
df_filtered = df_filtered[
    (df_filtered['total_points'].between(total_stats_range[0], total_stats_range[1])) &
    (df_filtered['hp'].between(hp_range[0], hp_range[1])) &
    (df_filtered['attack'].between(attack_range[0], attack_range[1])) &
    (df_filtered['defense'].between(defense_range[0], defense_range[1])) &
    (df_filtered['sp_attack'].between(special_attack_range[0], special_attack_range[1])) &
    (df_filtered['sp_defense'].between(special_defense_range[0], special_defense_range[1])) &
    (df_filtered['speed'].between(speed_range[0], speed_range[1])) &
    (df_filtered['height_m'].between(height_range[0], height_range[1])) &
    (df_filtered['weight_kg'].between(weight_range[0], weight_range[1]))
]

# --- Main Page ---
st.title("⚡ Enhanced Gen 1 Interactive Pokédex")
st.markdown(f"""
### 📊 Dataset Overview
Displaying **{len(df_filtered)}** of **{len(df)}** Generation 1 Pokémon based on your filters.

🗂️ **Data Sources:**
- **Main Pokedex:** Comprehensive stats, abilities, and competitive analysis
- **Pokemon Corpus:** Detailed descriptions and lore  
- **Pokemon Glossary:** {len(glossary)} terms and definitions
- **Alternative Pokedex:** Additional flavor text and information
""")

# Quick Stats
if len(df_filtered) > 0:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average BST", f"{df_filtered['total_points'].mean():.0f}")
    with col2:
        st.metric("Highest Attack", f"{df_filtered['attack'].max()}")
    with col3:
        st.metric("Most Common Type", df_filtered['primary_type'].mode().iloc[0] if not df_filtered['primary_type'].mode().empty else "N/A")
    with col4:
        st.metric("Avg Catch Rate", f"{df_filtered['catch_rate'].mean():.0f}%")

# --- Enhanced Pokémon Detail Viewer ---
st.header("🔍 Enhanced Pokémon Detail Viewer")

# Select a Pokémon from the *filtered* list
pokemon_list = df_filtered['name'].tolist()
if not pokemon_list:
    st.warning("❌ No Pokémon match your current filter criteria. Try adjusting your filters.")
else:
    selected_name = st.selectbox('Select a Pokémon to view its details:', pokemon_list, key="pokemon_selector")
    
    if selected_name:
        # Get all data for the selected Pokémon
        pokemon_data = df_filtered[df_filtered['name'] == selected_name].iloc[0]
        
        # Main Pokemon Info Layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Display Sprite
            st.image(pokemon_data['sprite_url'], caption=f"#{pokemon_data['id']} {pokemon_data['name']}", width=200)
            
            # Quick Stats Card
            st.markdown("### 📊 Quick Stats")
            st.metric("Total BST", pokemon_data['total_points'])
            st.metric("Catch Rate", f"{pokemon_data['catch_rate']:.0f}%")
            st.metric("Base Friendship", f"{pokemon_data['base_friendship']:.0f}")
        
        with col2:
            # Display Enhanced Basic Info
            st.subheader(f"#{pokemon_data['id']} - {pokemon_data['name']}")
            if pokemon_data['japanese_name']:
                st.caption(f"Japanese: {pokemon_data['japanese_name']}")
            
            # Pokemon Classification
            st.markdown(f"**Species:** {pokemon_data['species']}")
            
            # Types with better formatting
            type_1 = pokemon_data['primary_type']
            type_2 = pokemon_data['secondary_type']
            
            type_display = f"**Type:** {type_1.title()}"
            if pd.notna(type_2) and str(type_2) != 'nan':
                type_display += f" / {type_2.title()}"
            st.markdown(type_display)
            
            # Physical Stats
            st.markdown(f"**Height:** {pokemon_data['height_m']} m")
            st.markdown(f"**Weight:** {pokemon_data['weight_kg']} kg")
            st.markdown(f"**Growth Rate:** {pokemon_data['growth_rate']}")
            
            # Abilities Section
            if pokemon_data['abilities']:
                st.markdown("**Abilities:**")
                for i, ability in enumerate(pokemon_data['abilities'][:3]):  # Limit to 3 abilities
                    if ability and str(ability) != 'nan':
                        ability_desc = ""
                        if pokemon_data['ability_descriptions'] and ability in pokemon_data['ability_descriptions']:
                            ability_desc = pokemon_data['ability_descriptions'][ability]
                            if ability_desc and str(ability_desc) != 'nan':
                                ability_desc = f" - {ability_desc[:100]}{'...' if len(str(ability_desc)) > 100 else ''}"
                        
                        st.markdown(f"• **{ability}**{ability_desc}")
        
        with col3:
            # Breeding Info
            st.markdown("### 🥚 Breeding Info")
            st.write(f"**Egg Group 1:** {pokemon_data['egg_type_1']}")
            if pd.notna(pokemon_data['egg_type_2']) and str(pokemon_data['egg_type_2']) != 'nan':
                st.write(f"**Egg Group 2:** {pokemon_data['egg_type_2']}")
            st.write(f"**Male %:** {pokemon_data['percentage_male']:.1f}%")
            
            # Experience Info
            st.markdown("### ⭐ Experience")
            st.write(f"**Base Exp:** {pokemon_data['base_experience']:.0f}")

        # Enhanced Base Stats Visualization
        st.subheader("📈 Base Stats Analysis")
        
        # Create two columns for stats
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            # Prepare data for the bar chart with proper column names
            stats_data = {
                'HP': pokemon_data['hp'],
                'Attack': pokemon_data['attack'],
                'Defense': pokemon_data['defense'],
                'Sp. Attack': pokemon_data['sp_attack'],
                'Sp. Defense': pokemon_data['sp_defense'],
                'Speed': pokemon_data['speed']
            }
            stats_df = pd.DataFrame.from_dict(stats_data, orient='index', columns=['Base Stat'])
            
            st.bar_chart(stats_df, height=300)
        
        with stats_col2:
            # Stats table with rankings
            st.markdown("**Detailed Stats:**")
            for stat_name, stat_value in stats_data.items():
                # Calculate percentile ranking among all Pokemon
                all_stats = df[stat_name.lower().replace(' ', '_').replace('.', '')] if stat_name != 'Sp. Attack' and stat_name != 'Sp. Defense' else df['sp_attack' if 'Attack' in stat_name else 'sp_defense']
                percentile = (all_stats < stat_value).mean() * 100
                
                st.write(f"**{stat_name}:** {stat_value} ({percentile:.0f}th percentile)")
        
        # Enhanced Descriptions Section
        st.subheader("📖 Detailed Information")
        
        # Tabs for different information sources
        desc_tab1, desc_tab2, desc_tab3, desc_tab4 = st.tabs(["🎮 Game Info", "🏆 Competitive", "📚 Bulbapedia", "🔍 Additional"])
        
        with desc_tab1:
            if pokemon_data['additional_info'] and str(pokemon_data['additional_info']) != 'nan':
                st.write("**Game Description:**")
                st.write(pokemon_data['additional_info'])
            else:
                st.write("No game description available.")
        
        with desc_tab2:
            if pokemon_data['smogon_description'] and str(pokemon_data['smogon_description']) != 'nan':
                st.write("**Competitive Analysis (Smogon):**")
                # Truncate long descriptions
                desc = str(pokemon_data['smogon_description'])
                if len(desc) > 1000:
                    st.write(desc[:1000] + "...")
                    with st.expander("Read full analysis"):
                        st.write(desc)
                else:
                    st.write(desc)
            else:
                st.write("No competitive analysis available.")
        
        with desc_tab3:
            if pokemon_data['bulbapedia_description'] and str(pokemon_data['bulbapedia_description']) != 'nan':
                st.write("**Bulbapedia Description:**")
                desc = str(pokemon_data['bulbapedia_description'])
                if len(desc) > 1000:
                    st.write(desc[:1000] + "...")
                    with st.expander("Read full description"):
                        st.write(desc)
                else:
                    st.write(desc)
            else:
                st.write("No Bulbapedia description available.")
        
        with desc_tab4:
            if pokemon_data['corpus_info'] and str(pokemon_data['corpus_info']) != 'nan':
                st.write("**Corpus Information:**")
                # Clean and display corpus info
                corpus_text = str(pokemon_data['corpus_info']).strip()
                # Extract just the main description, not the move lists
                if "Here is the list of moves" in corpus_text:
                    corpus_text = corpus_text.split("Here is the list of moves")[0]
                
                if len(corpus_text) > 1000:
                    st.write(corpus_text[:1000] + "...")
                    with st.expander("Read full information"):
                        st.write(corpus_text)
                else:
                    st.write(corpus_text)
            else:
                st.write("No additional corpus information available.")

# --- Enhanced Data Table ---
st.header("📊 Complete Pokémon Dataset")

# Add data export functionality
col_export1, col_export2 = st.columns([3, 1])
with col_export1:
    st.write(f"Showing **{len(df_filtered)}** Pokemon entries with enhanced data from multiple sources.")
with col_export2:
    if st.button("💾 Download Filtered Data"):
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📁 Download CSV",
            data=csv,
            file_name=f"pokemon_filtered_data_{len(df_filtered)}_entries.csv",
            mime="text/csv"
        )

# Enhanced dataframe display with better column selection
display_columns = [
    'id', 'name', 'species', 'primary_type', 'secondary_type',
    'total_points', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed',
    'height_m', 'weight_kg', 'catch_rate', 'base_experience'
]

# Filter columns that exist in the dataframe
available_columns = [col for col in display_columns if col in df_filtered.columns]

if available_columns:
    display_df = df_filtered[available_columns].set_index('id')
    
    # Enhanced dataframe with styling
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        column_config={
            "name": st.column_config.TextColumn("Pokemon", width="medium"),
            "species": st.column_config.TextColumn("Species", width="medium"),  
            "primary_type": st.column_config.TextColumn("Primary Type", width="small"),
            "secondary_type": st.column_config.TextColumn("Secondary Type", width="small"),
            "total_points": st.column_config.NumberColumn("Total BST", width="small"),
            "hp": st.column_config.NumberColumn("HP", width="small"),
            "attack": st.column_config.NumberColumn("ATK", width="small"),
            "defense": st.column_config.NumberColumn("DEF", width="small"),
            "sp_attack": st.column_config.NumberColumn("SP.ATK", width="small"),
            "sp_defense": st.column_config.NumberColumn("SP.DEF", width="small"),
            "speed": st.column_config.NumberColumn("SPD", width="small"),
            "height_m": st.column_config.NumberColumn("Height (m)", width="small"),
            "weight_kg": st.column_config.NumberColumn("Weight (kg)", width="small"),
            "catch_rate": st.column_config.NumberColumn("Catch Rate %", width="small"),
            "base_experience": st.column_config.NumberColumn("Base EXP", width="small")
        }
    )
else:
    st.error("Unable to display data - column mismatch detected.")

# Footer with data sources attribution
st.markdown("---")
st.markdown("""
### 📋 Data Sources & Credits
This enhanced Pokemon dashboard combines data from multiple high-quality sources:

- **🎯 Main Pokedex Dataset:** Comprehensive Pokemon statistics, abilities, and competitive analysis
- **📖 Pokemon Corpus:** Detailed Pokemon descriptions and lore information  
- **📚 Pokemon Glossary:** Definitions of Pokemon-related terms and concepts
- **🎮 Alternative Pokedex:** Additional flavor text and game descriptions

**🔧 Built with:** Python, Streamlit, Pandas | **⚡ Enhanced by:** Charles Alivanera | **📧 Contact:** caalivanera@gmail.com
""")