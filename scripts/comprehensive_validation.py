#!/usr/bin/env python3
"""
Comprehensive Project Validation Script
Validates all aspects of the Pokemon Dashboard project
"""

import os
import sys
from pathlib import Path
import subprocess
from typing import List, Tuple, Dict

# ANSI colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{title:^60}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def check_pass(message: str):
    """Print a pass message."""
    print(f"{GREEN}✅ {message}{RESET}")


def check_fail(message: str):
    """Print a fail message."""
    print(f"{RED}❌ {message}{RESET}")


def check_warn(message: str):
    """Print a warning message."""
    print(f"{YELLOW}⚠️  {message}{RESET}")


def validate_directory_structure() -> bool:
    """Validate that all required directories exist."""
    print_section("Directory Structure Validation")
    
    required_dirs = [
        'src',
        'src/core',
        'src/data_loaders',
        'src/database',
        'tests',
        'data',
        'docs',
        'docs/guides',
        'docs/technical',
        'config',
        'config/docker',
        'config/github/workflows',
        'config/vscode',
        'scripts',
        '.streamlit'
    ]
    
    all_exist = True
    for directory in required_dirs:
        if Path(directory).exists():
            check_pass(f"Directory exists: {directory}")
        else:
            check_fail(f"Missing directory: {directory}")
            all_exist = False
    
    return all_exist


def validate_required_files() -> bool:
    """Validate that all required files exist."""
    print_section("Required Files Validation")
    
    required_files = {
        'Root Level': [
            'README.md',
            'requirements.txt',
            '.gitignore',
            'SECURITY.md',
            'CHANGELOG.md',
            'PROJECT_STRUCTURE.md'
        ],
        'Source Code': [
            'src/__init__.py',
            'src/core/__init__.py',
            'src/core/app.py',
            'src/data_loaders/__init__.py',
            'src/data_loaders/data_extractor.py',
            'src/data_loaders/yaml_loader.py',
            'src/database/__init__.py',
            'src/database/models.py',
            'src/database/connection.py',
            'src/database/data_loader.py'
        ],
        'Configuration': [
            '.streamlit/config.toml',
            'config/docker/Dockerfile',
            'config/docker/docker-compose.yml',
            'config/docker/.env.example',
            'config/github/workflows/ci.yml'
        ],
        'Data': [
            'data/pokedex.csv',
            'data/pokemon_glossary.csv',
            'data/poke_corpus.csv',
            'data/pokedex_otherVer.csv'
        ],
        'Tests': [
            'tests/__init__.py',
            'tests/test_enhanced_dashboard.py'
        ]
    }
    
    all_exist = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file_path in files:
            if Path(file_path).exists():
                check_pass(f"{file_path}")
            else:
                check_fail(f"Missing: {file_path}")
                all_exist = False
    
    return all_exist


def validate_git_tracking() -> bool:
    """Validate that all important files are tracked in git."""
    print_section("Git Tracking Validation")
    
    try:
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True,
            text=True,
            check=True
        )
        tracked_files = set(result.stdout.strip().split('\n'))
        
        check_pass(f"Found {len(tracked_files)} files tracked in git")
        
        # Check that important files are tracked
        important_files = [
            'src/core/app.py',
            'src/data_loaders/data_extractor.py',
            'requirements.txt',
            'README.md',
            'data/pokedex.csv'
        ]
        
        all_tracked = True
        for file_path in important_files:
            if file_path in tracked_files:
                check_pass(f"Tracked: {file_path}")
            else:
                check_fail(f"Not tracked: {file_path}")
                all_tracked = False
        
        # Check for untracked important files
        result = subprocess.run(
            ['git', 'status', '--short'],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            check_warn("There are uncommitted changes:")
            print(result.stdout)
        else:
            check_pass("All changes committed")
        
        return all_tracked
        
    except subprocess.CalledProcessError as e:
        check_fail(f"Git command failed: {e}")
        return False


def validate_python_syntax() -> bool:
    """Validate Python syntax for all Python files."""
    print_section("Python Syntax Validation")
    
    python_files = [
        'src/core/app.py',
        'src/data_loaders/data_extractor.py',
        'src/data_loaders/yaml_loader.py',
        'src/database/models.py',
        'src/database/connection.py',
        'src/database/data_loader.py',
        'tests/test_enhanced_dashboard.py'
    ]
    
    all_valid = True
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), file_path, 'exec')
            check_pass(f"Valid syntax: {file_path}")
        except SyntaxError as e:
            check_fail(f"Syntax error in {file_path}: {e}")
            all_valid = False
        except FileNotFoundError:
            check_fail(f"File not found: {file_path}")
            all_valid = False
    
    return all_valid


