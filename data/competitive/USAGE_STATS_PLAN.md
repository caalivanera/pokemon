# Pokemon Usage Statistics & Trends

## Overview

Integration of Pokemon usage data, move usage, ability rates, and temporal trends from competitive data sources.

## Data Sources

### 1. Smogon Usage Stats
- **URL:** https://www.smogon.com/stats/
- **Format:** Text files updated monthly
- **Data:** Pokemon usage %, move usage %, ability usage %, item usage %
- **Coverage:** All tiers (Uber, OU, UU, RU, NU, PU)

### 2. Pikalytics
- **URL:** https://pikalytics.com/
- **Format:** Web API / Scraping
- **Data:** VGC (Video Game Championships) usage data
- **Coverage:** Current generation competitive formats

### 3. Pokemon Showdown
- **URL:** https://pokemonshowdown.com/stats/
- **Format:** JSON/Text files
- **Data:** Real-time usage from simulator battles

## Data Structure

### usage_stats.csv Format

```csv
pokemon_name,month,year,tier,usage_percent,rank,battles_count,avg_weight,viability_ceiling
Landorus-Therian,10,2024,OU,62.83,1,8542123,85.2,95
Garchomp,10,2024,OU,48.31,2,6201874,72.1,90
```

### move_usage.csv Format

```csv
pokemon_name,move_name,tier,usage_percent,month,year
Landorus-Therian,Earthquake,OU,98.5,10,2024
Landorus-Therian,U-turn,OU,87.2,10,2024
```

### ability_usage.csv Format

```csv
pokemon_name,ability_name,tier,usage_percent,month,year
Landorus-Therian,Intimidate,OU,99.8,10,2024
Garchomp,Rough Skin,OU,95.2,10,2024
```

## Implementation

### Data Collection Script

```python
import requests
import pandas as pd
from datetime import datetime
import time

class SmogonStatsCollector:
    """Collect usage statistics from Smogon"""
    
    BASE_URL = "https://www.smogon.com/stats/"
    
    def __init__(self, year=2024, month=10):
        self.year = year
        self.month = month
        self.date_str = f"{year}-{month:02d}"
    
    def fetch_usage_stats(self, tier='ou', rating=1825):
        """Fetch usage statistics for a tier"""
        url = f"{self.BASE_URL}{self.date_str}/gen9{tier}-{rating}.txt"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return self.parse_usage_file(response.text, tier)
        except Exception as e:
            print(f"Error fetching {tier}: {e}")
            return None
    
    def parse_usage_file(self, text, tier):
        """Parse Smogon usage stats text file"""
        stats = []
        lines = text.split('\n')
        
        # Skip header lines
        in_data = False
        for line in lines:
            if '| Rank |' in line:
                in_data = True
                continue
            
            if in_data and '|' in line and '%' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 7:
                    try:
                        rank = int(parts[1])
                        name = parts[2]
                        usage_pct = float(parts[3].replace('%', ''))
                        raw_count = int(parts[4])
                        raw_pct = float(parts[5].replace('%', ''))
                        real = float(parts[6].replace('%', ''))
                        
                        stats.append({
                            'pokemon_name': name,
                            'rank': rank,
                            'usage_percent': usage_pct,
                            'raw_count': raw_count,
                            'raw_percent': raw_pct,
                            'real_percent': real,
                            'tier': tier.upper(),
                            'month': self.month,
                            'year': self.year
                        })
                    except (ValueError, IndexError):
                        continue
        
        return pd.DataFrame(stats)
    
    def fetch_moveset_stats(self, pokemon_name, tier='ou', rating=1825):
        """Fetch moveset statistics for specific Pokemon"""
        # Format: landorus-therian
        formatted_name = pokemon_name.lower().replace(' ', '-')
        url = f"{self.BASE_URL}{self.date_str}/moveset/gen9{tier}-{rating}/{formatted_name}.txt"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return self.parse_moveset_file(response.text, pokemon_name)
        except Exception as e:
            print(f"Error fetching moveset for {pokemon_name}: {e}")
            return None
    
    def parse_moveset_file(self, text, pokemon_name):
        """Parse moveset statistics"""
        data = {
            'pokemon_name': pokemon_name,
            'abilities': [],
            'items': [],
            'moves': [],
            'spreads': [],
            'teammates': []
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            if 'Abilities' in line:
                current_section = 'abilities'
            elif 'Items' in line:
                current_section = 'items'
            elif 'Moves' in line:
                current_section = 'moves'
            elif 'Spreads' in line:
                current_section = 'spreads'
            elif 'Teammates' in line:
                current_section = 'teammates'
            elif '%' in line and current_section:
                # Parse line like "Intimidate 99.8%"
                parts = line.strip().split()
                if len(parts) >= 2:
                    name = ' '.join(parts[:-1])
                    percent = float(parts[-1].replace('%', ''))
                    data[current_section].append({
                        'name': name,
                        'usage_percent': percent
                    })
        
        return data
    
    def collect_all_tiers(self):
        """Collect data for all major tiers"""
        all_stats = []
        
        tiers = ['uber', 'ou', 'uu', 'ru', 'nu', 'pu']
        for tier in tiers:
            print(f"Fetching {tier} stats...")
            stats = self.fetch_usage_stats(tier)
            if stats is not None:
                all_stats.append(stats)
            time.sleep(1)  # Rate limiting
        
        return pd.concat(all_stats, ignore_index=True)

# Usage
collector = SmogonStatsCollector(year=2024, month=10)
usage_df = collector.collect_all_tiers()
usage_df.to_csv('data/competitive/usage_stats.csv', index=False)
```

