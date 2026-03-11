import requests

# =====================================================
# Base Backend URL
# =====================================================
BASE_URL = "http://127.0.0.1:8000"


# =====================================================
# 1️⃣ Emission Calculation Endpoint
# =====================================================
def calculate_emissions(payload):
    """
    Sends emission data to backend for carbon calculation.
    """
    url = f"{BASE_URL}/calculate"  # fixed endpoint

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (calculate_emissions): {e}")
        return None


# =====================================================
# 2️⃣ Carbon Engine Endpoint
# =====================================================
def carbon_engine(payload):
    """
    Sends emission data to backend carbon engine.
    """
    url = f"{BASE_URL}/carbon-dna"  # mapped to Carbon DNA API

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (carbon_engine): {e}")
        return None


# =====================================================
# 3️⃣ Environmental Analysis
# =====================================================
def environmental_analysis(payload):
    """
    Calls backend environmental layer analysis.
    """
    url = f"{BASE_URL}/environmental-analysis"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (environmental_analysis): {e}")
        return None


# =====================================================
# 4️⃣ ESG Score
# =====================================================
def esg_score(payload):
    """
    Gets ESG environmental score from backend.
    """
    url = f"{BASE_URL}/esg-score"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (esg_score): {e}")
        return None


# =====================================================
# 5️⃣ Run Emission Simulation
# =====================================================
def run_simulation(payload):
    """
    Runs emission reduction simulation.
    """
    url = f"{BASE_URL}/run-simulation"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (run_simulation): {e}")
        return None


# =====================================================
# 6️⃣ Sustainability Roadmap
# =====================================================
def generate_roadmap(payload):
    """
    Generates sustainability roadmap.
    """
    url = f"{BASE_URL}/generate-roadmap"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (generate_roadmap): {e}")
        return None


# =====================================================
# 7️⃣ AI Insights
# =====================================================
def get_ai_insights():
    """
    Fetch AI sustainability insights.
    """
    url = f"{BASE_URL}/ai-insights"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (ai_insights): {e}")
        return None


# =====================================================
# 8️⃣ Ethical AI Evaluation
# =====================================================
def get_ethical_ai_status():
    """
    Fetch ethical AI evaluation from backend.
    """
    url = f"{BASE_URL}/ethical-ai"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (ethical_ai): {e}")
        return None


# =====================================================
# 9️⃣ Privacy Status
# =====================================================
def get_privacy_status():
    """
    Check privacy protection status of backend.
    """
    url = f"{BASE_URL}/privacy-status"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (privacy_status): {e}")
        return None


# =====================================================
# 🔟 Route Optimization (ADDED FOR ROUTING ENGINE)
# =====================================================
def optimize_route(payload):
    """
    Calls backend routing engine to find optimal path.
    """
    url = f"{BASE_URL}/optimize-route"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (optimize_route): {e}")
        return None
    
# =====================================================
# 11️⃣ Routing Insights
# =====================================================
def routing_insights(payload):
    """
    Fetch routing analytics insights from backend.
    """
    url = f"{BASE_URL}/routing-insights"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (routing_insights): {e}")
        return None
    
# =====================================================
# Sustainability Score Endpoint
# =====================================================

def get_sustainability_score(payload):
    """
    Calls sustainability score API
    """
    url = f"{BASE_URL}/sustainability-score"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Backend error (sustainability_score): {e}")
        return None