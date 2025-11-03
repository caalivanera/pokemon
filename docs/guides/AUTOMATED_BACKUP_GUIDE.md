# Automated Backup Setup Guide

## Overview

The `automated_backup.py` script provides scheduled backups for your Pokemon Dashboard data. It can be run manually or scheduled to run automatically.

## Usage

### Manual Backup

```bash
# Full backup (data + config)
python scripts/automated_backup.py

# Data files only
python scripts/automated_backup.py --type data

# Config files only
python scripts/automated_backup.py --type config

# Assets only
python scripts/automated_backup.py --type assets

# Keep only 10 most recent backups
python scripts/automated_backup.py --keep 10

# Quiet mode (no output)
python scripts/automated_backup.py --quiet
```

## Scheduled Backups

### Windows (Task Scheduler)

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task**
   - Click "Create Basic Task" in the right panel
   - Name: "Pokemon Dashboard Backup"
   - Description: "Daily automated backup"

3. **Trigger**
   - Select "Daily"
   - Start time: 2:00 AM (or your preferred time)
   - Recur every: 1 day

4. **Action**
   - Select "Start a program"
   - Program/script: `python`
   - Add arguments: `scripts\automated_backup.py --type full --keep 30`
   - Start in: `C:\Users\user\Desktop\pokemon\pokedex-dashboard`

5. **Finish**
   - Check "Open Properties" before clicking Finish
   - In Properties, check "Run whether user is logged on or not"
   - Check "Run with highest privileges"

### Linux/Mac (Cron)

1. **Edit crontab**
   ```bash
   crontab -e
   ```

2. **Add backup job** (runs daily at 2 AM)
   ```cron
   0 2 * * * cd /path/to/pokedex-dashboard && python scripts/automated_backup.py --type full --keep 30 >> logs/backup_cron.log 2>&1
   ```

3. **Save and exit**

### Alternative: Use Windows Batch File

Create `run_backup.bat`:
```batch
@echo off
cd /d "C:\Users\user\Desktop\pokemon\pokedex-dashboard"
python scripts\automated_backup.py --type full --keep 30
pause
```

Then schedule this batch file instead.

## Backup Types

### Full Backup (Recommended)
- Backs up data files AND config files
- Use for complete system backup

### Data Backup
- Only backs up Pokemon data files
- Faster, smaller file size
- Use for frequent backups

### Config Backup
- Only backs up configuration files
- Very small file size
- Use before making config changes

### Assets Backup
- Backs up sprite and image files
- Large file size (several GB)
- Use infrequently (weekly/monthly)

## Backup Retention

The script automatically cleans old backups based on `--keep` parameter:

- **Default**: Keep 30 most recent backups
- **Daily backups**: 30 backups = 1 month
- **Twice-daily**: 30 backups = 2 weeks

## Backup Location

All backups are stored in:
```
backups/
├── backup_log.json           # Backup history
├── data_backup_*.zip          # Data backups
├── config_backup_*.zip        # Config backups
└── full_backup_*.zip          # Full backups
```

## Monitoring

### Check Backup Status

1. **Via Admin Dashboard**
   - Open app: `streamlit run src/core/app.py`
   - Go to "🛠️ Admin Utilities" tab
   - Click "💾 Backups" section

2. **Via Command Line**
   ```python
   from src.utils.backup_manager import BackupManager
   
   manager = BackupManager()
   summary = manager.get_backup_summary()
   print(f"Total backups: {summary['total']}")
   print(f"Total size: {summary['total_size_mb']} MB")
   ```

### View Logs

Backup errors are logged to:
- `logs/errors/errors_YYYYMMDD.log` (text format)
- `logs/errors/errors_YYYYMMDD.json` (JSON format)

## Troubleshooting

### Script Not Running

1. **Check Python Path**
   ```bash
   where python  # Windows
   which python  # Linux/Mac
   ```

2. **Test Manual Run**
   ```bash
   python scripts/automated_backup.py --type data
   ```

3. **Check Permissions**
   - Ensure write access to `backups/` directory
   - Run as administrator if needed

### Task Scheduler Issues (Windows)

1. **Check Task Status**
   - Open Task Scheduler
   - Find your task in the list
   - Check "Last Run Result" column

2. **View Task History**
   - Right-click task → "History" tab
   - Look for error codes

3. **Common Error Codes**
   - `0x1`: General error (check Python path)
   - `0x2`: File not found (check paths)
   - `0x41301`: Task still running

### Cron Issues (Linux/Mac)

1. **Check Cron Logs**
   ```bash
   tail -f /var/log/syslog | grep CRON
   ```

2. **Test Cron Entry**
   ```bash
   # Run the command manually first
   cd /path/to/pokedex-dashboard && python scripts/automated_backup.py
   ```

3. **Common Issues**
   - PATH not set: Use absolute paths
   - Permissions: Ensure execute permissions
   - Environment: Cron runs with limited environment

## Best Practices

1. **Schedule Regular Backups**
   - Daily backups for active development
   - Weekly backups for stable systems

2. **Retention Policy**
   - Keep 30 daily backups (1 month)
   - Keep separate weekly/monthly backups

3. **Test Restores**
   - Periodically test backup restoration
   - Verify backup integrity

4. **Monitor Disk Space**
   - Check backup directory size regularly
   - Adjust retention policy if needed

5. **Off-site Backups**
   - Copy backups to external drive
   - Use cloud storage for critical backups

## Example Schedules

### Conservative (Daily)
```bash
# Windows Task Scheduler: Daily at 2 AM
python scripts\automated_backup.py --type full --keep 30

# Linux Cron: Daily at 2 AM
0 2 * * * cd /path/to/project && python scripts/automated_backup.py --type full --keep 30
```

### Aggressive (Twice Daily)
```bash
# Windows: 2 AM and 2 PM
python scripts\automated_backup.py --type data --keep 60

# Linux Cron
0 2,14 * * * cd /path/to/project && python scripts/automated_backup.py --type data --keep 60
```

### Mixed Strategy
```bash
# Daily data backup (2 AM)
0 2 * * * python scripts/automated_backup.py --type data --keep 30

# Weekly full backup (Sunday 3 AM)
0 3 * * 0 python scripts/automated_backup.py --type full --keep 8

# Monthly assets backup (1st of month, 4 AM)
0 4 1 * * python scripts/automated_backup.py --type assets --keep 3
```

## Restoration

To restore from a backup:

1. **Via Admin Dashboard**
   - Go to "🛠️ Admin Utilities" → "💾 Backups"
   - Select backup to restore
   - Click restore button

2. **Via Command Line**
   ```python
   from src.utils.backup_manager import BackupManager
   
   manager = BackupManager()
   manager.restore_backup('backups/data_backup_20241104_120000.zip', restore_dir='.')
   ```

3. **Manual Extraction**
   - Backups are standard ZIP files
   - Can be extracted with any ZIP tool

## Security

- Backups contain sensitive data
- Keep backups secure
- Don't commit backups to version control
- Add `backups/` to `.gitignore` (already done)

## Support

For issues or questions:
- Check error logs in `logs/errors/`
- Review backup logs in `backups/backup_log.json`
- See main documentation in `docs/guides/UTILITY_SYSTEM_GUIDE.md`
