from fastapi import FastAPI
from backend.carbon_dna import CarbonDNA
from backend.environmental_layer import run_environmental_analysis
from backend.esg_reporting import run_esg_analysis

# ADDED: logging for debugging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DIMDEA-API")

app = FastAPI()

@app.get("/")
def root():
    return {"message": "DIMDEA Backend Running"}


@app.post("/carbon-dna")
def carbon_dna(data: dict):

    try:

        emissions = data.get("emissions", {})
        baseline = data.get("baseline", 0)

        dna = CarbonDNA(emissions, baseline)
        result = dna.generate_profile()

        return result

    except Exception as e:

        logger.error(f"Carbon DNA analysis failed: {e}")

        return {
            "error": "Carbon DNA analysis failed",
            "details": str(e)
        }


@app.post("/environmental-analysis")
def environmental(data: dict):

    try:

        emissions = data.get("emissions", {})

        result = run_environmental_analysis(emissions)

        return result

    except Exception as e:

        logger.error(f"Environmental analysis failed: {e}")

        return {
            "error": "Environmental analysis failed",
            "details": str(e)
        }


@app.post("/esg-analysis")
def esg(data: dict):

    try:

        result = run_esg_analysis(data)

        return result

    except Exception as e:

        logger.error(f"ESG analysis failed: {e}")

        return {
            "error": "ESG analysis failed",
            "details": str(e)
        }