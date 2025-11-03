"""
Pokemon Favorites Manager
Allows users to save and manage their favorite Pokemon
Version 1.0.0
"""

import streamlit as st
import pandas as pd
from pathlib import Path


def initialize_favorites():
    """Initialize favorites in session state if not exists"""
    if 'favorites' not in st.session_state:
        st.session_state.favorites = set()


def add_to_favorites(pokemon_id: int, pokemon_name: str):
    """Add a Pokemon to favorites"""
    initialize_favorites()
    st.session_state.favorites.add((pokemon_id, pokemon_name))
    st.success(f"✅ Added {pokemon_name} to favorites!")
    st.rerun()


def remove_from_favorites(pokemon_id: int, pokemon_name: str):
    """Remove a Pokemon from favorites"""
    initialize_favorites()
    st.session_state.favorites.discard((pokemon_id, pokemon_name))
    st.info(f"➖ Removed {pokemon_name} from favorites")
    st.rerun()


def is_favorite(pokemon_id: int, pokemon_name: str) -> bool:
    """Check if a Pokemon is in favorites"""
    initialize_favorites()
    return (pokemon_id, pokemon_name) in st.session_state.favorites


def get_favorites_count() -> int:
    """Get total count of favorites"""
    initialize_favorites()
    return len(st.session_state.favorites)


def clear_all_favorites():
    """Clear all favorites"""
    initialize_favorites()
    count = len(st.session_state.favorites)
    st.session_state.favorites.clear()
    st.success(f"🗑️ Cleared {count} favorites")
    st.rerun()


def export_favorites() -> str:
    """Export favorites list as formatted string"""
    initialize_favorites()
    if not st.session_state.favorites:
        return "No favorites to export"
    
    favorites_list = sorted(st.session_state.favorites, key=lambda x: x[0])
    export_text = "MY FAVORITE POKEMON\n"
    export_text += "=" * 40 + "\n\n"
    
    for idx, (pid, pname) in enumerate(favorites_list, 1):
        export_text += f"{idx}. #{pid:04d} - {pname}\n"
    
    export_text += f"\nTotal: {len(favorites_list)} Pokemon"
    return export_text


def render_favorite_button(pokemon_id: int, pokemon_name: str, use_icon_only: bool = False):
    """
    Render a favorite toggle button for a Pokemon
    
    Args:
        pokemon_id: Pokemon ID
        pokemon_name: Pokemon name
        use_icon_only: If True, show only heart icon. If False, show with text
    """
    initialize_favorites()
    is_fav = is_favorite(pokemon_id, pokemon_name)
    
    if use_icon_only:
        if is_fav:
            if st.button("❤️", key=f"fav_{pokemon_id}_{pokemon_name}", help="Remove from favorites"):
                remove_from_favorites(pokemon_id, pokemon_name)
        else:
            if st.button("🤍", key=f"fav_{pokemon_id}_{pokemon_name}", help="Add to favorites"):
                add_to_favorites(pokemon_id, pokemon_name)
    else:
        if is_fav:
            if st.button(f"❤️ Remove from Favorites", key=f"fav_{pokemon_id}_{pokemon_name}", 
                        type="secondary", use_container_width=True):
                remove_from_favorites(pokemon_id, pokemon_name)
        else:
            if st.button(f"🤍 Add to Favorites", key=f"fav_{pokemon_id}_{pokemon_name}",
                        type="secondary", use_container_width=True):
                add_to_favorites(pokemon_id, pokemon_name)


