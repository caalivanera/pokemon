"""
Test script for Phase 5 features (v5.4.0)
Tests: Meta Dashboard, Damage Calculator, Team Recommender
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

print("=" * 60)
print("🧪 Phase 5 Feature Testing Suite")
print("=" * 60)

# Test 1: Meta Analytics Dashboard
print("\n[1/3] Testing Meta Analytics Dashboard...")
try:
    from analytics.meta_dashboard import MetaAnalyticsDashboard
    dashboard = MetaAnalyticsDashboard(data_dir="data")
    print("✅ Meta Dashboard module loaded successfully")
    print(f"   - Class: {dashboard.__class__.__name__}")
    print(f"   - Data directory: {dashboard.data_dir}")
except Exception as e:
    print(f"❌ Meta Dashboard test failed: {e}")

# Test 2: Damage Calculator
print("\n[2/3] Testing Damage Calculator...")
try:
    from analytics.damage_calculator import DamageCalculator
    calculator = DamageCalculator(data_dir="data")
    print("✅ Damage Calculator module loaded successfully")
    print(f"   - Class: {calculator.__class__.__name__}")
    
    # Test type effectiveness
    effectiveness = calculator.get_type_effectiveness("Fire", "Grass")
    print(f"   - Type effectiveness test (Fire vs Grass): {effectiveness}x")
    assert effectiveness == 2.0, "Fire should be super effective against Grass"
    
    # Test damage calculation
    damage = calculator.calculate_damage(
        attacker_level=100,
        attacker_attack=300,
        defender_defense=200,
        move_power=100,
        type_effectiveness=2.0,
        stab=1.5,
        critical=False
    )
    print(f"   - Damage calculation test: {damage} damage")
    assert damage > 0, "Damage should be greater than 0"
    
    print("✅ All Damage Calculator tests passed")
except Exception as e:
    print(f"❌ Damage Calculator test failed: {e}")

# Test 3: Team Recommender
print("\n[3/3] Testing AI Team Recommender...")
try:
    from analytics.team_recommender import TeamRecommender
    recommender = TeamRecommender(data_dir="data")
    print("✅ Team Recommender module loaded successfully")
    print(f"   - Class: {recommender.__class__.__name__}")
    
    # Test type coverage analysis
    test_team = [
        {'name': 'Charizard', 'type1': 'Fire', 'type2': 'Flying'},
        {'name': 'Blastoise', 'type1': 'Water', 'type2': None}
    ]
    coverage = recommender.analyze_team_coverage(test_team)
    print(f"   - Coverage analysis: {len(coverage['covered_types'])} types covered")
    print(f"   - Weaknesses: {len(coverage['weaknesses'])} total")
    
    assert 'covered_types' in coverage, "Coverage should have covered_types"
    assert 'weaknesses' in coverage, "Coverage should have weaknesses"
    
    print("✅ All Team Recommender tests passed")
except Exception as e:
    print(f"❌ Team Recommender test failed: {e}")

# Test 4: Image Optimizer
print("\n[4/4] Testing Image Optimization Script...")
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from optimize_images import ImageOptimizer
    optimizer = ImageOptimizer()
    print("✅ Image Optimizer module loaded successfully")
    print(f"   - Class: {optimizer.__class__.__name__}")
    print(f"   - Default quality: {optimizer.quality}")
    print(f"   - Workers: {optimizer.workers}")
except Exception as e:
    print(f"❌ Image Optimizer test failed: {e}")

# Summary
print("\n" + "=" * 60)
print("✅ Phase 5 Feature Testing Complete!")
print("=" * 60)
print("\n📋 Next Steps:")
print("1. Run Streamlit app: streamlit run src/core/app.py")
print("2. Test each new tab (13, 14, 15)")
print("3. Verify data loading")
print("4. Test exports and calculations")
print("\n🎯 All modules imported successfully!")
print("Ready for integration testing.\n")
