# Competitive Tier System Structure

## Smogon Tier Classifications

### Tier Hierarchy

1. **Uber** - Ban-worthy Pokemon (too powerful for standard play)
2. **OU (OverUsed)** - Most commonly used in standard competitive play
3. **UUBL (UnderUsed Banned List)** - Too strong for UU but not OU
4. **UU (UnderUsed)** - Less common but still viable
5. **RUBL (Rarely Used Banned List)** - Too strong for RU but not UU
6. **RU (Rarely Used)** - Situationally useful
7. **NUBL (Never Used Banned List)** - Too strong for NU but not RU
8. **NU (Never Used)** - Rarely seen in competitive
9. **PUBL (Partially Used Banned List)** - Too strong for PU but not NU
10. **PU (Partially Used)** - Bottom tier of usage
11. **ZU (Zero Used)** - Essentially unused
12. **Untiered** - Not assigned to any tier

## Data Structure

### tier_data.csv Format

```csv
pokemon_name,pokedex_number,tier,generation,usage_percent,tier_rank,notes
Mewtwo,150,Uber,1,45.2,1,Legendary psychic type
Landorus-Therian,645,OU,5,62.8,1,Most used OU Pokemon
Charizard,6,UU,1,18.5,12,Versatile fire/flying type
Pikachu,25,ZU,1,0.1,800,Too weak for competitive
```

### Columns

| Column | Type | Description |
|--------|------|-------------|
| pokemon_name | str | Pokemon name (with form if applicable) |
| pokedex_number | int | National dex number |
| tier | str | Current tier (Uber, OU, UU, RU, NU, PU, ZU) |
| generation | int | Generation (1-9) |
| usage_percent | float | Usage percentage in tier |
| tier_rank | int | Rank within tier |
| notes | str | Additional competitive notes |

## Sample Tier Distribution

### Generation 9 (Current Competitive Metagame)

**Uber (30-40 Pokemon):**
- Legendary Pokemon: Mewtwo, Rayquaza, Kyogre, Groudon
- Mega Evolutions: Mega Rayquaza, Mega Mewtwo
- Mythical Pokemon: Arceus, Zacian-Crowned

**OU (~50-60 Pokemon):**
- Landorus-Therian (62.8% usage)
- Garchomp (48.3% usage)
- Ferrothorn (42.1% usage)
- Toxapex (39.7% usage)
- Dragapult (38.2% usage)

**UU (~80-100 Pokemon):**
- Charizard
- Hydreigon
- Scizor
- Aegislash

**Lower Tiers (~1000+ Pokemon):**
- RU, NU, PU, ZU combined

## Implementation

### Loading Tier Data

```python
@st.cache_data
def load_tier_data():
    """Load Smogon tier classifications"""
    csv_path = Path("data/competitive/tier_data.csv")
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None

def get_pokemon_tier(pokemon_name, tier_df):
    """Get tier for specific Pokemon"""
    if tier_df is None:
        return "Untiered"
    
    result = tier_df[tier_df['pokemon_name'] == pokemon_name]
    if len(result) > 0:
        return result.iloc[0]['tier']
    return "Untiered"
```

### Tier Filtering

```python
def filter_by_tier(df, tier_df, selected_tiers):
    """Filter Pokemon by competitive tier"""
    if tier_df is None:
        return df
    
    # Merge with tier data
    merged = df.merge(
        tier_df[['pokemon_name', 'tier']], 
        left_on='name', 
        right_on='pokemon_name',
        how='left'
    )
    
    # Filter by selected tiers
    if selected_tiers:
        merged = merged[merged['tier'].isin(selected_tiers)]
    
    return merged
```

### Tier Statistics Dashboard

```python
def display_tier_statistics(df, tier_df):
    """Display competitive tier analysis"""
    st.header("🏆 Competitive Tier Analysis")
    
    if tier_df is None:
        st.warning("Tier data not available")
        return
    
    # Tier distribution pie chart
    tier_counts = tier_df['tier'].value_counts()
    fig = px.pie(
        values=tier_counts.values,
        names=tier_counts.index,
        title='Pokemon Distribution by Tier',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig)
    
    # Tier selector
    selected_tier = st.selectbox(
        "Select Tier",
        options=['Uber', 'OU', 'UU', 'RU', 'NU', 'PU', 'ZU']
    )
    
    # Show Pokemon in selected tier
    tier_pokemon = tier_df[tier_df['tier'] == selected_tier]
    tier_pokemon = tier_pokemon.sort_values('usage_percent', ascending=False)
    
    st.subheader(f"{selected_tier} Tier Pokemon")
    st.dataframe(
        tier_pokemon[['pokemon_name', 'usage_percent', 'tier_rank']],
        hide_index=True
    )
```

