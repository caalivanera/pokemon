# ⚡ Enhanced Interactive Pokédex Dashboard

A modern, interactive web application featuring all 1,076 Pokémon from Generations 1-9 with animated sprites, comprehensive stats, and advanced filtering. This dashboard combines data from multiple authoritative sources with a sleek dark theme featuring green accents.

The application provides a professional, responsive interface with animated Pokemon sprites, TBA placeholders for missing visuals, and deep analytical capabilities for Pokemon research and exploration.

## 📖 What is a Pokédex?

A **Pokédex** is a digital electronic encyclopedia that acts as a guide for Pokémon trainers, recording data on Pokémon species they encounter. In the games, it tracks the player's progress in catching or observing Pokémon, with detailed entries unlocked as a trainer catches or obtains a species. It's an essential tool for any trainer, and in some versions of the games and the anime, it functions as a reference tool to learn about Pokémon types, sizes, and locations.

This dashboard serves as your **digital Pokédex companion**, providing comprehensive data analysis and exploration tools for the complete National Pokédex spanning Generations 1 through 9.

## 📁 Project Structure

**This project has been reorganized with a use-case-based directory structure!**

See **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** for the complete directory layout and file organization.

**Quick Navigation:**
- Source Code: `src/` (core, data_loaders, database)
- Configuration: `config/` (docker, github, vscode)
- Documentation: `docs/` (guides, technical)
- Tests: `tests/`
- Scripts: `scripts/`
- Data: `data/` and `pokemondbgit/`

## ✨ Features

### 🎨 **Modern Dark Theme with Green Accents**
* **Professional Design:** Sleek dark theme (#141414) with vibrant green accents (#10B981)
* **Smooth Animations:** 0.15s-0.3s transitions for snappy, responsive interactions
* **Animated Sprites:** Floating Pokemon sprites with bounce effects on hover
* **TBA Placeholders:** Stylish "TBA" visual indicators for missing sprites
* **Responsive Layout:** Optimized for desktop and mobile viewing

### 🏠 **5-Tab Navigation System**
* **Gallery Tab:** Grid view displaying all 1,076 Pokemon with animated sprites
* **Search & Filter Tab:** Advanced multi-select filters for generation, type, and BST
* **Statistics Tab:** Analytics dashboard with charts, rankings, and insights
* **Glossary Tab:** 100+ Pokemon terms with searchable definitions
* **Settings Tab:** Display options, data export, and about information

### 🔍 **Advanced Filtering System**
* **Generation Filters:** Filter by 9 generations (Kanto through Paldea)
* **Type Filters:** 18 Pokemon types with color-coded badges
* **BST Range Slider:** Filter by Base Stat Total (0-1000)
* **Text Search:** Quick search across all Pokemon names
* **Real-time Updates:** Instant filter application with session state

### � **Comprehensive Pokemon Details**
* **Complete Stats:** All 6 base stats (HP, Attack, Defense, Sp. Attack, Sp. Defense, Speed)
* **High-Quality Sprites:** 475x475px official artwork from PokeAPI
* **Type Effectiveness:** Visual type badges with proper color coding
* **Detailed Information:** Abilities, breeding info, descriptions, and percentiles
* **Multiple Data Sources:** Integration of 4+ Pokemon datasets

### 🎬 **Animation Features**
* **Floating Sprites:** Continuous 3s float animation on all Pokemon sprites
* **Hover Bounce:** Dynamic bounce effect when hovering over cards
* **Smooth Transitions:** Optimized timing (0.15s-0.3s) for seamless UX
* **Card Effects:** Scale, shadow, and border animations on interaction
* **Sticky Header:** Animated slideDown header with backdrop blur

## �️ **Data Sources**

This enhanced dashboard integrates multiple high-quality Pokemon datasets:

### **Primary Data Sources:**
- **`pokedex.csv`** - Comprehensive Pokemon statistics, abilities, competitive analysis, and detailed game mechanics
- **`pokemon_glossary.csv`** - 100+ Pokemon terms and definitions for educational reference
- **`pokedex_otherVer.csv`** - Alternative Pokemon descriptions and flavor text
- **`poke_corpus.csv`** - Detailed Pokemon lore, descriptions, and extensive background information

### **Enhanced Data Integration:**
The application intelligently combines these sources to provide:
- **Complete stat analysis** with competitive insights
- **Multiple description sources** for comprehensive Pokemon information  
- **Educational glossary** integration for learning Pokemon mechanics
- **Rich metadata** including abilities, breeding info, and experience systems

## 🛠️ Tech Stack

* **Language:** Python 3.8+
* **Frontend Framework:** [Streamlit](https://streamlit.io/)
* **Data Processing:** [pandas](https://pandas.pydata.org/) + [numpy](https://numpy.org/)
* **HTTP Requests:** [requests](https://requests.readthedocs.io/en/latest/) (for sprite URLs)
* **Progress Indicators:** [tqdm](https://github.com/tqdm/tqdm)
* **Data Sources:** Multiple CSV datasets (see Data Sources section)

## � Installation

### **Prerequisites:**
* Python 3.8+
* `git` (for cloning)
* Access to the Pokemon CSV data files (included in project)

### **Installation Steps:**

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/caalivanera/pokemon.git
    cd pokemon/pokedex-dashboard
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

### **Running Locally:**

1. **Start the Streamlit App:**
    ```bash
    streamlit run src/core/app.py
    ```
    Your browser will automatically open at `http://localhost:8501`

2. **Explore the Dashboard:**
    - Use the sidebar filters to select Pokemon by type, stats, or physical attributes
    - Click on any Pokemon to see detailed information
    - Export filtered data as CSV for further analysis
    - Search the glossary for Pokemon terminology

### **Running with Docker:**

1. **Build and run using Docker Compose:**
    ```bash
    cd config/docker
    docker-compose up -d
    ```

2. **Access the dashboard at:** `http://localhost:8501`

### **Key Features to Try:**

- **Multi-Type Filtering:** Select multiple types to see Pokemon matching any selected type
- **Stat Filtering:** Use sliders to find Pokemon within specific stat ranges
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