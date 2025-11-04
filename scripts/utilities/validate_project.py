"""
Comprehensive Project Validation Script
Date: November 4, 2025

This script validates all project files, data integrity, and folder organization.
"""

import os
import json
import pandas as pd
from pathlib import Path
from collections import defaultdict

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Expected folder structure
EXPECTED_FOLDERS = {
    "assets": ["sprites", "animated", "icons", "shiny", "types"],
    "data": [],
    "scripts": ["data", "utilities"],
    "docs": [],
    "src": ["core", "components", "utils"],
    "tests": [],
    ".github": ["workflows"],
    ".streamlit": [],
    "config": [],
    "logs": []
}

# Required files
REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    "data/national_dex_with_variants.csv",
    "data/type_colors.json",
    "data/type_effectiveness.json",
    "src/core/app.py",
    ".streamlit/config.toml"
]


def validate_folder_structure():
    """Validate project folder structure."""
    print("="*80)
    print("📁 VALIDATING FOLDER STRUCTURE")
    print("="*80)
    
    issues = []
    
    for folder, subfolders in EXPECTED_FOLDERS.items():
        folder_path = PROJECT_ROOT / folder
        
        # Check if main folder exists
        if not folder_path.exists():
            issues.append(f"❌ Missing folder: {folder}")
            print(f"❌ Missing: {folder}")
        else:
            print(f"✅ Found: {folder}/")
            
            # Check subfolders
            for subfolder in subfolders:
                subfolder_path = folder_path / subfolder
                if not subfolder_path.exists():
                    issues.append(f"❌ Missing subfolder: {folder}/{subfolder}")
                    print(f"  ❌ Missing: {folder}/{subfolder}/")
                else:
                    print(f"  ✅ Found: {folder}/{subfolder}/")
    
    print(f"\n{'✅ All folders present' if not issues else f'⚠️  {len(issues)} folder issues found'}")
    return issues


def validate_required_files():
    """Validate required files exist."""
    print("\n" + "="*80)
    print("📄 VALIDATING REQUIRED FILES")
    print("="*80)
    
    issues = []
    
    for file_path_str in REQUIRED_FILES:
        file_path = PROJECT_ROOT / file_path_str
        
        if not file_path.exists():
            issues.append(f"❌ Missing file: {file_path_str}")
            print(f"❌ Missing: {file_path_str}")
        else:
            size = file_path.stat().st_size
            size_mb = size / (1024 * 1024)
            
            if size_mb > 1:
                print(f"✅ Found: {file_path_str} ({size_mb:.1f} MB)")
            else:
                size_kb = size / 1024
                print(f"✅ Found: {file_path_str} ({size_kb:.1f} KB)")
    
    print(f"\n{'✅ All files present' if not issues else f'⚠️  {len(issues)} file issues found'}")
    return issues


def validate_csv_data():
    """Validate the main CSV dataset."""
    print("\n" + "="*80)
    print("📊 VALIDATING CSV DATASET")
    print("="*80)
    
    csv_path = PROJECT_ROOT / "data" / "national_dex_with_variants.csv"
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        print(f"✅ CSV loaded successfully")
        print(f"   Total rows: {len(df)}")
        print(f"   Total columns: {len(df.columns)}")
        
        # Check for required columns
        required_cols = [
            'pokedex_number', 'name', 'generation', 'type_1',
            'region', 'sprite_path_static', 'sprite_path_animated',
            'sprite_path_shiny'
        ]
        
        missing_cols = []
        for col in required_cols:
            if col not in df.columns:
                missing_cols.append(col)
                print(f"   ❌ Missing column: {col}")
            else:
                non_null = df[col].notna().sum()
                percentage = (non_null / len(df)) * 100
                print(f"   ✅ Column '{col}': {percentage:.1f}% populated")
        
        # Check for duplicates
        duplicates = df.duplicated(subset=['pokedex_number', 'variant_type']).sum()
        if duplicates > 0:
            print(f"   ⚠️  Found {duplicates} duplicate entries")
        else:
            print(f"   ✅ No duplicate entries")
        
        # Regional distribution
        print(f"\n   📍 Regional Distribution:")
        region_counts = df['region'].value_counts()
        for region, count in region_counts.items():
            print(f"      {region:15} {count:4} Pokemon")
        
        return [] if not missing_cols else [f"Missing columns: {', '.join(missing_cols)}"]
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return [f"CSV load error: {e}"]


