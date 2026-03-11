"""
DIMDEA - Database Layer
------------------------
Handles:
✔ Database connection
✔ ORM models
✔ Query operations

Does NOT contain:
✖ API routes
✖ Authentication
✖ Frontend logic
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_URL = "sqlite:///dimdea.db"  
# Later you can switch to PostgreSQL:
# DATABASE_URL = "postgresql://user:password@localhost/dimdea"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


# ==========================================================
# ORM MODELS
# ==========================================================

class EmissionRecord(Base):
    """
    Stores raw emission data input.
    """

    __tablename__ = "emission_records"

    id = Column(Integer, primary_key=True, index=True)

    transportation = Column(Float, nullable=False)
    energy = Column(Float, nullable=False)
    industrial = Column(Float, nullable=False)
    waste = Column(Float, nullable=False)
    renewable = Column(Float, nullable=False)

    baseline = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class SimulationResult(Base):
    """
    Stores simulation outputs.
    """

    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True, index=True)

    total_before = Column(Float)
    total_after = Column(Float)
    emission_reduction = Column(Float)

    carbon_dna_score_before = Column(Float)
    carbon_dna_score_after = Column(Float)

    risk_level_before = Column(String(50))
    risk_level_after = Column(String(50))

    sustainability_improvement_percent = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def init_db():
    """
    Create database tables.
    """
    Base.metadata.create_all(bind=engine)


# ==========================================================
# QUERY FUNCTIONS (CRUD OPERATIONS)
# ==========================================================

def create_emission_record(data: dict):
    """
    Insert new emission record.
    """
    session = SessionLocal()
    try:
        record = EmissionRecord(**data)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    finally:
        session.close()


def get_emission_record(record_id: int):
    """
    Fetch emission record by ID.
    """
    session = SessionLocal()
    try:
        return session.query(EmissionRecord).filter(
            EmissionRecord.id == record_id
        ).first()
    finally:
        session.close()


def get_latest_emission_record(as_dict: bool = True):
    """
    Fetch the most recent emission record.
    Useful for frontend auto-loading the latest dataset.
    """
    session = SessionLocal()
    try:
        record = session.query(EmissionRecord).order_by(
            EmissionRecord.created_at.desc()
        ).first()
        if not record:
            return None
        if as_dict:
            return {
                "transportation": record.transportation,
                "energy": record.energy,
                "industrial": record.industrial,
                "waste": record.waste,
                "renewable": record.renewable,
                "baseline": record.baseline
            }
        return record
    finally:
        session.close()


def save_simulation_result(result: dict):
    """
    Store simulation output in database.
    """
    session = SessionLocal()
    try:
        sim = SimulationResult(
            total_before=result["total_before"],
            total_after=result["total_after"],
            emission_reduction=result["emission_reduction"],
            carbon_dna_score_before=result["carbon_dna_score_before"],
            carbon_dna_score_after=result["carbon_dna_score_after"],
            risk_level_before=result["risk_level_before"],
            risk_level_after=result["risk_level_after"],
            sustainability_improvement_percent=result[
                "sustainability_improvement_percent"
            ]
        )

        session.add(sim)
        session.commit()
        session.refresh(sim)
        return sim
    finally:
        session.close()


def get_all_simulations():
    """
    Fetch all simulation records.
    """
    session = SessionLocal()
    try:
        return session.query(SimulationResult).all()
    finally:
        session.close()


# ==========================================================
# TEST BLOCK
# ==========================================================

if __name__ == "__main__":

    init_db()

    # Example insert
    emission_data = {
        "transportation": 2000,
        "energy": 3000,
        "industrial": 4000,
        "waste": 1000,
        "renewable": 500,
        "baseline": 10000
    }

    record = create_emission_record(emission_data)
    print("Inserted Emission Record:", record.id)

    # Example fetch latest record
    latest = get_latest_emission_record()
    print("Latest Emission Record:", latest)