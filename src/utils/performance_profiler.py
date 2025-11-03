"""
Performance Profiler
Tracks and analyzes application performance metrics
"""

import time
import functools
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable
import json

# Optional psutil import
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("Warning: psutil not installed. Memory profiling disabled.")


class PerformanceProfiler:
    """Profile application performance and resource usage"""
    
    def __init__(self, log_dir: str = "logs/performance"):
        """Initialize performance profiler"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.profile_log = self.log_dir / f"profile_{datetime.now().strftime('%Y%m%d')}.json"
        self.profiles = self._load_profiles()
        self.current_timers = {}
    
    def _load_profiles(self) -> List[Dict]:
        """Load existing performance profiles"""
        if self.profile_log.exists():
            try:
                with open(self.profile_log, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_profiles(self):
        """Save performance profiles"""
        try:
            with open(self.profile_log, 'w') as f:
                json.dump(self.profiles, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save profiles: {e}")
    
    def start_timer(self, operation_name: str):
        """Start timing an operation"""
        start_memory = 0
        if HAS_PSUTIL:
            start_memory = psutil.Process().memory_info().rss / (1024 * 1024)
        
        self.current_timers[operation_name] = {
            'start_time': time.time(),
            'start_memory': start_memory
        }
    
    def end_timer(self, operation_name: str, metadata: Optional[Dict] = None) -> Dict:
        """End timing and log performance data"""
        if operation_name not in self.current_timers:
            return {}
        
        timer_data = self.current_timers.pop(operation_name)
        end_time = time.time()
        
        end_memory = 0
        if HAS_PSUTIL:
            end_memory = psutil.Process().memory_info().rss / (1024 * 1024)
        
        profile = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation_name,
            'duration_seconds': round(end_time - timer_data['start_time'], 4),
            'memory_start_mb': round(timer_data['start_memory'], 2),
            'memory_end_mb': round(end_memory, 2),
            'memory_delta_mb': round(end_memory - timer_data['start_memory'], 2),
            'metadata': metadata or {}
        }
        
        self.profiles.append(profile)
        self._save_profiles()
        
        return profile
    
    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile a function's performance"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__name__}"
            self.start_timer(func_name)
            
            try:
                result = func(*args, **kwargs)
                self.end_timer(func_name, {'status': 'success'})
                return result
            except Exception as e:
                self.end_timer(func_name, {'status': 'error', 'error': str(e)})
                raise
        
        return wrapper
    
    def get_system_info(self) -> Dict:
        """Get current system resource usage"""
        info = {'timestamp': datetime.now().isoformat()}
        
        if HAS_PSUTIL:
            process = psutil.Process()
            info.update({
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': process.memory_percent(),
                'memory_mb': round(process.memory_info().rss / (1024 * 1024), 2),
                'num_threads': process.num_threads(),
                'open_files': len(process.open_files()) if hasattr(process, 'open_files') else 0
            })
        else:
            info.update({
                'cpu_percent': 0,
                'memory_percent': 0,
                'memory_mb': 0,
                'num_threads': 0,
                'open_files': 0
            })
        
        return info
    
    def get_operation_stats(self, operation_name: str) -> Dict:
        """Get statistics for a specific operation"""
        op_profiles = [p for p in self.profiles if p['operation'] == operation_name]
        
        if not op_profiles:
            return {}
        
        durations = [p['duration_seconds'] for p in op_profiles]
        memory_deltas = [p['memory_delta_mb'] for p in op_profiles]
        
        return {
            'operation': operation_name,
            'call_count': len(op_profiles),
            'avg_duration': round(sum(durations) / len(durations), 4),
            'min_duration': round(min(durations), 4),
            'max_duration': round(max(durations), 4),
            'avg_memory_delta': round(sum(memory_deltas) / len(memory_deltas), 2),
            'total_time': round(sum(durations), 4)
        }
    
    def get_slowest_operations(self, count: int = 10) -> List[Dict]:
        """Get the slowest operations"""
        sorted_profiles = sorted(
            self.profiles,
            key=lambda x: x['duration_seconds'],
            reverse=True
        )
        return sorted_profiles[:count]
    
    def get_memory_intensive_operations(self, count: int = 10) -> List[Dict]:
        """Get operations with highest memory usage"""
        sorted_profiles = sorted(
            self.profiles,
            key=lambda x: abs(x['memory_delta_mb']),
            reverse=True
        )
        return sorted_profiles[:count]
    
    def get_all_operations(self) -> List[str]:
        """Get list of all profiled operations"""
        operations = set(p['operation'] for p in self.profiles)
        return sorted(list(operations))
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary"""
        if not self.profiles:
            return {
                'total_operations': 0,
                'unique_operations': 0,
                'total_time': 0,
                'avg_duration': 0,
                'avg_memory_delta': 0
            }
        
        durations = [p['duration_seconds'] for p in self.profiles]
        memory_deltas = [p['memory_delta_mb'] for p in self.profiles]
        
        return {
            'total_operations': len(self.profiles),
            'unique_operations': len(self.get_all_operations()),
            'total_time': round(sum(durations), 2),
            'avg_duration': round(sum(durations) / len(durations), 4),
            'avg_memory_delta': round(sum(memory_deltas) / len(memory_deltas), 2),
            'slowest_operation': max(self.profiles, key=lambda x: x['duration_seconds'])['operation'],
            'fastest_operation': min(self.profiles, key=lambda x: x['duration_seconds'])['operation']
        }
    
    def clear_profiles(self):
        """Clear all performance profiles"""
        self.profiles = []
        self._save_profiles()
    
    def export_performance_report(self, output_file: Optional[str] = None) -> str:
        """Export performance report to markdown"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.log_dir / f"performance_report_{timestamp}.md"
        
        summary = self.get_performance_summary()
        system_info = self.get_system_info()
        
        report = f"""# Performance Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## System Information
