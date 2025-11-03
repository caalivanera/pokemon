"""
Automated Backup Script
Run this script on a schedule (cron/Task Scheduler) for automated backups
"""

import sys
from pathlib import Path
from datetime import datetime
import argparse

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "utils"))

try:
    from backup_manager import BackupManager
    from error_logger import get_error_logger
except ImportError as e:
    print(f"Error: Could not import utilities: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


def run_backup(backup_type='full', keep_count=30, verbose=True):
    """
    Run automated backup
    
    Args:
        backup_type: 'full', 'data', 'config', or 'assets'
        keep_count: Number of recent backups to keep
        verbose: Print status messages
    """
    logger = get_error_logger()
    manager = BackupManager()
    
    if verbose:
        print("="*60)
        print(f"AUTOMATED BACKUP - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
    
    try:
        # Create backup based on type
        if backup_type == 'full':
            if verbose:
                print("\n📦 Creating full backup...")
            result = manager.full_backup()
            if verbose:
                print(f"✅ Full backup complete:")
                print(f"   Data: {Path(result['data']).name}")
                print(f"   Config: {Path(result['config']).name}")
        
        elif backup_type == 'data':
            if verbose:
                print("\n📦 Creating data backup...")
            path = manager.backup_data_files()
            if verbose:
                print(f"✅ Data backup complete: {Path(path).name}")
        
        elif backup_type == 'config':
            if verbose:
                print("\n📦 Creating config backup...")
            path = manager.backup_config_files()
            if verbose:
                print(f"✅ Config backup complete: {Path(path).name}")
        
        elif backup_type == 'assets':
            if verbose:
                print("\n📦 Creating assets backup...")
            path = manager.backup_assets()
            if verbose:
                print(f"✅ Assets backup complete: {Path(path).name}")
        
        else:
            raise ValueError(f"Unknown backup type: {backup_type}")
        
        # Clean old backups
        if verbose:
            print(f"\n🧹 Cleaning old backups (keeping {keep_count} most recent)...")
        
        initial_count = manager.get_backup_summary()['total']
        manager.clean_old_backups(keep_count=keep_count)
        final_count = manager.get_backup_summary()['total']
        
        if verbose:
            removed = initial_count - final_count
            print(f"✅ Cleaned {removed} old backup(s)")
        
        # Summary
        if verbose:
            summary = manager.get_backup_summary()
            print("\n" + "="*60)
            print("BACKUP SUMMARY")
            print("="*60)
            print(f"Total backups: {summary['total']}")
            print(f"Total size: {summary['total_size_mb']} MB")
            if summary['newest']:
                print(f"Latest: {summary['newest']}")
            print("\n✅ Backup completed successfully!")
        
        return True
    
    except Exception as e:
        logger.log_error(
            e,
            context={'script': 'automated_backup', 'backup_type': backup_type},
            severity='CRITICAL'
        )
        
        if verbose:
            print(f"\n❌ Backup failed: {e}")
            print("Check logs/errors/ for details")
        
        return False


def main():
    """Main function with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description='Automated backup script for Pokemon Dashboard'
    )
    
    parser.add_argument(
        '--type',
        choices=['full', 'data', 'config', 'assets'],
        default='full',
        help='Type of backup to create (default: full)'
    )
    
    parser.add_argument(
        '--keep',
        type=int,
        default=30,
        help='Number of recent backups to keep (default: 30)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress output messages'
    )
    
    args = parser.parse_args()
    
    success = run_backup(
        backup_type=args.type,
        keep_count=args.keep,
        verbose=not args.quiet
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
