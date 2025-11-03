"""
Automated Fix Script for Pokemon Dashboard v5.4.3
Fixes: Lint errors, syntax issues, data validation problems
"""

import os
import sys
from pathlib import Path
import re
import subprocess
from typing import List, Tuple

class AutoFixer:
    """Automatically fix common issues"""
    
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = Path(base_path)
        self.fixed_count = 0
        self.error_count = 0
    
    def fix_markdown_lint(self):
        """Fix common Markdown lint issues"""
        print("\n🔧 Fixing Markdown lint issues...")
        
        md_files = [
            self.base_path / "README.md",
            self.base_path / "CHANGELOG.md",
        ]
        
        for md_file in md_files:
            if not md_file.exists():
                continue
            
            print(f"  Processing {md_file.name}...")
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix horizontal rules: --- to ------
                content = re.sub(r'^---$', '------', content, flags=re.MULTILINE)
                
                # Fix headings: ensure blank lines before and after
                lines = content.split('\n')
                fixed_lines = []
                
                for i, line in enumerate(lines):
                    # Check if line is a heading
                    if line.startswith('#'):
                        # Add blank line before heading if previous line is not blank
                        if i > 0 and fixed_lines and fixed_lines[-1].strip():
                            fixed_lines.append('')
                        fixed_lines.append(line)
                        # Add blank line after heading if next line is not blank
                        if i < len(lines) - 1 and lines[i + 1].strip():
                            fixed_lines.append('')
                    else:
                        fixed_lines.append(line)
                
                content = '\n'.join(fixed_lines)
                
                # Save if changed
                if content != original_content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"    ✅ Fixed {md_file.name}")
                    self.fixed_count += 1
                else:
                    print(f"    ℹ️  No changes needed for {md_file.name}")
            
            except Exception as e:
                print(f"    ❌ Error fixing {md_file.name}: {e}")
                self.error_count += 1
    
    def fix_python_imports(self):
        """Fix unused imports in Python files"""
        print("\n🔧 Fixing Python import issues...")
        
        # Use autoflake if available
        try:
            result = subprocess.run(
                ['pip', 'show', 'autoflake'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("  Running autoflake to remove unused imports...")
                subprocess.run([
                    'autoflake',
                    '--in-place',
                    '--remove-unused-variables',
                    '--remove-all-unused-imports',
                    '-r',
                    str(self.base_path / 'src'),
                    str(self.base_path / 'tests')
                ])
                print("  ✅ Removed unused imports")
                self.fixed_count += 1
            else:
                print("  ℹ️  autoflake not installed, skipping unused import removal")
        
        except Exception as e:
            print(f"  ⚠️  Could not run autoflake: {e}")
    
    def format_python_code(self):
        """Format Python code with black"""
        print("\n🔧 Formatting Python code...")
        
        try:
            result = subprocess.run(
                ['pip', 'show', 'black'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("  Running black formatter...")
                subprocess.run([
                    'black',
                    '--line-length', '79',
                    str(self.base_path / 'src'),
                    str(self.base_path / 'tests')
                ])
                print("  ✅ Formatted Python code")
                self.fixed_count += 1
            else:
                print("  ℹ️  black not installed, skipping formatting")
        
        except Exception as e:
            print(f"  ⚠️  Could not run black: {e}")
    
    def validate_requirements(self):
        """Validate and fix requirements.txt"""
        print("\n🔧 Validating requirements.txt...")
        
        req_file = self.base_path / "requirements.txt"
        
        if not req_file.exists():
            print("  ❌ requirements.txt not found")
            self.error_count += 1
            return
        
        try:
            with open(req_file, 'r') as f:
                lines = f.readlines()
            
            # Remove duplicates while preserving order
            seen = set()
            fixed_lines = []
            
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    pkg_name = stripped.split('>=')[0].split('==')[0].strip()
                    if pkg_name not in seen:
                        seen.add(pkg_name)
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            
            # Write back if changed
            if len(fixed_lines) != len(lines):
                with open(req_file, 'w') as f:
                    f.writelines(fixed_lines)
                print(f"  ✅ Removed {len(lines) - len(fixed_lines)} duplicate entries")
                self.fixed_count += 1
            else:
                print("  ℹ️  No duplicates found")
        
        except Exception as e:
            print(f"  ❌ Error validating requirements.txt: {e}")
            self.error_count += 1
    
    def create_gitignore(self):
        """Create/update .gitignore"""
        print("\n🔧 Updating .gitignore...")
        
        gitignore = self.base_path / ".gitignore"
        
        essential_patterns = [
            "# Python",
            "__pycache__/",
            "*.py[cod]",
            "*$py.class",
            "*.so",
            ".Python",
            "venv/",
            "ENV/",
            ".venv/",
            "env/",
            "",
            "# Testing",
            ".pytest_cache/",
            ".coverage",
            "htmlcov/",
            "*.log",
            "",
            "# IDE",
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo",
            "",
            "# Data",
            "*.db",
            "*.sqlite",
            "*.csv.backup",
            "",
            "# Results",
            "TEST_RESULTS.txt",
            "STRESS_TEST_RESULTS.json",
            "bandit-report.json",
        ]
        
        try:
            existing = []
            if gitignore.exists():
                with open(gitignore, 'r') as f:
                    existing = [line.strip() for line in f.readlines()]
            
            # Add missing patterns
            new_patterns = [p for p in essential_patterns if p not in existing]
            
            if new_patterns:
                with open(gitignore, 'a') as f:
                    f.write('\n')
                    f.write('\n'.join(new_patterns))
                    f.write('\n')
                print(f"  ✅ Added {len(new_patterns)} patterns to .gitignore")
                self.fixed_count += 1
            else:
                print("  ℹ️  .gitignore is up to date")
        
        except Exception as e:
            print(f"  ❌ Error updating .gitignore: {e}")
            self.error_count += 1
    
    def run_all_fixes(self):
        """Run all automated fixes"""
        print("="*80)
        print("AUTOMATED FIX SCRIPT - Pokemon Dashboard v5.4.3")
        print("="*80)
        
        self.fix_markdown_lint()
        self.validate_requirements()
        self.create_gitignore()
        self.fix_python_imports()
        self.format_python_code()
        
        # Summary
        print("\n" + "="*80)
        print("FIX SUMMARY")
        print("="*80)
        print(f"✅ Fixed: {self.fixed_count} issues")
        print(f"❌ Errors: {self.error_count}")
        print("="*80)
        
        return self.fixed_count, self.error_count

def main():
    """Main entry point"""
    fixer = AutoFixer()
    fixed, errors = fixer.run_all_fixes()
    
    sys.exit(0 if errors == 0 else 1)

if __name__ == "__main__":
    main()
