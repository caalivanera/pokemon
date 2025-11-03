# 🚀 Quick Start Guide - v5.4.2 Utility System

## 🎯 What's New in v5.4.2

Pokemon Dashboard now includes a professional utility system with:
- 🛠️ **Admin Dashboard** (Tab 18) - System management interface
- 📝 **Error Logging** - Track and report all errors
- ✅ **Data Validation** - Ensure data integrity
- 💾 **Automated Backups** - Schedule and manage backups
- 📊 **Performance Monitoring** - Optimize operations

---

## ⚡ Quick Commands

### Run the Dashboard
```bash
cd pokedex-dashboard
streamlit run src/core/app.py
```

Then navigate to **Tab 18: 🛠️ Admin Utilities**

### Create a Backup
```bash
# Full backup (recommended)
python scripts/automated_backup.py

# Data only (faster)
python scripts/automated_backup.py --type data

# Keep only 10 most recent
python scripts/automated_backup.py --keep 10
```

### View Logs
```bash
# Error logs
cat logs/errors/errors_20241104.log

# Performance logs (JSON)
cat logs/performance/performance_20241104.json
```

---

## 🛠️ Admin Dashboard Features

### 1️⃣ System Overview
- View total errors, backups, and operations
- Check data file validation status
- See last backup timestamp

### 2️⃣ Error Logs
- View recent errors (50 most recent)
- Filter by severity (CRITICAL/ERROR/WARNING/INFO)
- View full traceback and context
- Export to markdown report

### 3️⃣ Data Validation
- Validate specific CSV/JSON files
- Run batch validation on all files
- View detailed validation reports
- Check for nulls, types, and structure

### 4️⃣ Backups
- Create new backups (one-click)
- List all available backups
- Restore from backup
- Clean old backups
- View backup history

### 5️⃣ Performance
- Monitor system resource usage
- View operation timings
- Identify slowest operations
- Export performance reports

---

## 📅 Schedule Automated Backups

### Windows (Task Scheduler)

1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task
3. Set trigger: Daily at 2:00 AM
4. Action: Start a program
   - Program: `python`
   - Arguments: `scripts\automated_backup.py --type full --keep 30`
   - Start in: `C:\Users\user\Desktop\pokemon\pokedex-dashboard`
5. Finish and enable

### Linux/Mac (Cron)

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /path/to/pokedex-dashboard && python scripts/automated_backup.py --type full --keep 30
```

---

## 🔍 Common Tasks

### Check System Status
1. Open dashboard → Tab 18
2. View "System Overview" panel
3. Check metrics: errors, backups, operations

### Review Recent Errors
1. Open dashboard → Tab 18
2. Click "Error Logs" tab
3. Select severity filter
4. Click "Export Report" if needed

### Create Backup
**Via UI:**
1. Open dashboard → Tab 18
2. Click "Backups" tab
3. Select backup type
4. Click "Create Backup"

**Via CLI:**
```bash
python scripts/automated_backup.py --type full
```

### Restore from Backup
**Via UI:**
1. Open dashboard → Tab 18
2. Click "Backups" tab
3. Select backup from list
4. Click "Restore" button

**Via Python:**
```python
from src.utils.backup_manager import BackupManager

manager = BackupManager()
manager.restore_backup('backups/data_backup_20241104_120000.zip')
```

### Validate Data Files
**Via UI:**
1. Open dashboard → Tab 18
2. Click "Data Validation" tab
3. Select file to validate
4. Click "Validate" button

**Via Python:**
```python
from src.utils.data_validator import DataValidator

validator = DataValidator()
result = validator.validate_csv('data/national_dex_with_variants.csv')
print(f"Valid: {result['valid']}")
```

### Monitor Performance
**Via UI:**
1. Open dashboard → Tab 18
2. Click "Performance" tab
3. View slowest operations
4. Export report if needed

**Via Python:**
```python
from src.utils.performance_profiler import get_profiler

profiler = get_profiler()
profiler.start_timer('my_operation')
# ... your code ...
profiler.end_timer('my_operation')
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [UTILITY_SYSTEM_GUIDE.md](docs/guides/UTILITY_SYSTEM_GUIDE.md) | Complete API reference |
| [AUTOMATED_BACKUP_GUIDE.md](docs/guides/AUTOMATED_BACKUP_GUIDE.md) | Backup scheduling guide |
| [v5.4.2_RELEASE_NOTES.md](docs/releases/v5.4.2_RELEASE_NOTES.md) | Full feature details |
| [README.md](README.md) | Project overview |

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'error_logger'"
**Solution:** Ensure you're running from the project root directory.

### Issue: "Warning: psutil not installed"
**Solution:** This is optional. Install with `pip install psutil` if you want memory profiling.

### Issue: Backup fails
**Solution:** 
1. Check disk space
2. Verify write permissions on `backups/` directory
3. Check error logs: `logs/errors/errors_*.log`

### Issue: Admin tab doesn't load
**Solution:**
1. Check browser console for errors
2. Verify `src/features/admin_utilities.py` exists
3. Check error logs for details

---

## 📊 File Locations

```
pokedex-dashboard/
├── src/
│   ├── utils/              # Utility modules
│   │   ├── error_logger.py
│   │   ├── data_validator.py
│   │   ├── backup_manager.py
│   │   └── performance_profiler.py
│   ├── features/
│   │   └── admin_utilities.py  # Admin dashboard
│   └── core/
│       └── app.py          # Main app (Tab 18)
├── scripts/
│   └── automated_backup.py # Backup script
├── logs/
│   ├── errors/             # Error logs
│   └── performance/        # Performance logs
├── backups/                # Backup files
│   └── backup_log.json     # Backup history
└── docs/
    ├── guides/             # Documentation
    └── releases/           # Release notes
```

---

## ⚙️ Configuration

All utility modules use sensible defaults. No configuration needed for basic usage.

**Advanced Configuration:**
- Error log format: JSON + text (auto-configured)
- Backup location: `backups/` (auto-created)
- Log location: `logs/` (auto-created)
- Retention policy: 30 backups (configurable with `--keep` flag)

---

## 🎯 Best Practices

1. **Regular Backups**: Schedule daily backups at 2 AM
2. **Monitor Errors**: Check error logs weekly
3. **Validate Data**: Run validation after data updates
4. **Clean Backups**: Keep last 30 backups (auto-cleaned)
5. **Performance**: Review performance metrics monthly

---

## 🔗 Quick Links

- **Live Demo**: https://1pokemon.streamlit.app/
- **Repository**: https://github.com/caalivanera/pokemon
- **Issues**: https://github.com/caalivanera/pokemon/issues

---

## 📞 Support

For help:
1. Check error logs: `logs/errors/`
2. Review documentation: `docs/guides/`
3. Check GitHub issues
4. See release notes: `docs/releases/`

---

## ✨ Tips

- Use `--quiet` flag for automated scripts (no output)
- Export reports to markdown for sharing
- Use performance profiler to find bottlenecks
- Schedule backups during low-usage hours
- Monitor disk space in backup directory

---

<div align="center">

**🎉 v5.4.2 - Professional Utility System**

*Error Logging | Data Validation | Automated Backups | Performance Monitoring*

</div>
