# api/schemas.py

from pydantic import BaseModel


# -----------------------------------------
# EMISSION INPUT
# -----------------------------------------

class EmissionInput(BaseModel):

    transportation: float
    energy: float
    industrial: float


# -----------------------------------------
# EMISSION OUTPUT
# -----------------------------------------

class EmissionOutput(BaseModel):

    transportation: float
    energy: float
    industrial: float
    total_emissions: float