"""
Pokemon Database Models - SQLAlchemy ORM
Enterprise-grade schema with relationships and constraints
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, 
    ForeignKey, DateTime, JSON, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Pokemon(Base):
    """Main Pokemon table with comprehensive attributes."""
    
    __tablename__ = 'pokemon'
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(100), nullable=False, unique=True, index=True)
    japanese_name = Column(String(100))
    species = Column(String(100))
    generation = Column(Integer, nullable=False, index=True)
    
    # Types
    primary_type = Column(String(50), nullable=False, index=True)
    secondary_type = Column(String(50), index=True)
    
    # Physical Stats
    height_m = Column(Float)
    weight_kg = Column(Float)
    
    # Base Stats
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    special_attack = Column(Integer, nullable=False)
    special_defense = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False, index=True)
    
    # Capture & Experience
    catch_rate = Column(Float)
    base_friendship = Column(Float)
    base_experience = Column(Float)
    growth_rate = Column(String(50))
    
    # Breeding
    egg_type_1 = Column(String(50))
    egg_type_2 = Column(String(50))
    percentage_male = Column(Float)
    
    # Extended Data (JSON fields for flexibility)
    abilities_json = Column(JSON)
    ability_descriptions_json = Column(JSON)
    yaml_enrichment = Column(JSON)
    
    # Descriptions
    smogon_description = Column(Text)
    bulbapedia_description = Column(Text)
    additional_info = Column(Text)
    corpus_info = Column(Text)
    
    # Metadata
    sprite_url = Column(String(500))
    has_yaml_data = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    moves = relationship("PokemonMove", back_populates="pokemon")
    stats_history = relationship("PokemonStatsHistory", back_populates="pokemon")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_pokemon_types', 'primary_type', 'secondary_type'),
        Index('idx_pokemon_generation', 'generation'),
        Index('idx_pokemon_total_points', 'total_points'),
    )
    
    def __repr__(self):
        return f"<Pokemon(id={self.id}, name='{self.name}', types={self.primary_type}/{self.secondary_type})>"


class Move(Base):
    """Pokemon moves with detailed stats."""
    
    __tablename__ = 'moves'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    move_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False, index=True)
    category = Column(String(50))  # physical, special, status
    power = Column(Integer)
    accuracy = Column(Integer)
    pp = Column(Integer)
    priority = Column(Integer, default=0)
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    pokemon_moves = relationship("PokemonMove", back_populates="move")
    
    def __repr__(self):
        return f"<Move(name='{self.name}', type='{self.type}', power={self.power})>"


class PokemonMove(Base):
    """Many-to-Many relationship between Pokemon and Moves."""
    
    __tablename__ = 'pokemon_moves'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    move_id = Column(Integer, ForeignKey('moves.id'), nullable=False)
    
    learn_method = Column(String(50))  # level-up, TM, egg, tutor
    level_learned = Column(Integer)
    
    # Relationships
    pokemon = relationship("Pokemon", back_populates="moves")
    move = relationship("Move", back_populates="pokemon_moves")
    
    __table_args__ = (
        UniqueConstraint('pokemon_id', 'move_id', name='unique_pokemon_move'),
        Index('idx_pokemon_moves', 'pokemon_id', 'move_id'),
    )


class Ability(Base):
    """Pokemon abilities."""
    
    __tablename__ = 'abilities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ability_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Ability(name='{self.name}')>"


class TypeEffectiveness(Base):
    """Type effectiveness chart for damage calculations."""
    
    __tablename__ = 'type_effectiveness'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    attacking_type = Column(String(50), nullable=False, index=True)
    defending_type = Column(String(50), nullable=False, index=True)
    effectiveness_multiplier = Column(Float, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('attacking_type', 'defending_type', name='unique_type_matchup'),
        Index('idx_type_matchup', 'attacking_type', 'defending_type'),
    )
    
    def __repr__(self):
        return f"<TypeEffectiveness({self.attacking_type} -> {self.defending_type}: {self.effectiveness_multiplier}x)>"


class PokemonStatsHistory(Base):
    """Track historical stat changes for analytics."""
    
    __tablename__ = 'pokemon_stats_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    
    # Stats snapshot
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)
    total_points = Column(Integer)
    
    # Metadata
    version = Column(String(50))  # Game version
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    pokemon = relationship("Pokemon", back_populates="stats_history")
    
    __table_args__ = (
        Index('idx_stats_history', 'pokemon_id', 'recorded_at'),
    )


class DataQualityMetrics(Base):
    """Track data quality metrics over time."""
    
    __tablename__ = 'data_quality_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    table_name = Column(String(100), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float)
    status = Column(String(50))  # pass, warn, fail
    details = Column(JSON)
    
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_quality_metrics', 'table_name', 'checked_at'),
    )


class UserAnalytics(Base):
    """Track user interactions for analytics."""
    
    __tablename__ = 'user_analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    session_id = Column(String(100), index=True)
    user_id = Column(String(100), index=True)
    
    event_type = Column(String(100), nullable=False)  # view, filter, export, etc.
    event_data = Column(JSON)
    
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'))
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_user_analytics', 'session_id', 'timestamp'),
        Index('idx_event_analytics', 'event_type', 'timestamp'),
    )


class MLPredictionLog(Base):
    """Log ML model predictions for monitoring."""
    
    __tablename__ = 'ml_prediction_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    model_name = Column(String(100), nullable=False, index=True)
    model_version = Column(String(50))
    
    input_features = Column(JSON)
    prediction = Column(JSON)
    confidence_score = Column(Float)
    
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'))
    
    predicted_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_ml_predictions', 'model_name', 'predicted_at'),
    )


if __name__ == "__main__":
    from sqlalchemy import create_engine
    
    # Create SQLite database for testing
    engine = create_engine('sqlite:///pokemon_enterprise.db', echo=True)
    Base.metadata.create_all(engine)
    print("✅ Database schema created successfully!")
