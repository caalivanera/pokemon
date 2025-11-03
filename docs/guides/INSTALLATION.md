# 🚀 Quick Start Installation Guide

Get the Pokemon Dashboard up and running in minutes!

---

## 📋 Prerequisites

- **Python:** 3.11 or higher
- **Git:** For version control
- **Docker:** (Optional) For containerized deployment
- **PostgreSQL:** (Optional) For production database

---

## 🎯 Installation Methods

Choose your preferred installation method:

### Method 1: Local Development (Recommended for First Time)
### Method 2: Docker Compose (Recommended for Production)
### Method 3: Manual Setup (Advanced)

---

## 🔧 Method 1: Local Development

### Step 1: Clone Repository

```powershell
# Navigate to your workspace
cd C:\Users\user\Desktop\pokemon

# If not already in pokedex-dashboard folder
cd pokedex-dashboard
```

### Step 2: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (you should see (venv) in prompt)
```

### Step 3: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This will install 37 packages including:
# - streamlit (dashboard framework)
# - pandas, numpy (data processing)
# - sqlalchemy (database ORM)
# - pytest (testing)
# - and more...
```

**Expected Installation Time:** 2-5 minutes

### Step 4: Set Up Environment Variables

```powershell
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# For development, you can use the default SQLite database
```

**Minimal .env for development:**
```env
DATABASE_URL=sqlite:///pokemon_enterprise.db
DEBUG=true
```

### Step 5: Initialize Database

```powershell
# Create database schema
python database/connection.py

# Load data from CSV and YAML sources
python database/data_loader.py
```

**Expected Output:**
```
🔧 Testing database connection...
✅ Database tables created successfully!
✅ Database is ready!

📂 Loading source data...
✅ Loaded 800+ Pokemon from CSV
✅ Loaded YAML data: 11 files
🔄 Populating Pokemon table...
✅ Populated 800+ Pokemon records
✅ Populated 900+ Move records
...
✅ Data load completed successfully!
```

### Step 6: Run Dashboard

```powershell
# Start Streamlit dashboard
streamlit run app.py

# Dashboard will open at http://localhost:8501
```

**Success Indicators:**
- Browser opens automatically
- Dashboard loads without errors
- You can see Pokemon data

---

## 🐳 Method 2: Docker Compose (Production-Ready)

### Step 1: Prerequisites

```powershell
# Verify Docker is installed
docker --version
docker-compose --version

# Expected output:
# Docker version 20.10.x
# Docker Compose version 2.20.x
```

**Don't have Docker?**
```powershell
# Install via Winget
winget install Docker.DockerDesktop

# Or download from: https://www.docker.com/products/docker-desktop/
```

### Step 2: Configure Environment

```powershell
# Copy environment template
cp .env.example .env

# Edit .env with secure passwords
# IMPORTANT: Change default passwords!
```

**Production .env example:**
```env
# Database
POSTGRES_DB=pokemon_db
POSTGRES_USER=pokemon_user
POSTGRES_PASSWORD=your_secure_password_here_change_me
POSTGRES_PORT=5432

# Redis
REDIS_PASSWORD=your_redis_password_here_change_me

# Application
APP_PORT=8501
DEBUG=false
```

**Generate secure passwords:**
```powershell
python -c "import secrets; print('Password:', secrets.token_urlsafe(32))"
```

### Step 3: Start All Services

```powershell
# Build and start all containers
docker-compose up -d

# Check status
docker-compose ps

# Expected output:
# pokemon-postgres   running   5432/tcp
# pokemon-redis      running   6379/tcp
# pokemon-dashboard  running   8501/tcp
# pokemon-adminer    running   8080/tcp
```

### Step 4: Verify Deployment

```powershell
# Check logs
docker-compose logs app

# Access services:
# Dashboard: http://localhost:8501
# Adminer (DB GUI): http://localhost:8080
# Database: localhost:5432
```

### Step 5: Management Commands

```powershell
# View logs
docker-compose logs -f app

# Stop services
docker-compose stop

# Start services
docker-compose start

# Restart services
docker-compose restart

# Remove everything (including data)
docker-compose down -v
```

---

## 🔨 Method 3: Manual Setup (Advanced)

For custom configurations or specific requirements.

### Step 1: Install PostgreSQL

