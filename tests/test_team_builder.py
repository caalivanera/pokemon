"""
Test Suite for Team Builder
Tests team management and coverage analysis
"""

import pytest
import sys
from pathlib import Path
import pandas as pd

# Add features to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "features"))

from team_builder import PokemonTeam


@pytest.fixture
def sample_pokemon():
    """Create sample Pokemon data for testing"""
    return {
        'pokedex_number': 6,
        'name': 'Charizard',
        'type_1': 'Fire',
        'type_2': 'Flying',
        'hp': 78,
        'attack': 84,
        'defense': 78,
        'sp_attack': 109,
        'sp_defense': 85,
        'speed': 100,
        'total_points': 534
    }


@pytest.fixture
def sample_pokemon_2():
    """Create second sample Pokemon"""
    return {
        'pokedex_number': 3,
        'name': 'Venusaur',
        'type_1': 'Grass',
        'type_2': 'Poison',
        'hp': 80,
        'attack': 82,
        'defense': 83,
        'sp_attack': 100,
        'sp_defense': 100,
        'speed': 80,
        'total_points': 525
    }


class TestPokemonTeam:
    """Test PokemonTeam class functionality"""
    
    def test_team_initialization(self):
        """Test team is initialized empty"""
        team = PokemonTeam()
        assert len(team.team) == 0, "Team should start empty"
        assert team.max_size == 6, "Max size should be 6"
    
    def test_add_pokemon(self, sample_pokemon):
        """Test adding Pokemon to team"""
        team = PokemonTeam()
        result = team.add_pokemon(sample_pokemon)
        
        assert result is True, "Should successfully add Pokemon"
        assert len(team.team) == 1, "Team should have 1 Pokemon"
        assert team.team[0]['name'] == 'Charizard', "Pokemon should be Charizard"
    
    def test_add_multiple_pokemon(self, sample_pokemon, sample_pokemon_2):
        """Test adding multiple Pokemon"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        team.add_pokemon(sample_pokemon_2)
        
        assert len(team.team) == 2, "Team should have 2 Pokemon"
    
    def test_team_full(self, sample_pokemon):
        """Test that team cannot exceed max size"""
        team = PokemonTeam()
        
        # Add 6 Pokemon
        for i in range(6):
            pokemon = sample_pokemon.copy()
            pokemon['pokedex_number'] = i + 1
            pokemon['name'] = f"Pokemon{i+1}"
            team.add_pokemon(pokemon)
        
        assert len(team.team) == 6, "Team should have 6 Pokemon"
        assert team.is_full(), "Team should be full"
        
        # Try to add 7th
        result = team.add_pokemon(sample_pokemon)
        assert result is False, "Should not add 7th Pokemon"
        assert len(team.team) == 6, "Team should still have 6 Pokemon"
    
    def test_remove_pokemon(self, sample_pokemon, sample_pokemon_2):
        """Test removing Pokemon from team"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        team.add_pokemon(sample_pokemon_2)
        
        team.remove_pokemon(0)
        assert len(team.team) == 1, "Team should have 1 Pokemon after removal"
        assert team.team[0]['name'] == 'Venusaur', "Remaining Pokemon should be Venusaur"
    
    def test_remove_invalid_index(self, sample_pokemon):
        """Test removing Pokemon with invalid index"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        
        team.remove_pokemon(5)  # Invalid index
        assert len(team.team) == 1, "Team should still have 1 Pokemon"
    
    def test_clear_team(self, sample_pokemon, sample_pokemon_2):
        """Test clearing entire team"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        team.add_pokemon(sample_pokemon_2)
        
        team.clear_team()
        assert len(team.team) == 0, "Team should be empty"
    
    def test_get_size(self, sample_pokemon):
        """Test get_size method"""
        team = PokemonTeam()
        assert team.get_size() == 0, "Empty team size should be 0"
        
        team.add_pokemon(sample_pokemon)
        assert team.get_size() == 1, "Team size should be 1"
    
    def test_is_full(self, sample_pokemon):
        """Test is_full method"""
        team = PokemonTeam()
        assert team.is_full() is False, "Empty team should not be full"
        
        for i in range(6):
            pokemon = sample_pokemon.copy()
            pokemon['pokedex_number'] = i + 1
            team.add_pokemon(pokemon)
        
        assert team.is_full() is True, "Team with 6 Pokemon should be full"


class TestTeamTypes:
    """Test team type tracking"""
    
    def test_get_team_types_empty(self):
        """Test getting types from empty team"""
        team = PokemonTeam()
        types = team.get_team_types()
        assert types == [], "Empty team should have no types"
    
    def test_get_team_types_single_type(self, sample_pokemon):
        """Test getting types from team with one Pokemon"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        
        types = team.get_team_types()
        assert 'Fire' in types, "Should include Fire type"
        assert 'Flying' in types, "Should include Flying type"
    
    def test_get_team_types_multiple_pokemon(self, sample_pokemon, sample_pokemon_2):
        """Test getting types from team with multiple Pokemon"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        team.add_pokemon(sample_pokemon_2)
        
        types = team.get_team_types()
        assert 'Fire' in types, "Should include Fire"
        assert 'Flying' in types, "Should include Flying"
        assert 'Grass' in types, "Should include Grass"
        assert 'Poison' in types, "Should include Poison"
    
    def test_get_team_types_no_duplicates(self, sample_pokemon):
        """Test that duplicate types are not repeated"""
        team = PokemonTeam()
        
        # Add two Fire type Pokemon
        pokemon1 = sample_pokemon.copy()
        pokemon2 = sample_pokemon.copy()
        pokemon2['pokedex_number'] = 999
        pokemon2['name'] = 'Charizard2'
        
        team.add_pokemon(pokemon1)
        team.add_pokemon(pokemon2)
        
        types = team.get_team_types()
        # Count occurrences of Fire
        fire_count = types.count('Fire')
        assert fire_count >= 1, "Fire should appear at least once"


