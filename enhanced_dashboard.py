"""
Enhanced Pokémon Dashboard - Comprehensive Statistics & Competitive Analysis
Version 4.0.0 - Enhanced UI/UX with Interactive Features (1,025 Pokémon)
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

# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="National Pokédex Dashboard - Enhanced",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern dynamic styling with enhanced design
st.markdown("""
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
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.8rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(16, 185, 129, 0.4);
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
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_main_dataset():
    """Load the main National Dex CSV - 1,025 Pokemon (Gen 1-9)"""
    csv_path = Path("data/national_dex.csv")
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        # Ensure we have the latest data
        if len(df) < 1025:
            st.warning(f"⚠️ Data may be outdated. Expected 1025 Pokemon, found {len(df)}")
        return df
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

def load_sprite(pokemon_id, sprite_type='official', use_animated=False):
    """
    Load Pokemon sprite image or animation
    
    Args:
        pokemon_id: Pokemon ID number
        sprite_type: 'official', 'icon', or 'animated'
        use_animated: If True, tries to load GIF animation first
    
    Returns:
        tuple: (content, is_gif) - content is either Image or file path
    """
    # Try animated GIF first if requested
    if use_animated or sprite_type == 'animated':
        animated_dir = Path("assets/animated")
        for file in animated_dir.glob(f"{pokemon_id:04d}_*.gif"):
            if file.exists():
                return (str(file), True)
    
    # Determine directory based on type
    if sprite_type == 'icon':
        sprite_dir = Path("assets/icons")
    else:  # official
        sprite_dir = Path("assets/sprites")
    
    # Try to find PNG sprite
    for file in sprite_dir.glob(f"{pokemon_id:04d}_*.png"):
        try:
            return (Image.open(file), False)
        except Exception:
            pass
    
    # Fallback: Try to load from PokeAPI URL directly
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

def get_type_color(type_name):
    """Get color for Pokemon type"""
    colors = {
        'Normal': '#A8A878', 'Fire': '#F08030', 'Water': '#6890F0',
        'Electric': '#F8D030', 'Grass': '#78C850', 'Ice': '#98D8D8',
        'Fighting': '#C03028', 'Poison': '#A040A0', 'Ground': '#E0C068',
        'Flying': '#A890F0', 'Psychic': '#F85888', 'Bug': '#A8B820',
        'Rock': '#B8A038', 'Ghost': '#705898', 'Dragon': '#7038F8',
        'Dark': '#705848', 'Steel': '#B8B8D0', 'Fairy': '#EE99AC'
    }
    return colors.get(type_name, '#777777')