## Data Collection Script

### Option 1: Web Scraping from Smogon

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_smogon_tiers():
    """Scrape tier data from Smogon"""
    tiers = []
    
    # Smogon usage stats URL
    base_url = "https://www.smogon.com/stats/2024-10/"
    
    for tier in ['ou', 'uu', 'ru', 'nu', 'pu']:
        url = f"{base_url}gen9{tier}-1825.txt"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse usage stats
            lines = response.text.split('\n')
            for line in lines:
                # Extract Pokemon name and usage %
                # Format: | 1 | Landorus-Therian | 62.8% |
                if '|' in line and '%' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4:
                        rank = parts[1]
                        name = parts[2]
                        usage = parts[3].replace('%', '')
                        tiers.append({
                            'pokemon_name': name,
                            'tier': tier.upper(),
                            'usage_percent': float(usage),
                            'tier_rank': int(rank)
                        })
    
    return pd.DataFrame(tiers)
```

### Option 2: Manual CSV Creation

Create CSV file manually with known tier placements from Smogon resources.

## Tier Color Coding

```python
def get_tier_color(tier):
    """Get color for tier badge"""
    colors = {
        'Uber': '#FF0000',    # Red
        'OU': '#FF8800',      # Orange
        'UUBL': '#FFAA00',    # Light Orange
        'UU': '#FFDD00',      # Yellow
        'RUBL': '#DDFF00',    # Yellow-Green
        'RU': '#88FF00',      # Light Green
        'NUBL': '#00FF88',    # Green-Cyan
        'NU': '#00DDFF',      # Cyan
        'PUBL': '#0088FF',    # Light Blue
        'PU': '#0044FF',      # Blue
        'ZU': '#8800FF',      # Purple
        'Untiered': '#888888' # Gray
    }
    return colors.get(tier, '#888888')
```

## Integration with Dashboard

### Add to Sidebar Filters

```python
# In sidebar
if tier_df is not None:
    st.sidebar.subheader("🏆 Competitive Tier")
    selected_tiers = st.sidebar.multiselect(
        "Filter by Tier",
        options=['Uber', 'OU', 'UU', 'RU', 'NU', 'PU', 'ZU', 'Untiered'],
        default=[]
    )
    
    if selected_tiers:
        filtered_df = filter_by_tier(filtered_df, tier_df, selected_tiers)
```

### Add Tier Badge to Pokemon Cards

```python
def display_pokemon_with_tier(pokemon, tier_df):
    """Display Pokemon card with tier badge"""
    tier = get_pokemon_tier(pokemon['name'], tier_df)
    tier_color = get_tier_color(tier)
    
    st.markdown(f"""
        <span style="background-color: {tier_color}; color: white; 
                     padding: 4px 12px; border-radius: 6px; font-weight: bold;">
            {tier}
        </span>
    """, unsafe_allow_html=True)
    
    display_pokemon_card(pokemon)
```

## Status

**Current Status:** ⏳ Structure Defined, Data Collection Needed

**Blockers:**
- Need to scrape Smogon usage stats
- Or manually compile tier data for ~1200 Pokemon
- Tiers change monthly with meta shifts

**Estimated Time:** 4-5 hours
- 2 hours: Data collection (scraping or manual)
- 1 hour: Data processing and validation
- 1 hour: Dashboard integration
- 1 hour: Testing and refinement

**Quick Solution:** Create CSV with top 100-200 competitive Pokemon, mark rest as "Untiered"

## Sample Data (Top 20 OU Pokemon)

```csv
pokemon_name,pokedex_number,tier,generation,usage_percent,tier_rank,notes
Landorus-Therian,645,OU,5,62.8,1,Intimidate ability makes it top pick
Garchomp,445,OU,4,48.3,2,Fast physical sweeper
Ferrothorn,598,OU,5,42.1,3,Defensive pivot
Toxapex,748,OU,7,39.7,4,Stall king
Dragapult,887,OU,8,38.2,5,Fast special attacker
Heatran,485,OU,4,35.6,6,Fire/Steel defensive core
Clefable,36,OU,1,33.4,7,Magic Guard utility
Tornadus-Therian,641,OU,5,31.2,8,Hurricane spam
Kartana,798,OU,7,29.8,9,Beast Boost sweeper
Tapu Lele,786,OU,7,28.5,10,Psychic Surge terrain setter
```

Save this as `data/competitive/tier_data_sample.csv` for testing.
