import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DIMDEA | Upload Emission Dataset",
    page_icon="📤",
    layout="wide"
)

# --- CUSTOM CSS FOR DIMDEA CLIMATE-TECH THEME ---
st.markdown("""
    <style>
        /* Main Theme Colors */
        :root {
            --primary: #050C16;
            --secondary: #0A192F;
            --accent: #00FFAB;
        }
        
        /* Global Background */
        .stApp {
            background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%) !important;
            color: #FFFFFF !important;
        }
        
        /* Header Styling */
        .main-title {
            color: #00D2FF;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        
        .sub-title {
            color: var(--accent);
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        /* Card-style Containers */
        .stMetric, .css-1r6slb0, .stDataFrame {
            border: 1px solid rgba(0, 210, 255, 0.2);
            padding: 15px;
            border-radius: 10px;
            background-color: rgba(255,255,255,0.05);
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
        }

        /* Success & Error Messages */
        .stAlert {
            border-radius: 8px;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #00D2FF !important;
            color: #0A192F !important;
            border-radius: 5px;
            border: none;
            font-weight: 700;
        }
        .stButton>button:hover {
            background-color: var(--accent) !important;
            color: var(--primary) !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- APP LAYOUT ---
st.markdown('<h1 class="main-title">📤 Upload Emission Dataset</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Ingest environmental data into the DIMDEA Climate Intelligence engines for anomaly detection and sustainability analytics.</p>', unsafe_allow_html=True)

# --- FILE UPLOADER COMPONENT ---
with st.container():
    uploaded_file = st.file_uploader(
        "Select your emission dataset (CSV or XLSX)",
        type=["csv", "xlsx"],
        help="Ensure your file contains transportation, energy, industry, waste, renewable, and baseline columns."
    )

if uploaded_file is not None:
    try:
        # Load File
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.divider()

        # --- VALIDATION LOGIC ---
        required_columns = ['transportation', 'energy', 'industry', 'waste', 'renewable', 'baseline']
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        # 1. Check for missing columns
        if missing_cols:
            st.error(f"❌ **Dataset missing required columns:** {', '.join(missing_cols)}")
        
        # 2. Check for numeric values and missing data
        elif df[required_columns].isnull().values.any():
            st.error("❌ **Validation Failed:** The dataset contains missing (NaN) values in required emission sectors.")
        
        elif not all(pd.api.types.is_numeric_dtype(df[col]) for col in required_columns):
            st.error("❌ **Validation Failed:** All emission sector columns must contain numeric values.")
            
        else:
            # --- SUCCESS PATH ---
            
            # Layout Columns: Summary on left, Preview on right
            col1, col2 = st.columns([1, 2], gap="large")

            with col1:
                st.subheader("📊 Dataset Summary")
                
                # Metric Cards
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("Total Rows", df.shape[0])
                m_col2.metric("Total Columns", df.shape[1])
                
                # Detected Sectors List
                st.markdown("### Detected Sectors")
                for col in required_columns:
                    st.markdown(f"✅ `{col.capitalize()}`")

            with col2:
                st.subheader("📄 Data Preview (First 5 Rows)")
                st.dataframe(df.head(5), use_container_width=True)

            # --- SAVE DATASET ---
            # Ensure 'data' directory exists
            if not os.path.exists('data'):
                os.makedirs('data')
            
            save_path = "data/user_inputs.csv"
            df.to_csv(save_path, index=False)

            # -----------------------------
            # ADDED FOR DIMDEA FRONTEND INTEGRATION
            # Store uploaded dataset path in session_state
            st.session_state.uploaded_dataset = save_path
            # -----------------------------

            # --- FINAL SUCCESS NOTIFICATION ---
            st.success("✅ **Dataset uploaded and validated successfully!**")
            
            with st.expander("Submission Details"):
                st.write(f"**Filename:** {uploaded_file.name}")
                st.write(f"**Storage Path:** `{save_path}`")
                st.write(f"**Status:** Ready for Backend Processing")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

else:
    # Placeholder when no file is uploaded
    st.info("Please upload a CSV or Excel file to begin.")

# --- FOOTER ---
st.markdown("---")
st.caption("DIMDEA Climate Intelligence Platform | Proprietary UI for Dataset Ingestion")