def validate_sprite_assets():
    """Validate sprite asset files."""
    print("\n" + "="*80)
    print("🖼️  VALIDATING SPRITE ASSETS")
    print("="*80)
    
    assets_path = PROJECT_ROOT / "assets"
    
    asset_types = {
        "sprites": "Static Sprites",
        "animated": "Animated Sprites",
        "shiny": "Shiny Sprites",
        "icons": "Pokemon Icons",
        "types": "Type Icons"
    }
    
    issues = []
    
    for folder_name, display_name in asset_types.items():
        folder_path = assets_path / folder_name
        
        if not folder_path.exists():
            issues.append(f"Missing asset folder: {folder_name}")
            print(f"❌ {display_name}: Folder not found")
        else:
            # Count files
            png_files = list(folder_path.glob("*.png"))
            gif_files = list(folder_path.glob("*.gif"))
            all_files = png_files + gif_files
            
            # Calculate size
            total_size = sum(f.stat().st_size for f in all_files)
            size_mb = total_size / (1024 * 1024)
            
            print(f"✅ {display_name}:")
            print(f"   Files: {len(all_files)} ({len(png_files)} PNG, {len(gif_files)} GIF)")
            print(f"   Size: {size_mb:.1f} MB")
    
    print(f"\n{'✅ All asset folders validated' if not issues else f'⚠️  {len(issues)} asset issues found'}")
    return issues


def validate_json_files():
    """Validate JSON configuration files."""
    print("\n" + "="*80)
    print("📋 VALIDATING JSON FILES")
    print("="*80)
    
    json_files = [
        "data/type_colors.json",
        "data/type_effectiveness.json"
    ]
    
    issues = []
    
    for json_file in json_files:
        json_path = PROJECT_ROOT / json_file
        
        if not json_path.exists():
            issues.append(f"Missing JSON: {json_file}")
            print(f"❌ Missing: {json_file}")
        else:
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"✅ Valid JSON: {json_file}")
                print(f"   Keys: {len(data)}")
                
                # Show first few keys
                if isinstance(data, dict):
                    keys = list(data.keys())[:5]
                    print(f"   Sample: {', '.join(keys)}")
                    
            except json.JSONDecodeError as e:
                issues.append(f"Invalid JSON: {json_file}")
                print(f"❌ Invalid JSON: {json_file} - {e}")
    
    print(f"\n{'✅ All JSON files valid' if not issues else f'⚠️  {len(issues)} JSON issues found'}")
    return issues


def validate_python_files():
    """Validate Python source files."""
    print("\n" + "="*80)
    print("🐍 VALIDATING PYTHON FILES")
    print("="*80)
    
    python_folders = [
        PROJECT_ROOT / "src",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "tests"
    ]
    
    total_files = 0
    total_lines = 0
    issues = []
    
    for folder in python_folders:
        if folder.exists():
            py_files = list(folder.rglob("*.py"))
            total_files += len(py_files)
            
            for py_file in py_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                except Exception as e:
                    issues.append(f"Error reading {py_file.name}: {e}")
    
    print(f"✅ Python Files: {total_files} files")
    print(f"   Total Lines: {total_lines:,}")
    print(f"   Average Lines per File: {total_lines // total_files if total_files > 0 else 0}")
    
    print(f"\n{'✅ All Python files validated' if not issues else f'⚠️  {len(issues)} Python issues found'}")
    return issues


def generate_project_summary():
    """Generate comprehensive project summary."""
    print("\n" + "="*80)
    print("📈 PROJECT SUMMARY")
    print("="*80)
    
    # Count all files
    all_files = list(PROJECT_ROOT.rglob("*"))
    file_count = len([f for f in all_files if f.is_file()])
    folder_count = len([f for f in all_files if f.is_dir()])
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in all_files if f.is_file())
    size_mb = total_size / (1024 * 1024)
    
    # Count by extension
    extension_counts = defaultdict(int)
    for f in all_files:
        if f.is_file():
            ext = f.suffix.lower() if f.suffix else "no_extension"
            extension_counts[ext] += 1
    
    print(f"Total Files: {file_count}")
    print(f"Total Folders: {folder_count}")
    print(f"Total Size: {size_mb:.1f} MB")
    
    print(f"\n📂 File Types:")
    for ext, count in sorted(extension_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {ext:15} {count:4} files")


def main():
    """Main validation function."""
    print("="*80)
    print("🔍 COMPREHENSIVE PROJECT VALIDATION")
    print("="*80)
    print(f"📁 Project Root: {PROJECT_ROOT}\n")
    
    all_issues = []
    
    # Run all validations
    all_issues.extend(validate_folder_structure())
    all_issues.extend(validate_required_files())
    all_issues.extend(validate_csv_data())
    all_issues.extend(validate_sprite_assets())
    all_issues.extend(validate_json_files())
    all_issues.extend(validate_python_files())
    
    # Project summary
    generate_project_summary()
    
    # Final report
    print("\n" + "="*80)
    print("✅ VALIDATION COMPLETE")
    print("="*80)
    
    if all_issues:
        print(f"\n⚠️  Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"   • {issue}")
    else:
        print("\n🎉 No issues found! Project is properly organized.")
    
    print("="*80)


if __name__ == "__main__":
    main()
