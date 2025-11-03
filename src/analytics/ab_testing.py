"""
A/B Testing Framework for Pokemon Dashboard
Enables feature variations and metrics tracking
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib

class ABTestManager:
    """Manage A/B tests for features"""
    
    def __init__(self):
        self.test_config_file = Path("config/ab_tests.json")
        self.results_file = Path("data/ab_test_results.json")
        self._init_session_state()
        self._load_config()
    
    def _init_session_state(self):
        """Initialize session state for A/B testing"""
        if 'ab_test_variant' not in st.session_state:
            st.session_state.ab_test_variant = {}
        if 'ab_test_metrics' not in st.session_state:
            st.session_state.ab_test_metrics = []
    
    def _load_config(self):
        """Load A/B test configuration"""
        if self.test_config_file.exists():
            with open(self.test_config_file) as f:
                self.config = json.load(f)
        else:
            self.config = self._get_default_config()
            self._save_config()
    
    def _save_config(self):
        """Save A/B test configuration"""
        self.test_config_file.parent.mkdir(exist_ok=True)
        with open(self.test_config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _get_default_config(self) -> Dict:
        """Get default A/B test configuration"""
        return {
            "tests": {
                "favorites_ui": {
                    "name": "Favorites UI Variants",
                    "active": True,
                    "variants": {
                        "A": {"name": "Heart Icon", "weight": 0.5},
                        "B": {"name": "Star Icon", "weight": 0.5}
                    },
                    "metrics": ["click_rate", "conversion_rate", "time_to_favorite"]
                },
                "similarity_algorithm": {
                    "name": "Similarity Algorithm Variants",
                    "active": True,
                    "variants": {
                        "A": {"name": "Euclidean", "weight": 0.33},
                        "B": {"name": "Cosine", "weight": 0.33},
                        "C": {"name": "Hybrid", "weight": 0.34}
                    },
                    "metrics": ["user_satisfaction", "result_clicks", "time_on_page"]
                },
                "evolution_layout": {
                    "name": "Evolution Graph Layout",
                    "active": True,
                    "variants": {
                        "A": {"name": "Horizontal", "weight": 0.5},
                        "B": {"name": "Vertical", "weight": 0.5}
                    },
                    "metrics": ["graph_interactions", "zoom_events", "hover_time"]
                },
                "preferences_tabs": {
                    "name": "Preferences Organization",
                    "active": False,
                    "variants": {
                        "A": {"name": "Tabbed", "weight": 0.5},
                        "B": {"name": "Accordion", "weight": 0.5}
                    },
                    "metrics": ["settings_changed", "time_in_settings", "completion_rate"]
                }
            }
        }
    
    def get_variant(self, test_name: str) -> str:
        """Get variant for a test"""
        # Check if user already has a variant assigned
        if test_name in st.session_state.ab_test_variant:
            return st.session_state.ab_test_variant[test_name]
        
        # Check if test exists and is active
        if test_name not in self.config["tests"]:
            return "A"  # Default variant
        
        test = self.config["tests"][test_name]
        if not test.get("active", False):
            return "A"  # Default variant
        
        # Assign variant based on user ID hash
        user_id = self._get_user_id()
        variant = self._assign_variant(test_name, user_id, test["variants"])
        
        # Store variant assignment
        st.session_state.ab_test_variant[test_name] = variant
        
        # Log assignment
        self._log_variant_assignment(test_name, variant)
        
        return variant
    
    def _get_user_id(self) -> str:
        """Get unique user ID"""
        # Use session ID as user ID
        if 'user_id' not in st.session_state:
            st.session_state.user_id = hashlib.md5(
                str(datetime.now().timestamp()).encode()
            ).hexdigest()[:16]
        return st.session_state.user_id
    
    def _assign_variant(self, test_name: str, user_id: str, 
                       variants: Dict[str, Dict]) -> str:
        """Assign variant based on user ID and weights"""
        # Create deterministic hash
        hash_input = f"{test_name}_{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        hash_percent = (hash_value % 100) / 100.0
        
        # Assign based on cumulative weights
        cumulative = 0.0
        for variant_id, variant_data in variants.items():
            cumulative += variant_data["weight"]
            if hash_percent <= cumulative:
                return variant_id
        
        return list(variants.keys())[0]  # Fallback to first variant
    
    def _log_variant_assignment(self, test_name: str, variant: str):
        """Log variant assignment"""
        self.track_event(test_name, "variant_assigned", {"variant": variant})
    
    def track_event(self, test_name: str, event_type: str, 
                   data: Optional[Dict] = None):
        """Track an A/B test event"""
        if test_name not in self.config["tests"]:
            return
        
        variant = st.session_state.ab_test_variant.get(test_name, "A")
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "user_id": self._get_user_id(),
            "test_name": test_name,
            "variant": variant,
            "event_type": event_type,
            "data": data or {}
        }
        
        st.session_state.ab_test_metrics.append(event)
    
    def save_metrics(self):
        """Save collected metrics to file"""
        if not st.session_state.ab_test_metrics:
            return
        
        self.results_file.parent.mkdir(exist_ok=True)
        
        # Load existing metrics
        existing_metrics = []
        if self.results_file.exists():
            with open(self.results_file) as f:
                existing_metrics = json.load(f)
        
        # Append new metrics
        all_metrics = existing_metrics + st.session_state.ab_test_metrics
        
        # Save
        with open(self.results_file, 'w') as f:
            json.dump(all_metrics, f, indent=2)
        
        # Clear session metrics
        st.session_state.ab_test_metrics = []
    
    def get_results(self, test_name: str) -> pd.DataFrame:
        """Get results for a test"""
        if not self.results_file.exists():
            return pd.DataFrame()
        
        with open(self.results_file) as f:
            metrics = json.load(f)
        
        # Filter for test
        test_metrics = [m for m in metrics if m["test_name"] == test_name]
        
        if not test_metrics:
            return pd.DataFrame()
        
        return pd.DataFrame(test_metrics)
    
    def analyze_test(self, test_name: str) -> Dict[str, Any]:
        """Analyze A/B test results"""
        df = self.get_results(test_name)
        
        if df.empty:
            return {"error": "No data available"}
        
        # Group by variant
        variants = df.groupby('variant').agg({
            'user_id': 'nunique',  # Unique users per variant
            'event_type': 'count'   # Total events per variant
        }).rename(columns={'user_id': 'unique_users', 'event_type': 'total_events'})
        
        # Calculate metrics
        analysis = {
            "test_name": test_name,
            "total_users": df['user_id'].nunique(),
            "total_events": len(df),
            "variants": variants.to_dict('index'),
            "event_types": df['event_type'].value_counts().to_dict(),
            "date_range": {
                "start": df['timestamp'].min(),
                "end": df['timestamp'].max()
            }
        }
        
        return analysis
    
    def create_admin_panel(self):
        """Create admin panel for A/B test management"""
        st.subheader("🧪 A/B Testing Dashboard")
        
        # Test overview
        col1, col2, col3 = st.columns(3)
        
        total_tests = len(self.config["tests"])
        active_tests = sum(1 for t in self.config["tests"].values() if t.get("active"))
        
        col1.metric("Total Tests", total_tests)
        col2.metric("Active Tests", active_tests)
        col3.metric("Inactive Tests", total_tests - active_tests)
        
        # Test list
        st.markdown("---")
        st.subheader("Active Tests")
        
        for test_id, test_data in self.config["tests"].items():
            if test_data.get("active"):
                with st.expander(f"📊 {test_data['name']}"):
                    st.write(f"**Test ID:** {test_id}")
                    st.write(f"**Status:** {'🟢 Active' if test_data['active'] else '🔴 Inactive'}")
                    
                    # Variants
                    st.write("**Variants:**")
                    for variant_id, variant_data in test_data["variants"].items():
                        st.write(f"  - {variant_id}: {variant_data['name']} (Weight: {variant_data['weight']*100:.1f}%)")
                    
                    # Metrics
                    st.write(f"**Tracked Metrics:** {', '.join(test_data['metrics'])}")
                    
                    # Results
                    if st.button(f"View Results", key=f"results_{test_id}"):
                        analysis = self.analyze_test(test_id)
                        if "error" not in analysis:
                            st.json(analysis)
                        else:
                            st.info("No data available yet")

# =============================================================================
# HELPER FUNCTIONS FOR FEATURE IMPLEMENTATIONS
# =============================================================================

def get_favorites_ui_variant() -> str:
    """Get UI variant for favorites feature"""
    ab_manager = ABTestManager()
    return ab_manager.get_variant("favorites_ui")

def track_favorite_click(pokemon_id: int, action: str):
    """Track favorite button click"""
    ab_manager = ABTestManager()
    ab_manager.track_event("favorites_ui", "favorite_click", {
        "pokemon_id": pokemon_id,
        "action": action
    })

def get_similarity_algorithm_variant() -> str:
    """Get algorithm variant for similarity search"""
    ab_manager = ABTestManager()
    return ab_manager.get_variant("similarity_algorithm")

def track_similarity_search(pokemon_id: int, results_count: int):
    """Track similarity search"""
    ab_manager = ABTestManager()
    ab_manager.track_event("similarity_algorithm", "search_performed", {
        "pokemon_id": pokemon_id,
        "results_count": results_count
    })

def get_evolution_layout_variant() -> str:
    """Get layout variant for evolution graph"""
    ab_manager = ABTestManager()
    return ab_manager.get_variant("evolution_layout")

def track_evolution_interaction(pokemon_id: int, interaction_type: str):
    """Track evolution graph interaction"""
    ab_manager = ABTestManager()
    ab_manager.track_event("evolution_layout", interaction_type, {
        "pokemon_id": pokemon_id
    })

# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example: Initialize A/B testing
    ab_manager = ABTestManager()
    
    # Get variant for favorites UI
    variant = ab_manager.get_variant("favorites_ui")
    print(f"Favorites UI Variant: {variant}")
    
    # Track event
    ab_manager.track_event("favorites_ui", "favorite_click", {
        "pokemon_id": 25,
        "action": "add"
    })
    
    # Save metrics
    ab_manager.save_metrics()
    
    # Analyze results
    analysis = ab_manager.analyze_test("favorites_ui")
    print(f"\nTest Analysis:")
    print(json.dumps(analysis, indent=2))
