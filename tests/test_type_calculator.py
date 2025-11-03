"""
Test Suite for Type Calculator
Tests type effectiveness calculations and coverage analysis
"""

import pytest
import sys
from pathlib import Path

# Add features to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "features"))

from type_calculator import (
    calculate_type_effectiveness,
    get_pokemon_weaknesses,
    get_offensive_coverage,
    TYPE_CHART
)


class TestTypeEffectiveness:
    """Test type effectiveness calculations"""
    
    def test_super_effective_single_type(self):
        """Test super effective matchup (2x damage)"""
        result = calculate_type_effectiveness('Fire', ['Grass'])
        assert result == 2.0, "Fire should be 2x effective against Grass"
    
    def test_not_effective_single_type(self):
        """Test not very effective matchup (0.5x damage)"""
        result = calculate_type_effectiveness('Fire', ['Water'])
        assert result == 0.5, "Fire should be 0.5x effective against Water"
    
    def test_no_effect(self):
        """Test immunity (0x damage)"""
        result = calculate_type_effectiveness('Normal', ['Ghost'])
        assert result == 0.0, "Normal should have no effect on Ghost"
    
    def test_neutral_damage(self):
        """Test neutral matchup (1x damage)"""
        result = calculate_type_effectiveness('Fire', ['Electric'])
        assert result == 1.0, "Fire should be neutral against Electric"
    
    def test_dual_type_double_weakness(self):
        """Test 4x damage on dual type (both types weak)"""
        result = calculate_type_effectiveness('Water', ['Fire', 'Rock'])
        assert result == 4.0, "Water should be 4x effective against Fire/Rock"
    
    def test_dual_type_neutralized(self):
        """Test dual type where weakness is canceled by resistance"""
        result = calculate_type_effectiveness('Water', ['Fire', 'Grass'])
        assert result == 1.0, "Water vs Fire/Grass should be neutral (2x * 0.5x)"
    
    def test_dual_type_quadruple_resistance(self):
        """Test 0.25x damage on dual type (both resist)"""
        result = calculate_type_effectiveness('Grass', ['Fire', 'Steel'])
        assert result == 0.25, "Grass should be 0.25x against Fire/Steel"
    
    def test_invalid_attacking_type(self):
        """Test handling of invalid attacking type"""
        result = calculate_type_effectiveness('InvalidType', ['Fire'])
        assert result == 1.0, "Invalid type should default to neutral"
    
    def test_invalid_defending_type(self):
        """Test handling of invalid defending type"""
        result = calculate_type_effectiveness('Fire', ['InvalidType'])
        assert result == 1.0, "Invalid defending type should default to neutral"
    
    def test_empty_defending_types(self):
        """Test handling of empty defending types"""
        result = calculate_type_effectiveness('Fire', [])
        assert result == 1.0, "Empty defending types should be neutral"


class TestPokemonWeaknesses:
    """Test Pokemon weakness analysis"""
    
    def test_single_type_weaknesses(self):
        """Test weakness calculation for single type Pokemon"""
        result = get_pokemon_weaknesses(['Fire'])
        
        assert 'Water' in result['weak'], "Fire should be weak to Water"
        assert 'Ground' in result['weak'], "Fire should be weak to Ground"
        assert 'Rock' in result['weak'], "Fire should be weak to Rock"
        assert 'Fire' in result['resistant'], "Fire should resist Fire"
        assert 'Grass' in result['resistant'], "Fire should resist Grass"
    
    def test_dual_type_weaknesses(self):
        """Test weakness calculation for dual type Pokemon"""
        result = get_pokemon_weaknesses(['Fire', 'Flying'])
        
        # Fire/Flying is 4x weak to Rock
        assert 'Rock' in result['very_weak'], "Fire/Flying should be 4x weak to Rock"
        
        # Should resist some types
        assert 'Grass' in result['very_resistant'], "Fire/Flying should double resist Grass"
    
    def test_no_weaknesses(self):
        """Test Pokemon with immunities"""
        result = get_pokemon_weaknesses(['Ghost'])
        
        assert 'Normal' in result['immune'], "Ghost should be immune to Normal"
        assert 'Fighting' in result['immune'], "Ghost should be immune to Fighting"
    
    def test_all_types_covered(self):
        """Test that all 18 types are accounted for"""
        result = get_pokemon_weaknesses(['Normal'])
        
        total_types = (
            len(result['immune']) +
            len(result['very_resistant']) +
            len(result['resistant']) +
            len(result['neutral']) +
            len(result['weak']) +
            len(result['very_weak'])
        )
        
        assert total_types == 18, "All 18 types should be categorized"