```powershell
# Download PostgreSQL 15 from:
# https://www.postgresql.org/download/windows/

# Or via Chocolatey:
choco install postgresql15

# Create database
psql -U postgres
CREATE DATABASE pokemon_db;
CREATE USER pokemon_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE pokemon_db TO pokemon_user;
\q
```

### Step 2: Install Redis (Optional)

```powershell
# Download Redis for Windows:
# https://github.com/microsoftarchive/redis/releases

# Or use Docker:
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

### Step 3: Configure Connection

Update `.env`:
```env
DATABASE_URL=postgresql://pokemon_user:your_password@localhost:5432/pokemon_db
REDIS_URL=redis://localhost:6379/0
```

### Step 4: Follow Method 1 Steps 2-6

---

## ✅ Verification Checklist

After installation, verify everything works:

### Database Check
```powershell
python -c "from database.connection import check_database_health; print('✅ Database OK' if check_database_health() else '❌ Database Failed')"
```

### Data Check
```powershell
python -c "from utils.data_extractor import fetch_all_pokemon; df = fetch_all_pokemon(); print(f'✅ Loaded {len(df)} Pokemon')"
```

### YAML Check
```powershell
python -c "from utils.yaml_loader import PokemonDataLoader; loader = PokemonDataLoader(); data = loader.load_all_yaml_data(); print(f'✅ Loaded {len(data)} YAML files')"
```

### App Check
```powershell
streamlit run app.py
# Dashboard should open in browser
```

---

## 🧪 Running Tests

```powershell
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

---

## 🔧 Troubleshooting

### Problem: Module not found

```powershell
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: Database connection failed

```powershell
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Problem: Port already in use

```powershell
# Find process using port 8501
netstat -ano | findstr :8501

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in .env
# APP_PORT=8502
```

### Problem: Docker permission denied

```powershell
# Run PowerShell as Administrator
# Or add your user to docker-users group
```

### Problem: Data not loading

```powershell
# Re-run data loader
python database/data_loader.py

# Check data files exist
dir data
dir pokemondbgit
```

---

## 📊 Post-Installation

### Explore Features

1. **Dashboard:** http://localhost:8501
   - Filter Pokemon by type, generation
   - View detailed stats
   - Search by name

2. **Database GUI:** http://localhost:8080 (Docker only)
   - Server: postgres
   - Username: pokemon_user
   - Password: (from .env)
   - Database: pokemon_db

3. **Redis:** localhost:6379
   - For caching (future feature)

### Next Steps

1. **Read Documentation**
   - `README.md` - Project overview
   - `GITHUB_LAUNCH_GUIDE.md` - Deployment guide
   - `TECH_STACK.md` - Technology details

2. **Customize Dashboard**
   - Edit `app.py`
   - Add new visualizations
   - Implement ML models

3. **Deploy to Production**
   - Follow `GITHUB_LAUNCH_GUIDE.md`
   - Choose deployment platform
   - Configure CI/CD

---

## 🚀 Quick Commands Reference

```powershell
# Development
venv\Scripts\activate              # Activate environment
pip install -r requirements.txt    # Install dependencies
python database/data_loader.py     # Load data
streamlit run app.py              # Run dashboard

# Docker
docker-compose up -d              # Start all services
docker-compose ps                 # Check status
docker-compose logs -f app        # View logs
docker-compose down               # Stop all services

# Testing
pytest tests/ -v                  # Run tests
flake8 . --max-line-length=79    # Lint code
black . --line-length=79         # Format code

# Database
python database/connection.py     # Test connection
python database/data_loader.py    # Reload data
```

---

## 📞 Getting Help

- **Documentation:** See README.md and guide files
- **Issues:** Create GitHub issue
- **Discussions:** GitHub Discussions
- **Email:** support@pokemon-dashboard.com

---

## 🎉 Success!

If you can:
- ✅ Access dashboard at http://localhost:8501
- ✅ See Pokemon data
- ✅ Filter and search works
- ✅ No console errors

**You're ready to go!** 🚀

**Next:** Explore the dashboard, read documentation, and start customizing!

---

**Installation Time:** 10-15 minutes  
**Difficulty:** Easy (Method 1), Medium (Method 2)  
**Support:** Community support available  

**Last Updated:** 2024  
**Version:** 1.0.0
