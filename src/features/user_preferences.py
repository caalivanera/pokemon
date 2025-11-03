"""
User Preferences Manager
Save and manage user settings and preferences
Version 1.0.0
"""

import streamlit as st
from typing import Dict, Any
import json


# Default preferences
DEFAULT_PREFERENCES = {
    "sprite_style": "static",  # static, animated, or home
    "shiny_mode": False,
    "gallery_limit": 50,
    "theme": "light",  # light or dark
    "show_variants": True,
    "auto_play_cries": False,
    "default_sort": "pokedex_number",
    "cards_per_row": 3,
    "show_type_effectiveness": True,
    "default_generation": "all",
    "favorite_type": None
}


def initialize_preferences():
    """Initialize preferences in session state"""
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = DEFAULT_PREFERENCES.copy()


def get_preference(key: str, default: Any = None) -> Any:
    """
    Get a user preference value
    
    Args:
        key: Preference key
        default: Default value if preference not found
        
    Returns:
        Preference value
    """
    initialize_preferences()
    return st.session_state.user_preferences.get(key, default)


def set_preference(key: str, value: Any):
    """
    Set a user preference value
    
    Args:
        key: Preference key
        value: New value
    """
    initialize_preferences()
    st.session_state.user_preferences[key] = value


def reset_preferences():
    """Reset all preferences to defaults"""
    st.session_state.user_preferences = DEFAULT_PREFERENCES.copy()
    st.success("✅ Preferences reset to defaults")
    st.rerun()


def export_preferences() -> str:
    """
    Export preferences as JSON string
    
    Returns:
        JSON string of preferences
    """
    initialize_preferences()
    return json.dumps(st.session_state.user_preferences, indent=2)


def import_preferences(json_str: str) -> bool:
    """
    Import preferences from JSON string
    
    Args:
        json_str: JSON string with preferences
        
    Returns:
        True if successful, False otherwise
    """
    try:
        preferences = json.loads(json_str)
        # Validate keys
        for key in preferences:
            if key not in DEFAULT_PREFERENCES:
                return False
        
        st.session_state.user_preferences = preferences
        return True
    except Exception:
        return False


