"""
DIMDEA ULTRA MASTER BACKEND ENGINE
"""

import pandas as pd
import numpy as np
import logging
from typing import List
import uvicorn   # ✅ ADDED (to run FastAPI server)

# ======================================================
# LOGGING (ADDED FOR DEBUGGING)
# ======================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DIMDEA")

# ======================================================
# ADDED: FASTAPI SERVER (Required for frontend connection)
# ======================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="DIMDEA Carbon Intelligence Engine",
    description="AI-powered carbon intelligence and sustainability platform",
    version="1.0"
)

# ======================================================
# ADDED: CORS (Allows Streamlit frontend to call API)
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# DATABASE
# ======================================================

from backend.database_layer import init_db, create_emission_record, save_simulation_result

# ======================================================
# CORE ANALYTICS
# ======================================================

from backend.carbon_engine import (
    calculate_total_emissions,
)

from backend.carbon_dna import CarbonDNA

from backend.baseline import BaselineCalculator

from backend.hotspot_detection import HotspotDetector
from backend.renewable_engine import RenewableEngine
from backend.environmental_layer import EnvironmentalLayer, generate_environmental_report
from backend.progress_tracker import ProgressTracker
from backend.anomaly_detection import AnomalyDetector
from backend.routing_insights import RoutingInsights
from backend.routing_engine import RoutingEngine
from backend.simulator import EmissionSimulator

from backend.optimization_engine import (
    train_reduction_model,
    optimize_emission_reduction,
    optimize_for_target_reduction
)

from backend.sustainability_score import SustainabilityScoreEngine
from backend.time_optimizer import TimeOptimizer

from backend.esg_reporting import (
    calculate_environmental_score
)

from backend.roadmap_generator import generate_sustainability_roadmap

from backend.privacy_guard import PrivacyGuard
from backend.ethical_ai import EthicalAI


# ======================================================
# API DATA MODELS
# ======================================================

class EmissionPayload(BaseModel):
    transportation: float = 0
    energy: float = 0
    industrial: float = 0
    waste: float = 0
    renewable: float = 0
    baseline: float = 15000


class SimulationPayload(BaseModel):
    reduction: float = 0
    year: int = 2025


class RoadmapPayload(BaseModel):
    target_year: int = 2030
    current_emissions: float = 10000
    target_reduction_percent: float = 40

class RoutingPayload(BaseModel):
    graph: dict
    start: str
    end: str


# ======================================================
# ADDED: OPTIMIZATION PAYLOAD MODEL
# ======================================================

class OptimizationPayload(BaseModel):
    cost_coefficients: List[float]
    reduction_potentials: List[float]
    budget: float

class RoutingInsightsPayload(BaseModel):
    total_distance: float
    total_time: float
    total_emissions: float
    fuel_consumption: float
    number_of_routes: int
    route_breakdown: list


# ======================================================
# SAMPLE DATA
# ======================================================

sample_data_dict = {
    "transportation": 2500,
    "energy": 4000,
    "industrial": 5000,
    "waste": 1200,
    "renewable": 800,
    "baseline": 15000
}


# ======================================================
# HEALTH CHECK ENDPOINT
# ======================================================

@app.get("/", tags=["System"])
def health_check():
    return {"status": "DIMDEA Backend Running"}


# ======================================================
# API ENDPOINT 1 (Carbon DNA Page uses this)
# ======================================================

@app.post("/calculate", tags=["Carbon"])
def calculate(payload: EmissionPayload):

    transportation = payload.transportation
    energy = payload.energy
    industrial = payload.industrial
    waste = payload.waste
    renewable = payload.renewable
    baseline = payload.baseline

    total = transportation + energy + industrial + waste - renewable

    ratio = total / baseline if baseline > 0 else 0

    return {
        "total_emissions": total,
        "baseline": baseline,
        "intensity_ratio": ratio
    }

# ======================================================
# EMISSION CALCULATION FOR DASHBOARD
# ======================================================

@app.post("/calculate-emissions", tags=["Carbon"])
def calculate_emissions_endpoint(payload: EmissionPayload):

    transportation = payload.transportation
    energy = payload.energy
    industrial = payload.industrial

    total = transportation + energy + industrial

    return {
        "total_emissions": total,
        "transportation": transportation,
        "energy": energy,
        "industrial": industrial
    }


