# 📁 Project Structure - Organized by Use Case

## Overview

The project has been reorganized with a **use-case-based directory structure** for better maintainability, scalability, and clarity. All files are now grouped by their purpose and functionality.

## 📂 Directory Structure

```
pokedex-dashboard/
│
├── 📱 src/                          # Source code organized by functionality
│   ├── __init__.py
│   │
│   ├── core/                        # Core application files
│   │   ├── __init__.py
│   │   └── app.py                   # Main Streamlit dashboard application
│   │
│   ├── data_loaders/                # Data loading and extraction modules
│   │   ├── __init__.py
│   │   ├── data_extractor.py        # CSV data extraction (4 CSV files)
│   │   └── yaml_loader.py           # YAML data loader (11 YAML files)
│   │
│   └── database/                    # Database layer
│       ├── __init__.py
│       ├── models.py                # SQLAlchemy ORM models (9 tables)
│       ├── connection.py            # Database connection manager
│       └── data_loader.py           # Populate database from sources
│
├── ⚙️  config/                       # All configuration files
│   ├── docker/                      # Docker-related configuration
│   │   ├── Dockerfile               # Multi-stage production build
│   │   ├── docker-compose.yml       # 4-service orchestration
│   │   └── .env.example             # Environment variable template
│   │
│   ├── github/                      # GitHub-specific configuration
│   │   └── workflows/
│   │       └── ci.yml               # CI/CD pipeline (6 jobs)
│   │
│   └── vscode/                      # VS Code workspace configuration
│       ├── extensions.json          # 38 recommended extensions
│       └── settings.json            # Workspace settings (linting, formatting)
│
├── 📚 docs/                         # Documentation organized by type
│   ├── guides/                      # User and setup guides
│   │   ├── GITHUB_LAUNCH_GUIDE.md   # Deployment step-by-step (500+ lines)
│   │   └── INSTALLATION.md          # Quick start guide (300+ lines)
│   │
│   └── technical/                   # Technical documentation
│       ├── TECH_STACK.md            # Technology details (400+ lines)
│       ├── IMPLEMENTATION_SUMMARY.md # Implementation report (300+ lines)
│       ├── OPEN_SOURCE_VERIFICATION.md # License verification (400+ lines)
│       └── PROJECT_COMPLETION_REPORT.md # Final status report
│
├── 🧪 tests/                        # Test files
│   ├── __init__.py
│   └── test_enhanced_dashboard.py   # Integration tests
│
├── 🔧 scripts/                      # Utility scripts
│   └── validate_project.py          # Comprehensive validation script
│
├── 📊 data/                         # Data files (CSV sources)
│   ├── pokedex.csv                  # Main Pokemon data (800+ entries)
│   ├── pokemon_glossary.csv         # Glossary terms (29 entries)
│   ├── poke_corpus.csv              # Additional Pokemon info
│   └── pokedex_otherVer.csv         # Alternative version data
│
├── 📦 pokemondbgit/                 # YAML data source (11 files)
│   ├── pokemon.yaml                 # Pokemon data (4101 lines)
│   ├── moves.yaml                   # Move data (7473 lines)
│   ├── abilities.yaml               # Ability data
│   ├── types.yaml                   # Type data
│   ├── type-chart.yaml              # Type effectiveness (73 lines)
│   ├── items.yaml                   # Item data
│   ├── locations.yaml               # Location data
│   ├── egg-groups.yaml              # Egg group data
│   ├── games.yaml                   # Game data
│   ├── releases.yaml                # Release data
│   └── pokemon-forms.yaml           # Pokemon form data
│
├── 📄 Root Files
│   ├── README.md                    # Project overview
│   ├── CHANGELOG.md                 # Version history
│   ├── PROJECT_STRUCTURE.md         # This file - structure documentation
│   ├── requirements.txt             # Python dependencies (37 packages)
│   └── .gitignore                   # Git ignore rules
│
└── 🗂️  Other
    └── logs/                        # Application logs (gitignored)
```

## 📋 File Organization by Use Case

### 1. **Application Code** (`src/`)
All Python source code organized by functionality:
- **Core** - Main application entry point
- **Data Loaders** - Data extraction and loading logic
- **Database** - Database models and connection management

### 2. **Configuration** (`config/`)
All configuration files grouped by tool/platform:
- **Docker** - Containerization configuration
- **GitHub** - CI/CD and GitHub-specific config
- **VS Code** - Editor and workspace settings

### 3. **Documentation** (`docs/`)
Documentation organized by audience:
- **Guides** - End-user and setup documentation
- **Technical** - Developer and implementation documentation

### 4. **Testing** (`tests/`)
All test files and test-related code

### 5. **Utilities** (`scripts/`)
Standalone utility scripts for maintenance and validation

### 6. **Data** (`data/` & `pokemondbgit/`)
All data source files:
- `data/` - CSV files
- `pokemondbgit/` - YAML files

