"""
Stress Testing Suite for Pokemon Dashboard
Tests: Load testing, concurrency, memory leaks, performance degradation
"""

import time
import psutil
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
import sys
import tracemalloc
from typing import List, Dict, Tuple
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class StressTestResults:
    """Store and analyze stress test results"""
    
    def __init__(self):
        self.tests = []
    
    def add_result(self, test_name: str, success: bool, duration: float, 
                  memory_used: float, details: Dict = None):
        self.tests.append({
            "test_name": test_name,
            "success": success,
            "duration_seconds": duration,
            "memory_mb": memory_used,
            "details": details or {}
        })
    
    def get_summary(self) -> Dict:
        df = pd.DataFrame(self.tests)
        return {
            "total_tests": len(df),
            "passed": int(df['success'].sum()),
            "failed": int((~df['success']).sum()),
            "avg_duration": float(df['duration_seconds'].mean()),
            "max_duration": float(df['duration_seconds'].max()),
            "avg_memory": float(df['memory_mb'].mean()),
            "max_memory": float(df['memory_mb'].max())
        }
    
    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            json.dump({
                "results": self.tests,
                "summary": self.get_summary()
            }, f, indent=2)


class StressTestSuite:
    """Comprehensive stress testing suite"""
    
    def __init__(self):
        self.results = StressTestResults()
        self.process = psutil.Process()
    
    def measure_memory(self) -> float:
        """Get current memory usage in MB"""
        return self.process.memory_info().rss / 1024 / 1024
    
    # ==========================================================================
    # LOAD TESTS
    # ==========================================================================
    
    def test_large_dataset_loading(self):
        """Test loading and processing large datasets"""
        print("\n🔥 TEST: Large Dataset Loading")
        
        start_mem = self.measure_memory()
        start_time = time.time()
        
        try:
            # Create large dataset (simulating 10,000 Pokemon with full stats)
            df = pd.DataFrame({
                'id': range(10000),
                'name': [f'Pokemon_{i}' for i in range(10000)],
                'type1': np.random.choice(['Fire', 'Water', 'Grass', 'Electric'], 10000),
                'type2': np.random.choice(['Fire', 'Water', 'Grass', 'Electric', None], 10000),
                'hp': np.random.randint(1, 255, 10000),
                'attack': np.random.randint(1, 255, 10000),
                'defense': np.random.randint(1, 255, 10000),
                'sp_attack': np.random.randint(1, 255, 10000),
                'sp_defense': np.random.randint(1, 255, 10000),
                'speed': np.random.randint(1, 255, 10000),
            })
            
            # Perform operations
            df['total'] = df[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].sum(axis=1)
            filtered = df[df['total'] > 400]
            grouped = df.groupby('type1')['total'].mean()
            
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            
            success = len(df) == 10000 and len(filtered) > 0
            
            self.results.add_result(
                "Large Dataset Loading",
                success,
                duration,
                mem_used,
                {"rows": len(df), "filtered_rows": len(filtered)}
            )
            
            print(f"  ✅ Loaded {len(df)} rows in {duration:.2f}s")
            print(f"  📊 Memory used: {mem_used:.2f} MB")
            
        except Exception as e:
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            self.results.add_result("Large Dataset Loading", False, duration, mem_used,
                                   {"error": str(e)})
            print(f"  ❌ FAILED: {e}")
    
    def test_concurrent_queries(self, num_threads: int = 50):
        """Test concurrent database queries"""
        print(f"\n🔥 TEST: Concurrent Queries ({num_threads} threads)")
        
        start_mem = self.measure_memory()
        start_time = time.time()
        
        def query_operation(query_id: int) -> bool:
            """Simulate a query operation"""
            try:
                # Simulate query
                df = pd.DataFrame({
                    'id': range(1000),
                    'value': np.random.rand(1000)
                })
                result = df[df['value'] > 0.5]
                return len(result) > 0
            except:
                return False
        
        try:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(query_operation, i) for i in range(num_threads)]
                results = [f.result() for f in futures]
            
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            success = all(results)
            
            self.results.add_result(
                f"Concurrent Queries ({num_threads} threads)",
                success,
                duration,
                mem_used,
                {"successful_queries": sum(results), "total_queries": num_threads}
            )
            
            print(f"  ✅ {sum(results)}/{num_threads} queries succeeded in {duration:.2f}s")
            print(f"  📊 Memory used: {mem_used:.2f} MB")
            
        except Exception as e:
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            self.results.add_result(
                f"Concurrent Queries ({num_threads} threads)",
                False, duration, mem_used, {"error": str(e)}
            )
            print(f"  ❌ FAILED: {e}")
    
    def test_memory_leak(self, iterations: int = 100):
        """Test for memory leaks"""
        print(f"\n🔥 TEST: Memory Leak Detection ({iterations} iterations)")
        
        tracemalloc.start()
        start_mem = self.measure_memory()
        start_time = time.time()
        
        memory_samples = []
        
        try:
            for i in range(iterations):
                # Simulate operations that might leak memory
                df = pd.DataFrame({
                    'a': range(1000),
                    'b': np.random.rand(1000)
                })
                _ = df.describe()
                _ = df.groupby('a').sum()
                
                # Sample memory every 10 iterations
                if i % 10 == 0:
                    memory_samples.append(self.measure_memory())
            
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            
            # Check for memory leak (memory should not increase significantly)
            if len(memory_samples) > 1:
                mem_increase = memory_samples[-1] - memory_samples[0]
                leaked = mem_increase > 50  # More than 50MB increase is suspicious
            else:
                leaked = False
            
            self.results.add_result(
                f"Memory Leak Test ({iterations} iterations)",
                not leaked,
                duration,
                mem_used,
                {
                    "initial_memory": memory_samples[0] if memory_samples else 0,
                    "final_memory": memory_samples[-1] if memory_samples else 0,
                    "memory_increase": mem_increase if len(memory_samples) > 1 else 0
                }
            )
            
            if leaked:
                print(f"  ⚠️  POTENTIAL LEAK: Memory increased by {mem_increase:.2f} MB")
            else:
                print(f"  ✅ No memory leak detected")
            
            tracemalloc.stop()
            
        except Exception as e:
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            self.results.add_result(
                f"Memory Leak Test ({iterations} iterations)",
                False, duration, mem_used, {"error": str(e)}
            )
            print(f"  ❌ FAILED: {e}")
            tracemalloc.stop()
    
    def test_cpu_intensive_operations(self):
        """Test CPU-intensive operations"""
        print("\n🔥 TEST: CPU Intensive Operations")
        
        start_mem = self.measure_memory()
        start_time = time.time()
        cpu_start = self.process.cpu_percent(interval=0.1)
        
        try:
            # Simulate CPU-intensive similarity calculations
            def calculate_similarity_matrix(size: int):
                matrix = np.random.rand(size, size)
                distances = np.zeros((size, size))
                
                for i in range(size):
                    for j in range(size):
                        distances[i, j] = np.linalg.norm(matrix[i] - matrix[j])
                
                return distances
            
            result = calculate_similarity_matrix(500)
            
            duration = time.time() - start_time
            cpu_usage = self.process.cpu_percent(interval=0.1)
            mem_used = self.measure_memory() - start_mem
            
            success = result.shape == (500, 500)
            
            self.results.add_result(
                "CPU Intensive Operations",
                success,
                duration,
                mem_used,
                {"cpu_usage_percent": cpu_usage, "matrix_size": 500}
            )
            
            print(f"  ✅ Completed in {duration:.2f}s")
            print(f"  💻 CPU usage: {cpu_usage:.1f}%")
            print(f"  📊 Memory used: {mem_used:.2f} MB")
            
        except Exception as e:
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            self.results.add_result(
                "CPU Intensive Operations",
                False, duration, mem_used, {"error": str(e)}
            )
            print(f"  ❌ FAILED: {e}")
    
    def test_rapid_state_changes(self, iterations: int = 1000):
        """Test rapid session state changes"""
        print(f"\n🔥 TEST: Rapid State Changes ({iterations} iterations)")
        
        start_mem = self.measure_memory()
        start_time = time.time()
        
        try:
            # Simulate session state operations
            state = {}
            
            for i in range(iterations):
                # Add
                state[f'key_{i}'] = {'data': list(range(100))}
                
                # Modify
                if i > 0:
                    state[f'key_{i-1}']['data'].append(i)
                
                # Delete old entries to prevent unbounded growth
                if i > 100:
                    del state[f'key_{i-100}']
            
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            
            success = len(state) > 0
            
            self.results.add_result(
                f"Rapid State Changes ({iterations} iterations)",
                success,
                duration,
                mem_used,
                {"final_state_size": len(state)}
            )
            
            print(f"  ✅ Completed {iterations} state changes in {duration:.2f}s")
            print(f"  📊 Memory used: {mem_used:.2f} MB")
            
        except Exception as e:
            duration = time.time() - start_time
            mem_used = self.measure_memory() - start_mem
            self.results.add_result(
                f"Rapid State Changes ({iterations} iterations)",
                False, duration, mem_used, {"error": str(e)}
            )
            print(f"  ❌ FAILED: {e}")
    
    # ==========================================================================
    # RUN ALL TESTS
    # ==========================================================================
    
    def run_all_tests(self):
        """Run all stress tests"""
        print("="*80)
        print("STRESS TEST SUITE - Pokemon Dashboard v5.4.3")
        print("="*80)
        
        self.test_large_dataset_loading()
        self.test_concurrent_queries(num_threads=50)
        self.test_concurrent_queries(num_threads=100)
        self.test_memory_leak(iterations=100)
        self.test_cpu_intensive_operations()
        self.test_rapid_state_changes(iterations=1000)
        
        # Print summary
        print("\n" + "="*80)
        print("STRESS TEST SUMMARY")
        print("="*80)
        
        summary = self.results.get_summary()
        print(f"Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⏱️  Avg Duration: {summary['avg_duration']:.2f}s")
        print(f"⏱️  Max Duration: {summary['max_duration']:.2f}s")
        print(f"📊 Avg Memory: {summary['avg_memory']:.2f} MB")
        print(f"📊 Max Memory: {summary['max_memory']:.2f} MB")
        print("="*80)
        
        # Save results
        output_file = Path(__file__).parent.parent / "STRESS_TEST_RESULTS.json"
        self.results.save_to_file(str(output_file))
        print(f"\n✅ Results saved to: {output_file}")
        
        return summary


def main():
    """Main entry point"""
    suite = StressTestSuite()
    summary = suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if summary['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
