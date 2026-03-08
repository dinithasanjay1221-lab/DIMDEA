# api/routes.py

from fastapi import APIRouter, Depends
from api.schemas import EmissionInput, EmissionOutput
from api.auth import get_current_user
from backend.carbon_engine import calculate_total_emissions
from backend.database_layer import create_emission_record

router = APIRouter(
    prefix="/api",
    tags=["DIMDEA API"]
)

# -----------------------------------------
# HEALTH CHECK
# -----------------------------------------

@router.get("/health")
def health_check():
    return {"status": "healthy"}


# -----------------------------------------
# CARBON CALCULATION
# -----------------------------------------

@router.post("/calculate", response_model=EmissionOutput)
def calculate_emissions(
    data: EmissionInput
):

    total = (
        data.transportation +
        data.energy +
        data.industrial
    )

    # SAVE DATA INTO DATABASE
    create_emission_record({
        "transportation": data.transportation,
        "energy": data.energy,
        "industrial": data.industrial,
        "waste": 0,
        "renewable": 0,
        "baseline": total
    })

    return EmissionOutput(
        transportation=data.transportation,
        energy=data.energy,
        industrial=data.industrial,
        total_emissions=total
    )

@router.post("/carbon-engine")
def carbon_engine(data: EmissionInput):

    result = calculate_total_emissions(
        data.transportation,
        data.energy,
        data.industrial
    )

    return {"result": result}