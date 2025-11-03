"""
Admin Utilities Dashboard
Provides access to error logs, backups, validation, and performance monitoring
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add utils to path
utils_path = Path(__file__).parent.parent / "utils"
sys.path.insert(0, str(utils_path))

try:
    from error_logger import get_error_logger
    from data_validator import DataValidator
    from backup_manager import BackupManager
    from performance_profiler import get_profiler
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False


def render_admin_dashboard():
    """Render the admin utilities dashboard"""
    if not UTILS_AVAILABLE:
        st.error("⚠️ Utility system not available. Please check installation.")
        st.info("Run: `pip install -r requirements.txt` to install dependencies")
        return
    
    st.title("🛠️ Admin Utilities Dashboard")
    st.markdown("System management, monitoring, and maintenance tools")
    
    # Create tabs for different admin functions
    admin_tabs = st.tabs([
        "📊 System Overview",
        "🔍 Error Logs",
        "✅ Data Validation",
        "💾 Backups",
        "⚡ Performance"
    ])
    
    # Tab 1: System Overview
    with admin_tabs[0]:
        render_system_overview()
    
    # Tab 2: Error Logs
    with admin_tabs[1]:
        render_error_logs()
    
    # Tab 3: Data Validation
    with admin_tabs[2]:
        render_data_validation()
    
    # Tab 4: Backups
    with admin_tabs[3]:
        render_backups()
    
    # Tab 5: Performance
    with admin_tabs[4]:
        render_performance()


def render_system_overview():
    """Render system overview"""
    st.header("📊 System Overview")
    
    try:
        logger = get_error_logger()
        validator = DataValidator()
        backup_mgr = BackupManager()
        profiler = get_profiler()
        
        # Error summary
        error_summary = logger.get_error_summary()
        
        # Backup summary
        backup_summary = backup_mgr.get_backup_summary()
        
        # Performance summary
        perf_summary = profiler.get_performance_summary()
        
        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Errors",
                error_summary['total'],
                delta=f"-{error_summary.get('by_severity', {}).get('CRITICAL', 0)} critical"
            )
        
        with col2:
            st.metric(
                "Backups",
                backup_summary['total'],
                delta=f"{backup_summary['total_size_mb']} MB"
            )
        
        with col3:
            st.metric(
                "Operations Profiled",
                perf_summary['total_operations'],
                delta=f"{perf_summary['unique_operations']} unique"
            )
        
        with col4:
            data_files = ['data/pokemon.csv', 'data/national_dex.csv']
            existing = sum(1 for f in data_files if Path(f).exists())
            st.metric("Data Files", f"{existing}/{len(data_files)}")
        
        # System status
        st.markdown("---")
        st.subheader("🚦 System Status")
        
        status_col1, status_col2 = st.columns(2)
        
        with status_col1:
            # Error status
            critical_count = error_summary.get('by_severity', {}).get('CRITICAL', 0)
            if critical_count > 0:
                st.error(f"⚠️ {critical_count} critical errors detected")
            elif error_summary['total'] > 0:
                st.warning(f"⚠️ {error_summary['total']} errors logged")
            else:
                st.success("✅ No errors detected")
        
        with status_col2:
            # Backup status
            if backup_summary['total'] == 0:
                st.warning("⚠️ No backups created yet")
            else:
                st.success(f"✅ {backup_summary['total']} backups available")
        
    except Exception as e:
        st.error(f"Error loading system overview: {e}")


def render_error_logs():
    """Render error logs viewer"""
    st.header("🔍 Error Logs")
    
    try:
        logger = get_error_logger()
        
        # Summary
        summary = logger.get_error_summary()
        
        st.markdown(f"**Total Errors:** {summary['total']}")
        
        if summary['total'] == 0:
            st.success("✅ No errors logged")
            return
        
        # Display error breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**By Severity:**")
            for severity, count in summary['by_severity'].items():
                st.write(f"- {severity}: {count}")
        
        with col2:
            st.markdown("**By Type:**")
            for error_type, count in list(summary['by_type'].items())[:5]:
                st.write(f"- {error_type}: {count}")
        
        # Recent errors
        st.markdown("---")
        st.subheader("Recent Errors")
        
        recent_errors = logger.get_recent_errors(20)
        
        for error in recent_errors:
            with st.expander(f"{error['severity']}: {error['type']} - {error['timestamp']}"):
                st.markdown(f"**Message:** {error['message']}")
                if error['context']:
                    st.json(error['context'])
                if st.checkbox("Show traceback", key=f"tb_{error['timestamp']}"):
                    st.code(error['traceback'], language='python')
        
        # Export button
        if st.button("📄 Export Error Report"):
            report_path = logger.export_errors_report()
            st.success(f"Report exported to: {report_path}")
        
    except Exception as e:
        st.error(f"Error loading error logs: {e}")


def render_data_validation():
    """Render data validation interface"""
    st.header("✅ Data Validation")
    
    try:
        validator = DataValidator()
        
        st.markdown("Validate data integrity and check for issues")
        
        # Validation options
        validate_option = st.radio(
            "Select validation type:",
            ["Validate All Data Files", "Validate Specific File", "Custom Validation"]
        )
        
        if validate_option == "Validate All Data Files":
            if st.button("🔍 Run Full Validation"):
                with st.spinner("Validating all data files..."):
                    results = validator.validate_all_data_files()
                    
                    st.success(f"Validation complete: {results['valid']}/{results['total']} files valid")
                    
                    for file_report in results['files']:
                        status = "✅" if file_report['is_valid'] else "❌"
                        with st.expander(f"{status} {Path(file_report['file']).name}"):
                            if file_report['errors']:
                                st.error("**Errors:**")
                                for error in file_report['errors']:
                                    st.write(f"- {error}")
                            
                            if file_report['warnings']:
                                st.warning("**Warnings:**")
                                for warning in file_report['warnings']:
                                    st.write(f"- {warning}")
                            
                            if file_report['statistics']:
                                st.info("**Statistics:**")
                                st.json(file_report['statistics'])
                    
                    # Export button
                    if st.button("📄 Export Validation Report"):
                        report_path = validator.generate_validation_report()
                        st.success(f"Report exported to: {report_path}")
        
        elif validate_option == "Validate Specific File":
            file_path = st.text_input("File path:", "data/pokemon.csv")
            
            if st.button("🔍 Validate File"):
                if Path(file_path).exists():
                    with st.spinner(f"Validating {file_path}..."):
                        # Determine validation type
                        if 'pokemon' in file_path.lower():
                            is_valid, report = validator.validate_pokemon_csv(file_path)
                        else:
                            is_valid, report = validator.validate_csv(file_path, [])
                        
                        if is_valid:
                            st.success("✅ File is valid")
                        else:
                            st.error("❌ Validation failed")
                        
                        # Show report
                        if report['errors']:
                            st.error("**Errors:**")
                            for error in report['errors']:
                                st.write(f"- {error}")
                        
                        if report['warnings']:
                            st.warning("**Warnings:**")
                            for warning in report['warnings']:
                                st.write(f"- {warning}")
                        
                        if report['statistics']:
                            st.info("**Statistics:**")
                            st.json(report['statistics'])
                else:
                    st.error(f"File not found: {file_path}")
        
    except Exception as e:
        st.error(f"Error in data validation: {e}")


def render_backups():
    """Render backup management interface"""
    st.header("💾 Backup Management")
    
    try:
        manager = BackupManager()
        
        # Backup summary
        summary = manager.get_backup_summary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Backups", summary['total'])
        with col2:
            st.metric("Total Size", f"{summary['total_size_mb']} MB")
        with col3:
            if summary['newest']:
                st.metric("Last Backup", summary['newest'][:10])
        
        st.markdown("---")
        
        # Create backup section
        st.subheader("Create New Backup")
        
        backup_type = st.radio(
            "Backup type:",
            ["Full Backup", "Data Files Only", "Config Files Only", "Custom"]
        )
        
        if st.button("📦 Create Backup"):
            with st.spinner("Creating backup..."):
                try:
                    if backup_type == "Full Backup":
                        result = manager.full_backup()
                        st.success(f"✅ Full backup created")
                        st.json(result)
                    elif backup_type == "Data Files Only":
                        path = manager.backup_data_files()
                        st.success(f"✅ Data backup created: {Path(path).name}")
                    elif backup_type == "Config Files Only":
                        path = manager.backup_config_files()
                        st.success(f"✅ Config backup created: {Path(path).name}")
                except Exception as e:
                    st.error(f"Backup failed: {e}")
        
        # List existing backups
        st.markdown("---")
        st.subheader("Existing Backups")
        
        backups = manager.list_backups()
        
        if not backups:
            st.info("No backups found")
        else:
            for backup in backups[:10]:
                with st.expander(f"📦 {backup['backup_name']}"):
                    st.write(f"**Time:** {backup['timestamp']}")
                    st.write(f"**Size:** {round(backup.get('size_bytes', 0) / (1024*1024), 2)} MB")
                    st.write(f"**Compressed:** {'Yes' if backup.get('compressed') else 'No'}")
                    st.write(f"**Files:** {len(backup['files'])}")
        
        # Cleanup section
        st.markdown("---")
        st.subheader("Maintenance")
        
        keep_count = st.number_input("Keep most recent backups:", min_value=5, max_value=100, value=20)
        
        if st.button("🧹 Clean Old Backups"):
            with st.spinner("Cleaning old backups..."):
                manager.clean_old_backups(keep_count=keep_count)
                st.success(f"✅ Cleaned! Kept {keep_count} most recent backups")
        
    except Exception as e:
        st.error(f"Error in backup management: {e}")


def render_performance():
    """Render performance monitoring interface"""
    st.header("⚡ Performance Monitoring")
    
    try:
        profiler = get_profiler()
        
        # System info
        sys_info = profiler.get_system_info()
        
        st.subheader("System Resources")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("CPU Usage", f"{sys_info['cpu_percent']}%")
        with col2:
            st.metric("Memory Usage", f"{sys_info['memory_mb']} MB")
        with col3:
            st.metric("Threads", sys_info['num_threads'])
        
        # Performance summary
        st.markdown("---")
        st.subheader("Performance Summary")
        
        summary = profiler.get_performance_summary()
        
        if summary['total_operations'] == 0:
            st.info("No operations profiled yet")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Operations", summary['total_operations'])
            st.metric("Unique Operations", summary['unique_operations'])
            st.metric("Average Duration", f"{summary['avg_duration']}s")
        
        with col2:
            st.metric("Total Time", f"{summary['total_time']}s")
            if 'slowest_operation' in summary:
                st.write(f"**Slowest:** {summary['slowest_operation']}")
            if 'fastest_operation' in summary:
                st.write(f"**Fastest:** {summary['fastest_operation']}")
        
        # Slowest operations
        st.markdown("---")
        st.subheader("Slowest Operations (Top 10)")
        
        slowest = profiler.get_slowest_operations(10)
        
        for op in slowest:
            st.write(f"**{op['operation']}** - {op['duration_seconds']}s (Memory: {op['memory_delta_mb']} MB)")
        
        # Export report
        if st.button("📄 Export Performance Report"):
            report_path = profiler.export_performance_report()
            st.success(f"Report exported to: {report_path}")
        
    except Exception as e:
        st.error(f"Error in performance monitoring: {e}")


if __name__ == "__main__":
    render_admin_dashboard()
