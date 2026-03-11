# api/schemas.py

from pydantic import BaseModel

# -----------------------------------------
# EMISSION INPUT
# -----------------------------------------
class EmissionInput(BaseModel):
    """
    Schema for inputting emission data.
    """
    transportation: float
    energy: float
    industrial: float

# -----------------------------------------
# EMISSION OUTPUT
# -----------------------------------------
class EmissionOutput(BaseModel):
    """
    Schema for returning calculated emission data.
    """
    transportation: float
    energy: float
    industrial: float
    total_emissions: float