## 🔄 Import Path Updates

### Old Structure → New Structure

| Old Path | New Path |
|----------|----------|
| `from utils.data_extractor import ...` | `from src.data_loaders.data_extractor import ...` |
| `from utils.yaml_loader import ...` | `from src.data_loaders.yaml_loader import ...` |
| `from database.models import ...` | `from src.database.models import ...` |
| `from database.connection import ...` | `from src.database.connection import ...` |
| `from database.data_loader import ...` | `from src.database.data_loader import ...` |
| `app.py` | `src/core/app.py` |

### Running the Application

#### Old Command:
```bash
streamlit run app.py
```

#### New Command:
```bash
streamlit run src/core/app.py
```

### Running Tests

#### Old Command:
```bash
python test_enhanced_dashboard.py
```

#### New Command:
```bash
python -m pytest tests/
# OR
python tests/test_enhanced_dashboard.py
```

### Running Validation

#### Old Command:
```bash
python validate_project.py
```

#### New Command:
```bash
python scripts/validate_project.py
```

## 🐳 Docker Updates

### docker-compose.yml
- **Build context**: Changed from `.` to `../..` (root directory)
- **Dockerfile path**: Changed from `Dockerfile` to `config/docker/Dockerfile`

### Dockerfile
- **CMD updated**: `streamlit run src/core/app.py` (was `app.py`)
- **Data loader**: `python src/database/data_loader.py` (was `database/data_loader.py`)

## 📦 Package Structure

The `src/` directory is now a proper Python package with `__init__.py` files:

```python
src/
├── __init__.py              # Makes src a package
├── core/
│   └── __init__.py          # Makes core a subpackage
├── data_loaders/
│   └── __init__.py          # Makes data_loaders a subpackage
└── database/
    └── __init__.py          # Makes database a subpackage
```

## 🎯 Benefits of New Structure

### 1. **Clarity**
- Purpose of each directory is immediately clear
- Related files are grouped together
- Easier to locate specific functionality

### 2. **Scalability**
- Easy to add new modules within existing structure
- Clear separation of concerns
- Follows enterprise best practices

### 3. **Maintainability**
- Configuration separated from code
- Documentation organized by audience
- Tests isolated from source code

### 4. **Professional**
- Follows Python packaging conventions
- Industry-standard directory layout
- Enterprise-grade organization

### 5. **Flexibility**
- Easy to convert to installable package
- Simple to add more data loaders or database models
- Clear extension points for new features

## 📖 Quick Reference

### Common Tasks

| Task | Command |
|------|---------|
| Start Dashboard | `streamlit run src/core/app.py` |
| Run Tests | `python -m pytest tests/` |
| Validate Project | `python scripts/validate_project.py` |
| Start Docker | `cd config/docker && docker-compose up` |
| Load Data to DB | `python src/database/data_loader.py` |
| View Docs | Open `docs/guides/INSTALLATION.md` |
| Check Tech Stack | Open `docs/technical/TECH_STACK.md` |

### File Locations

| What | Where |
|------|-------|
| Main App | `src/core/app.py` |
| CSV Loaders | `src/data_loaders/data_extractor.py` |
| YAML Loaders | `src/data_loaders/yaml_loader.py` |
| DB Models | `src/database/models.py` |
| Docker Files | `config/docker/` |
| CI/CD Config | `config/github/workflows/ci.yml` |
| VS Code Settings | `config/vscode/` |
| Installation Guide | `docs/guides/INSTALLATION.md` |
| Tech Docs | `docs/technical/TECH_STACK.md` |

## 🔍 Finding Things

### "Where is...?"

- **The Streamlit app?** → `src/core/app.py`
- **Database setup?** → `src/database/`
- **Data loading logic?** → `src/data_loaders/`
- **Docker config?** → `config/docker/`
- **CI/CD pipeline?** → `config/github/workflows/ci.yml`
- **Installation guide?** → `docs/guides/INSTALLATION.md`
- **Test files?** → `tests/`
- **Validation script?** → `scripts/validate_project.py`
- **CSV data?** → `data/`
- **YAML data?** → `pokemondbgit/`

## 📝 Migration Notes

All files have been moved and all import paths have been updated throughout the codebase:

✅ **Completed Updates:**
- `src/core/app.py` - Updated imports to use `src.data_loaders.*`
- `src/database/data_loader.py` - Updated imports to use `src.*` paths
- `tests/test_enhanced_dashboard.py` - Updated imports to use `src.*` paths
- `config/docker/Dockerfile` - Updated CMD paths
- `config/docker/docker-compose.yml` - Updated build context
- `scripts/validate_project.py` - Updated all file path checks

## 🎉 Summary

The project is now organized with a **professional, scalable, use-case-based structure** that:
- Groups related files together
- Separates concerns clearly
- Follows Python best practices
- Makes the codebase easier to navigate and maintain
- Enables future growth and feature additions

**Ready for production deployment!** 🚀
