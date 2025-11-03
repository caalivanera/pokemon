"""
Comprehensive Test Suite for Pokemon Dashboard v5.4.3
Includes: Syntax validation, import checks, data validation, stress tests
"""

import os
import sys
import ast
import importlib
import json
import csv
import traceback
from pathlib import Path
from typing import Dict, List, Tuple, Any
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestResult:
    """Store test results"""
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
        self.errors = []
    
    def add_pass(self, test_name: str, message: str = ""):
        self.passed.append((test_name, message))
    
    def add_fail(self, test_name: str, message: str, error: str = ""):
        self.failed.append((test_name, message, error))
    
    def add_warning(self, test_name: str, message: str):
        self.warnings.append((test_name, message))
    
    def add_error(self, test_name: str, error: str):
        self.errors.append((test_name, error))
    
    def print_summary(self):
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"✅ PASSED: {len(self.passed)}")
        print(f"❌ FAILED: {len(self.failed)}")
        print(f"⚠️  WARNINGS: {len(self.warnings)}")
        print(f"🔥 ERRORS: {len(self.errors)}")
        print("="*80)
        
        if self.failed:
            print("\n❌ FAILED TESTS:")
            for test_name, message, error in self.failed:
                print(f"  - {test_name}: {message}")
                if error:
                    print(f"    Error: {error[:200]}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for test_name, message in self.warnings:
                print(f"  - {test_name}: {message}")
        
        if self.errors:
            print("\n🔥 ERRORS:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error[:200]}")

class ComprehensiveTestSuite:
    """Comprehensive testing and validation suite"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = Path(base_path)
        self.results = TestResult()
    
    # ==========================================================================
    # SYNTAX AND IMPORT VALIDATION
    # ==========================================================================
    
    def test_python_syntax(self) -> None:
        """Test all Python files for syntax errors"""
        print("\n🔍 Testing Python syntax...")
        python_files = list(self.base_path.rglob("*.py"))
        
        for py_file in python_files:
            # Skip venv and cache
            if any(skip in str(py_file) for skip in ['.venv', '__pycache__', 'venv', 'env']):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                ast.parse(code)
                self.results.add_pass(f"Syntax: {py_file.name}", "Valid syntax")
            except SyntaxError as e:
                self.results.add_fail(
                    f"Syntax: {py_file.name}",
                    f"Syntax error at line {e.lineno}",
                    str(e)
                )
            except Exception as e:
                self.results.add_error(f"Syntax: {py_file.name}", str(e))
    
    def test_imports(self) -> None:
        """Test critical imports"""
        print("\n🔍 Testing imports...")
        
        critical_imports = [
            ('streamlit', 'streamlit'),
            ('pandas', 'pandas'),
            ('numpy', 'numpy'),
            ('plotly', 'plotly.express'),
            ('sklearn', 'sklearn'),
            ('networkx', 'networkx'),
        ]
        
        for name, module in critical_imports:
            try:
                importlib.import_module(module)
                self.results.add_pass(f"Import: {name}", "Successfully imported")
            except ImportError as e:
                self.results.add_fail(f"Import: {name}", "Import failed", str(e))
            except Exception as e:
                self.results.add_error(f"Import: {name}", str(e))
    
    def test_feature_imports(self) -> None:
        """Test feature module imports"""
        print("\n🔍 Testing feature module imports...")
        
        feature_modules = [
            'features.favorites_manager',
            'features.evolution_visualizer',
            'features.similar_pokemon_finder',
            'features.user_preferences',
        ]
        
        for module in feature_modules:
            try:
                importlib.import_module(module)
                self.results.add_pass(f"Feature: {module}", "Successfully imported")
            except ImportError as e:
                self.results.add_fail(f"Feature: {module}", "Import failed", str(e))
            except Exception as e:
                self.results.add_error(f"Feature: {module}", str(e))
    
    # ==========================================================================
    # DATA VALIDATION
    # ==========================================================================
    
    def test_csv_data(self) -> None:
        """Validate CSV data files"""
        print("\n🔍 Testing CSV data files...")
        
        csv_files = list(self.base_path.rglob("*.csv"))
        
        for csv_file in csv_files:
            if 'venv' in str(csv_file) or '.venv' in str(csv_file):
                continue
            
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    
                    if len(rows) == 0:
                        self.results.add_warning(f"CSV: {csv_file.name}", "Empty file")
                    else:
                        self.results.add_pass(
                            f"CSV: {csv_file.name}",
                            f"Valid ({len(rows)} rows)"
                        )
            except Exception as e:
                self.results.add_fail(f"CSV: {csv_file.name}", "Validation failed", str(e))
    
    def test_json_data(self) -> None:
        """Validate JSON data files"""
        print("\n🔍 Testing JSON data files...")
        
        json_files = list(self.base_path.rglob("*.json"))
        
        for json_file in json_files:
            if 'venv' in str(json_file) or '.venv' in str(json_file) or 'node_modules' in str(json_file):
                continue
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.results.add_pass(
                        f"JSON: {json_file.name}",
                        f"Valid JSON"
                    )
            except json.JSONDecodeError as e:
                self.results.add_fail(
                    f"JSON: {json_file.name}",
                    f"Invalid JSON at line {e.lineno}",
                    str(e)
                )
            except Exception as e:
                self.results.add_error(f"JSON: {json_file.name}", str(e))
    
    def test_requirements(self) -> None:
        """Validate requirements.txt"""
        print("\n🔍 Testing requirements.txt...")
        
        req_file = self.base_path / "requirements.txt"
        
        if not req_file.exists():
            self.results.add_fail("requirements.txt", "File not found", "")
            return
        
        try:
            with open(req_file, 'r') as f:
                lines = f.readlines()
            
            packages = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    packages.append(line)
            
            # Check critical packages
            critical = ['streamlit', 'pandas', 'numpy', 'plotly', 'networkx', 'scikit-learn']
            missing = []
            
            for pkg in critical:
                found = any(pkg in line.lower() for line in packages)
                if not found:
                    missing.append(pkg)
            
            if missing:
                self.results.add_fail(
                    "requirements.txt",
                    f"Missing critical packages: {', '.join(missing)}",
                    ""
                )
            else:
                self.results.add_pass(
                    "requirements.txt",
                    f"All critical packages present ({len(packages)} total)"
                )
        
        except Exception as e:
            self.results.add_error("requirements.txt", str(e))
    
    # ==========================================================================
    # STRESS TESTS
    # ==========================================================================
    
    def test_memory_usage(self) -> None:
        """Test memory usage with large datasets"""
        print("\n🔍 Testing memory usage...")
        
        try:
            import psutil
            process = psutil.Process()
            
            # Get initial memory
            mem_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Simulate loading data
            import pandas as pd
            import numpy as np
            
            # Create large dataframe
            df = pd.DataFrame({
                'id': range(10000),
                'name': ['Pokemon_' + str(i) for i in range(10000)],
                'hp': np.random.randint(1, 255, 10000),
                'attack': np.random.randint(1, 255, 10000),
            })
            
            # Get memory after
            mem_after = process.memory_info().rss / 1024 / 1024  # MB
            mem_used = mem_after - mem_before
            
            if mem_used < 100:  # Less than 100MB
                self.results.add_pass(
                    "Memory Test",
                    f"Memory usage acceptable: {mem_used:.2f} MB"
                )
            elif mem_used < 500:
                self.results.add_warning(
                    "Memory Test",
                    f"Memory usage moderate: {mem_used:.2f} MB"
                )
            else:
                self.results.add_fail(
                    "Memory Test",
                    f"Memory usage high: {mem_used:.2f} MB",
                    ""
                )
        
        except ImportError:
            self.results.add_warning("Memory Test", "psutil not installed, skipping")
        except Exception as e:
            self.results.add_error("Memory Test", str(e))
    
    def test_performance(self) -> None:
        """Test performance of critical operations"""
        print("\n🔍 Testing performance...")
        
        try:
            import pandas as pd
            import numpy as np
            
            # Test 1: DataFrame operations
            start = time.time()
            df = pd.DataFrame({
                'a': range(100000),
                'b': np.random.rand(100000),
            })
            filtered = df[df['b'] > 0.5]
            elapsed = time.time() - start
            
            if elapsed < 1.0:
                self.results.add_pass(
                    "Performance: DataFrame ops",
                    f"Fast: {elapsed:.3f}s"
                )
            else:
                self.results.add_warning(
                    "Performance: DataFrame ops",
                    f"Slow: {elapsed:.3f}s"
                )
            
            # Test 2: NumPy operations
            start = time.time()
            arr = np.random.rand(1000000)
            result = np.sqrt(arr) + np.sin(arr)
            elapsed = time.time() - start
            
            if elapsed < 0.5:
                self.results.add_pass(
                    "Performance: NumPy ops",
                    f"Fast: {elapsed:.3f}s"
                )
            else:
                self.results.add_warning(
                    "Performance: NumPy ops",
                    f"Slow: {elapsed:.3f}s"
                )
        
        except Exception as e:
            self.results.add_error("Performance Test", str(e))
    
    # ==========================================================================
    # FEATURE TESTS
    # ==========================================================================
    
    def test_favorites_manager(self) -> None:
        """Test Favorites Manager functionality"""
        print("\n🔍 Testing Favorites Manager...")
        
        try:
            from features.favorites_manager import (
                add_to_favorites,
                is_favorite,
                get_favorites,
                remove_from_favorites
            )
            
            # Clear state
            import streamlit as st
            if 'favorites' in st.session_state:
                del st.session_state['favorites']
            
            # Test add
            add_to_favorites(1, "Bulbasaur")
            if is_favorite(1):
                self.results.add_pass("Favorites: Add", "Successfully added")
            else:
                self.results.add_fail("Favorites: Add", "Failed to add", "")
            
            # Test get
            favs = get_favorites()
            if len(favs) == 1:
                self.results.add_pass("Favorites: Get", "Correct count")
            else:
                self.results.add_fail("Favorites: Get", f"Wrong count: {len(favs)}", "")
            
            # Test remove
            remove_from_favorites(1)
            if not is_favorite(1):
                self.results.add_pass("Favorites: Remove", "Successfully removed")
            else:
                self.results.add_fail("Favorites: Remove", "Failed to remove", "")
        
        except ImportError as e:
            self.results.add_warning("Favorites Manager", f"Could not import: {e}")
        except Exception as e:
            self.results.add_error("Favorites Manager", str(e))
    
    def test_similar_pokemon_finder(self) -> None:
        """Test Similar Pokemon Finder"""
        print("\n🔍 Testing Similar Pokemon Finder...")
        
        try:
            from features.similar_pokemon_finder import (
                calculate_stat_similarity,
                calculate_type_similarity,
                classify_role
            )
            
            # Test stat similarity
            stats1 = [100, 100, 100, 100, 100, 100]
            stats2 = [90, 90, 90, 90, 90, 90]
            similarity = calculate_stat_similarity(stats1, stats2)
            
            if 0 <= similarity <= 100:
                self.results.add_pass(
                    "Similarity: Stats",
                    f"Valid similarity score: {similarity:.2f}"
                )
            else:
                self.results.add_fail(
                    "Similarity: Stats",
                    f"Invalid score: {similarity}",
                    ""
                )
            
            # Test type similarity
            types1 = ['Fire', 'Flying']
            types2 = ['Fire', 'Dragon']
            type_sim = calculate_type_similarity(types1, types2)
            
            if 0 <= type_sim <= 1:
                self.results.add_pass(
                    "Similarity: Types",
                    f"Valid type similarity: {type_sim:.2f}"
                )
            else:
                self.results.add_fail(
                    "Similarity: Types",
                    f"Invalid score: {type_sim}",
                    ""
                )
            
            # Test role classification
            role = classify_role(stats1)
            if role in ['Physical Attacker', 'Special Attacker', 'Tank', 
                       'Physical Wall', 'Special Wall', 'Speedster', 'Balanced']:
                self.results.add_pass("Similarity: Role", f"Valid role: {role}")
            else:
                self.results.add_fail("Similarity: Role", f"Invalid role: {role}", "")
        
        except ImportError as e:
            self.results.add_warning("Similar Pokemon Finder", f"Could not import: {e}")
        except Exception as e:
            self.results.add_error("Similar Pokemon Finder", str(e))
    
    # ==========================================================================
    # RUN ALL TESTS
    # ==========================================================================
    
    def run_all_tests(self) -> TestResult:
        """Run all tests"""
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST SUITE - Pokemon Dashboard v5.4.3")
        print("="*80)
        
        # Syntax and Import Tests
        self.test_python_syntax()
        self.test_imports()
        self.test_feature_imports()
        
        # Data Validation Tests
        self.test_csv_data()
        self.test_json_data()
        self.test_requirements()
        
        # Performance Tests
        self.test_memory_usage()
        self.test_performance()
        
        # Feature Tests
        self.test_favorites_manager()
        self.test_similar_pokemon_finder()
        
        # Print summary
        self.results.print_summary()
        
        return self.results

def main():
    """Main entry point"""
    suite = ComprehensiveTestSuite()
    results = suite.run_all_tests()
    
    # Save results to file
    output_file = Path(__file__).parent.parent / "TEST_RESULTS.txt"
    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("COMPREHENSIVE TEST RESULTS\n")
        f.write("="*80 + "\n\n")
        f.write(f"PASSED: {len(results.passed)}\n")
        f.write(f"FAILED: {len(results.failed)}\n")
        f.write(f"WARNINGS: {len(results.warnings)}\n")
        f.write(f"ERRORS: {len(results.errors)}\n\n")
        
        if results.failed:
            f.write("\nFAILED TESTS:\n")
            for test_name, message, error in results.failed:
                f.write(f"  - {test_name}: {message}\n")
                if error:
                    f.write(f"    {error}\n")
        
        if results.warnings:
            f.write("\nWARNINGS:\n")
            for test_name, message in results.warnings:
                f.write(f"  - {test_name}: {message}\n")
    
    print(f"\n✅ Results saved to: {output_file}")
    
    # Exit with appropriate code
    sys.exit(0 if len(results.failed) == 0 else 1)

if __name__ == "__main__":
    main()