def display_pokemon_card(pokemon, show_sprite=True, use_animated=True):
    """Display a Pokemon card with sprite and info"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if show_sprite:
            pokemon_id = int(pokemon['pokedex_number'])
            sprite_data = load_sprite(pokemon_id, use_animated=use_animated)
            if sprite_data[0] is not None:
                display_sprite(sprite_data, width=150)
            else:
                st.write("🎮 No sprite")
    
    with col2:
        poke_num = int(pokemon['pokedex_number'])
        poke_name = pokemon['name']
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
    
    # Header
    st.markdown('<h1 class="main-header">⚡ National Pokédex Dashboard ⚡</h1>', unsafe_allow_html=True)
    st.markdown("### Version 4.0.0 - Complete Database: All 1,025 Pokémon (Gen 1-9) with Enhanced UI & Interactive Features")
    st.caption("🎮 New: Pokemon Randomizer | Who's That Pokemon Mini-Game | By-Game Filter | Modern UI")
    
    # Load data
    df = load_main_dataset()
    comp_df = load_competitive_data()
    natures = load_natures()
    
    if df is None:
        st.error("❌ Could not load Pokemon data. Please ensure data/national_dex.csv exists.")
        st.info("💡 Try refreshing the page or clearing the cache.")
        return
    
    # Display actual data count
    st.sidebar.info(f"📊 **Loaded {len(df)} Pokémon** | v4.0.0")
    
    # Sidebar - Global Filters
    with st.sidebar:
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
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Overview",
        "🔍 Pokémon Search",
        "⚔️ Competitive Analysis",
        "📈 Statistics & Trends",
        "🎨 Type Analysis",
        "🧬 Evolution & Forms",
        "🎮 By Game",
        "🎨 Sprite Gallery",
        "🏆 Team Builder"
    ])
    
    # ==================== TAB 1: OVERVIEW ====================
    with tab1:
        st.header("📊 Dataset Overview")
        
        # Key statistics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Total Pokémon", len(df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Generations", df['generation'].nunique())
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Types", df['type_1'].nunique())
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            legendary_count = len(df[df['status'] == 'Legendary'])
            st.metric("Legendary", legendary_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col5:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            mythical_count = len(df[df['status'] == 'Mythical'])
            st.metric("Mythical", mythical_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
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
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Pokemon by Generation
            gen_counts = df.groupby('generation').size().reset_index(name='count')
            fig = px.bar(
                gen_counts,
                x='generation',
                y='count',
                title='Pokémon Count by Generation',
                labels={'generation': 'Generation', 'count': 'Number of Pokémon'},
                color='count',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="overview_gen_bar")
        
        with col2:
            # Pokemon by Type
            type_counts = df['type_1'].value_counts().head(10)
            fig = px.bar(
                x=type_counts.index,
                y=type_counts.values,
                title='Top 10 Primary Types',
                labels={'x': 'Type', 'y': 'Count'},
                color=type_counts.values,
                color_continuous_scale='plasma'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="overview_type_bar")
        
        # Base Stat Total Distribution
        st.subheader("Base Stat Total Distribution")
        fig = create_stat_distribution_chart(df, 'total_points')
        st.plotly_chart(fig, use_container_width=True, key="overview_bst_dist")
    
    # ==================== TAB 2: POKEMON SEARCH ====================
    with tab2:
        st.header("🔍 Pokémon Search & Details")
        
        # Search options
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_query = st.text_input(
                "Search by name or Pokédex number",
                placeholder="e.g., Pikachu, 25, Charizard"
            )
        
        with search_col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Pokédex #", "Name", "Total Stats", "HP", "Attack", "Defense"]
            )
        
        # Display filtered Pokemon
        display_df = filtered_df.copy()
        
        if search_query:
            display_df = display_df[
                display_df['name'].str.contains(search_query, case=False, na=False) |
                display_df['pokedex_number'].astype(str).str.contains(search_query, na=False)
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
        display_df = display_df.sort_values(sort_mapping[sort_by])
        
        st.markdown(f"**Showing {len(display_df)} Pokémon**")
        
        # Pagination
        items_per_page = 20
        total_pages = (len(display_df) - 1) // items_per_page + 1
        page = st.number_input("Page", 1, total_pages, 1)
        
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        # Display Pokemon cards
        for idx in range(start_idx, min(end_idx, len(display_df))):
            pokemon = display_df.iloc[idx]
            
            poke_num = int(pokemon['pokedex_number'])
            poke_name = pokemon['name']
            with st.expander(f"#{poke_num:04d} - {poke_name}", expanded=False):
                display_pokemon_card(pokemon, use_animated=use_animations)
                
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
            pokemon_comp = comp_df[comp_df['name'] == selected_pokemon_name].iloc[0]
            
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                pokemon_id = int(pokemon_base['pokedex_number'])
                sprite_data = load_sprite(pokemon_id, use_animated=use_animations)
                display_sprite(sprite_data, width=200)
                st.markdown(f"### {pokemon_base['name']}")
                st.markdown(f"**Tier:** {pokemon_comp['competitive_tier']}")
                st.markdown(f"**Role:** {pokemon_comp['optimal_role']}")
                st.markdown(f"**Nature:** {pokemon_comp['optimal_nature']}")
            
            with col2:
                st.subheader("Optimal EV Spread")
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
            
            with col3:
                st.subheader("Stats at Level 100")
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
        display_df = filtered_df.head(gallery_limit)
        
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
                            sprite_data = load_sprite(
                                pokemon_id,
                                use_animated=use_animations
                            )
                            display_sprite(sprite_data, use_container_width=True)
                            
                            if show_names:
                                st.markdown(
                                    f"<div style='text-align: center; font-size: 0.75rem;'>"
                                    f"#{int(pokemon['pokedex_number']):04d}<br>"
                                    f"<b>{pokemon['name']}</b>"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )
    
    # ==================== TAB 9: TEAM BUILDER ====================
    with tab9:
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

# ==================== RUN APP ====================

if __name__ == "__main__":
    main()
