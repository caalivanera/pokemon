"""
Comprehensive Project Validation Script
Validates all code, data, and configuration files for consistency and correctness
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import pandas as pd
import yaml
import json


class ProjectValidator:
    """Comprehensive validation for the Pokemon Dashboard project."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        self.successes = []
        
    def log_error(self, message: str):
        """Log an error."""
        self.errors.append(f"❌ ERROR: {message}")
        print(f"❌ {message}")
    
    def log_warning(self, message: str):
        """Log a warning."""
        self.warnings.append(f"⚠️  WARNING: {message}")
        print(f"⚠️  {message}")
    
    def log_success(self, message: str):
        """Log a success."""
        self.successes.append(f"✅ SUCCESS: {message}")
        print(f"✅ {message}")
    
    def validate_csv_files(self) -> bool:
        """Validate all CSV data files."""
        print("\n" + "="*60)
        print("VALIDATING CSV DATA FILES")
        print("="*60)
        
        csv_files = {
            'pokedex.csv': ['pokedex_number', 'name', 'type_1'],
            'pokemon_glossary.csv': [],  # No required columns (custom format)
            'poke_corpus.csv': ['pokemon_info'],
            'pokedex_otherVer.csv': ['id']
        }
        
        all_valid = True
        
        for filename, required_cols in csv_files.items():
            filepath = self.base_path / 'data' / filename
            
            if not filepath.exists():
                self.log_error(f"Missing CSV file: {filename}")
                all_valid = False
                continue
            
            try:
                df = pd.read_csv(filepath)
                self.log_success(f"Loaded {filename}: {len(df)} rows")
                
                # Check required columns
                if required_cols:
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    if missing_cols:
                        self.log_error(f"{filename} missing columns: {missing_cols}")
                        all_valid = False
                    else:
                        self.log_success(f"{filename} has all required columns")
                
                # Check for empty data
                if len(df) == 0:
                    self.log_error(f"{filename} is empty!")
                    all_valid = False
                
            except Exception as e:
                self.log_error(f"Failed to load {filename}: {e}")
                all_valid = False
        
        return all_valid
    
    def validate_yaml_files(self) -> bool:
        """Validate all YAML files from pokemondbgit."""
        print("\n" + "="*60)
        print("VALIDATING YAML DATA FILES")
        print("="*60)
        
        yaml_files = [
            'pokemon.yaml',
            'moves.yaml',
            'abilities.yaml',
            'types.yaml',
            'type-chart.yaml',
            'items.yaml',
            'locations.yaml',
            'egg-groups.yaml',
            'games.yaml',
            'releases.yaml',
            'pokemon-forms.yaml'
        ]
        
        all_valid = True
        yaml_dir = self.base_path / 'pokemondbgit'
        
        if not yaml_dir.exists():
            self.log_error(f"pokemondbgit directory not found at {yaml_dir}")
            return False
        
        for filename in yaml_files:
            filepath = yaml_dir / filename
            
            if not filepath.exists():
                self.log_warning(f"Missing YAML file: {filename}")
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                if data is None:
                    self.log_error(f"{filename} is empty!")
                    all_valid = False
                else:
                    entry_count = len(data) if isinstance(data, dict) else "N/A"
                    self.log_success(f"Loaded {filename}: {entry_count} entries")
                
            except Exception as e:
                self.log_error(f"Failed to load {filename}: {e}")
                all_valid = False
        
        return all_valid
    
    def validate_python_files(self) -> bool:
        """Validate Python source files for syntax."""
        print("\n" + "="*60)
        print("VALIDATING PYTHON SOURCE FILES")
        print("="*60)
        
        python_files = [
            'src/core/app.py',
            'src/data_loaders/data_extractor.py',
            'src/data_loaders/yaml_loader.py',
            'src/database/models.py',
            'src/database/connection.py',
            'src/database/data_loader.py',
            'tests/test_enhanced_dashboard.py',
            'scripts/validate_project.py'
        ]
        
        all_valid = True
        
        for filename in python_files:
            filepath = self.base_path / filename
            
            if not filepath.exists():
                self.log_error(f"Missing Python file: {filename}")
                all_valid = False
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Check syntax
                compile(code, filename, 'exec')
                self.log_success(f"Valid Python syntax: {filename}")
                
                # Check for basic imports
                if 'import ' not in code:
                    self.log_warning(f"{filename} has no imports")
                
            except SyntaxError as e:
                self.log_error(f"Syntax error in {filename}: {e}")
                all_valid = False
            except Exception as e:
                self.log_error(f"Error validating {filename}: {e}")
                all_valid = False
        
        return all_valid
    
    def validate_config_files(self) -> bool:
        """Validate configuration files."""
        print("\n" + "="*60)
        print("VALIDATING CONFIGURATION FILES")
        print("="*60)
        
        all_valid = True
        
        # Check requirements.txt
        req_file = self.base_path / 'requirements.txt'
        if req_file.exists():
            try:
                with open(req_file, 'r') as f:
                    lines = f.readlines()
                
                packages = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
                self.log_success(f"requirements.txt: {len(packages)} packages")
                
                # Check for essential packages
                essential = ['streamlit', 'pandas', 'numpy', 'pyyaml']
                for pkg in essential:
                    if not any(pkg in line.lower() for line in packages):
                        self.log_error(f"Missing essential package: {pkg}")
                        all_valid = False
                
            except Exception as e:
                self.log_error(f"Error reading requirements.txt: {e}")
                all_valid = False
        else:
            self.log_error("Missing requirements.txt")
            all_valid = False
        
        # Check .env.example
        env_file = self.base_path / '.env.example'
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                
                required_vars = ['DATABASE_URL', 'POSTGRES_DB', 'POSTGRES_USER']
                for var in required_vars:
                    if var in content:
                        self.log_success(f"Found environment variable: {var}")
                    else:
                        self.log_warning(f"Missing environment variable template: {var}")
                
            except Exception as e:
                self.log_error(f"Error reading .env.example: {e}")
                all_valid = False
        else:
            self.log_warning("Missing .env.example")
        
        # Check docker-compose.yml
        compose_file = self.base_path / 'config' / 'docker' / 'docker-compose.yml'
        if compose_file.exists():
            try:
                with open(compose_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                if 'services' in data:
                    services = list(data['services'].keys())
                    self.log_success(f"docker-compose.yml services: {services}")
                else:
                    self.log_error("docker-compose.yml missing services section")
                    all_valid = False
                
            except Exception as e:
                self.log_error(f"Error reading docker-compose.yml: {e}")
                all_valid = False
        else:
            self.log_warning("Missing docker-compose.yml")
        
        # Check Dockerfile
        dockerfile = self.base_path / 'config' / 'docker' / 'Dockerfile'
        if dockerfile.exists():
            try:
                with open(dockerfile, 'r') as f:
                    content = f.read()
                
                if 'FROM python' in content:
                    self.log_success("Dockerfile has valid Python base image")
                else:
                    self.log_error("Dockerfile missing Python base image")
                    all_valid = False
                
            except Exception as e:
                self.log_error(f"Error reading Dockerfile: {e}")
                all_valid = False
        else:
            self.log_warning("Missing Dockerfile")
        
        return all_valid
    
    def validate_documentation(self) -> bool:
        """Validate documentation files."""
        print("\n" + "="*60)
        print("VALIDATING DOCUMENTATION FILES")
        print("="*60)
        
        doc_files = [
            'README.md',
            'CHANGELOG.md',
            'docs/guides/GITHUB_LAUNCH_GUIDE.md',
            'docs/technical/TECH_STACK.md',
            'docs/guides/INSTALLATION.md',
            'docs/technical/IMPLEMENTATION_SUMMARY.md',
            'docs/technical/OPEN_SOURCE_VERIFICATION.md',
            'docs/technical/PROJECT_COMPLETION_REPORT.md'
        ]
        
        all_valid = True
        
        for filename in doc_files:
            filepath = self.base_path / filename
            
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if len(content) < 100:
                        self.log_warning(f"{filename} seems too short")
                    else:
                        self.log_success(f"Valid documentation: {filename} ({len(content)} chars)")
                
                except Exception as e:
                    self.log_error(f"Error reading {filename}: {e}")
                    all_valid = False
            else:
                self.log_warning(f"Missing documentation: {filename}")
        
        return all_valid
    
    def validate_directory_structure(self) -> bool:
        """Validate project directory structure."""
        print("\n" + "="*60)
        print("VALIDATING DIRECTORY STRUCTURE")
        print("="*60)
        
        required_dirs = [
            'data',
            'src/core',
            'src/data_loaders',
            'src/database',
            'pokemondbgit',
            'config/github/workflows',
            'config/vscode',
            'config/docker',
            'docs/guides',
            'docs/technical',
            'tests',
            'scripts'
        ]
        
        all_valid = True
        
        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            
            if dir_path.exists() and dir_path.is_dir():
                self.log_success(f"Directory exists: {dir_name}")
            else:
                self.log_error(f"Missing directory: {dir_name}")
                all_valid = False
        
        return all_valid
    
    def generate_report(self):
        """Generate validation report."""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        print(f"\n✅ Successes: {len(self.successes)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        print("\n" + "="*60)
        if len(self.errors) == 0:
            print("✅ ALL VALIDATIONS PASSED!")
        else:
            print(f"❌ VALIDATION FAILED WITH {len(self.errors)} ERRORS")
        print("="*60)
        
        return len(self.errors) == 0
    
    def run_all_validations(self) -> bool:
        """Run all validation checks."""
        print("\n🔍 POKEMON DASHBOARD - COMPREHENSIVE VALIDATION")
        print("="*60)
        
        results = {
            'Directory Structure': self.validate_directory_structure(),
            'CSV Files': self.validate_csv_files(),
            'YAML Files': self.validate_yaml_files(),
            'Python Files': self.validate_python_files(),
            'Configuration Files': self.validate_config_files(),
            'Documentation': self.validate_documentation()
        }
        
        return self.generate_report()


def main():
    """Main validation entry point."""
    # Get project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir
    
    print(f"Project root: {project_root}")
    
    validator = ProjectValidator(project_root)
    success = validator.run_all_validations()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
