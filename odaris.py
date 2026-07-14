"""
GLUCOVISION AI PRO ULTRA (ENTERPRISE EDITION)
AI-Powered Personalized Diabetes Management & Glycemic Predictive Twin
Educational Sandbox Prototype - Secure Architecture Build
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io
import math

# ─── ADVANCED PAGE ARCHITECTURE ──────────────────────────────────────────────
st.set_page_config(
    page_title="GlucoVision AI Pro Ultra",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PREMIUM CYBERPUNK DARK THEME INTERFACE CUSTOMIZATION ─────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc;
}

/* Base Canvas Styling */
.stApp {
    background-color: #030712;
    background-image: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #030712 70%);
}

/* Sidebar Component Mapping */
section[data-testid="stSidebar"] {
    background-color: #0b0f19;
    border-right: 2px solid #3b82f6;
    box-shadow: 5px 0 25px rgba(0,0,0,0.5);
}

/* Inputs & Component Borders */
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div {
    background-color: #111827 !important;
    border: 2px solid #374151 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.4) !important;
}

/* Form Headings and Labels */
label {
    color: #9ca3af !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    font-size: 0.85rem !important;
}

/* Custom Action Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
    letter-spacing: 0.05em;
    padding: 0.75rem 2.5rem !important;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(29, 78, 216, 0.4);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%) !important;
}

/* Premium Card Panels */
.crypto-card {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid #1f2937;
    border-top: 4px solid #3b82f6;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
}

/* Component Metric Widgets */
.metric-box {
    background: linear-gradient(145deg, #111827, #1f2937);
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 100%; height: 4px;
    background: #3b82f6;
}
.mb-green::before { background: #10b981; }
.mb-red::before { background: #ef4444; }
.mb-purple::before { background: #a855f7; }
.mb-orange::before { background: #f59e0b; }

.metric-box-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.25rem;
    font-weight: 700;
    color: #ffffff;
    margin[-bottom]: 0.25rem;
}
.metric-box-lbl {
    font-size: 0.75rem;
    color: #9ca3af;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Dynamic Section Header Layouts */
.sec-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0 1.25rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #1f2937;
}
.sec-icon {
    font-size: 1.5rem;
    background: rgba(59, 130, 246, 0.1);
    padding: 0.5rem;
    border-radius: 8px;
    color: #3b82f6;
    border: 1px solid rgba(59, 130, 246, 0.2);
}
.sec-title {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    color: #ffffff;
}

/* Alert Notification Matrix */
.alert-banner {
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-weight: 600;
    border-left: 5px solid transparent;
}
.ab-danger { background: rgba(239, 68, 68, 0.1); border-color: #ef4444; color: #fca5a5; }
.ab-warning { background: rgba(245, 158, 11, 0.1); border-color: #f59e0b; color: #fde68a; }
.ab-success { background: rgba(16, 185, 129, 0.1); border-color: #10b981; color: #a7f3d0; }

</style>
""", unsafe_allow_html=True)

