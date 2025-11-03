# ⚡ Pokemon National Dex Dashboard v5.2.0

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/demo-live-green.svg)](https://1pokemon.streamlit.app/)
[![Data: 1,194 Forms](https://img.shields.io/badge/forms-1,194-red.svg)](https://bulbapedia.bulbagarden.net)
[![Sprites: 98.6%](https://img.shields.io/badge/sprites-98.6%25-brightgreen.svg)]()
[![Type Icons: 18](https://img.shields.io/badge/type%20icons-18-blue.svg)]()
[![Regional Data](https://img.shields.io/badge/regional-grouping-green.svg)]()
[![Dark Mode](https://img.shields.io/badge/dark%20mode-enabled-purple.svg)]()
[![Type Calculator](https://img.shields.io/badge/type-calculator-orange.svg)]()
[![Team Builder](https://img.shields.io/badge/team-builder-green.svg)]()

> **Comprehensive Pokemon Database Dashboard** featuring all **1,194** Pokemon forms (**1,089 base Pokemon + 105 variants**) from Generations I-IX with **98.6% sprite coverage**, **Regional Grouping**, **Type Icons & Color Mapping**, **Dark Mode**, **Type Calculator**, **Team Builder**, **Advanced Search**, interactive visualizations, competitive data, and **5,036+ high-quality assets** (including 649 animated sprites, 1,238 icons, and 72 type icons).

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
| **Documentation** | 2,500+ lines (16,000+ words) |
| **Code Base** | 14,800+ lines of Python |
| **Repository Size** | 992.7 MB |
| **Regions Covered** | 9 (Kanto-Paldea) |
| **Regional Variants** | 55 forms (Alolan, Galarian, Hisuian, Paldean) |

📈 **See detailed statistics:** [QUANTIFIABLE_STATISTICS.md](QUANTIFIABLE_STATISTICS.md)

---

## 🎉 What's New in v5.2.0

### 🗺️ **Regional Grouping** (NEW!)
- Complete regional classification for all 1,194 Pokemon forms
- 9 regions covered: Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar, Paldea
- Regional variant tracking (55 forms: Alolan, Galarian, Hisuian, Paldean)
- Regional evolution methods by generation
- Regional Pokedex numbers
- Debut generation tracking

### 🎨 **Type Icons & Color Mapping** (NEW!)
- Official Pokemon type icons for all 18 types
- Multiple sizes available (32px, 64px, 128px, original)
- Type color associations with light and dark variants
- Complete type effectiveness data (strengths, weaknesses, immunities)
- Professional icon integration throughout dashboard

### 🖼️ **Expanded Asset Library**
- **3,077 static sprites** (100% coverage - UP from 98.6%)
- **649 animated sprites** (54.4% coverage - UP from 15.9%)
- **1,238 Pokemon icons** (103.7% coverage - NEW!)
- **72 type icons** in 4 sizes (NEW!)
- Total asset library: **5,036+ files** (UP from 1,583)

### 🛠️ **Enhanced Infrastructure**
- Fixed green box display issue on dataset overview
- Comprehensive asset downloader with 8+ sources
- Improved file organization structure
- Project validation and health monitoring tools
- Enhanced documentation and statistics tracking

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

## ✨ Features

**This project has been reorganized with a use-case-based directory structure!**

## ✨ Features

### 📊 Core Capabilities

- **Complete Pokemon Database**: All 1,130 forms (1,025 base + 105 variants) from Gen I-IX
- **2,909 High-Quality Sprites**: Base, shiny, variant, and animated sprites (Gen 1-5)
- **Multi-Tab Interface**: 11 specialized tabs for different analyses
- **Light/Dark Theme**: Toggle-able themes with persistent settings
- **Interactive Visualizations**: Plotly-powered charts and graphs
- **Real-Time Search**: Advanced filtering with instant results
- **Competitive Data**: Complete stat analysis and team building tools
- **Game Filtering**: Filter Pokemon by 38+ Pokemon games

### 🎯 Dashboard Tabs

1. **📊 Overview** - Overall statistics and distribution charts
2. **🔍 Pokemon Search** - Advanced search with comprehensive filters (NEW: Advanced Filters!)
3. **⚔️ Competitive Analysis** - Tier information and strategies
4. **📈 Statistics & Trends** - Detailed base stats visualization
5. **🎨 Type Analysis** - Type distribution and effectiveness
6. **🧬 Evolution & Forms** - Evolution chains and alternate forms
7. **🎮 By Game** - Filter by Pokemon games
8. **🎨 Sprite Gallery** - Browse all Pokemon sprites
9. **⚡ Type Calculator** - NEW! Type effectiveness calculator with heatmap
10. **👥 Team Builder** - NEW! Build and analyze 6-Pokemon teams
11. **🏆 Legacy Team Builder** - Classic team builder interface

8. **🎯 Type Effectiveness** - Interactive type matchup chart* **Responsive Layout:** Optimized for desktop and mobile viewing

9. **🎮 Mini-Game** - "Who's That Pokemon?" quiz

### 🏠 **5-Tab Navigation System**

---* **Gallery Tab:** Grid view displaying all 1,076 Pokemon with animated sprites

* **Search & Filter Tab:** Advanced multi-select filters for generation, type, and BST

## 🚀 Quick Start* **Statistics Tab:** Analytics dashboard with charts, rankings, and insights

* **Glossary Tab:** 100+ Pokemon terms with searchable definitions

### Installation* **Settings Tab:** Display options, data export, and about information



```bash### 🔍 **Advanced Filtering System**

# Clone the repository* **Generation Filters:** Filter by 9 generations (Kanto through Paldea)

git clone https://github.com/caalivanera/pokemon.git* **Type Filters:** 18 Pokemon types with color-coded badges

cd pokedex-dashboard* **BST Range Slider:** Filter by Base Stat Total (0-1000)

* **Text Search:** Quick search across all Pokemon names

# Install dependencies* **Real-time Updates:** Instant filter application with session state

pip install -r requirements.txt

### � **Comprehensive Pokemon Details**

# Run the dashboard* **Complete Stats:** All 6 base stats (HP, Attack, Defense, Sp. Attack, Sp. Defense, Speed)

streamlit run enhanced_dashboard.py* **High-Quality Sprites:** 475x475px official artwork from PokeAPI

```* **Type Effectiveness:** Visual type badges with proper color coding

* **Detailed Information:** Abilities, breeding info, descriptions, and percentiles

### Access* **Multiple Data Sources:** Integration of 4+ Pokemon datasets

Open your browser and navigate to `http://localhost:8501`

### 🎬 **Animation Features**

---* **Floating Sprites:** Continuous 3s float animation on all Pokemon sprites

* **Hover Bounce:** Dynamic bounce effect when hovering over cards

## 📊 Data Coverage* **Smooth Transitions:** Optimized timing (0.15s-0.3s) for seamless UX

* **Card Effects:** Scale, shadow, and border animations on interaction

- **Pokemon**: 1,025 (Gen I-IX)* **Sticky Header:** Animated slideDown header with backdrop blur

- **Games**: 38 Pokemon games

- **Latest Update**: Pokemon Legends: Z-A (457 Pokemon, Kalos Pokedex)## �️ **Data Sources**

- **Data Sources**: Bulbapedia, Serebii, Smogon University

This enhanced dashboard integrates multiple high-quality Pokemon datasets:

---

### **Primary Data Sources:**

## 🎯 Latest Updates (v4.0.0)- **`pokedex.csv`** - Comprehensive Pokemon statistics, abilities, competitive analysis, and detailed game mechanics

- **`pokemon_glossary.csv`** - 100+ Pokemon terms and definitions for educational reference

- ✅ Enhanced Evolution & Forms tab with case-insensitive search- **`pokedex_otherVer.csv`** - Alternative Pokemon descriptions and flavor text

- ✅ Fixed Pokemon Legends: Z-A to official Kalos Pokedex (457 Pokemon)- **`poke_corpus.csv`** - Detailed Pokemon lore, descriptions, and extensive background information

- ✅ Improved alternate forms display (Mega, Regional, Gigantamax)

- ✅ Added evolution chain visualization### **Enhanced Data Integration:**

- ✅ Workspace cleanup - removed 19 redundant filesThe application intelligently combines these sources to provide:

- ✅ Code quality improvements and validation- **Complete stat analysis** with competitive insights

- ✅ Synchronized deployment files- **Multiple description sources** for comprehensive Pokemon information  

- **Educational glossary** integration for learning Pokemon mechanics

---- **Rich metadata** including abilities, breeding info, and experience systems



## 🛠️ Development## 🛠️ Tech Stack



### File Structure* **Language:** Python 3.8+

```* **Frontend Framework:** [Streamlit](https://streamlit.io/)

pokedex-dashboard/* **Data Processing:** [pandas](https://pandas.pydata.org/) + [numpy](https://numpy.org/)

├── data/                      # Pokemon databases* **HTTP Requests:** [requests](https://requests.readthedocs.io/en/latest/) (for sprite URLs)

├── assets/sprites/            # Sprite cache* **Progress Indicators:** [tqdm](https://github.com/tqdm/tqdm)

├── src/core/app.py            # Streamlit Cloud entry point* **Data Sources:** Multiple CSV datasets (see Data Sources section)

├── enhanced_dashboard.py      # Main application

├── requirements.txt           # Dependencies## � Installation

└── .streamlit/config.toml     # Configuration

```### **Prerequisites:**

* Python 3.8+

### Testing* `git` (for cloning)

```bash* Access to the Pokemon CSV data files (included in project)

# Validate data integrity

python check_version.py### **Installation Steps:**



# Run comprehensive audit1.  **Clone the Repository:**

python comprehensive_audit.py    ```bash

    git clone https://github.com/caalivanera/pokemon.git

# Test locally    cd pokemon/pokedex-dashboard

streamlit run enhanced_dashboard.py    ```

```

2.  **Create and Activate a Virtual Environment (Recommended):**

---    ```bash

    # For Mac/Linux

## 📝 Documentation    python3 -m venv venv

    source venv/bin/activate

- **Complete Guide**: See full documentation in repo    

- **CHANGELOG**: Version history and updates    # For Windows

- **SECURITY**: Security policy and guidelines    python -m venv venv

    .\venv\Scripts\activate

---    ```



## 🤝 Contributing3.  **Install Dependencies:**

    ```bash

Contributions welcome! Please:    pip install -r requirements.txt

1. Fork the repository    ```

2. Create a feature branch

3. Test changes locally## 🚀 Usage

4. Submit a Pull Request

### **Running Locally:**

---

1. **Start the Streamlit App:**

## 📄 License    ```bash

    streamlit run src/core/app.py

MIT License - See [LICENSE](LICENSE) for details    ```

    Your browser will automatically open at `http://localhost:8501`

---

2. **Explore the Dashboard:**

## 🙏 Acknowledgments    - Use the sidebar filters to select Pokemon by type, stats, or physical attributes

    - Click on any Pokemon to see detailed information

- The Pokemon Company - Pokemon data and sprites    - Export filtered data as CSV for further analysis

- Bulbapedia - Comprehensive Pokemon database    - Search the glossary for Pokemon terminology

- Serebii.net - Game data and Pokedex information

- Smogon University - Competitive data### **Running with Docker:**

- Streamlit - Dashboard framework

1. **Build and run using Docker Compose:**

---    ```bash

    cd config/docker

<div align="center">    docker-compose up -d

    ```

**Made with ❤️ for Pokemon Trainers Worldwide**

2. **Access the dashboard at:** `http://localhost:8501`

*Gotta Catch 'Em All!*

### **Key Features to Try:**

[Live Demo](https://1pokemon.streamlit.app/) • [Report Bug](https://github.com/caalivanera/pokemon/issues) • [Request Feature](https://github.com/caalivanera/pokemon/issues)

- **Multi-Type Filtering:** Select multiple types to see Pokemon matching any selected type

</div>- **Stat Filtering:** Use sliders to find Pokemon within specific stat ranges

- **Glossary Search:** Look up Pokemon terms and mechanics
- **Data Export:** Download filtered datasets for your own analysis

## ☁️ Deployment

This application is ready to be deployed directly to [Streamlit Community Cloud](https://streamlit.io/cloud).

1.  Push this entire project (all files) to your GitHub repository.
2.  Sign up for Streamlit Community Cloud (it's free) and link your GitHub account.
3.  Click "New app" and select your repository, the `main` branch, and the `app.py` file.
4.  Click "Deploy!"

## � **Advanced Data Engineering Highlights**

This enhanced project demonstrates sophisticated data engineering and analysis capabilities:

### **Multi-Source Data Integration**
* **Complex ETL Pipeline:** Intelligently merges 4 different CSV data sources with different schemas
* **Data Quality Management:** Handles missing values, data type conversions, and schema mismatches
* **Automated Data Processing:** Seamlessly combines competitive data, lore, and statistical information
* **Performance Optimization:** Efficient data loading with Streamlit caching for sub-second response times

### **Advanced Analytics & Visualization**  
* **Statistical Analysis:** Percentile rankings, distribution analysis, and comparative metrics
* **Interactive Filtering:** Real-time multi-dimensional filtering with complex boolean logic
* **Dynamic Visualizations:** Professional charts that update instantly based on filter selections
* **Export Capabilities:** Generate filtered datasets for further analysis

### **Production-Ready Features**
* **Error Handling:** Comprehensive error management for missing data and edge cases
* **User Experience:** Intuitive interface with contextual help and educational features
* **Scalable Architecture:** Modular design supporting easy dataset expansion
* **Documentation:** Extensive inline documentation and user guides

## 🎯 **Enhanced Portfolio Value** 

This project showcases advanced skills in:

### **Data Engineering Excellence**
* **Multi-Source Integration:** Combining disparate datasets with different formats and schemas
* **ETL Pipeline Development:** Sophisticated data transformation and loading processes  
* **Data Quality Assurance:** Robust validation, cleaning, and integrity checks
* **Performance Engineering:** Optimized data processing with intelligent caching strategies

### **Advanced Analytics Capabilities**
* **Statistical Analysis:** Complex calculations including percentile rankings and distributions
* **Interactive Visualization:** Professional-grade charts and real-time data exploration
* **Business Intelligence:** Comprehensive filtering and data discovery features
* **Export & Reporting:** Data export capabilities for stakeholder consumption

### **Full-Stack Development Skills**
* **Frontend Development:** Professional UI/UX with Streamlit and modern design principles
* **Backend Architecture:** Modular Python design with proper separation of concerns
* **Documentation & Communication:** Comprehensive documentation for technical and non-technical audiences
* **Production Deployment:** Ready for cloud deployment with proper configuration management

### **Technical Leadership Qualities**
* **Code Organization:** Clean, maintainable code structure following best practices
* **User-Centric Design:** Features designed around actual user needs and workflows
* **Educational Value:** Built-in glossary and help features demonstrating knowledge sharing
* **Innovation:** Creative use of multiple data sources to provide unique insights

---

**Built by Charles Alivanera** | [GitHub](https://github.com/caalivanera) | [Email](mailto:caalivanera@gmail.com)