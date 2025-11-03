# 📚 Master Documentation - Pokemon Dashboard Project

**Last Updated:** November 3, 2025  
**Version:** 3.0  
**Project Status:** Production Ready

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Data Specifications](#data-specifications)
3. [File Structure](#file-structure)
4. [Setup Instructions](#setup-instructions)
5. [Column Mappings](#column-mappings)
6. [Known Issues & Fixes](#known-issues--fixes)
7. [Deployment](#deployment)

---

## 🎯 Project Overview

### Description
This is a comprehensive **National Pokédex Dashboard** featuring complete data for **1,045 Pokémon** (includes regional forms and variants) from **Generations 1 through 9**. The application is built with **Streamlit** and provides advanced analytics, filtering, and visualization capabilities.

### Key Features
- ✅ Complete National Dex coverage (Gen 1-9)
- ✅ 94 data columns including base stats, abilities, types, and derived metrics
- ✅ Advanced filtering system (types, stats, physical attributes)
- ✅ Interactive visualizations with Plotly
- ✅ Pokemon glossary with 100+ terms
- ✅ YAML data integration for moves, abilities, items, locations
- ✅ Comprehensive documentation

### Technologies
- **Python 3.13**
- **Streamlit 1.29+**
- **Pandas 2.0+**
- **Plotly Express**
- **PyYAML 6.0+**

---

## 📊 Data Specifications

### National Dex Statistics

| Metric | Value |
|--------|-------|
| **Total Pokemon** | 1,045 |
| **Unique Base Forms** | 1,025 (Gen 1-9 official count) |
| **Alternate Forms/Variants** | 20 |
| **Total Columns** | 94 |
| **Data Sources** | 4 CSV files + 11 YAML files |
| **File Size** | 21.78 MB (national_dex.csv) |

### Pokemon Distribution by Generation

```
Generation 1: 192 Pokemon (includes forms)
Generation 2: 107 Pokemon
Generation 3: 165 Pokemon
Generation 4: 121 Pokemon
Generation 5: 171 Pokemon
Generation 6:  85 Pokemon
Generation 7:  99 Pokemon
Generation 8: 105 Pokemon
Generation 9:   0 Pokemon (forms included in other gens)
```

### Data Source Files

#### CSV Files (4 total)
1. **pokedex.csv** - 1,045 rows, main comprehensive dataset
2. **poke_corpus.csv** - 1,045 rows, Pokemon descriptions
3. **pokedex_otherVer.csv** - 1,025 rows, alternate data source
4. **pokemon_glossary.csv** - 112 rows, Pokemon terminology

#### YAML Files (11 total)
Located in: `pokedex-dashboard/data/`

1. **pokemon.yaml** - 1,025 base Pokemon definitions
2. **moves.yaml** - Complete move database
3. **abilities.yaml** - All Pokemon abilities
4. **types.yaml** - Type definitions
5. **type-chart.yaml** - Type effectiveness matrix
6. **items.yaml** - Item database
7. **locations.yaml** - Location data
8. **egg-groups.yaml** - Breeding groups
9. **games.yaml** - Game version data
10. **releases.yaml** - Release information
11. **pokemon-forms.yaml** - Regional/alternate forms (20 entries)

---

## 📁 File Structure

```
pokemon/
├── pokedex-dashboard/              # Main application directory
│   ├── .git/                       # Git repository
│   ├── .gitignore                  # Git ignore rules
│   ├── .streamlit/                 # Streamlit configuration
│   │   └── config.toml
│   ├── data/                       # All data files
│   │   ├── national_dex.csv        # 🔴 MAIN DATASET (1,045 Pokemon, 94 cols)
│   │   ├── pokedex.csv             # Source file 1
│   │   ├── poke_corpus.csv         # Source file 2
│   │   ├── pokedex_otherVer.csv    # Source file 3 (1,025 Pokemon)
│   │   ├── pokemon_glossary.csv    # Glossary terms
│   │   ├── national_dex_dictionary.json  # Data dictionary
│   │   ├── pokemon.yaml            # 🔴 CANONICAL SOURCE (1,025 base Pokemon)
│   │   ├── moves.yaml
│   │   ├── abilities.yaml
│   │   ├── types.yaml
│   │   ├── type-chart.yaml
│   │   ├── items.yaml
│   │   ├── locations.yaml
│   │   ├── egg-groups.yaml
│   │   ├── games.yaml
│   │   ├── releases.yaml
│   │   └── pokemon-forms.yaml      # 20 alternate forms
│   ├── src/
│   │   ├── core/
│   │   │   ├── app.py              # 🔴 MAIN APPLICATION
│   │   │   └── enhanced_dashboard.py  # Advanced analytics (7 pages)
│   │   ├── data_loaders/
│   │   │   ├── data_extractor.py   # Legacy CSV loader
│   │   │   ├── national_dex_builder.py  # Dex builder class
│   │   │   └── yaml_loader.py      # YAML data loader
│   │   └── database/
│   │       └── db_manager.py       # Database utilities
│   ├── config/                     # Configuration files
│   ├── docs/                       # Additional documentation
│   ├── scripts/                    # Utility scripts
│   ├── tests/                      # Test files
│   ├── README.md                   # Project README
│   ├── requirements.txt            # Python dependencies
│   ├── AUDIT_REPORT.md
│   ├── CHANGELOG.md
│   ├── ENHANCEMENT_UPDATE_V2.md
│   ├── PROJECT_STRUCTURE.md
│   ├── SECURITY.md
│   └── VALIDATION_COMPLETE.md
│
├── POKEMON_DASHBOARD_README.md     # 🔴 ROOT DOCUMENTATION (copy of README)
├── ENHANCEMENT_UPDATE.md           # 🔴 ROOT DOCUMENTATION (enhancement details)
└── MASTER_DOCUMENTATION.md         # 🔴 THIS FILE (comprehensive guide)
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9 or higher (tested on Python 3.13)
- Git
- 500 MB free disk space (for data files)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/caalivanera/pokemon.git
cd pokemon/pokedex-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify data files exist
ls data/national_dex.csv  # Should show file size ~22 MB

# 4. Run the application
streamlit run src/core/app.py

# Alternative: Run enhanced dashboard
streamlit run src/core/enhanced_dashboard.py
```

### Required Python Packages

```txt
streamlit>=1.29.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
pyyaml>=6.0
sqlalchemy>=2.0.0
```

---

## 🗂️ Column Mappings

### National Dex CSV Column Reference

The `national_dex.csv` has **94 columns**. Here's the complete mapping:

#### Core Identity Columns (1-9)
```
1.  pokedex_number     → id (alias added in code)
2.  name               → Pokemon name (e.g., "Bulbasaur")
3.  japanese_name      → Japanese name
4.  generation         → Generation number (1-8)
5.  status             → Status (Normal/Legendary/Mythical)
6.  species            → Species description
7.  type_number        → Number of types (1 or 2)
8.  type_1             → Primary type → primary_type (alias)
9.  type_2             → Secondary type → secondary_type (alias)
```

#### Physical Attributes (10-12)
```
10. height_m           → Height in meters
11. weight_kg          → Weight in kilograms
12. abilities_number   → Number of abilities
```

#### Base Stats (13-19)
```
13. total_points       → Base Stat Total (BST)
14. hp                 → Hit Points
15. attack             → Attack stat
16. defense            → Defense stat
17. sp_attack          → 🔴 Special Attack (NOT special_attack)
18. sp_defense         → 🔴 Special Defense (NOT special_defense)
19. speed              → Speed stat
```

#### Game Mechanics (20-28)
```
20. catch_rate         → Catch rate percentage
21. base_friendship    → Base friendship value
22. base_experience    → Base experience yield
23. growth_rate        → EXP growth curve
24. egg_type_number    → Number of egg groups
25. egg_type_1         → Primary egg group
26. egg_type_2         → Secondary egg group
27. percentage_male    → Gender ratio (% male)
28. egg_cycles         → Breeding cycles
```

#### Type Effectiveness (29-46)
```
29-46. against_[type]  → Damage multipliers vs each type
       (normal, fire, water, electric, grass, ice, fight, poison,
        ground, flying, psychic, bug, rock, ghost, dragon, dark,
        steel, fairy)
```

#### Descriptions & Details (47-55)
```
47. smogon_description → Competitive analysis
48. bulba_description  → Bulbapedia description
49. moves              → Learnable moves list
50. ability_1          → First ability name
51. ability_2          → Second ability name
52. ability_hidden     → Hidden ability name
53. ability_1_description
54. ability_2_description
55. ability_hidden_description
56. corpus_description → General description
```

#### Alternate Data (57-69)
```
57. alt_id             → ID from alternate source
58. alt_name           → Name from alternate source
59-67. alt_[stat]      → Stats from alternate source
68. evolution_chain    → Evolution family
69. alternate_info     → Additional info
```

#### Derived Statistics (70-94)
```
70-76. [stat]_percentile  → Percentile rankings
77. physical_special_ratio → ATK/SP.ATK ratio
78. offensive_rating      → Average offensive stat
79. defensive_rating      → Average defensive stat
80. bmi                   → Body Mass Index
81. speed_tier            → Speed classification
82. bst_tier              → BST tier classification
83. resistances_count     → Number of resistances
84. weaknesses_count      → Number of weaknesses
85. immunities_count      → Number of immunities
86. defensive_score       → Overall defensive rating
87. is_legendary          → Boolean flag
88. is_starter            → Boolean flag
89. is_pseudo_legendary   → Boolean flag
90. type_count            → 1 or 2
91. is_dual_type          → Boolean flag
92. full_type             → Combined type string
93. size_category         → Size classification
94. weight_category       → Weight classification
```

---

## ⚠️ Known Issues & Fixes

### Issue 1: KeyError 'special_attack'
**Problem:** National dex CSV uses `sp_attack` and `sp_defense`, not `special_attack`/`special_defense`

**Fix Applied:** 
- All references updated in `src/core/app.py` (lines 208-502)
- Changed column names from `special_attack` → `sp_attack`
- Changed column names from `special_defense` → `sp_defense`

**Status:** ✅ FIXED (commit a8e19cf)

### Issue 2: KeyError 'primary_type'
**Problem:** CSV uses `type_1` and `type_2`, not `primary_type`/`secondary_type`

**Fix Applied:**
- Added column aliases in `load_national_dex()` function
- Creates `primary_type` → `type_1` alias
- Creates `secondary_type` → `type_2` alias
- Creates `id` → `pokedex_number` alias

**Status:** ✅ FIXED (commit a8e19cf)

### Issue 3: CSV Path Not Found on Streamlit Cloud
**Problem:** Relative paths fail on Streamlit Cloud deployment

**Fix Applied:**
- Using absolute paths with `Path(parent_dir) / 'data'`
- Verified with `NATIONAL_DEX_FILE.exists()` check

**Status:** ✅ FIXED (previous commit)

### Issue 4: Pokemon Count Discrepancy
**Observation:** 
- pokemon.yaml: 1,025 Pokemon (official Gen 1-9 base forms)
- national_dex.csv: 1,045 Pokemon (includes 20 regional/alternate forms)

**Resolution:** This is expected behavior. The extra 20 entries are:
- Regional forms (Alolan, Galarian, Hisuian variants)
- Mega evolutions
- Special forms (e.g., different Rotom forms)

**Status:** ✅ DOCUMENTED (working as intended)

---

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Repository Setup**
   - Repository: `https://github.com/caalivanera/pokemon`
   - Branch: `main`
   - Main file: `pokedex-dashboard/src/core/app.py`

2. **Configuration Files**
   - `.streamlit/config.toml` - Streamlit settings
   - `requirements.txt` - Python dependencies
   - `.gitignore` - Excludes unnecessary files

3. **Environment Variables**
   None required (all data is local CSV/YAML files)

4. **Deployment Steps**
   ```bash
   # Push to GitHub
   git add -A
   git commit -m "Deploy: Ready for production"
   git push origin main
   
   # On Streamlit Cloud Dashboard:
   # 1. Connect GitHub repo
   # 2. Select branch: main
   # 3. Set main file: pokedex-dashboard/src/core/app.py
   # 4. Deploy
   ```

5. **Post-Deployment Verification**
   - Check that national_dex.csv loads (1,045 Pokemon)
   - Verify YAML files are accessible (11 files)
   - Test filters and visualizations
   - Confirm no KeyErrors in logs

### Local Testing
```bash
# Test standard app
streamlit run src/core/app.py

# Test enhanced dashboard
streamlit run src/core/enhanced_dashboard.py

# Check data integrity
python -c "import pandas as pd; df = pd.read_csv('data/national_dex.csv'); print(f'{len(df)} Pokemon, {len(df.columns)} columns')"
```

---

## 📈 Recent Updates

### Version 3.0 (November 3, 2025)
- ✅ Fixed `special_attack`/`special_defense` KeyError
- ✅ Added column aliases for `primary_type`/`secondary_type`
- ✅ Moved pokemondbgit YAML files to data folder
- ✅ Updated README to remove Gen 1 limitations
- ✅ Created comprehensive master documentation
- ✅ Committed and pushed all fixes to GitHub

### Version 2.0 (Previous)
- ✅ Created national_dex.csv with 1,045 Pokemon
- ✅ Implemented 94-column dataset with derived stats
- ✅ Built enhanced_dashboard.py with 7 pages
- ✅ Added data dictionary JSON

---

## 🔧 Maintenance Notes

### Data Updates
To update the National Dex with new generations:

1. Update source CSVs in `data/` folder
2. Run the National Dex builder:
   ```python
   from src.data_loaders.national_dex_builder import NationalDexBuilder
   builder = NationalDexBuilder()
   builder.build_national_dex()
   ```
3. Verify new Pokemon count
4. Update documentation

### Code Modifications
- Main app: `src/core/app.py`
- Enhanced dashboard: `src/core/enhanced_dashboard.py`
- Data loaders: `src/data_loaders/`

### Testing
Run validation script:
```bash
python scripts/comprehensive_validation.py
```

---

## 📞 Support & Resources

### Documentation Files
- **README.md** - Project overview and quick start
- **ENHANCEMENT_UPDATE_V2.md** - Detailed enhancement log
- **PROJECT_STRUCTURE.md** - Directory structure
- **SECURITY.md** - Security audit report
- **AUDIT_REPORT.md** - Validation results

### External Resources
- PokeAPI: https://pokeapi.co/
- Bulbapedia: https://bulbapedia.bulbagarden.net/
- Serebii: https://www.serebii.net/
- Smogon: https://www.smogon.com/

---

## 🎓 Data Dictionary

For complete column definitions and data types, see:
`pokedex-dashboard/data/national_dex_dictionary.json`

Key sections:
- **Core Columns**: Basic Pokemon info
- **Stats Columns**: Base stat values
- **Type Columns**: Type and type effectiveness
- **Derived Columns**: Calculated metrics
- **Metadata Columns**: Source and processing info

---

## ✅ Verification Checklist

Before deployment, verify:

- [ ] national_dex.csv exists and is 21+ MB
- [ ] 11 YAML files present in data folder
- [ ] app.py loads without KeyErrors
- [ ] All 1,045 Pokemon render correctly
- [ ] Filters work (type, stats, physical)
- [ ] Visualizations display properly
- [ ] Git repository is clean (`git status`)
- [ ] Latest changes pushed to GitHub
- [ ] Documentation is updated

---

**End of Master Documentation**

*For questions or issues, please refer to the GitHub repository or contact the maintainer.*