# ======================================================
# HOTSPOT ANALYSIS
# ======================================================

@app.post("/hotspot-analysis", tags=["Carbon"])
def hotspot_analysis(payload: EmissionPayload):

    try:

        emission_data = {
            "transportation": payload.transportation,
            "energy": payload.energy,
            "industrial": payload.industrial,
            "waste": payload.waste,
            "renewable": payload.renewable,
            "baseline": payload.baseline
        }

        detector = HotspotDetector(emission_data)

        result = detector.analyze()

        logger.info("Hotspot analysis executed successfully")

        return result

    except Exception as e:

        logger.error(f"Hotspot analysis failed: {e}")

        return {
            "error": "Hotspot analysis failed",
            "details": str(e)
        }


# ======================================================
# CARBON DNA PROFILE
# ======================================================

@app.post("/carbon-dna", tags=["Carbon"])
def carbon_dna_endpoint(payload: EmissionPayload):

    emissions = {
        "transportation": payload.transportation,
        "energy": payload.energy,
        "industry": payload.industrial,
        "waste": payload.waste,
        "renewable": payload.renewable
    }

    dna = CarbonDNA(emissions, payload.baseline)

    return dna.generate_profile()

@app.post("/optimize-route")
def optimize_route(payload: RoutingPayload):

    try:
        graph = payload.graph
        start = payload.start
        end = payload.end

        engine = RoutingEngine(graph)

        path, distance = engine.shortest_path(start, end)

        return {
            "route": path,
            "distance": distance
        }

    except Exception as e:
        return {
            "error": str(e)
        }
    
@app.post("/routing-insights")
def routing_insights(payload: RoutingInsightsPayload):

    try:
        routing_data = {
            "total_distance": payload.total_distance,
            "total_time": payload.total_time,
            "total_emissions": payload.total_emissions,
            "fuel_consumption": payload.fuel_consumption,
            "number_of_routes": payload.number_of_routes,
            "route_breakdown": payload.route_breakdown
        }

        analyzer = RoutingInsights(routing_data)

        insights = analyzer.generate_insights()

        return insights

    except Exception as e:
        return {
            "error": str(e)
        }


# ======================================================
# ENVIRONMENTAL ANALYSIS
# ======================================================

@app.post("/environmental-analysis", tags=["Environment"])
def environmental_analysis(payload: EmissionPayload):

    data = {
        "transportation": payload.transportation,
        "energy": payload.energy,
        "industrial": payload.industrial,
        "waste": payload.waste,
        "renewable": payload.renewable
    }

    layer = EnvironmentalLayer(data)

    return generate_environmental_report(data)


# ======================================================
# ESG SCORE
# ======================================================

@app.post("/esg-score", tags=["ESG"])
def esg_score(payload: EmissionPayload):

    score = calculate_environmental_score(
        carbon_emissions=payload.transportation,
        energy_consumption=payload.energy,
        waste_generated=payload.waste,
        renewable_energy_ratio=0.5
    )

    return {
        "environmental_score": score
    }

# ======================================================
# SUSTAINABILITY SCORE
# ======================================================

@app.post("/sustainability-score", tags=["Sustainability"])
def sustainability_score(payload: EmissionPayload):

    try:

        metrics = {
            "emissions": payload.transportation + payload.energy + payload.industrial,
            "energy_efficiency": payload.energy,
            "waste_recycling": payload.waste,
            "water_usage": payload.waste,
            "renewable_usage": payload.renewable
        }

        engine = SustainabilityScoreEngine()

        result = engine.calculate_score(metrics)

        return result

    except Exception as e:

        logger.error(f"Sustainability score failed: {e}")

        return {
            "error": "Sustainability score failed",
            "details": str(e)
        }

# ======================================================
# SIMULATION
# ======================================================