### Dashboard Integration

```python
@st.cache_data
def load_usage_stats():
    """Load usage statistics"""
    csv_path = Path("data/competitive/usage_stats.csv")
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None

def display_usage_trends(df, usage_df):
    """Display usage trends over time"""
    st.header("📊 Competitive Usage Trends")
    
    if usage_df is None:
        st.warning("Usage data not available")
        return
    
    # Pokemon selector
    selected_pokemon = st.selectbox(
        "Select Pokemon",
        options=df['name'].tolist()
    )
    
    # Get usage history for Pokemon
    pokemon_usage = usage_df[
        usage_df['pokemon_name'] == selected_pokemon
    ].sort_values('month')
    
    if len(pokemon_usage) > 0:
        # Usage over time chart
        fig = px.line(
            pokemon_usage,
            x='month',
            y='usage_percent',
            color='tier',
            title=f'{selected_pokemon} Usage Trends',
            labels={'month': 'Month', 'usage_percent': 'Usage %'}
        )
        st.plotly_chart(fig)
        
        # Current stats
        latest = pokemon_usage.iloc[-1]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Tier", latest['tier'])
        with col2:
            st.metric("Usage %", f"{latest['usage_percent']:.2f}%")
        with col3:
            st.metric("Rank", int(latest['rank']))
    else:
        st.info(f"No usage data available for {selected_pokemon}")

def display_move_usage(pokemon_name, moveset_data):
    """Display move usage statistics"""
    st.subheader("Most Used Moves")
    
    if moveset_data and 'moves' in moveset_data:
        moves_df = pd.DataFrame(moveset_data['moves'])
        moves_df = moves_df.sort_values('usage_percent', ascending=False).head(10)
        
        fig = px.bar(
            moves_df,
            x='usage_percent',
            y='name',
            orientation='h',
            title='Top 10 Moves by Usage',
            labels={'usage_percent': 'Usage %', 'name': 'Move'}
        )
        st.plotly_chart(fig)
```

### Temporal Analysis

```python
def analyze_meta_shifts(usage_df, months=6):
    """Analyze meta game shifts over time"""
    st.header("🔄 Meta Game Shifts")
    
    # Get recent months
    recent = usage_df[usage_df['month'] >= (datetime.now().month - months)]
    
    # Pokemon that gained popularity
    gaining = recent.groupby('pokemon_name')['usage_percent'].mean().sort_values(ascending=False).head(10)
    
    st.subheader("Rising Stars")
    st.bar_chart(gaining)
    
    # Pokemon that lost popularity
    declining = recent.groupby('pokemon_name')['usage_percent'].mean().sort_values(ascending=True).head(10)
    
    st.subheader("Declining Usage")
    st.bar_chart(declining)
```

## Status

**Current Status:** ⏳ Structure Defined, Implementation Pending

**Requirements:**
- Web scraping for Smogon stats (monthly updates)
- Data storage (~5-10MB for 12 months of data)
- Automated collection script (run monthly)
- Dashboard integration

**Estimated Time:** 5-6 hours
- 2 hours: Collection script development
- 2 hours: Data processing and storage
- 2 hours: Dashboard integration and charts

**Quick Solution:** 
1. Manually download 1 month of stats from Smogon
2. Parse and store in CSV
3. Display in simple table format
4. Automate later

## Sample Data

Top 10 OU Pokemon (October 2024):

```csv
pokemon_name,month,year,tier,usage_percent,rank
Landorus-Therian,10,2024,OU,62.83,1
Garchomp,10,2024,OU,48.31,2
Ferrothorn,10,2024,OU,42.15,3
Toxapex,10,2024,OU,39.72,4
Dragapult,10,2024,OU,38.21,5
Heatran,10,2024,OU,35.64,6
Clefable,10,2024,OU,33.42,7
Tornadus-Therian,10,2024,OU,31.18,8
Kartana,10,2024,OU,29.83,9
Tapu Lele,10,2024,OU,28.54,10
```

Save as `data/competitive/usage_stats_sample.csv` for testing.

## Notes

- Usage stats change monthly with meta shifts
- New Pokemon can dramatically alter the competitive landscape
- Seasonal tournaments affect usage patterns
- Different rating tiers (1500 vs 1825) show different trends
