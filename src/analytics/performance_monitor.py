"""
Performance Monitoring System
Tracks app usage, performance metrics, and user analytics
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go


class PerformanceMonitor:
    """Monitor and track application performance metrics"""
    
    def __init__(self, metrics_file: str = "data/analytics/metrics.json"):
        """Initialize performance monitor"""
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.session_start = time.time()
        self.page_loads = {}
        self.feature_usage = {}
        
    def load_metrics(self) -> Dict:
        """Load existing metrics from file"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return self._create_empty_metrics()
        return self._create_empty_metrics()
    
    def _create_empty_metrics(self) -> Dict:
        """Create empty metrics structure"""
        return {
            'sessions': [],
            'page_views': {},
            'feature_usage': {},
            'performance': [],
            'errors': [],
            'search_queries': [],
            'exports': [],
            'last_updated': datetime.now().isoformat()
        }
    
    def save_metrics(self, metrics: Dict):
        """Save metrics to file"""
        try:
            metrics['last_updated'] = datetime.now().isoformat()
            with open(self.metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)
        except Exception as e:
            st.warning(f"Could not save metrics: {e}")
    
    def track_session(self):
        """Track a new session"""
        metrics = self.load_metrics()
        
        session_data = {
            'session_id': st.session_state.get('session_id', str(time.time())),
            'start_time': datetime.now().isoformat(),
            'user_agent': st.session_state.get('user_agent', 'unknown'),
            'duration': 0
        }
        
        metrics['sessions'].append(session_data)
        self.save_metrics(metrics)
    
    def track_page_view(self, page_name: str):
        """Track page/tab view"""
        metrics = self.load_metrics()
        
        if page_name not in metrics['page_views']:
            metrics['page_views'][page_name] = 0
        
        metrics['page_views'][page_name] += 1
        self.save_metrics(metrics)
    
    def track_feature_usage(self, feature_name: str, details: Optional[Dict] = None):
        """Track feature usage"""
        metrics = self.load_metrics()
        
        if feature_name not in metrics['feature_usage']:
            metrics['feature_usage'][feature_name] = {
                'count': 0,
                'last_used': None,
                'details': []
            }
        
        metrics['feature_usage'][feature_name]['count'] += 1
        metrics['feature_usage'][feature_name]['last_used'] = datetime.now().isoformat()
        
        if details:
            metrics['feature_usage'][feature_name]['details'].append({
                'timestamp': datetime.now().isoformat(),
                **details
            })
        
        self.save_metrics(metrics)
    
    def track_performance(self, operation: str, duration: float, success: bool = True):
        """Track performance metrics"""
        metrics = self.load_metrics()
        
        perf_data = {
            'operation': operation,
            'duration': duration,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        
        metrics['performance'].append(perf_data)
        
        # Keep only last 1000 performance entries
        if len(metrics['performance']) > 1000:
            metrics['performance'] = metrics['performance'][-1000:]
        
        self.save_metrics(metrics)
    
    def track_error(self, error_type: str, error_message: str, context: Optional[Dict] = None):
        """Track errors"""
        metrics = self.load_metrics()
        
        error_data = {
            'type': error_type,
            'message': error_message,
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        
        metrics['errors'].append(error_data)
        
        # Keep only last 500 errors
        if len(metrics['errors']) > 500:
            metrics['errors'] = metrics['errors'][-500:]
        
        self.save_metrics(metrics)
    
    def track_search(self, query: str, results_count: int):
        """Track search queries"""
        metrics = self.load_metrics()
        
        search_data = {
            'query': query,
            'results': results_count,
            'timestamp': datetime.now().isoformat()
        }
        
        metrics['search_queries'].append(search_data)
        
        # Keep only last 500 searches
        if len(metrics['search_queries']) > 500:
            metrics['search_queries'] = metrics['search_queries'][-500:]
        
        self.save_metrics(metrics)
    
    def track_export(self, format_type: str, rows: int, columns: int):
        """Track data exports"""
        metrics = self.load_metrics()
        
        export_data = {
            'format': format_type,
            'rows': rows,
            'columns': columns,
            'timestamp': datetime.now().isoformat()
        }
        
        metrics['exports'].append(export_data)
        self.save_metrics(metrics)
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics"""
        metrics = self.load_metrics()
        
        return {
            'total_sessions': len(metrics['sessions']),
            'total_page_views': sum(metrics['page_views'].values()),
            'total_features_used': sum([f['count'] for f in metrics['feature_usage'].values()]),
            'total_searches': len(metrics['search_queries']),
            'total_exports': len(metrics['exports']),
            'total_errors': len(metrics['errors']),
            'avg_performance': self._calculate_avg_performance(metrics['performance'])
        }
    
    def _calculate_avg_performance(self, perf_data: List[Dict]) -> float:
        """Calculate average performance"""
        if not perf_data:
            return 0.0
        
        durations = [p['duration'] for p in perf_data if p['success']]
        return sum(durations) / len(durations) if durations else 0.0
    
    def render_dashboard(self):
        """Render analytics dashboard"""
        st.title("📊 Performance Analytics Dashboard")
        st.markdown("Monitor app usage, performance, and user behavior")
        
        metrics = self.load_metrics()
        
        if not metrics['sessions'] and not metrics['page_views']:
            st.info("No analytics data available yet. Start using the app to collect data!")
            return
        
        # Summary cards
        st.markdown("### 📈 Overview")
        summary = self.get_summary_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sessions", summary['total_sessions'])
        with col2:
            st.metric("Page Views", summary['total_page_views'])
        with col3:
            st.metric("Feature Uses", summary['total_features_used'])
        with col4:
            st.metric("Avg Load Time", f"{summary['avg_performance']:.2f}s")
        
        # Page views chart
        st.markdown("---")
        st.markdown("### 📄 Most Popular Pages")
        
        if metrics['page_views']:
            page_df = pd.DataFrame([
                {'Page': page, 'Views': count}
                for page, count in metrics['page_views'].items()
            ]).sort_values('Views', ascending=False)
            
            fig = px.bar(
                page_df.head(10),
                x='Page',
                y='Views',
                title="Top 10 Most Viewed Pages",
                color='Views',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Feature usage
        st.markdown("---")
        st.markdown("### 🎯 Feature Usage")
        
        if metrics['feature_usage']:
            feature_df = pd.DataFrame([
                {'Feature': feature, 'Uses': data['count'], 
                 'Last Used': data['last_used']}
                for feature, data in metrics['feature_usage'].items()
            ]).sort_values('Uses', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    feature_df.head(8),
                    values='Uses',
                    names='Feature',
                    title="Feature Usage Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(feature_df, hide_index=True, use_container_width=True)
        
        # Performance metrics
        st.markdown("---")
        st.markdown("### ⚡ Performance Metrics")
        
        if metrics['performance']:
            perf_df = pd.DataFrame(metrics['performance'])
            perf_df['timestamp'] = pd.to_datetime(perf_df['timestamp'])
            
            # Group by operation
            perf_summary = perf_df.groupby('operation')['duration'].agg([
                'mean', 'median', 'min', 'max', 'count'
            ]).round(3)
            
            st.dataframe(
                perf_summary.sort_values('mean', ascending=False),
                use_container_width=True
            )
            
            # Performance over time
            fig = px.line(
                perf_df.tail(100),
                x='timestamp',
                y='duration',
                color='operation',
                title="Performance Trend (Last 100 Operations)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Search analytics
        st.markdown("---")
        st.markdown("### 🔍 Search Analytics")
        
        if metrics['search_queries']:
            search_df = pd.DataFrame(metrics['search_queries'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Searches", len(search_df))
                avg_results = search_df['results'].mean()
                st.metric("Avg Results per Search", f"{avg_results:.1f}")
            
            with col2:
                # Top searches
                top_searches = search_df['query'].value_counts().head(10)
                st.markdown("**Top Search Queries:**")
                for query, count in top_searches.items():
                    st.markdown(f"- {query}: {count} times")
        
        # Export analytics
        st.markdown("---")
        st.markdown("### 📤 Export Analytics")
        
        if metrics['exports']:
            export_df = pd.DataFrame(metrics['exports'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                format_counts = export_df['format'].value_counts()
                fig = px.bar(
                    x=format_counts.index,
                    y=format_counts.values,
                    title="Exports by Format",
                    labels={'x': 'Format', 'y': 'Count'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("Total Exports", len(export_df))
                st.metric("Total Rows Exported", export_df['rows'].sum())
                st.metric("Avg Rows per Export", f"{export_df['rows'].mean():.0f}")
        
        # Error tracking
        st.markdown("---")
        st.markdown("### ⚠️ Error Tracking")
        
        if metrics['errors']:
            error_df = pd.DataFrame(metrics['errors'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Errors", len(error_df))
                error_types = error_df['type'].value_counts()
                st.markdown("**Error Types:**")
                for error_type, count in error_types.items():
                    st.markdown(f"- {error_type}: {count}")
            
            with col2:
                st.markdown("**Recent Errors:**")
                recent_errors = error_df.tail(5)
                for _, error in recent_errors.iterrows():
                    st.error(f"{error['type']}: {error['message']}")


def main():
    """Main function for standalone testing"""
    st.set_page_config(page_title="Performance Monitor", layout="wide")
    
    monitor = PerformanceMonitor()
    monitor.render_dashboard()


if __name__ == "__main__":
    main()
