# Utility System Guide

## Overview

The Pokemon Dashboard now includes a comprehensive utility system for error logging, data validation, backups, and performance profiling.

## Modules

### 1. Error Logger (`error_logger.py`)

Centralized error tracking with timestamps and context.

**Features:**
- File-based logging (text and JSON)
- Categorized error tracking
- Error summaries and reports
- Context preservation

**Usage:**
```python
from utils.error_logger import get_error_logger, log_error

# Get logger instance
logger = get_error_logger()

# Log errors with context
try:
    # Your code here
    pass
except Exception as e:
    logger.log_error(e, context={'function': 'my_function', 'user': 'admin'})

# Or use convenience function
log_error(Exception("Something went wrong"), severity="CRITICAL")

# Generate report
logger.export_errors_report()
```

**Error Categories:**
- `data_error`: Data-related issues
- `feature_error`: Feature-specific errors
- `import_error`: Module import failures
- `uncategorized`: General errors

### 2. Data Validator (`data_validator.py`)

Validates CSV files and JSON data for integrity.

**Features:**
- CSV column validation
- Data type checking
- Null value detection
- Categorical value validation
- Pokemon-specific validators

**Usage:**
```python
from utils.data_validator import DataValidator

validator = DataValidator()

# Validate Pokemon CSV
is_valid, report = validator.validate_pokemon_csv("data/pokemon.csv")

# Validate custom CSV
is_valid, report = validator.validate_csv(
    "data/mydata.csv",
    required_columns=['id', 'name'],
    numeric_columns=['value'],
    categorical_columns={'status': ['active', 'inactive']}
)

# Validate all data files
results = validator.validate_all_data_files()

# Generate report
validator.generate_validation_report()
```

### 3. Backup Manager (`backup_manager.py`)

Automated backup system with versioning.

**Features:**
- Timestamped backups
- ZIP compression
- Selective file backup
- Backup logs and history
- Automatic cleanup

**Usage:**
```python
from utils.backup_manager import BackupManager

manager = BackupManager()

# Backup specific files
backup_path = manager.create_backup(
    files=['data/pokemon.csv', 'data/national_dex.csv'],
    backup_name='my_backup',
    compress=True
)

# Quick backups
manager.backup_data_files()     # Backup all data
manager.backup_config_files()   # Backup configs
manager.full_backup()           # Full backup

# List backups
backups = manager.list_backups()

# Restore backup
manager.restore_backup(backup_path, restore_dir='restore/')

# Clean old backups (keep 10 most recent)
manager.clean_old_backups(keep_count=10)

# Export report
manager.export_backup_report()
```

### 4. Performance Profiler (`performance_profiler.py`)

Tracks and analyzes application performance.

**Features:**
- Operation timing
- Memory usage tracking (requires psutil)
- Function decorators
- Performance reports
- Slowest operation detection

**Usage:**
```python
from utils.performance_profiler import get_profiler, profile

profiler = get_profiler()

# Manual timing
profiler.start_timer('my_operation')
# ... your code ...
result = profiler.end_timer('my_operation')

# Decorator approach
@profile
def expensive_function():
    # Your code here
    pass

# Get statistics
stats = profiler.get_operation_stats('my_operation')
slowest = profiler.get_slowest_operations(10)
summary = profiler.get_performance_summary()

# Generate report
profiler.export_performance_report()
```

## Integration Example

```python
from utils import (
    get_error_logger,
    DataValidator,
    BackupManager,
    get_profiler,
    profile
)

# Initialize utilities
logger = get_error_logger()
validator = DataValidator()
backup = BackupManager()
profiler = get_profiler()

@profile
def load_and_validate_data(file_path):
    """Load and validate data with error handling"""
    try:
        # Validate data
        is_valid, report = validator.validate_pokemon_csv(file_path)
        
        if not is_valid:
            logger.log_data_error(
                file_path,
                "validation_failed",
                f"Errors: {report['errors']}"
            )
            return None
        
        # Load data
        import pandas as pd
        df = pd.read_csv(file_path)
        return df
        
    except Exception as e:
        logger.log_error(
            e,
            context={'function': 'load_and_validate_data', 'file': file_path}
        )
        return None

# Use with automatic backup
backup.backup_data_files()
data = load_and_validate_data('data/pokemon.csv')

# Generate reports
logger.export_errors_report()
validator.generate_validation_report()
profiler.export_performance_report()
```

## File Structure

```
logs/
├── errors/
│   ├── errors_20241104.log        # Text error log
│   ├── errors_20241104.json       # JSON error log
│   └── error_report_*.md          # Generated reports
└── performance/
    ├── profile_20241104.json      # Performance data
    └── performance_report_*.md    # Generated reports

backups/
├── backup_log.json                # Backup history
├── data_backup_20241104_*.zip     # Compressed backups
└── backup_report_*.md             # Generated reports

data_validation_report_*.md        # Validation reports
```

## Command Line Usage

### Test Error Logger
```bash
python src/utils/error_logger.py
```

### Test Data Validator
```bash
python src/utils/data_validator.py
```

### Test Backup Manager
```bash
python src/utils/backup_manager.py
```

### Test Performance Profiler
```bash
python src/utils/performance_profiler.py
```

## Best Practices

1. **Error Logging**
   - Always log errors with context
   - Use appropriate severity levels
   - Review error reports regularly

2. **Data Validation**
   - Validate data before processing
   - Run validation after data updates
   - Check validation reports for warnings

3. **Backups**
   - Create backups before major changes
   - Keep reasonable number of backups (10-20)
   - Test restore process periodically

4. **Performance Profiling**
   - Profile critical operations
   - Review slowest operations
   - Install psutil for memory profiling

## Troubleshooting

### psutil Not Installed
Performance profiling will work without psutil, but memory tracking will be disabled. To enable:
```bash
pip install psutil
```

### Permission Errors
Ensure write permissions for:
- `logs/` directory
- `backups/` directory

### Large Backup Files
Use selective backups instead of full backups:
```python
# Instead of full_backup()
manager.backup_data_files()  # Only data
manager.backup_config_files()  # Only configs
```

## Version History

- **v1.0.0** (2024-11-04)
  - Initial release
  - Error logging system
  - Data validation
  - Backup manager
  - Performance profiler