def display_preferences_tab():
    """Display the user preferences settings tab"""
    st.markdown("### ⚙️ User Preferences")
    st.caption("Customize your Pokemon Dashboard experience")
    
    initialize_preferences()
    
    # Create tabs for different preference categories
    pref_tabs = st.tabs([
        "🎨 Display",
        "🖼️ Sprites",
        "🔢 Data",
        "🎯 Defaults",
        "💾 Import/Export"
    ])
    
    # Display Settings Tab
    with pref_tabs[0]:
        st.markdown("#### Display Settings")
        
        # Theme
        theme = st.selectbox(
            "Theme",
            ["light", "dark"],
            index=0 if get_preference("theme") == "light" else 1,
            key="pref_theme"
        )
        set_preference("theme", theme)
        
        # Cards per row
        cards_per_row = st.slider(
            "Cards per row in gallery",
            1, 5, get_preference("cards_per_row", 3),
            key="pref_cards_per_row"
        )
        set_preference("cards_per_row", cards_per_row)
        
        # Show type effectiveness
        show_type_eff = st.checkbox(
            "Show type effectiveness hints",
            value=get_preference("show_type_effectiveness", True),
            key="pref_show_type_eff"
        )
        set_preference("show_type_effectiveness", show_type_eff)
        
        # Show variants
        show_variants = st.checkbox(
            "Include variant forms in searches",
            value=get_preference("show_variants", True),
            key="pref_show_variants"
        )
        set_preference("show_variants", show_variants)
    
    # Sprite Settings Tab
    with pref_tabs[1]:
        st.markdown("#### Sprite Settings")
        
        # Sprite style
        sprite_style = st.radio(
            "Default sprite style",
            ["static", "animated", "home"],
            index=["static", "animated", "home"].index(
                get_preference("sprite_style", "static")
            ),
            key="pref_sprite_style",
            help="Static: PNG sprites | Animated: GIF sprites | Home: 3D models"
        )
        set_preference("sprite_style", sprite_style)
        
        # Shiny mode
        shiny_mode = st.checkbox(
            "Show shiny sprites by default",
            value=get_preference("shiny_mode", False),
            key="pref_shiny_mode"
        )
        set_preference("shiny_mode", shiny_mode)
        
        # Auto-play cries
        auto_play = st.checkbox(
            "Auto-play Pokemon cries",
            value=get_preference("auto_play_cries", False),
            key="pref_auto_play_cries"
        )
        set_preference("auto_play_cries", auto_play)
    
    # Data Settings Tab
    with pref_tabs[2]:
        st.markdown("#### Data Display Settings")
        
        # Gallery limit
        gallery_limit = st.slider(
            "Maximum Pokemon in gallery view",
            10, 200, get_preference("gallery_limit", 50),
            step=10,
            key="pref_gallery_limit"
        )
        set_preference("gallery_limit", gallery_limit)
        
        # Default sort
        sort_options = [
            "pokedex_number",
            "name",
            "total",
            "hp",
            "attack",
            "defense",
            "speed"
        ]
        default_sort = st.selectbox(
            "Default sort field",
            sort_options,
            index=sort_options.index(
                get_preference("default_sort", "pokedex_number")
            ),
            key="pref_default_sort"
        )
        set_preference("default_sort", default_sort)
    
    # Defaults Tab
    with pref_tabs[3]:
        st.markdown("#### Default Filters")
        
        # Default generation
        gen_options = ["all", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        default_gen = st.selectbox(
            "Default generation filter",
            gen_options,
            index=gen_options.index(
                str(get_preference("default_generation", "all"))
            ),
            key="pref_default_gen"
        )
        set_preference("default_generation", default_gen)
        
        # Favorite type
        type_options = [
            None, "normal", "fire", "water", "electric", "grass", "ice",
            "fighting", "poison", "ground", "flying", "psychic", "bug",
            "rock", "ghost", "dragon", "dark", "steel", "fairy"
        ]
        favorite_type = st.selectbox(
            "Favorite type (for quick filters)",
            type_options,
            index=type_options.index(get_preference("favorite_type")),
            format_func=lambda x: "None" if x is None else x.title(),
            key="pref_favorite_type"
        )
        set_preference("favorite_type", favorite_type)
    
    # Import/Export Tab
    with pref_tabs[4]:
        st.markdown("#### Import / Export Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Export**")
            if st.button("📥 Export Preferences", use_container_width=True):
                prefs_json = export_preferences()
                st.download_button(
                    label="💾 Download JSON",
                    data=prefs_json,
                    file_name="pokemon_dashboard_preferences.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with st.expander("View Current Preferences"):
                st.code(export_preferences(), language="json")
        
        with col2:
            st.markdown("**Import**")
            uploaded_file = st.file_uploader(
                "Upload preferences JSON",
                type=['json'],
                key="pref_upload"
            )
            
            if uploaded_file is not None:
                try:
                    json_str = uploaded_file.read().decode()
                    if import_preferences(json_str):
                        st.success("✅ Preferences imported successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid preferences file")
                except Exception as e:
                    st.error(f"❌ Error importing: {e}")
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            reset_preferences()
    
    # Summary
    st.markdown("---")
    st.markdown("### 📊 Current Settings Summary")
    
    summary_cols = st.columns(3)
    
    with summary_cols[0]:
        st.metric("Theme", get_preference("theme", "light").title())
        st.metric("Sprite Style", get_preference("sprite_style", "static").title())
        st.metric("Gallery Limit", get_preference("gallery_limit", 50))
    
    with summary_cols[1]:
        st.metric("Cards/Row", get_preference("cards_per_row", 3))
        st.metric("Default Sort", get_preference("default_sort", "pokedex_number"))
        st.metric("Default Gen", get_preference("default_generation", "all"))
    
    with summary_cols[2]:
        st.metric("Shiny Mode", "On" if get_preference("shiny_mode") else "Off")
        st.metric("Show Variants", "Yes" if get_preference("show_variants") else "No")
        fav_type = get_preference("favorite_type")
        st.metric("Favorite Type", fav_type.title() if fav_type else "None")


def render_preferences_sidebar():
    """Render quick preferences in sidebar"""
    initialize_preferences()
    
    with st.sidebar.expander("⚙️ Quick Settings"):
        # Quick theme toggle
        current_theme = get_preference("theme", "light")
        if st.checkbox("🌙 Dark Mode", value=(current_theme == "dark"), key="quick_dark_mode"):
            set_preference("theme", "dark")
        else:
            set_preference("theme", "light")
        
        # Quick shiny toggle
        shiny = st.checkbox(
            "✨ Shiny Sprites",
            value=get_preference("shiny_mode", False),
            key="quick_shiny"
        )
        set_preference("shiny_mode", shiny)


def apply_preferences_to_query(df, query_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply user preferences to search/filter parameters
    
    Args:
        df: Pokemon DataFrame
        query_params: Current query parameters
        
    Returns:
        Updated query parameters with preferences applied
    """
    initialize_preferences()
    
    # Apply default generation filter if not specified
    if 'generation' not in query_params:
        default_gen = get_preference("default_generation", "all")
        if default_gen != "all":
            query_params['generation'] = int(default_gen)
    
    # Apply favorite type if no type specified
    if 'type' not in query_params:
        favorite_type = get_preference("favorite_type")
        if favorite_type:
            query_params['type'] = favorite_type
    
    # Apply default sort
    if 'sort_by' not in query_params:
        query_params['sort_by'] = get_preference("default_sort", "pokedex_number")
    
    # Apply variant filter
    if not get_preference("show_variants", True):
        query_params['exclude_variants'] = True
    
    return query_params
