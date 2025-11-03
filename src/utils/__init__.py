"""
Utility Module Initialization
Provides easy access to all utility modules
"""

from .error_logger import ErrorLogger, get_error_logger, log_error
from .data_validator import DataValidator
from .backup_manager import BackupManager
from .performance_profiler import PerformanceProfiler, get_profiler, profile

__all__ = [
    'ErrorLogger',
    'get_error_logger',
    'log_error',
    'DataValidator',
    'BackupManager',
    'PerformanceProfiler',
    'get_profiler',
    'profile'
]

__version__ = '1.0.0'
