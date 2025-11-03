"""
Data Validation System
Validates CSV files, JSON data, and ensures data integrity
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime


class DataValidator:
    """Validate Pokemon data files for integrity and correctness"""
    
    def __init__(self):
        """Initialize data validator"""
        self.validation_results = []
        self.errors = []
        self.warnings = []
    
    def validate_csv(
        self, 
        file_path: str, 
        required_columns: List[str],
        numeric_columns: Optional[List[str]] = None,
        categorical_columns: Optional[Dict[str, List[Any]]] = None
    ) -> Tuple[bool, Dict]:
        """
        Validate a CSV file
        
        Args:
            file_path: Path to CSV file
            required_columns: List of columns that must exist
            numeric_columns: Columns that should contain numeric values
            categorical_columns: Dict of column: valid_values pairs
            
        Returns:
            Tuple of (is_valid, validation_report)
        """
        report = {
            'file': file_path,
            'timestamp': datetime.now().isoformat(),
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
        
        # Check file exists
        path = Path(file_path)
        if not path.exists():
            report['is_valid'] = False
            report['errors'].append(f"File not found: {file_path}")
            return False, report
        
        try:
            # Load CSV
            df = pd.read_csv(file_path)
            report['statistics']['total_rows'] = len(df)
            report['statistics']['total_columns'] = len(df.columns)
            
            # Check required columns
            missing_cols = set(required_columns) - set(df.columns)
            if missing_cols:
                report['is_valid'] = False
                report['errors'].append(
                    f"Missing required columns: {', '.join(missing_cols)}"
                )
            
            # Check for empty dataframe
            if df.empty:
                report['warnings'].append("Dataframe is empty")
            
            # Check for duplicate rows
            duplicates = df.duplicated().sum()
            if duplicates > 0:
                report['warnings'].append(f"Found {duplicates} duplicate rows")
                report['statistics']['duplicate_rows'] = int(duplicates)
            
            # Validate numeric columns
            if numeric_columns:
                for col in numeric_columns:
                    if col in df.columns:
                        non_numeric = df[col].apply(
                            lambda x: not isinstance(x, (int, float)) and pd.notna(x)
                        ).sum()
                        if non_numeric > 0:
                            report['warnings'].append(
                                f"Column '{col}' has {non_numeric} non-numeric values"
                            )
                    else:
                        report['warnings'].append(f"Numeric column '{col}' not found")
            
            # Validate categorical columns
            if categorical_columns:
                for col, valid_values in categorical_columns.items():
                    if col in df.columns:
                        invalid = df[~df[col].isin(valid_values) & df[col].notna()]
                        if len(invalid) > 0:
                            unique_invalid = invalid[col].unique()
                            report['warnings'].append(
                                f"Column '{col}' has {len(invalid)} invalid values: "
                                f"{list(unique_invalid)[:5]}"
                            )
            
            # Check for null values in each column
            null_counts = df.isnull().sum()
            null_cols = null_counts[null_counts > 0]
            if len(null_cols) > 0:
                report['statistics']['null_values'] = {
                    col: int(count) for col, count in null_cols.items()
                }
                report['warnings'].append(
                    f"{len(null_cols)} columns have null values"
                )
            
            # Data type analysis
            dtype_info = {}
            for col in df.columns:
                dtype_info[col] = str(df[col].dtype)
            report['statistics']['column_types'] = dtype_info
            
        except Exception as e:
            report['is_valid'] = False
            report['errors'].append(f"Error reading CSV: {str(e)}")
            return False, report
        
        self.validation_results.append(report)
        return report['is_valid'], report
    
    def validate_json(
        self, 
        file_path: str,
        required_keys: Optional[List[str]] = None
    ) -> Tuple[bool, Dict]:
        """
        Validate a JSON file
        
        Args:
            file_path: Path to JSON file
            required_keys: List of keys that must exist in JSON
            
        Returns:
            Tuple of (is_valid, validation_report)
        """
        report = {
            'file': file_path,
            'timestamp': datetime.now().isoformat(),
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
        
        # Check file exists
        path = Path(file_path)
        if not path.exists():
            report['is_valid'] = False
            report['errors'].append(f"File not found: {file_path}")
            return False, report
        
        try:
            # Load JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if it's a list or dict
            if isinstance(data, list):
                report['statistics']['type'] = 'array'
                report['statistics']['length'] = len(data)
                
                # Check required keys in each item
                if required_keys and len(data) > 0:
                    first_item = data[0] if isinstance(data[0], dict) else {}
                    missing_keys = set(required_keys) - set(first_item.keys())
                    if missing_keys:
                        report['warnings'].append(
                            f"Items missing keys: {', '.join(missing_keys)}"
                        )
            
            elif isinstance(data, dict):
                report['statistics']['type'] = 'object'
                report['statistics']['keys'] = list(data.keys())
                
                # Check required keys
                if required_keys:
                    missing_keys = set(required_keys) - set(data.keys())
                    if missing_keys:
                        report['is_valid'] = False
                        report['errors'].append(
                            f"Missing required keys: {', '.join(missing_keys)}"
                        )
            
            else:
                report['warnings'].append(f"Unexpected JSON type: {type(data)}")
            
        except json.JSONDecodeError as e:
            report['is_valid'] = False
            report['errors'].append(f"Invalid JSON: {str(e)}")
            return False, report
        except Exception as e:
            report['is_valid'] = False
            report['errors'].append(f"Error reading JSON: {str(e)}")
            return False, report
        
        self.validation_results.append(report)
        return report['is_valid'], report
    
    def validate_pokemon_csv(self, file_path: str) -> Tuple[bool, Dict]:
        """Validate Pokemon CSV with specific rules"""
        required_columns = [
            'pokedex_number', 'name', 'type_1',
            'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'
        ]
        
        numeric_columns = [
            'pokedex_number', 'hp', 'attack', 'defense',
            'sp_attack', 'sp_defense', 'speed', 'total_points'
        ]
        
        valid_types = [
            'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
            'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic',
            'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'
        ]
        
        categorical_columns = {
            'type_1': valid_types,
            'type_2': valid_types + [None]  # Type 2 can be null
        }
        
        return self.validate_csv(
            file_path,
            required_columns,
            numeric_columns,
            categorical_columns
        )
    
    def validate_competitive_json(self, file_path: str) -> Tuple[bool, Dict]:
        """Validate competitive data JSON"""
        required_keys = ['pokemon_id', 'name', 'tier']
        return self.validate_json(file_path, required_keys)
    
    def generate_validation_report(self, output_file: Optional[str] = None) -> str:
        """Generate a markdown validation report"""
        if output_file is None:
            output_file = f"data_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report = f"""# Data Validation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Files Validated**: {len(self.validation_results)}