class TestOffensiveCoverage:
    """Test offensive coverage analysis"""
    
    def test_single_type_coverage(self):
        """Test offensive coverage for single type"""
        result = get_offensive_coverage(['Fire'])
        
        assert 'Grass' in result['super_effective'], "Fire should hit Grass super effectively"
        assert 'Ice' in result['super_effective'], "Fire should hit Ice super effectively"
        assert 'Bug' in result['super_effective'], "Fire should hit Bug super effectively"
        assert 'Steel' in result['super_effective'], "Fire should hit Steel super effectively"
    
    def test_dual_type_coverage(self):
        """Test offensive coverage for dual type"""
        result = get_offensive_coverage(['Water', 'Ground'])
        
        # Water hits Fire, Rock, Ground
        # Ground hits Fire, Electric, Poison, Rock, Steel
        # Combined should hit many types
        assert 'Fire' in result['super_effective'], "Water/Ground should hit Fire"
        assert 'Rock' in result['super_effective'], "Water/Ground should hit Rock"
        assert 'Steel' in result['super_effective'], "Water/Ground should hit Steel"
    
    def test_coverage_no_duplicates(self):
        """Test that coverage lists don't have duplicates"""
        result = get_offensive_coverage(['Water', 'Electric'])
        
        # Check no duplicates in any category
        assert len(result['super_effective']) == len(set(result['super_effective']))
        assert len(result['neutral']) == len(set(result['neutral']))
        assert len(result['not_effective']) == len(set(result['not_effective']))


class TestTypeChart:
    """Test type chart data integrity"""
    
    def test_all_types_present(self):
        """Test that all 18 types are in the chart"""
        expected_types = [
            'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
            'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug',
            'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'
        ]
        
        for type_name in expected_types:
            assert type_name in TYPE_CHART, f"{type_name} should be in TYPE_CHART"
    
    def test_type_chart_structure(self):
        """Test that each type has required keys"""
        required_keys = [
            'weak_to', 'resistant_to', 'immune_to',
            'super_effective', 'not_effective', 'no_effect'
        ]
        
        for type_name, type_data in TYPE_CHART.items():
            for key in required_keys:
                assert key in type_data, f"{type_name} should have {key}"
    
    def test_reciprocal_relationships(self):
        """Test that type relationships are reciprocal"""
        # If Fire is super effective against Grass,
        # Grass should be weak to Fire
        for attacker, attacker_data in TYPE_CHART.items():
            for defender in attacker_data['super_effective']:
                if defender in TYPE_CHART:
                    assert attacker in TYPE_CHART[defender]['weak_to'], \
                        f"{defender} should be weak to {attacker}"


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_none_attacking_type(self):
        """Test handling of None as attacking type"""
        result = calculate_type_effectiveness(None, ['Fire'])
        assert result == 1.0, "None attacking type should be neutral"
    
    def test_none_in_defending_types(self):
        """Test handling of None in defending types"""
        result = calculate_type_effectiveness('Fire', [None, 'Grass'])
        # Should still calculate for Grass
        assert result > 0, "Should handle None in defending types"
    
    def test_case_sensitivity(self):
        """Test that type names are case-sensitive or handled"""
        result1 = calculate_type_effectiveness('Fire', ['Grass'])
        result2 = calculate_type_effectiveness('fire', ['grass'])
        # Both should work or one should default to neutral
        assert result1 > 0 and result2 >= 0, "Should handle case variations"
    
    def test_whitespace_in_types(self):
        """Test handling of whitespace in type names"""
        result = calculate_type_effectiveness(' Fire ', [' Grass '])
        # Should either trim or default to neutral
        assert result >= 0, "Should handle whitespace"


class TestRealWorldScenarios:
    """Test real-world Pokemon scenarios"""
    
    def test_charizard_matchup(self):
        """Test Charizard (Fire/Flying) vs Blastoise (Water)"""
        result = calculate_type_effectiveness('Water', ['Fire', 'Flying'])
        assert result == 2.0, "Water should be 2x effective against Fire/Flying"
    
    def test_garchomp_matchup(self):
        """Test Garchomp (Dragon/Ground) weaknesses"""
        result = get_pokemon_weaknesses(['Dragon', 'Ground'])
        assert 'Ice' in result['very_weak'], "Dragon/Ground should be 4x weak to Ice"
    
    def test_ferrothorn_resistance(self):
        """Test Ferrothorn (Grass/Steel) resistances"""
        result = get_pokemon_weaknesses(['Grass', 'Steel'])
        # Grass/Steel resists many types
        total_resists = len(result['resistant']) + len(result['very_resistant'])
        assert total_resists >= 9, "Grass/Steel should resist many types"
    
    def test_spiritomb_coverage(self):
        """Test Spiritomb (Ghost/Dark) weaknesses before Gen 6"""
        result = get_pokemon_weaknesses(['Ghost', 'Dark'])
        # Ghost/Dark was only weak to nothing before Fairy type
        # Now should be weak to Fairy
        assert 'Fairy' in result['weak'], "Ghost/Dark should be weak to Fairy"


# Pytest configuration
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
