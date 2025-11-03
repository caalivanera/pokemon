"""
Dark Mode Feature Module
Provides theme switching between light and dark modes with persistent settings
"""

import streamlit as st

# Dark mode color scheme
DARK_THEME = {
    'background': '#0f172a',
    'secondary_bg': '#1e293b',
    'card_bg': '#1e293b',
    'card_hover_bg': '#334155',
    'text': '#f1f5f9',
    'text_secondary': '#cbd5e1',
    'border': '#334155',
    'accent': '#22c55e',
    'accent_hover': '#16a34a',
    'shadow': 'rgba(0, 0, 0, 0.5)',
}

# Light mode color scheme
LIGHT_THEME = {
    'background': '#ffffff',
    'secondary_bg': '#f8fafc',
    'card_bg': '#ffffff',
    'card_hover_bg': '#f1f5f9',
    'text': '#0f172a',
    'text_secondary': '#475569',
    'border': '#e2e8f0',
    'accent': '#22c55e',
    'accent_hover': '#16a34a',
    'shadow': 'rgba(0, 0, 0, 0.1)',
}


def apply_dark_mode(is_dark: bool = True) -> None:
    """
    Apply dark or light mode styling to the Streamlit app
    
    Args:
        is_dark: True for dark mode, False for light mode
    """
    theme = DARK_THEME if is_dark else LIGHT_THEME
    
    st.markdown(f"""
    <style>
        /* Global theme colors */
        :root {{
            --bg-color: {theme['background']};
            --secondary-bg: {theme['secondary_bg']};
            --card-bg: {theme['card_bg']};
            --text-color: {theme['text']};
            --text-secondary: {theme['text_secondary']};
            --border-color: {theme['border']};
            --accent-color: {theme['accent']};
            --shadow: {theme['shadow']};
        }}
        
        /* Main app background */
        .stApp {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {theme['secondary_bg']};
            border-right: 1px solid {theme['border']};
        }}
        
        section[data-testid="stSidebar"] * {{
            color: {theme['text']} !important;
        }}
        
        /* Card containers */
        .stMetric {{
            background-color: {theme['card_bg']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
            padding: 1rem;
            transition: all 0.3s ease;
        }}
        
        .stMetric:hover {{
            background-color: {theme['card_hover_bg']};
            box-shadow: 0 4px 12px {theme['shadow']};
            transform: translateY(-2px);
        }}
        
        /* Pokemon cards */
        .pokemon-card {{
            background-color: {theme['card_bg']} !important;
            border: 2px solid {theme['border']} !important;
            color: {theme['text']} !important;
        }}
        
        .pokemon-card:hover {{
            border-color: {theme['accent']} !important;
            box-shadow: 0 8px 24px {theme['shadow']} !important;
        }}
        
        /* Dataframe styling */
        .stDataFrame {{
            background-color: {theme['card_bg']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
        }}
        
        .stDataFrame tbody tr:hover {{
            background-color: {theme['card_hover_bg']} !important;
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {theme['secondary_bg']};
            border-bottom: 2px solid {theme['border']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {theme['text_secondary']};
        }}
        
        .stTabs [aria-selected="true"] {{
            color: {theme['accent']} !important;
            border-bottom-color: {theme['accent']} !important;
        }}
        
        /* Input fields */
        .stTextInput input, .stSelectbox select, .stMultiSelect {{
            background-color: {theme['card_bg']} !important;
            color: {theme['text']} !important;
            border: 1px solid {theme['border']} !important;
        }}
        
        /* Buttons */
        .stButton button {{
            background-color: {theme['accent']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stButton button:hover {{
            background-color: {theme['accent_hover']};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px {theme['shadow']};
        }}
        
        /* Charts */
        .js-plotly-plot .plotly {{
            background-color: {theme['card_bg']} !important;
        }}
        
        .js-plotly-plot .plotly .bg {{
            fill: {theme['card_bg']} !important;
        }}
        
        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: {theme['text']} !important;
        }}
        
        /* Labels and text */
        p, span, div {{
            color: {theme['text']};
        }}
        
        .stMarkdown {{
            color: {theme['text']};
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: {theme['card_bg']};
            border: 1px solid {theme['border']};
            color: {theme['text']};
        }}
        
        .streamlit-expanderContent {{
            background-color: {theme['secondary_bg']};
            border: 1px solid {theme['border']};
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {theme['secondary_bg']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {theme['border']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {theme['accent']};
        }}
    </style>
    """, unsafe_allow_html=True)


def dark_mode_toggle() -> bool:
    """
    Create a dark mode toggle widget in the sidebar
    
    Returns:
        bool: True if dark mode is enabled
    """
    # Initialize session state
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True
    
    # Create toggle with custom label
    dark_mode = st.sidebar.checkbox(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode,
        help="Toggle between dark and light themes"
    )
    
    # Update session state
    st.session_state.dark_mode = dark_mode
    
    return dark_mode


def get_theme_colors(is_dark: bool = True) -> dict:
    """
    Get the current theme color scheme
    
    Args:
        is_dark: True for dark mode, False for light mode
        
    Returns:
        dict: Theme color scheme
    """
    return DARK_THEME if is_dark else LIGHT_THEME
