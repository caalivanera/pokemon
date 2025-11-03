"""
Final Validation Report Generator
Creates comprehensive validation summary for Pokemon Dashboard v5.4.3
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class ValidationReport:
    """Generate comprehensive validation report"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "version": "5.4.3",
            "sections": {}
        }
    
    def count_files(self) -> Dict:
        """Count files by type"""
        counts = {
            "python": len(list(self.base_path.rglob("*.py"))),
            "markdown": len(list(self.base_path.rglob("*.md"))),
            "csv": len(list(self.base_path.rglob("*.csv"))),
            "json": len(list(self.base_path.rglob("*.json"))),
            "yml": len(list(self.base_path.rglob("*.yml"))),
        }
        return counts
    
    def check_critical_files(self) -> Dict:
        """Check existence of critical files"""
        critical = {
            "requirements.txt": (self.base_path / "requirements.txt").exists(),
            "README.md": (self.base_path / "README.md").exists(),
            ".gitignore": (self.base_path / ".gitignore").exists(),
            "src/core/app.py": (self.base_path / "src/core/app.py").exists(),
            "tests/comprehensive_test_suite.py": (
                self.base_path / "tests/comprehensive_test_suite.py"
            ).exists(),
            "tests/stress_tests.py": (
                self.base_path / "tests/stress_tests.py"
            ).exists(),
            ".github/workflows/ci-cd.yml": (
                self.base_path / ".github/workflows/ci-cd.yml"
            ).exists(),
        }
        return critical
    
    def check_feature_files(self) -> Dict:
        """Check v5.4.3 feature files"""
        features = {
            "favorites_manager.py": (
                self.base_path / "src/features/favorites_manager.py"
            ).exists(),
            "evolution_visualizer.py": (
                self.base_path / "src/features/evolution_visualizer.py"
            ).exists(),
            "similar_pokemon_finder.py": (
                self.base_path / "src/features/similar_pokemon_finder.py"
            ).exists(),
            "user_preferences.py": (
                self.base_path / "src/features/user_preferences.py"
            ).exists(),
        }
        return features
    
    def check_test_results(self) -> Dict:
        """Check test result files"""
        test_results = {}
        
        # Check TEST_RESULTS.txt
        test_file = self.base_path / "TEST_RESULTS.txt"
        if test_file.exists():
            with open(test_file, 'r') as f:
                content = f.read()
                test_results["comprehensive_tests"] = {
                    "exists": True,
                    "passed": "PASSED:" in content,
                    "failed": "FAILED:" in content,
                }
        else:
            test_results["comprehensive_tests"] = {"exists": False}
        
        # Check STRESS_TEST_RESULTS.json
        stress_file = self.base_path / "STRESS_TEST_RESULTS.json"
        if stress_file.exists():
            with open(stress_file, 'r') as f:
                data = json.load(f)
                test_results["stress_tests"] = {
                    "exists": True,
                    "summary": data.get("summary", {})
                }
        else:
            test_results["stress_tests"] = {"exists": False}
        
        return test_results
    
    def generate_report(self) -> Dict:
        """Generate full validation report"""
        print("\n" + "="*80)
        print("GENERATING VALIDATION REPORT")
        print("="*80)
        
        # File counts
        print("\n📊 Counting files...")
        file_counts = self.count_files()
        self.report["sections"]["file_counts"] = file_counts
        for file_type, count in file_counts.items():
            print(f"  {file_type}: {count}")
        
        # Critical files
        print("\n🔍 Checking critical files...")
        critical = self.check_critical_files()
        self.report["sections"]["critical_files"] = critical
        missing = [k for k, v in critical.items() if not v]
        if missing:
            print(f"  ❌ Missing: {', '.join(missing)}")
        else:
            print(f"  ✅ All critical files present")
        
        # Feature files
        print("\n✨ Checking v5.4.3 feature files...")
        features = self.check_feature_files()
        self.report["sections"]["feature_files"] = features
        missing_features = [k for k, v in features.items() if not v]
        if missing_features:
            print(f"  ❌ Missing: {', '.join(missing_features)}")
        else:
            print(f"  ✅ All feature files present")
        
        # Test results
        print("\n🧪 Checking test results...")
        test_results = self.check_test_results()
        self.report["sections"]["test_results"] = test_results
        
        return self.report
    
    def save_report(self, filename: str = "VALIDATION_REPORT.json"):
        """Save report to file"""
        report_file = self.base_path / filename
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"\n✅ Report saved to: {report_file}")
        return report_file
    
    def print_summary(self):
        """Print human-readable summary"""
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        
        file_counts = self.report["sections"]["file_counts"]
        print(f"\n📊 Project Size:")
        print(f"  Python files: {file_counts['python']}")
        print(f"  Markdown files: {file_counts['markdown']}")
        print(f"  Total files: {sum(file_counts.values())}")
        
        critical = self.report["sections"]["critical_files"]
        critical_ok = all(critical.values())
        print(f"\n🔍 Critical Files: {'✅ PASS' if critical_ok else '❌ FAIL'}")
        
        features = self.report["sections"]["feature_files"]
        features_ok = all(features.values())
        print(f"\n✨ Feature Files: {'✅ PASS' if features_ok else '❌ FAIL'}")
        
        print("\n" + "="*80)
        print("VALIDATION COMPLETE")
        print("="*80)

def main():
    """Main entry point"""
    report_gen = ValidationReport()
    report_gen.generate_report()
    report_gen.save_report()
    report_gen.print_summary()

if __name__ == "__main__":
    main()
