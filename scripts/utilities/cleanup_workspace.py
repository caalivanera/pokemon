"""
Workspace Cleanup and Consolidation Script
Removes redundant files and organizes the project structure
"""

import os
from pathlib import Path
import shutil

# Files to remove (redundant documentation)
REDUNDANT_DOCS = [
    'AUDIT_REPORT.md',
    'COMPLETE_UPDATE_SUMMARY.md',
    'CONSOLIDATED_README.md',
    'DASHBOARD_GUIDE.md',
    'DATA_VERIFICATION_REPORT.md',
    'DEPLOYMENT_COMPLETE.md',
    'ENHANCEMENT_SUMMARY.md',
    'IMPLEMENTATION_SUMMARY_V4.md',
    'MASTER_DOCUMENTATION.md',
    'NATIONAL_DEX_UPDATE.md',
    'NEXT_STEPS_GUIDE.md',
    'PROJECT_COMPLETION.md',
    'PROJECT_STRUCTURE.md',
    'SPRITE_UPDATE.md',
    'STREAMLIT_DEPLOY.md',
    'VERSION_4.0_CHANGELOG.md',
]

# Files to remove (redundant scripts/backups)
REDUNDANT_FILES = [
    'src/core/app.py.backup',
    'deploy_streamlit.py',  # Functionality integrated into main app
    'update_legends_za.py',  # Replaced by fix_legends_za_kalos_dex.py
]

def cleanup_workspace():
    """Remove redundant files and organize workspace"""
    print("="*60)
    print("WORKSPACE CLEANUP")
    print("="*60)
    
    removed = []
    kept = []
    
    # Remove redundant documentation
    print("\n📄 Cleaning up redundant documentation...")
    for doc_file in REDUNDANT_DOCS:
        path = Path(doc_file)
        if path.exists():
            try:
                path.unlink()
                removed.append(doc_file)
                print(f"  ✓ Removed: {doc_file}")
            except Exception as e:
                print(f"  ✗ Failed to remove {doc_file}: {e}")
                kept.append(doc_file)
        else:
            print(f"  - Not found: {doc_file}")
    
    # Remove redundant files
    print("\n🔧 Cleaning up redundant scripts and backups...")
    for file_path in REDUNDANT_FILES:
        path = Path(file_path)
        if path.exists():
            try:
                path.unlink()
                removed.append(file_path)
                print(f"  ✓ Removed: {file_path}")
            except Exception as e:
                print(f"  ✗ Failed to remove {file_path}: {e}")
                kept.append(file_path)
        else:
            print(f"  - Not found: {file_path}")
    
    # Report
    print("\n" + "="*60)
    print("CLEANUP SUMMARY")
    print("="*60)
    print(f"\n✅ Removed {len(removed)} files")
    if removed:
        for file in removed[:10]:
            print(f"  - {file}")
        if len(removed) > 10:
            print(f"  ... and {len(removed) - 10} more")
    
    if kept:
        print(f"\n⚠️  Could not remove {len(kept)} files:")
        for file in kept:
            print(f"  - {file}")
    
    print(f"\n✅ Essential files retained:")
    essential = [
        'README.md',
        'CHANGELOG.md',
        'SECURITY.md',
        'enhanced_dashboard.py',
        'src/core/app.py',
        'requirements.txt'
    ]
    for file in essential:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ Missing: {file}")

if __name__ == '__main__':
    cleanup_workspace()
    print("\n" + "="*60)
    print("CLEANUP COMPLETE")
    print("="*60)
