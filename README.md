# ⚡ Pokemon National Dex Dashboard v5.4.1

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/demo-live-green.svg)](https://1pokemon.streamlit.app/)
[![Data: 1,194 Forms](https://img.shields.io/badge/forms-1,194-red.svg)](https://bulbapedia.bulbagarden.net)
[![Completion: 100%](https://img.shields.io/badge/completion-100%25-brightgreen.svg)]()
[![Competitive Data](https://img.shields.io/badge/competitive-tiers%20%26%20stats-orange.svg)]()
[![Movesets: 1,010](https://img.shields.io/badge/movesets-1,010-purple.svg)]()
[![Dark Mode](https://img.shields.io/badge/dark%20mode-enabled-purple.svg)]()
[![AI Features](https://img.shields.io/badge/AI-team%20recommender-blue.svg)]()
[![Meta Analytics](https://img.shields.io/badge/meta-analytics-cyan.svg)]()

> **100% Complete Pokemon Database Dashboard** with **Advanced Analytics**, **AI Team Recommender**, **Damage Calculator**, featuring all **1,194** Pokemon forms with **98.6% sprite coverage**, **Competitive Tier Data** (86 Pokemon), **Usage Statistics** (516 records), **Comprehensive Movesets** (1,010 Pokemon), and **5,036+ high-quality assets**.

🌐 **Live Application:** [https://1pokemon.streamlit.app/](https://1pokemon.streamlit.app/)

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Total Pokemon Forms** | 1,194 |
| **Base Forms** | 1,089 (91.2%) |
| **Variant Forms** | 105 (8.8%) |
| **Static Sprites** | 3,077 (100% coverage) |
| **Animated Sprites** | 649 (54.4% coverage) |
| **Pokemon Icons** | 1,238 (103.7% coverage) |
| **Type Icons** | 72 (18 types × 4 sizes) |
| **Total Asset Files** | 5,036+ files |
| **Competitive Tier Data** | 86 Pokemon (8 tiers) |
| **Usage Statistics** | 516 monthly records |
| **Moveset Database** | 1,010 Pokemon (4,040 moves) |
| **Game Posters** | 32 games (9 generations) |
| **Documentation** | 4,000+ lines |
| **Code Base** | 17,400+ lines |
| **Tasks Complete** | 16/16 (100%) + Phase 5 |
| **Analytics Modules** | 3 (Meta, Damage, Team AI) |

📈 **See detailed statistics:** [docs/reports/QUANTIFIABLE_STATISTICS.md](docs/reports/QUANTIFIABLE_STATISTICS.md)

---

## 🎉 What's New in v5.4.1

### 🆕 **Latest: Comparison & Analytics Tools**

#### 🔍 **Sprite Comparison** | ⚔️ **Advanced Export** | 📊 **Performance Monitor**
**New in v5.4.1**: Compare Pokemon side-by-side • Export in 5 formats • Track analytics

---

### 🚀 **Phase 5: Advanced Analytics (v5.4.0)**

#### 📊 **Meta Analytics Dashboard**
- Real-time competitive usage trends (516 records)
- Rising/falling Pokemon detection algorithm
- Move popularity analysis (237 moves tracked)
- Ability statistics visualization (96 abilities)
- Tier distribution across 8 competitive tiers
- Interactive Plotly charts with export capabilities

#### ⚔️ **Damage Calculator**
- Exact Gen 5+ damage formula implementation
- Complete 18×18 type effectiveness matrix
- STAB (Same Type Attack Bonus) calculation
- Critical hit damage simulation
- Weather, item, and ability modifiers
- Stat boost/drop support (-6 to +6 stages)
- OHKO/2HKO prediction system
- Supports 1,010 Pokemon and 4,040 moves

#### 🤖 **AI Team Recommender**
- Intelligent team building algorithm
- Type coverage optimization
- Weakness/resistance analysis
- Role balancing (Sweeper, Tank, Support, Balanced)
- Seed Pokemon support (build around favorites)
- Meta-based recommendations using usage statistics
- Team scoring system (BST + type coverage + usage)
- JSON/Text export functionality

#### � **Image Optimization Tool**
- PNG to WebP conversion script
- Parallel processing (multi-threaded)
- Expected 50-70% file size reduction
- Quality control (default: 85%)
- Batch processing for entire directories
- Original file preservation option

#### 📈 **Enhanced Integration**
- 15-tab interface (was 12 tabs)
- Tab 13: 📊 Meta Analytics
- Tab 14: ⚔️ Damage Calculator
- Tab 15: 🤖 Team Recommender
- Error handling for missing data
- Graceful degradation

---

### 🎯 **Previous: v5.3.2 Completion**
- ✅ All 16 planned tasks implemented
- ✅ Critical IndexError bug fixed
- ✅ Complete competitive data integration
- ✅ Production-ready deployment

### 🏆 **Competitive Tier System**
- 86 Pokemon across 8 competitive tiers
- Tiers: AG, Uber, OU, UU, RU, NU, PU, ZU
- Usage percentage tracking
- Tier-specific rankings
- Sample data includes top competitive Pokemon

### 📈 **Usage Statistics & Trends**
- 516 monthly usage records (6 months of data)
- 237 move usage combinations analyzed
- 96 ability usage variations tracked
- Temporal trend analysis
- Month-over-month meta tracking

### ⚔️ **Comprehensive Moveset Database**
- 1,010 Pokemon with complete movesets
- 4,040 individual move entries
- 18 type categories with STAB moves
- Move power, accuracy, and learn methods
- Physical, Special, and Status moves

### 🎮 **Game Poster Collection**
- 32 Pokemon games organized by generation
- Complete metadata with regions
- Gen I through Gen IX coverage
- Download instructions and structure

### � **Dynamic Pokemon Search**
- Live search with instant results
- Search by name, number, type, or generation
- Type indicators `[Fire/Flying]` in results
- Adjustable pagination (10/20/50/100)
- Enhanced success/warning feedback

### ⚡ **Performance Optimization**
- Caching implemented with `@st.cache_data`
- Optimized type color lookups
- Consistent sprite gallery performance
- DataFrame index management fixes

### 🌙 **Dark Mode**
Toggle between light and dark themes with persistent settings! Optimized color schemes for Pokemon data visualization with smooth transitions.

### ⚡ **Type Effectiveness Calculator**
- Complete 18x18 type effectiveness matrix
- Calculate damage multipliers (0x, 0.25x, 0.5x, 1x, 2x, 4x)
- Offensive and defensive coverage analysis
- Interactive type matchup heatmap
- Real-time dual-type combination analysis

### 👥 **Advanced Team Builder**
- Build and manage 6-Pokemon competitive teams
- Team type coverage analysis
- Defensive weakness tracking
- Offensive coverage visualization
- Average team stats with radar chart
- Export teams to JSON
- Coverage heatmap showing team synergy

### 🔍 **Advanced Search & Filters**
- Quick search bar for instant results
- BST range filtering
- Individual stat sliders (HP, Attack, Defense, Sp.Attack, Sp.Defense, Speed)
- Type combination filters
- Ability search
- Generation filtering (Gen 1-9)
- Regional filtering (NEW!)
- Variant type filtering
- **5 Predefined Presets**:
  - Starter Pokemon (all 9 generations)
  - Pseudo-Legendaries (BST 600)
  - Fast Attackers (Speed 100+, Attack 100+)
  - Tanks (HP 100+, Defense 80+, Sp.Defense 80+)
  - Glass Cannons (Attack 110+, Defense ≤70)
- Filter result summaries with match rates

---

## 📑 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Quick Start](#-quick-start)
- [Technical Documentation](#-technical-documentation)
- [Data Architecture](#-data-architecture)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

A **Pokédex** is a digital electronic encyclopedia that acts as a guide for Pokémon trainers, recording data on Pokémon species they encounter. In the games, it tracks the player's progress in catching or observing Pokémon, with detailed entries unlocked as a trainer catches or obtains a species. It's an essential tool for any trainer, and in some versions of the games and the anime, it functions as a reference tool to learn about Pokémon types, sizes, and locations.

🌐 **Live Application:** [https://1pokemon.streamlit.app/](https://1pokemon.streamlit.app/)

This dashboard serves as your **digital Pokédex companion**, providing comprehensive data analysis and exploration tools for the complete National Pokédex spanning Generations 1 through 9.

---

## 📁 Project Structure

```
pokedex-dashboard/
├── assets/                      # All visual assets
│   ├── sprites/                # Pokemon sprites (static & animated)
│   ├── icons/                  # Pokemon icons
│   ├── types/                  # Type icons (18 types × 4 sizes)
│   └── games/                  # Game poster structure (32 games)
│
├── data/                        # All data files
│   ├── competitive/            # Competitive battle data
│   │   ├── tier_data.csv      # 86 Pokemon, 8 tiers
│   │   ├── usage_stats.csv    # 516 monthly records
│   │   ├── move_usage.csv     # 237 move combinations
│   │   └── ability_usage.csv  # 96 ability variations
│   ├── moves/                  # Moveset database
│   │   └── pokemon_movesets.json  # 1,010 Pokemon
│   ├── reference/              # Reference YAML files
│   │   ├── abilities.yaml
│   │   ├── types.yaml
│   │   └── pokemon-forms.yaml
│   ├── metadata/               # Metadata & validation
│   │   ├── type_colors.json
│   │   └── type_effectiveness.json
│   ├── backups/                # Backup CSV files
│   └── pokemon.csv             # Main dataset (1,194 Pokemon)
│
├── src/                         # Application source code
│   └── core/
│       └── app.py              # Main Streamlit app (2,010 lines)
│
├── scripts/                     # Data collection scripts
│   ├── collect_tier_data.py   # Tier data collector
│   ├── generate_usage_stats.py # Usage statistics generator
│   ├── generate_moveset_db.py # Moveset database creator
│   └── setup_game_posters.py  # Game poster organizer
│
├── docs/                        # Documentation
│   ├── reports/                # Session & completion reports
│   │   ├── FINAL_COMPLETION_REPORT_v5.3.2.md
│   │   ├── QUANTIFIABLE_STATISTICS.md
│   │   └── session reports...
│   ├── guides/                 # Implementation guides
│   └── technical/              # Technical documentation
│
├── tests/                       # Test files
├── config/                      # Configuration files
├── .streamlit/                  # Streamlit config
└── README.md                    # This file
```

---

## ✨ Features

### 📊 Core Capabilities

- **Complete Pokemon Database**: All 1,194 forms (1,089 base + 105 variants) from Gen I-IX
- **5,036+ High-Quality Assets**: Sprites, icons, and type graphics
- **Multi-Tab Interface**: 11 specialized tabs for different analyses
- **Light/Dark Theme**: Toggle-able themes with persistent settings
- **Interactive Visualizations**: Plotly-powered charts and graphs
- **Real-Time Search**: Dynamic search with instant results
- **Competitive Data**: Tier rankings, usage stats, and movesets
- **Type Calculator**: Complete 18×18 type effectiveness matrix

### 🎯 Dashboard Tabs

1. **📊 Overview** - Statistics and distribution charts
2. **🔍 Pokemon Search** - Dynamic search with type indicators
3. **⚔️ Competitive Analysis** - Tier information and strategies
4. **📈 Statistics & Trends** - Usage trends and meta analysis
5. **🎨 Type Analysis** - Moveset analysis by type
6. **🧬 Evolution & Forms** - Evolution chains and variants
7. **🎮 By Game** - Filter by 32 Pokemon games
8. **🎨 Sprite Gallery** - Browse all Pokemon sprites
9. **⚡ Type Calculator** - Type effectiveness calculator
10. **👥 Team Builder** - Build and analyze 6-Pokemon teams
11. **🎮 Mini-Game** - "Who's That Pokemon?" quiz

---


---

## 📊 Data Coverage

- **Pokemon**: 1,194 forms (1,089 base + 105 variants)
- **Generations**: 9 (Gen I-IX)
- **Games**: 32 Pokemon games across 9 generations
- **Tiers**: 8 competitive tiers (86 Pokemon with tier data)
- **Movesets**: 1,010 Pokemon (4,040 individual moves)
- **Usage Stats**: 516 monthly records (6 months of data)
- **Sprites**: 5,036+ assets (sprites, icons, type graphics)
- **Data Sources**: Bulbapedia, Serebii.net, Smogon University, PokeAPI

---

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Framework**: [Streamlit](https://streamlit.io/) 1.28+
- **Data Processing**: pandas + numpy
- **Visualizations**: Plotly Express
- **Web Scraping**: BeautifulSoup4 (for data collection)
- **HTTP Requests**: requests library
- **Data Storage**: CSV + JSON formats

---

## 📝 Documentation

- **Project Reports**: See [docs/reports/](docs/reports/) for completion and session reports
- **Implementation Guides**: See [docs/guides/](docs/guides/) for enhancement plans
- **Technical Docs**: See [docs/technical/](docs/technical/) for technical specifications
- **CHANGELOG**: [CHANGELOG.md](CHANGELOG.md) - Version history and updates
- **Statistics**: [docs/reports/QUANTIFIABLE_STATISTICS.md](docs/reports/QUANTIFIABLE_STATISTICS.md)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Steps to Contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- **The Pokemon Company** - Pokemon data and sprites
- **Bulbapedia** - Comprehensive Pokemon database
- **Serebii.net** - Game data and Pokedex information
- **Smogon University** - Competitive tier data and analysis
- **PokeAPI** - Pokemon sprites and assets
- **Streamlit** - Dashboard framework

---

<div align="center">

**Made with ❤️ for Pokemon Trainers Worldwide**

*Gotta Catch 'Em All!*

[Live Demo](https://1pokemon.streamlit.app/) • [Report Bug](https://github.com/caalivanera/pokemon/issues) • [Request Feature](https://github.com/caalivanera/pokemon/issues)

**Built by Charles Alivanera** | [GitHub](https://github.com/caalivanera) | [Email](mailto:caalivanera@gmail.com)

</div>