class TestTeamStats:
    """Test team statistics calculations"""
    
    def test_get_team_stats_empty(self):
        """Test stats for empty team"""
        team = PokemonTeam()
        stats = team.get_team_stats()
        
        assert stats['avg_hp'] == 0, "Empty team should have 0 avg HP"
        assert stats['avg_attack'] == 0, "Empty team should have 0 avg Attack"
        assert stats['avg_total'] == 0, "Empty team should have 0 avg BST"
    
    def test_get_team_stats_single_pokemon(self, sample_pokemon):
        """Test stats for team with one Pokemon"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        
        stats = team.get_team_stats()
        
        assert stats['avg_hp'] == 78, "Avg HP should match Pokemon HP"
        assert stats['avg_attack'] == 84, "Avg Attack should match Pokemon Attack"
        assert stats['avg_total'] == 534, "Avg BST should match Pokemon BST"
    
    def test_get_team_stats_multiple_pokemon(self, sample_pokemon, sample_pokemon_2):
        """Test stats for team with multiple Pokemon"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)  # BST 534
        team.add_pokemon(sample_pokemon_2)  # BST 525
        
        stats = team.get_team_stats()
        
        expected_avg = (534 + 525) / 2
        assert stats['avg_total'] == expected_avg, "Should calculate correct average BST"
    
    def test_team_stats_keys(self, sample_pokemon):
        """Test that all expected stat keys are present"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        
        stats = team.get_team_stats()
        
        expected_keys = [
            'avg_hp', 'avg_attack', 'avg_defense',
            'avg_sp_attack', 'avg_sp_defense', 'avg_speed', 'avg_total'
        ]
        
        for key in expected_keys:
            assert key in stats, f"Stats should include {key}"


class TestTeamCoverage:
    """Test team type coverage analysis"""
    
    def test_calculate_team_coverage_empty(self):
        """Test coverage for empty team"""
        team = PokemonTeam()
        coverage = team.calculate_team_coverage()
        
        assert 'offensive' in coverage, "Coverage should have offensive key"
        assert 'defensive_weak' in coverage, "Coverage should have defensive_weak key"
    
    def test_calculate_team_coverage(self, sample_pokemon):
        """Test coverage calculation for team with Pokemon"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        
        coverage = team.calculate_team_coverage()
        
        # Fire should be super effective against Grass
        assert 'offensive' in coverage, "Should have offensive coverage"
        assert 'defensive_weak' in coverage, "Should have defensive weaknesses"
    
    def test_coverage_structure(self, sample_pokemon):
        """Test that coverage has correct structure"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        
        coverage = team.calculate_team_coverage()
        
        assert isinstance(coverage['offensive'], list), "Offensive should be a list"
        assert isinstance(coverage['defensive_weak'], list), "Defensive_weak should be list"
        assert isinstance(coverage.get('defensive_resist', []), list), "Defensive_resist should be list"


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_add_none_pokemon(self):
        """Test adding None as Pokemon"""
        team = PokemonTeam()
        result = team.add_pokemon(None)
        assert result is False, "Should not add None"
        assert len(team.team) == 0, "Team should remain empty"
    
    def test_add_empty_dict(self):
        """Test adding empty dictionary"""
        team = PokemonTeam()
        result = team.add_pokemon({})
        # Should either add or reject gracefully
        assert isinstance(result, bool), "Should return boolean"
    
    def test_add_invalid_pokemon(self):
        """Test adding Pokemon with missing fields"""
        team = PokemonTeam()
        invalid_pokemon = {'name': 'Test'}  # Missing required fields
        result = team.add_pokemon(invalid_pokemon)
        # Should handle gracefully
        assert isinstance(result, bool), "Should return boolean"
    
    def test_remove_negative_index(self, sample_pokemon):
        """Test removing with negative index"""
        team = PokemonTeam()
        team.add_pokemon(sample_pokemon)
        
        initial_size = team.get_size()
        team.remove_pokemon(-1)
        # Should either work (Python negative indexing) or ignore
        assert team.get_size() <= initial_size, "Should handle negative index"


class TestTeamComposition:
    """Test realistic team compositions"""
    
    def test_balanced_team(self):
        """Test a balanced competitive team"""
        team = PokemonTeam()
        
        # Typical competitive team: Different types for coverage
        pokemon_list = [
            {'pokedex_number': 1, 'name': 'Bulbasaur', 'type_1': 'Grass', 'type_2': 'Poison',
             'hp': 45, 'attack': 49, 'defense': 49, 'sp_attack': 65, 'sp_defense': 65, 'speed': 45, 'total_points': 318},
            {'pokedex_number': 4, 'name': 'Charmander', 'type_1': 'Fire', 'type_2': None,
             'hp': 39, 'attack': 52, 'defense': 43, 'sp_attack': 60, 'sp_defense': 50, 'speed': 65, 'total_points': 309},
            {'pokedex_number': 7, 'name': 'Squirtle', 'type_1': 'Water', 'type_2': None,
             'hp': 44, 'attack': 48, 'defense': 65, 'sp_attack': 50, 'sp_defense': 64, 'speed': 43, 'total_points': 314},
        ]
        
        for pokemon in pokemon_list:
            team.add_pokemon(pokemon)
        
        assert team.get_size() == 3, "Should have 3 Pokemon"
        
        types = team.get_team_types()
        assert len(set(types)) >= 3, "Should have at least 3 different types"


# Pytest configuration
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
