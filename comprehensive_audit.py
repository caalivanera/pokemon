"""
Comprehensive Audit Script for Pokemon Dashboard
Validates data integrity, checks for inconsistencies, and reports issues
"""

import json
import pandas as pd
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re


class PokemonDashboardAuditor:
    """Comprehensive auditing tool for the Pokemon Dashboard"""
    
    def __init__(self):
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.stats: Dict = {}
        
    def log_issue(self, message: str):
        """Log a critical issue"""
        self.issues.append(f"❌ {message}")
        
    def log_warning(self, message: str):
        """Log a warning"""
        self.warnings.append(f"⚠️  {message}")
        
    def log_info(self, message: str):
        """Log info"""
        self.info.append(f"ℹ️  {message}")
        
    def audit_file_structure(self) -> bool:
        """Check if all required files exist"""
        print("\n" + "="*60)
        print("FILE STRUCTURE AUDIT")
        print("="*60)
        
        required_files = {
            'data/national_dex.csv': 'Main Pokemon database',
            'data/enhanced/comprehensive_game_data.json': 'Game availability data',
            'data/competitive/competitive_data.json': 'Competitive data',
            'data/games.yaml': 'Game definitions',
            'enhanced_dashboard.py': 'Main dashboard application',
            'src/core/app.py': 'Streamlit Cloud entry point',
            'requirements.txt': 'Python dependencies',
            '.streamlit/config.toml': 'Streamlit configuration'
        }
        
        all_exist = True
        for filepath, description in required_files.items():
            path = Path(filepath)
            if path.exists():
                size = path.stat().st_size
                self.log_info(f"{filepath}: {description} ({size:,} bytes)")
            else:
                self.log_issue(f"Missing: {filepath} - {description}")
                all_exist = False
                
        return all_exist
    
    def audit_national_dex(self) -> pd.DataFrame:
        """Audit the national_dex.csv file"""
        print("\n" + "="*60)
        print("NATIONAL DEX AUDIT")
        print("="*60)
        
        try:
            df = pd.read_csv('data/national_dex.csv')
            self.log_info(f"Loaded {len(df)} Pokemon from national_dex.csv")
            
            # Check for expected 1,025 Pokemon
            if len(df) != 1025:
                self.log_warning(f"Expected 1,025 Pokemon, found {len(df)}")
            
            # Check for duplicates
            duplicates = df[df.duplicated(subset=['pokedex_number'], keep=False)]
            if len(duplicates) > 0:
                self.log_warning(f"Found {len(duplicates)} duplicate Pokedex numbers")
                
            # Check for missing critical columns
            required_cols = ['pokedex_number', 'name', 'type_1', 'generation', 
                           'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                self.log_issue(f"Missing columns: {missing_cols}")
                
            # Check for null values in critical columns
            for col in required_cols:
                if col in df.columns:
                    null_count = df[col].isna().sum()
                    if null_count > 0:
                        self.log_warning(f"Column '{col}' has {null_count} null values")
            
            # Check evolution_chain data
            evo_null = df['evolution_chain'].isna().sum()
            self.log_info(f"Evolution chain: {len(df) - evo_null} filled, {evo_null} empty")
            
            # Check alternate forms
            alt_forms = df[df['alt_name'].notna()]
            self.log_info(f"Alternate forms: {len(alt_forms)} Pokemon with alt_name data")
            
            self.stats['national_dex'] = {
                'total_pokemon': len(df),
                'duplicates': len(duplicates),
                'with_evolution': len(df) - evo_null,
                'with_alt_forms': len(alt_forms)
            }
            
            return df
            
        except Exception as e:
            self.log_issue(f"Failed to load national_dex.csv: {e}")
            return None
    
    def audit_game_data(self) -> Dict:
        """Audit the comprehensive_game_data.json file"""
        print("\n" + "="*60)
        print("GAME DATA AUDIT")
        print("="*60)
        
        try:
            with open('data/enhanced/comprehensive_game_data.json', 'r', encoding='utf-8') as f:
                game_data = json.load(f)
                
            self.log_info(f"Loaded game data for {len(game_data)} Pokemon")
            
            # Check structure
            if len(game_data) != 1025:
                self.log_warning(f"Expected 1,025 entries, found {len(game_data)}")
            
            # Analyze game tags
            all_games = set()
            for pokemon in game_data:
                games = pokemon.get('games', [])
                all_games.update(games)
            
            self.log_info(f"Found {len(all_games)} unique game tags")
            self.log_info(f"Game tags: {sorted(all_games)}")
            
            # Check specific game counts
            game_counts = {}
            for game_tag in all_games:
                count = sum(1 for p in game_data if game_tag in p.get('games', []))
                game_counts[game_tag] = count
            
            self.log_info(f"\nPokemon per game:")
            for game, count in sorted(game_counts.items()):
                self.log_info(f"  {game}: {count} Pokemon")
            
            self.stats['game_data'] = {
                'total_entries': len(game_data),
                'unique_games': len(all_games),
                'game_counts': game_counts
            }
            
            return game_data
            
        except Exception as e:
            self.log_issue(f"Failed to load game data: {e}")
            return None
    
    def audit_games_yaml(self) -> Dict:
        """Audit the games.yaml configuration"""
        print("\n" + "="*60)
        print("GAMES YAML AUDIT")
        print("="*60)
        
        try:
            with open('data/games.yaml', 'r', encoding='utf-8') as f:
                games = yaml.safe_load(f)
                
            self.log_info(f"Loaded {len(games)} game definitions")
            
            # Check structure
            for game_key, game_info in games.items():
                if 'name' not in game_info:
                    self.log_warning(f"Game '{game_key}' missing 'name' field")
                if 'release' not in game_info:
                    self.log_warning(f"Game '{game_key}' missing 'release' field")
            
            self.stats['games_yaml'] = {
                'total_games': len(games),
                'game_keys': list(games.keys())
            }
            
            return games
            
        except Exception as e:
            self.log_issue(f"Failed to load games.yaml: {e}")
            return None
    
    def audit_code_quality(self):
        """Audit code files for quality issues"""
        print("\n" + "="*60)
        print("CODE QUALITY AUDIT")
        print("="*60)
        
        code_files = [
            'enhanced_dashboard.py',
            'src/core/app.py',
            'check_version.py',
            'check_data.py'
        ]
        
        for filepath in code_files:
            path = Path(filepath)
            if not path.exists():
                self.log_warning(f"Code file not found: {filepath}")
                continue
                
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Basic checks
            self.log_info(f"\n{filepath}:")
            self.log_info(f"  Lines: {len(lines)}")
            self.log_info(f"  Size: {len(content):,} bytes")
            
            # Check for TODO/FIXME comments
            todos = [i+1 for i, line in enumerate(lines) if 'TODO' in line or 'FIXME' in line]
            if todos:
                self.log_warning(f"  Found TODO/FIXME at lines: {todos[:5]}")
            
            # Check for proper encoding declaration (Python files)
            if filepath.endswith('.py'):
                if content.startswith('"""') or content.startswith('#'):
                    self.log_info(f"  ✓ Has docstring/header")
    
    def check_data_consistency(self, nat_dex_df: pd.DataFrame, game_data: List[Dict]):
        """Check consistency between different data sources"""
        print("\n" + "="*60)
        print("DATA CONSISTENCY CHECK")
        print("="*60)
        
        if nat_dex_df is None or game_data is None:
            self.log_issue("Cannot check consistency - data not loaded")
            return
        
        # Check if all Pokemon in nat_dex have game data
        nat_dex_ids = set(nat_dex_df['pokedex_number'].values)
        game_data_ids = set(p['pokedex_number'] for p in game_data)
        
        missing_in_game = nat_dex_ids - game_data_ids
        missing_in_nat = game_data_ids - nat_dex_ids
        
        if missing_in_game:
            self.log_warning(f"Pokemon in nat_dex but not in game_data: {sorted(missing_in_game)[:10]}")
        if missing_in_nat:
            self.log_warning(f"Pokemon in game_data but not in nat_dex: {sorted(missing_in_nat)[:10]}")
        
        if not missing_in_game and not missing_in_nat:
            self.log_info("✓ All Pokemon IDs consistent between datasets")
    
    def generate_report(self):
        """Generate final audit report"""
        print("\n" + "="*60)
        print("AUDIT REPORT SUMMARY")
        print("="*60)
        
        print(f"\n📊 STATISTICS:")
        for key, value in self.stats.items():
            print(f"\n{key.upper()}:")
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, (int, float, str)):
                        print(f"  {k}: {v}")
        
        print(f"\n\n❌ CRITICAL ISSUES ({len(self.issues)}):")
        for issue in self.issues:
            print(f"  {issue}")
        
        print(f"\n\n⚠️  WARNINGS ({len(self.warnings)}):")
        for warning in self.warnings[:20]:  # Limit to first 20
            print(f"  {warning}")
        if len(self.warnings) > 20:
            print(f"  ... and {len(self.warnings) - 20} more warnings")
        
        print(f"\n\n✅ OVERALL STATUS:")
        if len(self.issues) == 0:
            print("  ✓ No critical issues found!")
        else:
            print(f"  ✗ Found {len(self.issues)} critical issues that need attention")
        
        if len(self.warnings) == 0:
            print("  ✓ No warnings")
        else:
            print(f"  ⚠  Found {len(self.warnings)} warnings to review")


def main():
    """Run comprehensive audit"""
    auditor = PokemonDashboardAuditor()
    
    print("="*60)
    print("POKEMON DASHBOARD COMPREHENSIVE AUDIT")
    print("="*60)
    
    # Run all audits
    auditor.audit_file_structure()
    nat_dex_df = auditor.audit_national_dex()
    game_data = auditor.audit_game_data()
    games_yaml = auditor.audit_games_yaml()
    auditor.audit_code_quality()
    auditor.check_data_consistency(nat_dex_df, game_data)
    
    # Generate report
    auditor.generate_report()
    
    print("\n" + "="*60)
    print("AUDIT COMPLETE")
    print("="*60)


if __name__ == '__main__':
    main()
