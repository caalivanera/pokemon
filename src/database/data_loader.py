"""
Data Loader - Populate database from CSV and YAML sources
Integrates CSV data with YAML enrichment from pokemondbgit
"""

import sys
from pathlib import Path
from typing import Dict, List, Any
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.database.connection import db_manager, init_database
from src.database.models import (
    Pokemon, Move, Ability, TypeEffectiveness,
    PokemonMove, DataQualityMetrics
)
from src.data_loaders.data_extractor import fetch_all_pokemon
from src.data_loaders.yaml_loader import PokemonDataLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedDataLoader:
    """Load and merge data from CSV and YAML sources into database."""

    def __init__(self):
        self.yaml_loader = PokemonDataLoader()
        self.pokemon_df = None
        self.yaml_data = None
        self.stats = {
            'pokemon_loaded': 0,
            'moves_loaded': 0,
            'abilities_loaded': 0,
            'type_effectiveness_loaded': 0,
            'errors': []
        }

    def load_source_data(self):
        """Load data from CSV and YAML sources."""
        logger.info("📂 Loading source data...")

        # Load CSV data
        try:
            self.pokemon_df = fetch_all_pokemon(limit=None)
            logger.info(f"✅ Loaded {len(self.pokemon_df)} Pokemon from CSV")
        except Exception as e:
            logger.error(f"❌ Failed to load CSV data: {e}")
            self.stats['errors'].append(f"CSV load error: {e}")
            return False

        # Load YAML data
        try:
            self.yaml_data = self.yaml_loader.load_all_yaml_data()
            yaml_keys = list(self.yaml_data.keys())
            logger.info(f"✅ Loaded YAML data: {len(yaml_keys)} files")
        except Exception as e:
            logger.error(f"❌ Failed to load YAML data: {e}")
            self.stats['errors'].append(f"YAML load error: {e}")
            return False

        return True

    def populate_pokemon(self):
        """Populate Pokemon table with merged CSV + YAML data."""
        logger.info("🔄 Populating Pokemon table...")

        with db_manager.get_session() as session:
            for _, row in self.pokemon_df.iterrows():
                try:
                    # Get YAML enrichment if available
                    yaml_enrichment = row.get('yaml_enrichment', {})
                    has_yaml = row.get('has_yaml_data', False)

                    pokemon = Pokemon(
                        name=row['name'],
                        japanese_name=row.get('japanese_name'),
                        species=row.get('species'),
                        generation=int(row.get('generation', 1)),
                        primary_type=row['type1'],
                        secondary_type=row.get('type2'),
                        height_m=float(row['height_m'])
                        if row.get('height_m') else None,
                        weight_kg=float(row['weight_kg'])
                        if row.get('weight_kg') else None,
                        hp=int(row['hp']),
                        attack=int(row['attack']),
                        defense=int(row['defense']),
                        special_attack=int(row['sp_attack']),
                        special_defense=int(row['sp_defense']),
                        speed=int(row['speed']),
                        total_points=int(row['base_total']),
                        catch_rate=float(row['catch_rate'])
                        if row.get('catch_rate') else None,
                        base_friendship=float(row['base_friendship'])
                        if row.get('base_friendship') else None,
                        base_experience=float(row['base_experience'])
                        if row.get('base_experience') else None,
                        growth_rate=row.get('growth_rate'),
                        egg_type_1=row.get('egg_type_1'),
                        egg_type_2=row.get('egg_type_2'),
                        percentage_male=float(row['percentage_male'])
                        if row.get('percentage_male') else None,
                        abilities_json=row.get('abilities'),
                        ability_descriptions_json=row.get(
                            'ability_descriptions'
                        ),
                        yaml_enrichment=yaml_enrichment
                        if has_yaml else None,
                        smogon_description=row.get('smogon_description'),
                        bulbapedia_description=row.get(
                            'bulbapedia_description'
                        ),
                        additional_info=row.get('additional_info'),
                        corpus_info=row.get('corpus_info'),
                        has_yaml_data=has_yaml
                    )

                    session.add(pokemon)
                    self.stats['pokemon_loaded'] += 1

                except Exception as e:
                    error_msg = f"Error loading {row.get('name', 'unknown')}: {e}"
                    logger.warning(f"⚠️  {error_msg}")
                    self.stats['errors'].append(error_msg)
                    continue

        logger.info(
            f"✅ Populated {self.stats['pokemon_loaded']} Pokemon records"
        )

    def populate_moves(self):
        """Populate Move table from YAML data."""
        logger.info("🔄 Populating Move table...")

        if 'moves' not in self.yaml_data:
            logger.warning("⚠️  No moves data in YAML")
            return

        moves_yaml = self.yaml_data['moves']

        with db_manager.get_session() as session:
            for move_id, move_data in moves_yaml.items():
                try:
                    move = Move(
                        move_id=move_id,
                        name=move_data.get('name', move_id),
                        type=move_data.get('type'),
                        category=move_data.get('category'),
                        power=move_data.get('power'),
                        accuracy=move_data.get('accuracy'),
                        pp=move_data.get('pp'),
                        priority=move_data.get('priority', 0)
                    )

                    session.add(move)
                    self.stats['moves_loaded'] += 1

                except Exception as e:
                    error_msg = f"Error loading move {move_id}: {e}"
                    logger.warning(f"⚠️  {error_msg}")
                    self.stats['errors'].append(error_msg)
                    continue

        logger.info(f"✅ Populated {self.stats['moves_loaded']} Move records")

    def populate_abilities(self):
        """Populate Ability table from YAML data."""
        logger.info("🔄 Populating Ability table...")

        if 'abilities' not in self.yaml_data:
            logger.warning("⚠️  No abilities data in YAML")
            return

        abilities_yaml = self.yaml_data['abilities']

        with db_manager.get_session() as session:
            for ability_id, ability_data in abilities_yaml.items():
                try:
                    ability = Ability(
                        ability_id=ability_id,
                        name=ability_data.get('name', ability_id)
                    )

                    session.add(ability)
                    self.stats['abilities_loaded'] += 1

                except Exception as e:
                    error_msg = f"Error loading ability {ability_id}: {e}"
                    logger.warning(f"⚠️  {error_msg}")
                    self.stats['errors'].append(error_msg)
                    continue

        logger.info(
            f"✅ Populated {self.stats['abilities_loaded']} Ability records"
        )

    def populate_type_effectiveness(self):
        """Populate TypeEffectiveness table from YAML data."""
        logger.info("🔄 Populating TypeEffectiveness table...")

        if 'type_chart' not in self.yaml_data:
            logger.warning("⚠️  No type chart data in YAML")
            return

        type_chart = self.yaml_data['type_chart']

        with db_manager.get_session() as session:
            for attacking_type, effectiveness in type_chart.items():
                # Super effective (2x)
                for defending_type in effectiveness.get(
                    'super-effective', []
                ):
                    try:
                        te = TypeEffectiveness(
                            attacking_type=attacking_type,
                            defending_type=defending_type,
                            effectiveness_multiplier=2.0
                        )
                        session.add(te)
                        self.stats['type_effectiveness_loaded'] += 1
                    except Exception as e:
                        logger.warning(
                            f"⚠️  Error: {attacking_type}->{defending_type}: {e}"
                        )

                # Not very effective (0.5x)
                for defending_type in effectiveness.get(
                    'not-very-effective', []
                ):
                    try:
                        te = TypeEffectiveness(
                            attacking_type=attacking_type,
                            defending_type=defending_type,
                            effectiveness_multiplier=0.5
                        )
                        session.add(te)
                        self.stats['type_effectiveness_loaded'] += 1
                    except Exception as e:
                        logger.warning(
                            f"⚠️  Error: {attacking_type}->{defending_type}: {e}"
                        )

                # No effect (0x)
                for defending_type in effectiveness.get('no-effect', []):
                    try:
                        te = TypeEffectiveness(
                            attacking_type=attacking_type,
                            defending_type=defending_type,
                            effectiveness_multiplier=0.0
                        )
                        session.add(te)
                        self.stats['type_effectiveness_loaded'] += 1
                    except Exception as e:
                        logger.warning(
                            f"⚠️  Error: {attacking_type}->{defending_type}: {e}"
                        )

        logger.info(
            f"✅ Populated {self.stats['type_effectiveness_loaded']} "
            f"TypeEffectiveness records"
        )

    def record_quality_metrics(self):
        """Record data quality metrics."""
        logger.info("📊 Recording data quality metrics...")

        with db_manager.get_session() as session:
            # Pokemon completeness
            metric = DataQualityMetrics(
                table_name='pokemon',
                metric_name='records_loaded',
                metric_value=float(self.stats['pokemon_loaded']),
                status='pass' if self.stats['pokemon_loaded'] > 0 else 'fail'
            )
            session.add(metric)

            # Moves completeness
            metric = DataQualityMetrics(
                table_name='moves',
                metric_name='records_loaded',
                metric_value=float(self.stats['moves_loaded']),
                status='pass' if self.stats['moves_loaded'] > 0 else 'fail'
            )
            session.add(metric)

            # Error tracking
            metric = DataQualityMetrics(
                table_name='all',
                metric_name='load_errors',
                metric_value=float(len(self.stats['errors'])),
                status='pass' if len(self.stats['errors']) < 10 else 'warn',
                details={'errors': self.stats['errors'][:20]}
            )
            session.add(metric)

        logger.info("✅ Quality metrics recorded")

    def load_all(self):
        """Execute full data load pipeline."""
        logger.info("🚀 Starting data load pipeline...")

        # Initialize database
        init_database()

        # Load source data
        if not self.load_source_data():
            logger.error("❌ Failed to load source data, aborting")
            return False

        # Populate tables
        self.populate_pokemon()
        self.populate_moves()
        self.populate_abilities()
        self.populate_type_effectiveness()

        # Record metrics
        self.record_quality_metrics()

        # Print summary
        logger.info("\n" + "="*60)
        logger.info("📊 DATA LOAD SUMMARY")
        logger.info("="*60)
        logger.info(f"Pokemon loaded: {self.stats['pokemon_loaded']}")
        logger.info(f"Moves loaded: {self.stats['moves_loaded']}")
        logger.info(f"Abilities loaded: {self.stats['abilities_loaded']}")
        logger.info(
            f"Type effectiveness: {self.stats['type_effectiveness_loaded']}"
        )
        logger.info(f"Errors: {len(self.stats['errors'])}")
        logger.info("="*60)

        if self.stats['errors']:
            logger.warning("\n⚠️  Errors encountered:")
            for error in self.stats['errors'][:10]:
                logger.warning(f"  - {error}")

        return True


if __name__ == "__main__":
    loader = EnhancedDataLoader()
    success = loader.load_all()

    if success:
        print("\n✅ Data load completed successfully!")
    else:
        print("\n❌ Data load failed!")