# ─── INITIALIZE MASTER INTERACTION STORAGE DATABASE (SESSION STATE) ───────────
if "users_db" not in st.session_state:
    st.session_state.users_db = {"admin": "admin123", "patient": "glucose"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "patient_logs" not in st.session_state:
    st.session_state.patient_logs = []

# ─── HUGE NUTRITIONAL MACRO DICTIONARY GRID (2X PLUS EXPANDED) ────────────────
FOOD_DB = {
    "White Cooked Rice (100g)": {"calories": 130, "carbs": 28.0, "protein": 2.7, "fat": 0.3, "gi": 73},
    "Basmati Rice (100g)": {"calories": 121, "carbs": 25.0, "protein": 2.7, "fat": 0.4, "gi": 58},
    "Brown Rice Cooked (100g)": {"calories": 111, "carbs": 23.0, "protein": 2.6, "fat": 0.9, "gi": 55},
    "Wheat Roti / Chapati (1 Medium)": {"calories": 104, "carbs": 20.0, "protein": 3.0, "fat": 1.7, "gi": 62},
    "Millet Roti / Bajra (50g)": {"calories": 135, "carbs": 24.0, "protein": 3.6, "fat": 2.1, "gi": 54},
    "Plain Naan (90g)": {"calories": 260, "carbs": 45.0, "protein": 7.0, "fat": 6.0, "gi": 71},
    "Idli (2 Pcs)": {"calories": 78, "carbs": 16.0, "protein": 2.5, "fat": 0.4, "gi": 65},
    "Plain Dosa (80g)": {"calories": 168, "carbs": 28.0, "protein": 3.9, "fat": 3.7, "gi": 66},
    "Ragi Mudde Ball (100g)": {"calories": 125, "carbs": 27.0, "protein": 2.2, "fat": 0.6, "gi": 59},
    "Poha Bowl (150g)": {"calories": 180, "carbs": 38.0, "protein": 3.6, "fat": 1.8, "gi": 75},
    "Upma Semolina (150g)": {"calories": 200, "carbs": 32.0, "protein": 4.5, "fat": 6.0, "gi": 68},
    "Toor Dal Cooked (150g)": {"calories": 170, "carbs": 28.0, "protein": 10.5, "fat": 1.5, "gi": 42},
    "Moong Dal Cooked (150g)": {"calories": 150, "carbs": 25.0, "protein": 10.0, "fat": 0.6, "gi": 38},
    "Soya Chunks Curry (150g)": {"calories": 160, "carbs": 11.0, "protein": 18.0, "fat": 5.0, "gi": 20},
    "Paneer Tikka cubes (100g)": {"calories": 265, "carbs": 1.2, "protein": 18.3, "fat": 20.8, "gi": 15},
    "Tofu Stir-Fry Organic (100g)": {"calories": 95, "carbs": 2.5, "protein": 10.1, "fat": 5.5, "gi": 15},
    "Boiled Egg Large": {"calories": 78, "carbs": 0.6, "protein": 6.3, "fat": 5.3, "gi": 0},
    "Grilled Chicken Breast (100g)": {"calories": 165, "carbs": 0.0, "protein": 31.0, "fat": 3.6, "gi": 0},
    "Fish Rohu Curry (100g)": {"calories": 105, "carbs": 0.0, "protein": 20.0, "fat": 2.4, "gi": 0},
    "Boiled Diced Potato (100g)": {"calories": 87, "carbs": 20.0, "protein": 1.9, "fat": 0.1, "gi": 78},
    "Sweet Potato Baked (100g)": {"calories": 90, "carbs": 20.7, "protein": 2.0, "fat": 0.1, "gi": 63},
    "Steamed Broccoli Florets (100g)": {"calories": 35, "carbs": 7.0, "protein": 2.8, "fat": 0.4, "gi": 15},
    "Spinach Palak Cooked (100g)": {"calories": 23, "carbs": 3.6, "protein": 2.9, "fat": 0.4, "gi": 15},
    "Fresh Cucumber Slices (100g)": {"calories": 15, "carbs": 3.6, "protein": 0.7, "fat": 0.1, "gi": 15},
    "Avocado Halved Core (80g)": {"calories": 130, "carbs": 6.8, "protein": 1.5, "fat": 11.7, "gi": 10},
    "Ripe Whole Banana (120g)": {"calories": 105, "carbs": 27.0, "protein": 1.3, "fat": 0.4, "gi": 51},
    "Apple with Skin (150g)": {"calories": 78, "carbs": 21.0, "protein": 0.4, "fat": 0.3, "gi": 39},
    "Fresh Mango Slices (200g)": {"calories": 120, "carbs": 30.0, "protein": 1.6, "fat": 0.6, "gi": 56},
    "Blueberries Raw (150g)": {"calories": 84, "carbs": 21.0, "protein": 1.1, "fat": 0.5, "gi": 53},
    "Greek Yogurt Unsweetened (100g)": {"calories": 59, "carbs": 3.6, "protein": 10.0, "fat": 0.4, "gi": 12},
    "Roasted Peanuts Crunch (30g)": {"calories": 170, "carbs": 6.0, "protein": 7.7, "fat": 14.5, "gi": 14},
    "Raw Almonds Kernel (12g)": {"calories": 70, "carbs": 2.6, "protein": 2.6, "fat": 6.0, "gi": 10},
    "Chia Seeds Organic (12g)": {"calories": 60, "carbs": 5.0, "protein": 2.0, "fat": 4.0, "gi": 5},
    "Flaxseeds Whole Powder (7g)": {"calories": 37, "carbs": 2.0, "protein": 1.3, "fat": 3.0, "gi": 10},
    "Samosa Deep Fried (60g)": {"calories": 260, "carbs": 24.0, "protein": 3.5, "fat": 17.0, "gi": 75},
    "Vada Pav Treat (120g)": {"calories": 290, "carbs": 40.0, "protein": 7.0, "fat": 11.0, "gi": 71},
    "Pav Bhaji Plate Combo (250g)": {"calories": 400, "carbs": 50.0, "protein": 8.0, "fat": 18.0, "gi": 69},
    "Instant Packet Noodles (70g)": {"calories": 310, "carbs": 44.0, "protein": 6.0, "fat": 12.0, "gi": 73},
    "Refined Sugar Crystals (5g)": {"calories": 19, "carbs": 5.0, "protein": 0.0, "fat": 0.0, "gi": 65},
    "Pure Organic Honey (7g)": {"calories": 21, "carbs": 5.6, "protein": 0.0, "fat": 0.0, "gi": 58},
    "Dark Chocolate (85% Cocoa) (20g)": {"calories": 120, "carbs": 7.0, "protein": 2.0, "fat": 10.0, "gi": 20},
    "Gulab Jamun Dessert (2 Pcs)": {"calories": 300, "carbs": 40.0, "protein": 4.0, "fat": 14.0, "gi": 82},
}

# ─── SECURE GATEWAY ENGINES (LOGIN/REGISTRATION UIs) ─────────────────────────
def render_authentication_gateway():
    st.markdown("""
    <div style='text-align: center; margin-top: 5vh; margin-bottom: 3vh;'>
        <h1 style='color: #3b82f6; font-size: 3.5rem; font-weight:800; margin-bottom:0;'>GLUCOVISION AI</h1>
        <p style='color: #9ca3af; font-size: 1.1rem; text-transform:uppercase; letter-spacing:0.15em;'>Clinical Intelligence Portal Gateway</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.5, 1])
    with col_b:
        auth_mode = st.tabs(["🔐 Secure User Login", "🚀 Create Digital Twin Account"])
        
        with auth_mode[0]:
            with st.form("login_form"):
                st.markdown("<h3 style='margin-top:0;'>Access Dashboard Control</h3>", unsafe_allow_html=True)
                username_in = st.text_input("Username / Patient Identifier", key="login_uid")
                password_in = st.text_input("Security Passkey Phrase", type="password", key="login_pwd")
                submit_login = st.form_submit_button("AUTHORIZE SECURITY CLEARANCE")
                
                if submit_login:
                    if username_in in st.session_state.users_db and st.session_state.users_db[username_in] == password_in:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username_in
                        st.success(f"Security clearance confirmed. Welcome back, {username_in}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials profile. Check system settings or access phrase.")
                        
        with auth_mode[1]:
            with st.form("signup_form"):
                st.markdown("<h3 style='margin-top:0;'>Register New Twin Identity</h3>", unsafe_allow_html=True)
                new_user = st.text_input("Desired Unique Username", key="sign_uid")
                new_pass = st.text_input("Assign Complex Passkey Phrase", type="password", key="sign_pwd")
                confirm_pass = st.text_input("Re-verify Complex Passkey Phrase", type="password", key="sign_pwd_conf")
                submit_signup = st.form_submit_button("INITIALIZE BIOLOGICAL SEED PROFILE")
                
                if submit_signup:
                    if not new_user or not new_pass:
                        st.error("Fields cannot be processed as null values.")
                    elif new_user in st.session_state.users_db:
                        st.error("Identity identifier mapping token matches existing record.")
                    elif new_pass != confirm_pass:
                        st.error("Passkey validation parameters do not match.")
                    else:
                        st.session_state.users_db[new_user] = new_pass
                        st.success("Identity vector instantiated successfully! Proceed to standard login portal tab.")

# ─── EXTENDED MULTI-COMPARTMENT PHYSIOLOGICAL MATH SIMULATORS ─────────────────
def run_advanced_simulation(
    current_glucose: float, carbs: float, diabetes_type: str, insulin_type: str,
    insulin_dose: float, exercise_type: str, exercise_dur: float, avg_gi: float,
    stress_mode: str, dawn_mode: bool, weight: float
) -> dict:
    
    timeline = list(range(0, 241, 5))
    glucose_curve = []
    
    # Sensitivity Indices
    isf = 1800.0 / (weight * 0.5) if diabetes_type == "Type 1 Diabetes" else 2200.0 / (weight * 0.6)
    if diabetes_type == "No Diabetes": isf *= 1.5
    cr = (weight * 0.35) if diabetes_type == "Type 1 Diabetes" else (weight * 0.45)
    
    # Stress / Dawn Factors
    stress_modifier = 40.0 if stress_mode == "High Stress Matrix" else (15.0 if stress_mode == "Moderate / Fatigue" else 0.0)
    dawn_bump = 35.0 if dawn_mode else 0.0
    
    # Exercise absorption coefficients
    ex_multiplier = 1.0
    if exercise_type == "Moderate Aerobic": ex_multiplier = 1.4
    elif exercise_type == "HIIT/Anaerobic Circuit": ex_multiplier = 1.9
    ex_drop = (exercise_dur * 0.5) * ex_multiplier

    for t in timeline:
        # Complex dual-smoothstep curve modelling
        # Carb Absorption Profile Function
        t_peak = 55.0 * (avg_gi / 55.0)
        if t <= t_peak:
            c_frac = (t / t_peak) ** 2 * (3.0 - 2.0 * (t / t_peak))
        else:
            t_decay = 120.0
            rem = max(0.0, min(1.0, (t - t_peak) / t_decay))
            c_frac = 1.0 - (rem ** 2 * (3.0 - 2.0 * rem))
        carb_impact = (carbs / cr * 40.0 * c_frac) if cr > 0 else 0
        
        # Insulin Profile Clearance Function
        i_onset, i_peak, i_end = 15.0, 75.0, 240.0
        if insulin_type == "Regular Short-Acting": i_onset, i_peak, i_end = 45, 120, 360
        elif insulin_type == "Basal Long-Acting": i_onset, i_peak, i_end = 90, 300, 1440
        
        if t <= i_onset: ins_frac = 0.0
        elif t <= i_peak: ins_frac = 0.5 * ((t - i_onset) / (i_peak - i_onset)) ** 2
        elif t <= i_end: ins_frac = 0.5 + 0.5 * ((t - i_peak) / (i_end - i_peak))
        else: ins_frac = 1.0
        insulin_impact = insulin_dose * isf * ins_frac
        
        # Linearization shifts
        ex_frac = min(1.0, t / max(15.0, exercise_dur)) if exercise_dur > 0 else 0
        current_ex_impact = ex_drop * ex_frac
        
        stress_impact = stress_modifier * (t / 90.0 if t <= 90 else 1.0)
        dawn_impact = dawn_bump * (t / 180.0 if t <= 180 else 1.0)
        
        g_t = current_glucose + carb_impact - insulin_impact - current_ex_impact + stress_impact + dawn_impact
        glucose_curve.append(max(40.0, round(g_t, 1)))
        
    return {"timeline": timeline, "curve": glucose_curve}

def run_analytics(curve: list[float]) -> dict:
    arr = np.array(curve)
    tir = np.sum((arr >= 70) & (arr <= 180)) / len(arr) * 100
    tbr = np.sum(arr < 70) / len(arr) * 100
    tar = np.sum(arr > 180) / len(arr) * 100
    avg = np.mean(arr)
    hba1c = (avg + 46.7) / 28.7
    cv = (np.std(arr) / avg) * 100
    
    return {"tir": round(tir, 1), "tbr": round(tbr, 1), "tar": round(tar, 1), "avg": round(avg, 1), "hba1c": round(hba1c, 2), "cv": round(cv, 1)}

# ─── MAIN APP ROUTING ENGINE CONTROLLER ───────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        render_authentication_gateway()
        return

    # --- SIDEBAR CONTROLS ---
    with st.sidebar:
        st.markdown(f"""
        <div style='background: rgba(59,130,246,0.1); padding:1rem; border-radius:10px; border:1px solid #3b82f6; text-align:center; margin-bottom:1rem;'>
            <span style='font-size:0.8rem; color:#9ca3af; font-weight:700; display:block;'>SECURE OPERATOR</span>
            <span style='font-size:1.2rem; color:#ffffff; font-weight:800; display:block;'>👤 {st.session_state.current_user}</span>
        </div>
        """, unsafe_allow_html=True)
        
        panel = st.radio(
            "🎛️ CONTROL CENTER MODULES",
            ["Twin Predictive Grid", "Smart Bolus Calculator", "Multi-Day Trend Lab", "Nutrient Matrix Library"],
            index=0
        )
        st.markdown("---")
        if st.button("🔒 DE-AUTHORIZE & LOGOUT"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()

    # -------------------------------------------------------------------------
    # MODULE 1: INTERACTIVE BIO-TWIN SIMULATION & PREDICTIVE ALERT ARCHITECTURE
    # -------------------------------------------------------------------------
    if panel == "Twin Predictive Grid":
        st.markdown("""
        <div class="sec-header">
            <div class="sec-icon">🔮</div>
            <div class="sec-title">Predictive Digital Twin Simulation Canvas</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns([1, 2])
        
        with col_p1:
            st.markdown("<div class='crypto-card'><h4>Biometric Baselines</h4>", unsafe_allow_html=True)
            d_type = st.selectbox("Diabetes Class Profile", ["Type 1 Diabetes", "Type 2 Diabetes", "Prediabetes", "No Diabetes"])
            w_kg = st.number_input("Patient Mass (kg)", min_value=30.0, max_value=200.0, value=75.0)
            g_start = st.number_input("Realtime Baseline Glucose (mg/dL)", min_value=40, max_value=450, value=140)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='crypto-card'><h4>Nutrient Ingestion Matrix</h4>", unsafe_allow_html=True)
            selected_items = st.multiselect("Select Target Meal Logs", list(FOOD_DB.keys()), default=["White Cooked Rice (100g)"])
            
            calc_carbs = 0.0
            calc_gi = 55.0
            if selected_items:
                sum_gi_w = 0.0
                for item in selected_items:
                    calc_carbs += FOOD_DB[item]["carbs"]
                    sum_gi_w += FOOD_DB[item]["gi"] * FOOD_DB[item]["carbs"]
                if calc_carbs > 0:
                    calc_gi = sum_gi_w / calc_carbs
            
            custom_carbs = st.number_input("Adjust Net Carbs Overhead (grams)", min_value=0.0, max_value=250.0, value=float(calc_carbs))
            custom_gi = st.slider("Resultant Meal Glycemic Index", min_value=10, max_value=100, value=int(calc_gi))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='crypto-card'><h4>Active Pharmacology / Stress Modifiers</h4>", unsafe_allow_html=True)
            i_type = st.selectbox("Insulin Action Track", ["Rapid-Acting Analogue", "Regular Short-Acting", "Basal Long-Acting"])
            i_dose = st.number_input("Administered Dose Load (Units)", min_value=0.0, max_value=50.0, value=4.0, step=0.5)
            ex_type = st.selectbox("Physical Metabolism Clearance", ["Sedentary / Rest", "Moderate Aerobic", "HIIT/Anaerobic Circuit"])
            ex_dur = st.number_input("Activity Duration (Minutes)", min_value=0, max_value=120, value=0)
            stress_mode = st.selectbox("Systemic Stress State", ["Homeostasis / Normal", "Moderate / Fatigue", "High Stress Matrix"])
            dawn_mode = st.checkbox("Dawn Effect Cortisol Spike")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_p2:
            # RUN CORE SIMULATION MATHEMATICAL PIPELINE
            sim = run_advanced_simulation(g_start, custom_carbs, d_type, i_type, i_dose, ex_type, ex_dur, custom_gi, stress_mode, dawn_mode, w_kg)
            an = run_analytics(sim["curve"])
            
            # CRITICAL REALTIME PREDICTIVE ALERTS (NEW STUFF)
            min_val = min(sim["curve"])
            max_val = max(sim["curve"])
            
            if min_val < 55:
                st.markdown("<div class='alert-banner ab-danger'>🚨 CRITICAL ALERT: Severe Hypoglycemia (< 55 mg/dL) predicted within timeline! Immediate ingestion of fast glucose required.</div>", unsafe_allow_html=True)
            elif min_val < 70:
                st.markdown("<div class='alert-banner ab-warning'>⚠️ WARNING: Mild Hypoglycemia trends predicted. Review correction calculations.</div>", unsafe_allow_html=True)
            
            if max_val > 250:
                st.markdown("<div class='alert-banner ab-danger'>🔥 SPECTRUM HAZARD: Severe Hyperglycemic saturation peak exceeding 250 mg/dL predicted.</div>", unsafe_allow_html=True)
            elif max_val > 180:
                st.markdown("<div class='alert-banner ab-warning'>📈 ELEVATION: Extended Time-Above-Range detected in digital twin forecast matrix.</div>", unsafe_allow_html=True)
            
            if min_val >= 70 and max_val <= 180:
                st.markdown("<div class='alert-banner ab-success'>🛡️ COMPLIANCE OPTIMAL: Twin system models perfect metabolic envelope constraints throughout projection timeline.</div>", unsafe_allow_html=True)
            
            # DASHBOARD TELEMETRY READOUT METRIC MATRICES
            m1, m2, m3, m4 = st.columns(4)
            with m1: st.markdown(f"<div class='metric-box mb-green'><div class='metric-box-val'>{an['tir']}%</div><div class='metric-box-lbl'>Time In Range</div></div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div class='metric-box mb-purple'><div class='metric-box-val'>{an['hba1c']}%</div><div class='metric-box-lbl'>Est. HbA1c</div></div>", unsafe_allow_html=True)
            with m3: st.markdown(f"<div class='metric-box mb-orange'><div class='metric-box-val'>{an['cv']}%</div><div class='metric-box-lbl'>Glycemic Var (CV)</div></div>", unsafe_allow_html=True)
            with m4: st.markdown(f"<div class='metric-box mb-red'><div class='metric-box-val'>{an['avg']}</div><div class='metric-box-lbl'>Mean Trend (mg/dL)</div></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # TIMELINE SCATTER PLOT
            fig = go.Figure()
            fig.add_shape(type="rect", x0=0, y0=70, x1=240, y1=180, fillcolor="rgba(16, 185, 129, 0.06)", line_width=0)
            fig.add_trace(go.Scatter(x=sim["timeline"], y=sim["curve"], mode='lines+markers', name='Twin Projection', line=dict(color='#3b82f6', width=4), marker=dict(size=5, color='#ffffff')))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17, 24, 39, 0.5)',
                title=dict(text="Continuous 240-Minute Simulated Vector Track", font=dict(color="#ffffff", size=16)),
                xaxis=dict(title="Time Inception (Minutes)", color="#9ca3af", gridcolor="#374151"),
                yaxis=dict(title="Glucose Vector (mg/dL)", color="#9ca3af", gridcolor="#374151"),
                margin=dict(l=40, r=40, t=50, b=40), height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # PERSIST SIMULATION LOG DATA BUTTON
            if st.button("💾 COMMITT LOG DATA POINT TO CLOUD STORAGE"):
                log_entry = {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "carbs": custom_carbs,
                    "dose": i_dose,
                    "tir": an["tir"],
                    "hba1c": an["hba1c"]
                }
                st.session_state.patient_logs.append(log_entry)
                st.success("State parameters preserved inside ephemeral network logs successfully.")

    # -------------------------------------------------------------------------
    # MODULE 2: CLINICAL INTEGRATION SMART INSULIN BOLUS CALCULATOR ENGINE
    # -------------------------------------------------------------------------
    elif panel == "Smart Bolus Calculator":
        st.markdown("""
        <div class="sec-header">
            <div class="sec-icon">📐</div>
            <div class="sec-title">Clinical Smart Bolus Dose Decider Engine</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 **Precision Medicine Architecture:** Calculates targeted corrections based on personal Carb-to-Insulin Ratios and target physiological bounds.")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("<div class='crypto-card'>", unsafe_allow_html=True)
            target_g = st.number_input("Target Desired Blood Glucose (mg/dL)", min_value=80, max_value=140, value=100)
            current_g = st.number_input("Actual Measured Capillary Glucose (mg/dL)", min_value=40, max_value=450, value=185)
            meal_carbs = st.number_input("Carbohydrate Mass Ingestion Forecast (grams)", min_value=0, max_value=200, value=60)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_c2:
            st.markdown("<div class='crypto-card'>", unsafe_allow_html=True)
            user_cr = st.number_input("Insulin-to-Carbohydrate Ratio (ICR) [grams of carb covered by 1 Unit]", min_value=2.0, max_value=30.0, value=10.0)
            user_isf = st.number_input("Insulin Sensitivity Factor (ISF) [mg/dL drop caused by 1 Unit]", min_value=10.0, max_value=100.0, value=50.0)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # CALCULATOR LOGIC MATHEMATICS
        carb_dose = meal_carbs / user_cr if user_cr > 0 else 0
        correction_dose = (current_g - target_g) / user_isf if current_g > target_g else 0.0
        total_recommended_bolus = round(carb_dose + correction_dose, 2)
        
        st.markdown("### Suggested Dose Metrics Summary Output")
        rc1, rc2, rc3 = st.columns(3)
        with rc1: st.markdown(f"<div class='metric-box mb-purple'><div class='metric-box-val'>{round(carb_dose,2)} U</div><div class='metric-box-lbl'>Nutrient Carbohydrate Load Component</div></div>", unsafe_allow_html=True)
        with rc2: st.markdown(f"<div class='metric-box mb-orange'><div class='metric-box-val'>{round(correction_dose,2)} U</div><div class='metric-box-lbl'>Correction Shift Component</div></div>", unsafe_allow_html=True)
        with rc3: st.markdown(f"<div class='metric-box mb-green'><div class='metric-box-val' style='color:#10b981;'>{total_recommended_bolus} U</div><div class='metric-box-lbl'>Total Optimized Suggestion Dose</div></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MODULE 3: MULTI-DAY DEEP TREND GRAPH ANALYSIS SANDBOX
    # -------------------------------------------------------------------------
    elif panel == "Multi-Day Trend Lab":
        st.markdown("""
        <div class="sec-header">
            <div class="sec-icon">📈</div>
            <div class="sec-title">Multi-Day Longitudinal Glycemic Synthesizer</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='color:#9ca3af;'>Simulates dynamic trend timelines over a 7-day period to analyze systemic volatility variance.</p>", unsafe_allow_html=True)
        
        days_count = st.slider("Select Longitudinal Window Duration (Days)", min_value=2, max_value=14, value=7)
        volatility_factor = st.slider("Set Metabolic Volatility Scaling Coefficient", min_value=10, max_value=100, value=35)
        
        # Generating a structural randomized deterministic multi-day continuous walk
        np.random.seed(42)
        total_datapoints = days_count * 24
        time_index = [datetime.now() - timedelta(hours=total_datapoints - i) for i in range(total_datapoints)]
        
        base_walk = 130.0 + np.sin(np.linspace(0, days_count * 2 * np.pi, total_datapoints)) * 30.0
        random_noise = np.random.normal(0, volatility_factor, total_datapoints)
        synthesized_glucose = np.clip(base_walk + random_noise, 45.0, 380.0)
        
        df_trends = pd.DataFrame({"Timeline": time_index, "Capillary Glucose Vector": synthesized_glucose})
        
        fig_trend = px.line(df_trends, x="Timeline", y="Capillary Glucose Vector", title=f"Continuous System Synthesis Profile Across {days_count} Full Diurnal Cycles")
        fig_trend.update_traces(line_color="#10b981", line_width=2.5)
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17, 24, 39, 0.5)',
            xaxis=dict(color="#ffffff", gridcolor="#1f2937"),
            yaxis=dict(color="#ffffff", gridcolor="#1f2937", range=[30, 400]),
            title_font=dict(color="#ffffff")
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Display summary tables
        st.markdown("#### Cloud Preserved History Snapshots")
        if st.session_state.patient_logs:
            st.dataframe(pd.DataFrame(st.session_state.patient_logs), use_container_width=True)
        else:
            st.markdown("<p style='color:#6b7280; font-style:italic;'>No local twin instances initialized to current runtime buffers yet.</p>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MODULE 4: EXTENDED 2X FOOD METABOLIC REGISTRY EXPLORER INDEX
    # -------------------------------------------------------------------------
    elif panel == "Nutrient Matrix Library":
        st.markdown("""
        <div class="sec-header">
            <div class="sec-icon">🥗</div>
            <div class="sec-title">Metabolic Macro Nutrient Inventory Query Explorer</div>
        </div>
        """, unsafe_allow_html=True)
        
        search_filter = st.text_input("Filter Registry Records (e.g. Rice, Seeds, Roti, Chicken)...", value="")
        
        rows = []
        for name_key, values in FOOD_DB.items():
            if search_filter.lower() in name_key.lower():
                rows.append({
                    "Nutrient Nomenclature Key": name_key,
                    "Energy (kcal)": values["calories"],
                    "Carbohydrates (g)": values["carbs"],
                    "Proteins (g)": values["protein"],
                    "Lipids (g)": values["fat"],
                    "Glycemic Index Speed": values["gi"],
                    "Glycemic Impact Level": "🔴 HIGH SPEED" if values["gi"] >= 70 else ("🟡 MODERATE" if values["gi"] >= 50 else "🟢 STABLE / SMOOTH")
                })
                
        if rows:
            df_view = pd.DataFrame(rows)
            st.dataframe(df_view.style.background_gradient(cmap="coolwarm", subset=["Glycemic Index Speed"]), use_container_width=True, height=550)
        else:
            st.error("No database rows discovered matching filter query array tokens.")

    # ─── LEGAL COMPLIANCE FOOTER DISCLAIMER GRID BLOCK ──────────────────────────
    st.markdown("""
    <hr style='border-color: #1f2937;'/>
    <div style='text-align:center; padding: 1.5rem; opacity: 0.7;'>
        <p style='color:#ef4444; font-size:0.85rem; font-weight:700; margin-bottom:4px;'>🛑 CLINICAL SAFETY DIRECTIVE MANDATE REGULATION NOTICE</p>
        <p style='color:#9ca3af; font-size:0.75rem; max-width:900px; margin: 0 auto; line-height:1.6;'>
            GlucoVision AI Pro Ultra is an advanced, non-certified experimental numerical simulation twin network. All data outputs, prediction arrays, and dosage metrics are algorithmic estimations designed for display showcase validation prototyping. They do not constitute actionable medical telemetry advice. Always consult an authenticated endocrinologist for actual therapeutic management adjustments.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
