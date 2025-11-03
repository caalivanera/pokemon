"""
Automated Backup System
Creates timestamped backups of data files and configurations
"""

import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
import json


class BackupManager:
    """Manage automated backups of data files"""
    
    def __init__(self, backup_dir: str = "backups"):
        """Initialize backup manager"""
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.backup_log = self.backup_dir / "backup_log.json"
        self.logs = self._load_logs()
    
    def _load_logs(self) -> List[Dict]:
        """Load backup logs"""
        if self.backup_log.exists():
            try:
                with open(self.backup_log, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_logs(self):
        """Save backup logs"""
        try:
            with open(self.backup_log, 'w') as f:
                json.dump(self.logs, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save backup log: {e}")
    
    def create_backup(
        self, 
        files: List[str],
        backup_name: Optional[str] = None,
        compress: bool = True
    ) -> str:
        """
        Create a backup of specified files
        
        Args:
            files: List of file/directory paths to backup
            backup_name: Optional custom name for backup
            compress: Whether to compress backup as ZIP
            
        Returns:
            Path to backup file/directory
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if backup_name is None:
            backup_name = f"backup_{timestamp}"
        else:
            backup_name = f"{backup_name}_{timestamp}"
        
        if compress:
            backup_path = self.backup_dir / f"{backup_name}.zip"
            self._create_zip_backup(files, backup_path)
        else:
            backup_path = self.backup_dir / backup_name
            backup_path.mkdir(parents=True, exist_ok=True)
            self._create_dir_backup(files, backup_path)
        
        # Log the backup
        log_entry = {
            'timestamp': timestamp,
            'backup_name': backup_name,
            'backup_path': str(backup_path),
            'files': files,
            'compressed': compress,
            'size_bytes': backup_path.stat().st_size if backup_path.exists() else 0
        }
        self.logs.append(log_entry)
        self._save_logs()
        
        return str(backup_path)
    
    def _create_zip_backup(self, files: List[str], backup_path: Path):
        """Create compressed ZIP backup"""
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files:
                path = Path(file_path)
                if path.exists():
                    if path.is_file():
                        zipf.write(path, path.name)
                    elif path.is_dir():
                        for file in path.rglob('*'):
                            if file.is_file():
                                arcname = file.relative_to(path.parent)
                                zipf.write(file, arcname)
    
    def _create_dir_backup(self, files: List[str], backup_path: Path):
        """Create directory-based backup"""
        for file_path in files:
            path = Path(file_path)
            if path.exists():
                dest = backup_path / path.name
                if path.is_file():
                    shutil.copy2(path, dest)
                elif path.is_dir():
                    shutil.copytree(path, dest, dirs_exist_ok=True)
    
    def backup_data_files(self) -> str:
        """Backup all data files"""
        data_files = [
            "data/pokemon.csv",
            "data/national_dex.csv",
            "data/national_dex_with_variants.csv",
            "data/competitive",
            "data/moves",
            "data/enhanced"
        ]
        
        existing_files = [f for f in data_files if Path(f).exists()]
        return self.create_backup(existing_files, "data_backup")
    
    def backup_config_files(self) -> str:
        """Backup configuration files"""
        config_files = [
            ".streamlit/config.toml",
            "requirements.txt",
            ".gitignore"
        ]
        
        existing_files = [f for f in config_files if Path(f).exists()]
        return self.create_backup(existing_files, "config_backup")
    
    def backup_assets(self) -> str:
        """Backup asset files"""
        asset_dirs = [
            "assets/sprites",
            "assets/type_icons",
            "assets/games"
        ]
        
        existing_dirs = [d for d in asset_dirs if Path(d).exists()]
        return self.create_backup(existing_dirs, "assets_backup")
    
    def full_backup(self) -> Dict[str, str]:
        """Create a full backup of all critical files"""
        results = {
            'data': self.backup_data_files(),
            'config': self.backup_config_files(),
            'timestamp': datetime.now().isoformat()
        }
        return results
    
    def restore_backup(self, backup_path: str, restore_dir: str = ".") -> bool:
        """
        Restore files from a backup
        
        Args:
            backup_path: Path to backup file/directory
            restore_dir: Directory to restore files to
            
        Returns:
            True if successful, False otherwise
        """
        path = Path(backup_path)
        restore_path = Path(restore_dir)
        
        if not path.exists():
            print(f"Backup not found: {backup_path}")
            return False
        
        try:
            if path.suffix == '.zip':
                # Extract ZIP backup
                with zipfile.ZipFile(path, 'r') as zipf:
                    zipf.extractall(restore_path)
            else:
                # Copy directory backup
                for item in path.iterdir():
                    dest = restore_path / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                    elif item.is_dir():
                        shutil.copytree(item, dest, dirs_exist_ok=True)
            
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        return sorted(self.logs, key=lambda x: x['timestamp'], reverse=True)
    
    def get_backup_info(self, backup_name: str) -> Optional[Dict]:
        """Get information about a specific backup"""
        for log in self.logs:
            if log['backup_name'] == backup_name:
                return log
        return None
    
    def clean_old_backups(self, keep_count: int = 10):
        """Remove old backups, keeping only the most recent ones"""
        if len(self.logs) <= keep_count:
            return
        
        sorted_logs = sorted(self.logs, key=lambda x: x['timestamp'], reverse=True)
        logs_to_remove = sorted_logs[keep_count:]
        
        for log in logs_to_remove:
            backup_path = Path(log['backup_path'])
            if backup_path.exists():
                try:
                    if backup_path.is_file():
                        backup_path.unlink()
                    elif backup_path.is_dir():
                        shutil.rmtree(backup_path)
                    print(f"Removed old backup: {backup_path.name}")
                except Exception as e:
                    print(f"Could not remove {backup_path}: {e}")
        
        # Update logs
        self.logs = sorted_logs[:keep_count]
        self._save_logs()
    
    def get_backup_summary(self) -> Dict:
        """Get summary statistics of backups"""
        if not self.logs:
            return {
                'total': 0,
                'total_size_mb': 0,
                'oldest': None,
                'newest': None
            }
        
        total_size = sum(log.get('size_bytes', 0) for log in self.logs)
        sorted_logs = sorted(self.logs, key=lambda x: x['timestamp'])
        
        return {
            'total': len(self.logs),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'oldest': sorted_logs[0]['timestamp'] if sorted_logs else None,
            'newest': sorted_logs[-1]['timestamp'] if sorted_logs else None
        }
    
    def export_backup_report(self, output_file: Optional[str] = None) -> str:
        """Export backup report to markdown"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.backup_dir / f"backup_report_{timestamp}.md"
        
        summary = self.get_backup_summary()
        
        report = f"""# Backup Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Backups**: {summary['total']}
- **Total Size**: {summary['total_size_mb']} MB
- **Oldest Backup**: {summary['oldest']}
- **Newest Backup**: {summary['newest']}

## Backup History
"""
        
        for log in self.list_backups():
            size_mb = round(log.get('size_bytes', 0) / (1024 * 1024), 2)
            report += f"\n### {log['backup_name']}\n"
            report += f"- **Time**: {log['timestamp']}\n"
            report += f"- **Size**: {size_mb} MB\n"
            report += f"- **Compressed**: {'Yes' if log.get('compressed') else 'No'}\n"
            report += f"- **Files**: {', '.join(log['files'][:5])}"
            if len(log['files']) > 5:
                report += f" (and {len(log['files']) - 5} more)"
            report += "\n"
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        return str(output_file)


if __name__ == "__main__":
    # Test backup manager
    manager = BackupManager()
    
    print("="*60)
    print("BACKUP SYSTEM TEST")
    print("="*60)
    
    # Create a test backup
    print("\n📦 Creating test backup...")
    test_files = ["README.md", "requirements.txt"]
    backup_path = manager.create_backup(test_files, "test_backup")
    print(f"✅ Backup created: {backup_path}")
    
    # Show summary
    print("\n📊 Backup Summary:")
    summary = manager.get_backup_summary()
    print(f"   Total backups: {summary['total']}")
    print(f"   Total size: {summary['total_size_mb']} MB")
    
    # Generate report
    report_path = manager.export_backup_report()
    print(f"\n📄 Report generated: {report_path}")
    
    # List backups
    print("\n📋 Available Backups:")
    for backup in manager.list_backups()[:5]:
        print(f"   - {backup['backup_name']} ({backup['timestamp']})")