@app.post("/run-simulation", tags=["Simulation"])
def run_simulation(payload: SimulationPayload):

    reduction = payload.reduction
    year = payload.year

    sim = EmissionSimulator(sample_data_dict)

    result = sim.run_simulation()

    simulated = result["simulated_emissions"]

    data = [
        {"sector": "transportation", "emissions": simulated["transportation"]},
        {"sector": "energy", "emissions": simulated["energy"]},
        {"sector": "industrial", "emissions": simulated["industrial"]},
        {"sector": "waste", "emissions": simulated["waste"]}
    ]

    try:
        save_simulation_result({
            "total_before": 12000,
            "total_after": 9000,
            "emission_reduction": 25,
            "carbon_dna_score_before": 55,
            "carbon_dna_score_after": 72,
            "risk_level_before": "High",
            "risk_level_after": "Moderate",
            "sustainability_improvement_percent": 32
        })
    except Exception as e:
        logger.warning(f"Simulation result not saved: {e}")

    return data


# ======================================================
# OPTIMIZATION ENGINE
# ======================================================

@app.post("/optimize-reduction", tags=["Optimization"])
def optimize_reduction(payload: OptimizationPayload):

    try:

        result = optimize_emission_reduction(
            payload.cost_coefficients,
            payload.reduction_potentials,
            payload.budget
        )

        return result

    except Exception as e:

        logger.error(f"Optimization failed: {e}")

        return {
            "error": "Optimization failed",
            "details": str(e)
        }

@app.get("/debug-endpoints")
def debug_endpoints():
    return {
        "available_endpoints": [
            "/calculate",
            "/calculate-emissions",
            "/hotspot-analysis",
            "/carbon-dna",
            "/routing-insights",
            "/environmental-analysis",
            "/esg-score",
            "/sustainability-score",
            "/run-simulation",
            "/optimize-reduction",
            "/generate-roadmap",
            "/ai-insights"
        ]
    }

# ======================================================
# ROADMAP GENERATOR
# ======================================================

@app.post("/generate-roadmap", tags=["Planning"])
def generate_roadmap(payload: RoadmapPayload):

    roadmap = generate_sustainability_roadmap(
        current_emissions=payload.current_emissions,
        target_reduction_percent=payload.target_reduction_percent,
        target_year=payload.target_year
    )

    return roadmap


# ======================================================
# AI INSIGHTS
# ======================================================

@app.get("/ai-insights", tags=["AI"])
def ai_insights():

    insights = {
        "sustainability_score": 91,
        "decision_score": 96.4,
        "confidence_index": 98,
        "forecast": "Carbon intensity expected to drop by 15%",
        "priority": "Micro-Grid Deployment"
    }

    return insights


# ======================================================
# ETHICAL AI CHECK
# ======================================================

@app.get("/ethical-ai", tags=["AI"])
def ethical_ai_check():

    engine = EthicalAI()

    predictions = [1,0,1,1,0,1]
    actuals = [1,0,1,0,0,1]
    sensitive = ["A","A","B","B","A","B"]

    feature_importance = {
        "energy":0.45,
        "transport":0.32,
        "industry":0.21
    }

    result = engine.evaluate(
        predictions,
        actuals,
        sensitive,
        feature_importance
    )

    return result


# ======================================================
# PRIVACY CHECK
# ======================================================

@app.get("/privacy-status", tags=["Security"])
def privacy_status():

    sample_input = {
        "name": "GreenTech Industries",
        "email": "contact@greentech.com",
        "phone": "9876543210",
        "address": "Chennai, India",
        "organization_id": "GTX-2024",
        "sector": "Manufacturing",
        "emissions": 12000,
        "year": 2024
    }

    guard = PrivacyGuard(sample_input, role="analyst")

    return guard.enforce_privacy()


# ======================================================
# MASTER EXECUTION
# ======================================================

def run_dimdea_ultra():

    print("\n=================================================")
    print("        DIMDEA ULTRA MASTER BACKEND ENGINE")
    print("=================================================\n")

    print("1️⃣ Initializing Database")

    init_db()
    create_emission_record(sample_data_dict)

    print("\n🎉 DIMDEA ULTRA MASTER EXECUTION COMPLETE 🎉")


# ======================================================
# AUTO DATABASE INIT ON STARTUP
# ======================================================

@app.on_event("startup")
def startup_event():
    logger.info("DIMDEA Backend Starting...")
    init_db()


# ======================================================
# LOCAL EXECUTION
# ======================================================

if __name__ == "__main__":
    run_dimdea_ultra()
    uvicorn.run("main_engine:app", host="127.0.0.1", port=8000, reload=True)