"""
Error Logging System
Centralized error tracking with timestamps and context
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import traceback
import sys


class ErrorLogger:
    """Centralized error logging system for the application"""
    
    def __init__(self, log_dir: str = "logs/errors"):
        """Initialize error logger"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup file logging
        self.error_log_file = self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        self.json_log_file = self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Configure logger
        self.logger = logging.getLogger('PokemonDashboard')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler for text logs
        file_handler = logging.FileHandler(self.error_log_file)
        file_handler.setLevel(logging.ERROR)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Error storage for JSON
        self.errors = self._load_json_errors()
    
    def _load_json_errors(self) -> List[Dict]:
        """Load existing JSON error logs"""
        if self.json_log_file.exists():
            try:
                with open(self.json_log_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_json_errors(self):
        """Save errors to JSON file"""
        try:
            with open(self.json_log_file, 'w') as f:
                json.dump(self.errors, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save JSON errors: {e}")
    
    def log_error(
        self, 
        error: Exception, 
        context: Optional[Dict[str, Any]] = None,
        severity: str = "ERROR"
    ):
        """
        Log an error with context
        
        Args:
            error: The exception that occurred
            context: Additional context (function name, parameters, etc.)
            severity: Error severity (ERROR, CRITICAL, WARNING)
        """
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        # Add to JSON storage
        self.errors.append(error_data)
        self._save_json_errors()
        
        # Log to file
        log_msg = f"{error_data['type']}: {error_data['message']}"
        if context:
            log_msg += f" | Context: {json.dumps(context)}"
        
        if severity == "CRITICAL":
            self.logger.critical(log_msg)
        elif severity == "ERROR":
            self.logger.error(log_msg)
        elif severity == "WARNING":
            self.logger.warning(log_msg)
    
    def log_data_error(
        self, 
        file_path: str, 
        error_type: str, 
        details: str,
        severity: str = "ERROR"
    ):
        """Log data-related errors"""
        context = {
            'category': 'data_error',
            'file': file_path,
            'error_type': error_type,
            'details': details
        }
        self.log_error(
            Exception(f"Data error in {file_path}: {error_type}"),
            context=context,
            severity=severity
        )
    
    def log_feature_error(
        self,
        feature_name: str,
        error: Exception,
        user_action: Optional[str] = None
    ):
        """Log feature-specific errors"""
        context = {
            'category': 'feature_error',
            'feature': feature_name,
            'user_action': user_action
        }
        self.log_error(error, context=context)
    
    def log_import_error(
        self,
        module_name: str,
        error: Exception
    ):
        """Log import errors"""
        context = {
            'category': 'import_error',
            'module': module_name
        }
        self.log_error(error, context=context, severity="CRITICAL")
    
    def get_recent_errors(self, count: int = 10) -> List[Dict]:
        """Get most recent errors"""
        return self.errors[-count:] if self.errors else []
    
    def get_errors_by_type(self, error_type: str) -> List[Dict]:
        """Get errors filtered by type"""
        return [e for e in self.errors if e['type'] == error_type]
    
    def get_errors_by_severity(self, severity: str) -> List[Dict]:
        """Get errors filtered by severity"""
        return [e for e in self.errors if e['severity'] == severity]
    
    def get_error_summary(self) -> Dict:
        """Get summary statistics of errors"""
        if not self.errors:
            return {
                'total': 0,
                'by_type': {},
                'by_severity': {},
                'by_category': {}
            }
        
        summary = {
            'total': len(self.errors),
            'by_type': {},
            'by_severity': {},
            'by_category': {}
        }
        
        for error in self.errors:
            # Count by type
            error_type = error['type']
            summary['by_type'][error_type] = summary['by_type'].get(error_type, 0) + 1
            
            # Count by severity
            severity = error['severity']
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            
            # Count by category
            category = error['context'].get('category', 'uncategorized')
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
        
        return summary
    
    def clear_old_errors(self, days: int = 30):
        """Remove errors older than specified days"""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        self.errors = [
            e for e in self.errors
            if datetime.fromisoformat(e['timestamp']).timestamp() > cutoff_date
        ]
        self._save_json_errors()
    
    def export_errors_report(self, output_file: Optional[str] = None) -> str:
        """Export errors to a markdown report"""
        if output_file is None:
            output_file = self.log_dir / f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        summary = self.get_error_summary()
        
        report = f"""# Error Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Errors**: {summary['total']}
- **Critical**: {summary['by_severity'].get('CRITICAL', 0)}
- **Errors**: {summary['by_severity'].get('ERROR', 0)}
- **Warnings**: {summary['by_severity'].get('WARNING', 0)}

## Errors by Type
"""
        for error_type, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True):
            report += f"- **{error_type}**: {count}\n"
        
        report += "\n## Errors by Category\n"
        for category, count in sorted(summary['by_category'].items(), key=lambda x: x[1], reverse=True):
            report += f"- **{category}**: {count}\n"
        
        report += "\n## Recent Errors (Last 10)\n"
        for error in self.get_recent_errors(10):
            report += f"\n### {error['severity']}: {error['type']}\n"
            report += f"**Time**: {error['timestamp']}\n\n"
            report += f"**Message**: {error['message']}\n\n"
            if error['context']:
                report += f"**Context**: {json.dumps(error['context'], indent=2)}\n\n"
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        return str(output_file)


# Global logger instance
_error_logger = None

def get_error_logger() -> ErrorLogger:
    """Get the global error logger instance"""
    global _error_logger
    if _error_logger is None:
        _error_logger = ErrorLogger()
    return _error_logger


def log_error(error: Exception, context: Optional[Dict] = None, severity: str = "ERROR"):
    """Convenience function to log errors"""
    logger = get_error_logger()
    logger.log_error(error, context, severity)


if __name__ == "__main__":
    # Test the error logger
    logger = ErrorLogger()
    
    # Test different error types
    try:
        raise ValueError("Test value error")
    except Exception as e:
        logger.log_error(e, context={'test': 'value_error'})
    
    try:
        1 / 0
    except Exception as e:
        logger.log_error(e, context={'test': 'division'}, severity="CRITICAL")
    
    logger.log_data_error(
        "data/test.csv",
        "missing_columns",
        "Required columns [name, type] not found"
    )
    
    # Generate report
    print("\n" + "="*60)
    print("ERROR SUMMARY")
    print("="*60)
    summary = logger.get_error_summary()
    print(f"Total Errors: {summary['total']}")
    print(f"By Type: {summary['by_type']}")
    print(f"By Severity: {summary['by_severity']}")
    print(f"By Category: {summary['by_category']}")
    
    report_path = logger.export_errors_report()
    print(f"\n✅ Report exported to: {report_path}")