- **CPU Usage**: {system_info['cpu_percent']}%
- **Memory Usage**: {system_info['memory_mb']} MB ({system_info['memory_percent']:.1f}%)
- **Threads**: {system_info['num_threads']}

## Performance Summary
- **Total Operations**: {summary['total_operations']}
- **Unique Operations**: {summary['unique_operations']}
- **Total Time**: {summary['total_time']}s
- **Average Duration**: {summary['avg_duration']}s
- **Average Memory Delta**: {summary['avg_memory_delta']} MB

"""
        
        if summary['total_operations'] > 0:
            report += f"- **Slowest Operation**: {summary['slowest_operation']}\n"
            report += f"- **Fastest Operation**: {summary['fastest_operation']}\n"
        
        # Slowest operations
        report += "\n## Slowest Operations (Top 10)\n\n"
        report += "| Operation | Duration | Memory Delta |\n"
        report += "|-----------|----------|-------------|\n"
        
        for profile in self.get_slowest_operations(10):
            report += f"| {profile['operation']} | {profile['duration_seconds']}s | "
            report += f"{profile['memory_delta_mb']} MB |\n"
        
        # Memory intensive operations
        report += "\n## Memory Intensive Operations (Top 10)\n\n"
        report += "| Operation | Duration | Memory Delta |\n"
        report += "|-----------|----------|-------------|\n"
        
        for profile in self.get_memory_intensive_operations(10):
            report += f"| {profile['operation']} | {profile['duration_seconds']}s | "
            report += f"{profile['memory_delta_mb']} MB |\n"
        
        # Operation statistics
        report += "\n## Operation Statistics\n\n"
        report += "| Operation | Calls | Avg Time | Min | Max | Total Time |\n"
        report += "|-----------|-------|----------|-----|-----|------------|\n"
        
        for operation in self.get_all_operations():
            stats = self.get_operation_stats(operation)
            report += f"| {stats['operation']} | {stats['call_count']} | "
            report += f"{stats['avg_duration']}s | {stats['min_duration']}s | "
            report += f"{stats['max_duration']}s | {stats['total_time']}s |\n"
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        return str(output_file)


# Global profiler instance
_profiler = None

def get_profiler() -> PerformanceProfiler:
    """Get the global profiler instance"""
    global _profiler
    if _profiler is None:
        _profiler = PerformanceProfiler()
    return _profiler


def profile(func: Callable) -> Callable:
    """Decorator to profile a function"""
    profiler = get_profiler()
    return profiler.profile_function(func)


if __name__ == "__main__":
    # Test the profiler
    profiler = PerformanceProfiler()
    
    print("="*60)
    print("PERFORMANCE PROFILER TEST")
    print("="*60)
    
    # Test timing
    profiler.start_timer("test_operation")
    time.sleep(0.1)
    result = profiler.end_timer("test_operation")
    print(f"\n✅ Operation profiled: {result['duration_seconds']}s")
    
    # Test decorator
    @profiler.profile_function
    def slow_function():
        time.sleep(0.2)
        return "done"
    
    slow_function()
    
    # Show summary
    print("\n📊 Performance Summary:")
    summary = profiler.get_performance_summary()
    print(f"   Total operations: {summary['total_operations']}")
    print(f"   Average duration: {summary['avg_duration']}s")
    
    # Generate report
    report_path = profiler.export_performance_report()
    print(f"\n📄 Report generated: {report_path}")
