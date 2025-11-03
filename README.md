# ⚡ Enhanced Interactive Pokédex Dashboard

This is a comprehensive, data-rich interactive web application for exploring the original 151 Pokémon with enhanced information from multiple authoritative sources. The dashboard combines data from comprehensive CSV datasets including competitive analysis, detailed descriptions, and a Pokemon glossary.

The application loads enhanced Pokemon data from multiple local CSV sources and provides deep analytical capabilities for Pokemon research and exploration.

## 📖 What is a Pokédex?

A **Pokédex** is a digital electronic encyclopedia that acts as a guide for Pokémon trainers, recording data on Pokémon species they encounter. In the games, it tracks the player's progress in catching or observing Pokémon, with detailed entries unlocked as a trainer catches or obtains a species. It's an essential tool for any trainer, and in some versions of the games and the anime, it functions as a reference tool to learn about Pokémon types, sizes, and locations.

This dashboard serves as your **digital Pokédex companion**, providing comprehensive data analysis and exploration tools for all 151 Generation 1 Pokémon.

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

## ✨ Enhanced Features

### 🔍 **Advanced Filtering System**
* **Multi-Type Filtering:** Filter Pokémon by one or more types with logical OR operations
* **Comprehensive Stat Filtering:** Individual sliders for all six base stats plus BST (Base Stat Total)
* **Physical Attribute Filters:** Filter by height and weight ranges
* **Real-time Updates:** All filters update the dataset and visualizations in real-time

### 📊 **Enhanced Pokemon Details**
* **Multi-Source Information:** Combines data from 4+ different Pokemon datasets
* **Comprehensive Stats Analysis:** Base stats with percentile rankings among all Pokemon
* **Detailed Abilities:** Full ability descriptions and effects
* **Breeding Information:** Egg groups, gender ratios, and breeding mechanics
* **Multiple Description Sources:** Game descriptions, competitive analysis, and detailed lore

### 📚 **Interactive Pokemon Glossary**
* **Searchable Terms:** 100+ Pokemon terms with detailed definitions
* **Contextual Help:** Integrated glossary accessible from the sidebar
* **Educational Value:** Perfect for learning Pokemon mechanics and terminology

### 📈 **Advanced Analytics**
* **Statistical Insights:** Dataset overview with key metrics
* **Percentile Rankings:** See how each Pokemon compares statistically
* **Export Functionality:** Download filtered datasets as CSV files
* **Enhanced Visualizations:** Professional charts and data displays

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

## 🚀 How to Run Locally

### **Prerequisites:**
* Python 3.8+
* `git` (for cloning)
* Access to the Pokemon CSV data files (included in project)

**Steps:**

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/caalivanera/pokedex-dashboard.git
    cd pokedex-dashboard
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

4.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    Your browser will automatically open, and the app will begin fetching data.

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