def validate_imports() -> bool:
    """Validate that critical imports work."""
    print_section("Import Validation")
    
    imports_to_test = [
        ('streamlit', 'Streamlit framework'),
        ('pandas', 'Pandas data analysis'),
        ('numpy', 'NumPy numerical computing'),
        ('yaml', 'YAML file parsing'),
        ('sqlalchemy', 'SQLAlchemy ORM'),
        ('plotly', 'Plotly visualization'),
    ]
    
    all_valid = True
    for module, description in imports_to_test:
        try:
            __import__(module)
            check_pass(f"{description} ({module})")
        except ImportError:
            check_fail(f"Cannot import {module} - {description}")
            all_valid = False
    
    return all_valid


def validate_data_files() -> bool:
    """Validate data file integrity."""
    print_section("Data Files Validation")
    
    try:
        import pandas as pd
        
        data_files = {
            'data/pokedex.csv': {'min_rows': 1000, 'required_cols': ['name', 'pokedex_number']},
            'data/pokemon_glossary.csv': {'min_rows': 20, 'required_cols': []},
            'data/poke_corpus.csv': {'min_rows': 1000, 'required_cols': []},
            'data/pokedex_otherVer.csv': {'min_rows': 900, 'required_cols': []}
        }
        
        all_valid = True
        for file_path, requirements in data_files.items():
            try:
                df = pd.read_csv(file_path)
                rows = len(df)
                
                if rows >= requirements['min_rows']:
                    check_pass(f"{file_path}: {rows} rows")
                else:
                    check_warn(f"{file_path}: Only {rows} rows (expected >= {requirements['min_rows']})")
                
                # Check required columns
                for col in requirements['required_cols']:
                    if col in df.columns:
                        check_pass(f"  Column '{col}' present")
                    else:
                        check_fail(f"  Missing column '{col}'")
                        all_valid = False
                        
            except Exception as e:
                check_fail(f"Error reading {file_path}: {e}")
                all_valid = False
        
        return all_valid
        
    except ImportError:
        check_fail("Pandas not installed, cannot validate data files")
        return False


def validate_security() -> bool:
    """Validate security configurations."""
    print_section("Security Validation")
    
    # Check .gitignore
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        security_patterns = [
            ('*.env', 'Environment files'),
            ('__pycache__', 'Python cache'),
            ('*.pyc', 'Python bytecode'),
            ('.vscode/', 'VS Code settings')
        ]
        
        all_valid = True
        for pattern, description in security_patterns:
            if pattern in gitignore_content:
                check_pass(f"{description} ignored ({pattern})")
            else:
                check_warn(f"{description} not in .gitignore ({pattern})")
        
        return all_valid
    else:
        check_fail(".gitignore file missing")
        return False


def validate_documentation() -> bool:
    """Validate documentation completeness."""
    print_section("Documentation Validation")
    
    docs = {
        'README.md': ['Installation', 'Features', 'Usage'],
        'SECURITY.md': ['Security', 'Validation'],
        'PROJECT_STRUCTURE.md': ['Structure', 'Directory']
    }
    
    all_valid = True
    for doc_file, keywords in docs.items():
        if Path(doc_file).exists():
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            found_all = True
            for keyword in keywords:
                if keyword.lower() in content:
                    check_pass(f"{doc_file}: Contains '{keyword}'")
                else:
                    check_warn(f"{doc_file}: Missing '{keyword}' section")
                    found_all = False
            
            if not found_all:
                all_valid = False
        else:
            check_fail(f"Missing documentation: {doc_file}")
            all_valid = False
    
    return all_valid


def main():
    """Run all validation checks."""
    print(f"\n{BLUE}{'*' * 60}{RESET}")
    print(f"{BLUE}{'Pokemon Dashboard - Comprehensive Validation':^60}{RESET}")
    print(f"{BLUE}{'*' * 60}{RESET}")
    
    # Track results
    results = {}
    
    # Run all validations
    results['Directory Structure'] = validate_directory_structure()
    results['Required Files'] = validate_required_files()
    results['Git Tracking'] = validate_git_tracking()
    results['Python Syntax'] = validate_python_syntax()
    results['Imports'] = validate_imports()
    results['Data Files'] = validate_data_files()
    results['Security'] = validate_security()
    results['Documentation'] = validate_documentation()
    
    # Print summary
    print_section("Validation Summary")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for check, result in results.items():
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"{check:.<40} {status}")
    
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"Total Checks: {total}")
    print(f"{GREEN}Passed: {passed}{RESET}")
    print(f"{RED}Failed: {total - passed}{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 All validation checks passed!{RESET}")
        return 0
    else:
        print(f"\n{YELLOW}⚠️  Some validation checks failed. Please review above.{RESET}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