- **Valid Files**: {sum(1 for r in self.validation_results if r['is_valid'])}
- **Invalid Files**: {sum(1 for r in self.validation_results if not r['is_valid'])}

"""
        
        for result in self.validation_results:
            status = "✅ VALID" if result['is_valid'] else "❌ INVALID"
            report += f"\n## {status}: {result['file']}\n\n"
            
            if result['errors']:
                report += "### Errors\n"
                for error in result['errors']:
                    report += f"- ❌ {error}\n"
                report += "\n"
            
            if result['warnings']:
                report += "### Warnings\n"
                for warning in result['warnings']:
                    report += f"- ⚠️ {warning}\n"
                report += "\n"
            
            if result['statistics']:
                report += "### Statistics\n"
                for key, value in result['statistics'].items():
                    if isinstance(value, dict):
                        report += f"**{key}**:\n"
                        for k, v in value.items():
                            report += f"  - {k}: {v}\n"
                    else:
                        report += f"- **{key}**: {value}\n"
                report += "\n"
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        return output_file
    
    def validate_all_data_files(self, data_dir: str = "data") -> Dict:
        """Validate all data files in the project"""
        data_path = Path(data_dir)
        results = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'files': []
        }
        
        # Validate Pokemon CSV
        pokemon_csv = data_path / "pokemon.csv"
        if pokemon_csv.exists():
            is_valid, report = self.validate_pokemon_csv(str(pokemon_csv))
            results['total'] += 1
            results['valid' if is_valid else 'invalid'] += 1
            results['files'].append(report)
        
        # Validate national_dex CSV
        national_dex = data_path / "national_dex.csv"
        if national_dex.exists():
            required_cols = ['pokedex_number', 'name', 'type_1']
            is_valid, report = self.validate_csv(str(national_dex), required_cols)
            results['total'] += 1
            results['valid' if is_valid else 'invalid'] += 1
            results['files'].append(report)
        
        # Validate competitive data
        comp_json = data_path / "competitive" / "competitive_data.json"
        if comp_json.exists():
            is_valid, report = self.validate_competitive_json(str(comp_json))
            results['total'] += 1
            results['valid' if is_valid else 'invalid'] += 1
            results['files'].append(report)
        
        return results


if __name__ == "__main__":
    # Test the validator
    validator = DataValidator()
    
    print("="*60)
    print("DATA VALIDATION TEST")
    print("="*60)
    
    # Validate all data files
    results = validator.validate_all_data_files()
    
    print(f"\n✅ Validated {results['total']} files")
    print(f"   Valid: {results['valid']}")
    print(f"   Invalid: {results['invalid']}")
    
    # Generate report
    report_path = validator.generate_validation_report()
    print(f"\n📄 Report generated: {report_path}")