def display_favorites_tab(df: pd.DataFrame):
    """
    Display the favorites management tab
    
    Args:
        df: Main Pokemon DataFrame
    """
    initialize_favorites()
    
    st.markdown("### ❤️ My Favorite Pokemon")
    st.caption("Save your favorite Pokemon for quick access")
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Favorites", get_favorites_count())
    with col2:
        if st.session_state.favorites:
            avg_id = sum(pid for pid, _ in st.session_state.favorites) / len(st.session_state.favorites)
            st.metric("Average Dex #", f"{avg_id:.0f}")
        else:
            st.metric("Average Dex #", "—")
    with col3:
        if st.button("🗑️ Clear All", help="Remove all favorites", use_container_width=True):
            if st.session_state.favorites:
                clear_all_favorites()
    
    st.markdown("---")
    
    # Display favorites
    if not st.session_state.favorites:
        st.info("👆 No favorites yet! Add Pokemon to your favorites from any tab using the ❤️ button.")
        st.markdown("#### 💡 Tips:")
        st.markdown("""
        - Browse Pokemon in the Explorer tab and click the heart to add favorites
        - Use favorites to build your dream team
        - Export your list to share with friends
        - Favorites are saved for your current session
        """)
    else:
        # Export button
        if st.button("📥 Export Favorites List", use_container_width=True):
            export_text = export_favorites()
            st.download_button(
                label="💾 Download as Text File",
                data=export_text,
                file_name="my_favorite_pokemon.txt",
                mime="text/plain"
            )
        
        st.markdown("---")
        
        # Filter by favorites
        favorites_list = sorted(st.session_state.favorites, key=lambda x: x[0])
        favorite_ids = [pid for pid, _ in favorites_list]
        favorite_df = df[df['pokedex_number'].isin(favorite_ids)].copy()
        
        # Sort options
        sort_col1, sort_col2 = st.columns([3, 1])
        with sort_col1:
            sort_by = st.selectbox(
                "Sort by",
                ["Pokedex Number", "Name", "Total Stats", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],
                key="favorites_sort"
            )
        with sort_col2:
            sort_order = st.radio("Order", ["Ascending", "Descending"], horizontal=True, key="favorites_order")
        
        # Apply sorting
        sort_mapping = {
            "Pokedex Number": "pokedex_number",
            "Name": "name",
            "Total Stats": "total",
            "HP": "hp",
            "Attack": "attack",
            "Defense": "defense",
            "Sp. Atk": "sp_attack",
            "Sp. Def": "sp_defense",
            "Speed": "speed"
        }
        
        if sort_by in sort_mapping:
            sort_column = sort_mapping[sort_by]
            if sort_column in favorite_df.columns:
                favorite_df = favorite_df.sort_values(
                    by=sort_column,
                    ascending=(sort_order == "Ascending")
                )
        
        st.markdown(f"### 📋 {len(favorite_df)} Favorite Pokemon")
        
        # Display in grid
        cols_per_row = 3
        for idx in range(0, len(favorite_df), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx, col in enumerate(cols):
                if idx + col_idx < len(favorite_df):
                    row = favorite_df.iloc[idx + col_idx]
                    with col:
                        display_favorite_card(row)


def display_favorite_card(pokemon: pd.Series):
    """
    Display a Pokemon card in favorites view
    
    Args:
        pokemon: Pokemon data as pandas Series
    """
    with st.container():
        st.markdown(f"""
        <div style="
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 15px;
            background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        ">
        """, unsafe_allow_html=True)
        
        # Header with remove button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### #{pokemon['pokedex_number']:04d} {pokemon['name']}")
        with col2:
            render_favorite_button(
                int(pokemon['pokedex_number']),
                pokemon['name'],
                use_icon_only=True
            )
        
        # Types
        types = [pokemon['type1']]
        if pd.notna(pokemon.get('type2')):
            types.append(pokemon['type2'])
        
        type_badges = " ".join([f"**`{t.upper()}`**" for t in types])
        st.markdown(type_badges)
        
        # Stats summary
        if 'total' in pokemon.index:
            st.markdown(f"**Total Stats:** {pokemon['total']}")
        
        # Stat bars (mini version)
        stat_names = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        for stat in stat_names:
            if stat in pokemon.index:
                stat_value = pokemon[stat]
                stat_label = stat.replace('_', ' ').title()
                # Simple text representation
                st.caption(f"{stat_label}: {stat_value}")
        
        st.markdown("</div>", unsafe_allow_html=True)


def get_favorites_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter DataFrame to show only favorites
    
    Args:
        df: Pokemon DataFrame
        
    Returns:
        Filtered DataFrame with only favorites
    """
    initialize_favorites()
    if not st.session_state.favorites:
        return df.head(0)  # Return empty DataFrame
    
    favorite_ids = [pid for pid, _ in st.session_state.favorites]
    return df[df['pokedex_number'].isin(favorite_ids)]


def render_favorites_sidebar():
    """Render favorites summary in sidebar"""
    initialize_favorites()
    
    count = get_favorites_count()
    if count > 0:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ❤️ Favorites")
        st.sidebar.metric("Saved Pokemon", count)
        
        if count >= 6:
            st.sidebar.success("✅ Team ready!")
        elif count > 0:
            st.sidebar.info(f"📝 {6 - count} more for a team")
