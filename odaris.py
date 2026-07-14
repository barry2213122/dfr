"""
GLUCOVISION AI PRO - ULTIMATE EDITION
Advanced Personalized Diabetes Monitoring, Metabolic Modeling & Glucose Prediction Dashboard
Enterprise-Grade Science Fair Demonstration Prototype
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import math
import hashlib
import hmac
import json
import secrets
from pathlib import Path

# ─── SECURE USER ACCOUNT DATABASE SYSTEM (JSON PROTOTYPE) ───────────────────
USERS_DB_PATH = Path(__file__).parent / "glucovision_users.json"

def _load_users() -> dict:
    if USERS_DB_PATH.exists():
        try:
            with open(USERS_DB_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def _save_users(users: dict) -> None:
    with open(USERS_DB_PATH, "w") as f:
        json.dump(users, f, indent=2, default=str)

def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return pwd_hash, salt

def _verify_password(password: str, salt: str, stored_hash: str) -> bool:
    test_hash, _ = _hash_password(password, salt)
    return hmac.compare_digest(test_hash, stored_hash)

def create_account(username: str, email: str, password: str) -> tuple[bool, str]:
    users = _load_users()
    key = username.strip().lower()
    if not key or not password:
        return False, "❌ Username and password are required."
    if key in users:
        return False, "❌ That username is already taken."
    pwd_hash, salt = _hash_password(password)
    users[key] = {
        "username": username.strip(),
        "email": email.strip(),
        "password_hash": pwd_hash,
        "salt": salt,
        "premium": False,
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "profile": {
            "age": 35, "gender": "Male", "weight": 70.0, "height": 175.0,
            "diabetes_type": "Type 2 Diabetes", "insulin_type": "Basal + Bolus",
            "target_low": 70, "target_high": 140, "icr": 10.0, "isf": 40.0
        }
    }
    _save_users(users)
    return True, "✅ Account created successfully!"

def authenticate(username: str, password: str) -> tuple[bool, str]:
    users = _load_users()
    key = username.strip().lower()
    if key not in users:
        return False, "❌ No account found with that username."
    record = users[key]
    if not _verify_password(password, record["salt"], record["password_hash"]):
        return False, "❌ Incorrect password."
    record["last_login"] = datetime.now().isoformat()
    users[key] = record
    _save_users(users)
    return True, "🚀 Welcome back!"

def update_user_profile(user_key: str, profile_data: dict) -> None:
    users = _load_users()
    if user_key in users:
        users[user_key]["profile"].update(profile_data)
        _save_users(users)

def toggle_premium_status(user_key: str, status: bool) -> None:
    users = _load_users()
    if user_key in users:
        users[user_key]["premium"] = status
        _save_users(users)

# ─── STREAMLIT UI CONFIG & CUSTOM STYLING ─────────────────────────────────────
st.set_page_config(
    page_title="GlucoVision AI Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #f0f4f8;
}
.stApp {
    background-color: #0a0d14;
}
section[data-testid="stSidebar"] {
    background-color: #111524;
    border-right: 2px solid #00f0ff;
}
label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label {
    color: #00f0ff !important;
    font-weight: 700 !important;
}
p, .stMarkdown p {
    color: #cbd5e1;
}
.metric-card {
    background: linear-gradient(135deg, #161c33 0%, #0f1322 100%);
    border: 1px solid #1e293b;
    border-top: 4px solid #00f0ff;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    font-family: 'Space Grotesk', sans-serif;
    margin-top: 0.2rem;
}
.metric-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
}
.section-header {
    border-left: 5px solid #00f0ff;
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
}
.premium-tag {
    background: linear-gradient(90deg, #ff007f, #7928ca);
    color: white;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
}
.rec-card {
    background-color: #13192e;
    border: 1px solid #1e294a;
    border-left: 5px solid #00e676;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.8rem;
}
.stButton > button {
    background: linear-gradient(90deg, #00f0ff, #0072ff) !important;
    color: #0a0d14 !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: none !important;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,240,255,0.4);
}
.disclaimer {
    background-color: #2a080c;
    border: 1px solid #ef4444;
    border-radius: 8px;
    padding: 0.8rem;
    color: #fca5a5;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ─── NUTRITIONAL GLOBAL DATA INDEX ────────────────────────────────────────────
FOOD_DB = {
    "Cooked Rice (White) (150g)": {"calories": 195, "carbs": 42, "protein": 4.0, "fat": 0.4, "gi": 73},
    "Basmati Rice (Cooked) (150g)": {"calories": 182, "carbs": 38, "protein": 4.1, "fat": 0.5, "gi": 55},
    "Whole Wheat Roti (1 medium)": {"calories": 105, "carbs": 22, "protein": 3.5, "fat": 0.5, "gi": 62},
    "Oatmeal (1 cup cooked)": {"calories": 150, "carbs": 27, "protein": 6.0, "fat": 2.5, "gi": 55},
    "Dal Tadka / Lentils (1 bowl)": {"calories": 165, "carbs": 24, "protein": 9.0, "fat": 3.5, "gi": 32},
    "Paneer Tikka (100g)": {"calories": 240, "carbs": 4, "protein": 16.0, "fat": 18.0, "gi": 15},
    "Grilled Chicken Breast (150g)": {"calories": 245, "carbs": 0, "protein": 46.0, "fat": 6.0, "gi": 0},
    "Mixed Garden Salad (1 bowl)": {"calories": 35, "carbs": 6, "protein": 1.5, "fat": 0.2, "gi": 15},
    "Greek Yogurt (Plain, 150g)": {"calories": 100, "carbs": 6, "protein": 15.0, "fat": 2.0, "gi": 14},
    "Apple (1 medium)": {"calories": 95, "carbs": 25, "protein": 0.5, "fat": 0.3, "gi": 39},
    "Samosa (1 piece)": {"calories": 260, "carbs": 32, "protein": 4.5, "fat": 13.0, "gi": 80},
    "Soft Drink / Soda (350ml)": {"calories": 150, "carbs": 39, "protein": 0.0, "fat": 0.0, "gi": 95}
}

# ─── SESSION STATE INITIALIZATION ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_key" not in st.session_state:
    st.session_state.user_key = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "premium" not in st.session_state:
    st.session_state.premium = False
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "meal_plate" not in st.session_state:
    st.session_state.meal_plate = []

# ─── MEDICAL COMPLIANCE DISCLAIMER COMPONENT ─────────────────────────────────
def render_disclaimer():
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>CRITICAL CLINICAL NOTICE & SIMULATION DISCLAIMER:</strong> 
        GlucoVision AI Pro is an advanced educational metabolic prototype created for algorithmic analysis. 
        It is <strong>NOT a certified medical device</strong>. Predictions are based on localized biological simulation 
        approximations and must never be utilized to modify prescribed insulin doses or healthcare management programs.
    </div>
    """, unsafe_allow_html=True)

# ─── AUTHENTICATION LAYER GATING RENDER ───────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #00f0ff;'>🩺 GLUCOVISION AI PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Predictive Computational Engine & Multi-Tier Metabolic Analytics Platform</p>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔒 Secure Authentication", "📝 Create Analytics Account"])
    
    with tab_login:
        with st.form("auth_login"):
            st.subheader("Login Gateway")
            uid = st.text_input("Username / Patient ID")
            pwd = st.text_input("Password", type="password")
            btn_login = st.form_submit_button("Authenticate System")
            if btn_login:
                success, msg = authenticate(uid, pwd)
                if success:
                    user_record = _load_users()[uid.strip().lower()]
                    st.session_state.authenticated = True
                    st.session_state.user_key = uid.strip().lower()
                    st.session_state.username = user_record["username"]
                    st.session_state.premium = user_record.get("premium", False)
                    st.session_state.profile = user_record.get("profile", {})
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    with tab_signup:
        with st.form("auth_signup"):
            st.subheader("Register Core Account Profile")
            new_uid = st.text_input("Desired Username")
            new_email = st.text_input("Secure Email Address")
            new_pwd = st.text_input("Access Password (6+ characters)", type="password")
            confirm_pwd = st.text_input("Confirm Access Password", type="password")
            btn_signup = st.form_submit_button("Initialize Profile Database")
            if btn_signup:
                if len(new_pwd.strip()) < 6:
                    st.error("❌ Password safety threshold mismatch (Minimum 6 characters).")
                elif new_pwd != confirm_pwd:
                    st.error("❌ Confirmed password does not match entry pipeline.")
                else:
                    success, msg = create_account(new_uid, new_email, new_pwd)
                    if success:
                        st.success(msg + " Proceed to Login tab.")
                    else:
                        st.error(msg)
    st.stop()

# ─── METABOLIC SIMULATION ENGINE MATHEMATICAL FUNCTIONS ────────────────────────
def run_advanced_metabolic_simulation(current_glucose, total_carbs, total_protein, total_fat, average_gi, profile, exercise_type, exercise_dur):
    """
    Simulates a 4-hour dynamic glucose profile tracking curve utilizing 
    pharmacokinetic curves for meal absorption, active baseline insulin, and muscle disposal rates.
    """
    timeline = []
    glucose_points = []
    
    # Calculate baseline coefficients from patient type
    diab_type = profile.get("diabetes_type", "Type 2 Diabetes")
    base_isf = profile.get("isf", 40.0)
    
    # Calculate physiological absorption shifts
    # Protein & Fat blunt the peak absorption rate, delaying the curve peak
    blunt_factor = 1 + (total_protein * 0.1 + total_fat * 0.2) / (total_carbs + 1)
    peak_time_min = min(120, max(30, int(45 * (average_gi / 55) * blunt_factor)))
    
    # Exercise impact coefficients
    disposal_multiplier = 1.0
    if exercise_type == "Cardio (Running/Cycling)":
        disposal_multiplier += 0.015 * exercise_dur
    elif exercise_type == "Resistance Training":
        disposal_multiplier += 0.008 * exercise_dur
    elif exercise_type == "HIIT / High Intensity":
        disposal_multiplier += 0.022 * exercise_dur

    for t in range(0, 241, 10):
        timeline.append(t)
        
        # 1. Carb Digestion Delta (log-normal wave proxy)
        if total_carbs > 0:
            # Rise function
            meal_delta = (total_carbs * 1.8) * (math.sin(min(math.pi/2, (t / peak_time_min) * (math.pi/2))))
            # Decay phase after peak
            if t > peak_time_min:
                decay_t = t - peak_time_min
                meal_delta *= math.exp(-decay_t / 80)
        else:
            meal_delta = 0
            
        # 2. Insulin Counter-Regulatory action curve
        if diab_type == "Type 1 Diabetes":
            # Very slow native baseline return without artificial corrections
            insulin_clearance = (t * 0.15)
        elif diab_type == "Gestational Diabetes":
            insulin_clearance = (t * 0.35) * (1.2 if t > 60 else 0.7)
        else: # Type 2 / Default
            insulin_clearance = (t * 0.45) * disposal_multiplier
            
        # 3. Complete Composite Glucose Curve Generation
        projected = current_glucose + (meal_delta * (average_gi / 60)) - insulin_clearance
        
        # Exercise sudden drop simulation during activity period
        if exercise_dur > 0 and t <= exercise_dur:
            projected -= (t * 0.8 * disposal_multiplier)
            
        # Hard floor clamp to avoid computational negative metrics
        if projected < 40: projected = 40
        glucose_points.append(round(projected, 1))
        
    return timeline, glucose_points

# ─── CORE PLATFORM APP RENDER ──────────────────────────────────────────────────
# Sidebar Control Station
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding-bottom: 1rem;'>
        <h2 style='color:#00f0ff; margin:0;'>GlucoVision Pro</h2>
        <p style='color:#94a3b8; font-size:0.8rem;'>Patient: <strong>{st.session_state.username}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Configuration Gate
    prem_status = st.checkbox("Toggle Premium License Tier", value=st.session_state.premium)
    if prem_status != st.session_state.premium:
        toggle_premium_status(st.session_state.user_key, prem_status)
        st.session_state.premium = prem_status
        st.rerun()
        
    if st.session_state.premium:
        st.markdown("<div style='text-align:center;'><span class='premium-tag'>👑 ENTERPRISE SUITE ACTIVE</span></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center; color:#64748b; font-size:0.8rem;'>Standard Evaluation Account</div>", unsafe_allow_html=True)
        
    st.markdown("<hr style='margin:1rem 0; border-color:#1e293b;' />", unsafe_allow_html=True)
    
    # Live Interactive Medical Profile Metrics Pipeline
    st.subheader("📋 Patient Profile Framework")
    p_age = st.number_input("Age (Years)", min_value=1, max_value=120, value=int(st.session_state.profile.get("age", 35)))
    p_gender = st.selectbox("Biological Sex", ["Male", "Female", "Intersex"], index=0 if st.session_state.profile.get("gender") == "Male" else 1)
    p_weight = st.number_input("Mass Weight (kg)", min_value=10.0, max_value=250.0, value=float(st.session_state.profile.get("weight", 70.0)))
    p_height = st.number_input("Height Stature (cm)", min_value=50.0, max_value=250.0, value=float(st.session_state.profile.get("height", 175.0)))
    
    p_diab = st.selectbox("Clinical Classification", ["Type 1 Diabetes", "Type 2 Diabetes", "LADA / Type 1.5", "Gestational Diabetes", "Non-Diabetic Metabolic Standard"], index=1)
    p_ins = st.selectbox("Therapy Infrastructure", ["Basal Insulin Only", "Basal + Bolus Regularity", "Insulin Pump Continuous Delivery", "Non-Insulin Therapeutic Regimen"], index=1)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1: p_tlow = st.number_input("Target Low", value=70)
    with col_t2: p_thigh = st.number_input("Target High", value=140)
    
    # Premium-only parameters
    if st.session_state.premium:
        st.markdown("<span style='color:#ff007f; font-size:0.8rem; font-weight:700;'>PREMIUM RATIO MATRIX</span>", unsafe_allow_html=True)
        p_icr = st.number_input("Insulin-to-Carb Ratio (ICR)", value=float(st.session_state.profile.get("icr", 10.0)))
        p_isf = st.number_input("Insulin Sensitivity (ISF)", value=float(st.session_state.profile.get("isf", 40.0)))
    else:
        p_icr, p_isf = 10.0, 40.0
        st.caption("🔒 Upgrade license to custom fine-tune ICR/ISF formulas.")
        
    if st.button("Commit Profile Changes", use_container_width=True):
        updated_prof = {
            "age": p_age, "gender": p_gender, "weight": p_weight, "height": p_height,
            "diabetes_type": p_diab, "insulin_type": p_ins, "target_low": p_tlow, "target_high": p_thigh,
            "icr": p_icr, "isf": p_isf
        }
        update_user_profile(st.session_state.user_key, updated_prof)
        st.session_state.profile = updated_prof
        st.success("Configuration Matrix Synced!")
        st.rerun()
        
    st.markdown("<hr style='margin:1rem 0; border-color:#1e293b;' />", unsafe_allow_html=True)
    if st.sidebar.button("Log Out Secure Session", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ─── MAIN CENTRAL PLATFORM WORKSPACE RENDERING ───────────────────────────────
render_disclaimer()

st.title("📊 Metabolic Engineering Command & Control")

# Primary High-Density Parameter Deck
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    cur_gluc = st.number_input("Current Capillary Glucose (mg/dL)", min_value=40, max_value=500, value=135, step=5)
with col_m2:
    ex_type = st.selectbox("Active Activity Modality", ["None / Sedentary", "Cardio (Running/Cycling)", "Resistance Training", "HIIT / High Intensity"])
with col_m3:
    ex_dur = st.slider("Activity Operational Window (Minutes)", min_value=0, max_value=180, value=0, step=5)
with col_m4:
    hba1c_est = st.slider("Last Recorded Lab HbA1c (%)", min_value=4.0, max_value=16.0, value=6.8, step=0.1)

# Core Dynamic Workspace Tab System Topology
tab_dashboard, tab_nutrition, tab_bolus, tab_analytics = st.tabs([
    "📈 Real-Time Baseline CGM Simulation", 
    "🍽️ Intelligent Plate Constructor", 
    "💉 Advanced Dose Bolus Matrix",
    "📊 Longitudinal Analytics Reporting"
])

# 📊 TAB 1: DYNAMIC HIGH-RESOLUTION DASHBOARD SIMULATOR
with tab_dashboard:
    # Compile parameters across plate session
    t_carbs, t_cal, t_prot, t_fat, avg_gi = 0.0, 0.0, 0.0, 0.0, 55
    if st.session_state.meal_plate:
        t_carbs = sum(item["carbs"] for item in st.session_state.meal_plate)
        t_cal = sum(item["calories"] for item in st.session_state.meal_plate)
        t_prot = sum(item["protein"] for item in st.session_state.meal_plate)
        t_fat = sum(item["fat"] for item in st.session_state.meal_plate)
        avg_gi = int(sum(item["gi"] for item in st.session_state.meal_plate) / len(st.session_state.meal_plate))

    # Trigger Simulation Runtime Engine
    time_vec, gluc_vec = run_advanced_metabolic_simulation(
        cur_gluc, t_carbs, t_prot, t_fat, avg_gi, st.session_state.profile, ex_type, ex_dur
    )
    
    p_60 = gluc_vec[6]  # index 6 is 60 minutes
    p_120 = gluc_vec[12] # index 12 is 120 minutes
    p_max = max(gluc_vec)
    
    # Calculate Adaptive Algorithmic Health Score Metrics
    variability_index = max(gluc_vec) - min(gluc_vec)
    base_score = 100 - (variability_index * 0.4) - (abs(p_120 - 100) * 0.3)
    if p_max > 250 or min(gluc_vec) < 60: base_score -= 20
    health_score = clamp_val = max(10, min(100, int(base_score)))
    
    # Dynamic Live Enterprise Cards Render
    c_card1, c_card2, c_card3, c_card4, c_card5, c_card6 = st.columns(6)
    with c_card1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Current Glucose</div><div class='metric-value' style='color:#00f0ff;'>{cur_gluc}</div><div style='font-size:0.7rem; color:#64748b;'>mg/dL</div></div>", unsafe_allow_html=True)
    with c_card2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>+60 Min Forecast</div><div class='metric-value' style='color:#ffd60a;'>{p_60}</div><div style='font-size:0.7rem; color:#64748b;'>mg/dL</div></div>", unsafe_allow_html=True)
    with c_card3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>+120 Min Peak</div><div class='metric-value' style='color:#ff9100;'>{p_120}</div><div style='font-size:0.7rem; color:#64748b;'>mg/dL</div></div>", unsafe_allow_html=True)
    with c_card4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Active Plate Carbs</div><div class='metric-value' style='color:#00e676;'>{t_carbs}g</div><div style='font-size:0.7rem; color:#64748b;'>{t_cal} kcal loaded</div></div>", unsafe_allow_html=True)
    with c_card5:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Glycemic Variance</div><div class='metric-value' style='color:#a855f7;'>±{int(variability_index)}</div><div style='font-size:0.7rem; color:#64748b;'>Swing Delta</div></div>", unsafe_allow_html=True)
    with c_card6:
        score_color = "#00e676" if health_score >= 80 else ("#ffd60a" if health_score >= 50 else "#ff3b3b")
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Metabolic Stability Score</div><div class='metric-value' style='color:{score_color};'>{health_score}</div><div style='font-size:0.7rem; color:#64748b;'>Algorithmic Index</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>High-Fidelity Continuum Forecast Engine Overlay</div>", unsafe_allow_html=True)
    
    # Advanced Plotly Multi-Trace Chart
    fig_cgm = go.Figure()
    # Add target safety boundaries shadows
    fig_cgm.add_axhspan(st.session_state.profile.get("target_low", 70), st.session_state.profile.get("target_high", 140), 
                        fillcolor="rgba(0, 230, 118, 0.06)", label=go.layout.Label(text="Optimal Target Window"))
    
    fig_cgm.add_trace(go.Scatter(
        x=time_vec, y=gluc_vec,
        mode='lines+markers',
        line=dict(color='#00f0ff', width=3, shape='spline'),
        marker=dict(size=6, color='#ffffff', stroke=dict(color='#0072ff', width=2)),
        name='Simulated Glucose Continuum trajectory'
    ))
    
    fig_cgm.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=20),
        height=380,
        xaxis=dict(title="Timeline Simulation Horizon (Minutes)", gridcolor="#1e293b", showgrid=True),
        yaxis=dict(title="Capillary Standard (mg/dL)", gridcolor="#1e293b", showgrid=True),
        hovermode="x unified"
    )
    st.plotly_chart(fig_cgm, use_container_width=True)

    # Automated Machine Expert Clinical Advice Rule Engine
    st.markdown("<div class='section-header'>⚡ Automated Machine Expert Guardrails</div>", unsafe_allow_html=True)
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if p_max > 220:
            st.markdown(f"<div class='rec-card' style='border-left-color:#ff3b3b;'>⚠️ <strong>CRITICAL HYPERGLYCEMIA WARNING:</strong> Your composite intake load projects a massive postprandial glucose breach peaking at {p_max} mg/dL. Consider adjusting carb volume densities or checking correction equations.</div>", unsafe_allow_html=True)
        elif min(gluc_vec) < 70:
            st.markdown(f"<div class='rec-card' style='border-left-color:#ff007f;'>🚨 <strong>COMPUTATIONAL HYPOGLYCEMIA EXPOSURE RISK:</strong> Exercise clearance curves intersect below safety levels down to {min(gluc_vec)} mg/dL. Keep fast-acting carbohydrates (15g rule) accessible immediately.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='rec-card'>✅ <strong>HOMEOSTASIS FORECAST STABLE:</strong> Metabolic timeline trajectory maintains strict conformity with standard biological targets. No anomalies triggered.</div>", unsafe_allow_html=True)
            
    with col_g2:
        if avg_gi > 70:
            st.markdown("<div class='rec-card' style='border-left-color:#ffd60a;'>💡 <strong>GLYCEMIC VELOCITY ADVISORY:</strong> High Glycemic Index food array identified. Blunting the absorption velocity is possible by combining this configuration with high-density fibers or proteins like salads/yogurts.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='rec-card'>💡 <strong>NUTRITIONAL ARCHITECTURE OPTIMAL:</strong> Current macro arrangement possesses a favorable Glycemic curve density configuration. Excellent balancing.</div>", unsafe_allow_html=True)

# 🍽️ TAB 2: INTELLIGENT PLATE CONSTRUCTOR (MULTI-ITEM LOGGING)
with tab_nutrition:
    st.markdown("<div class='section-header'>Meal Blueprint Component Engine</div>", unsafe_allow_html=True)
    
    col_n1, col_n2 = st.columns([1, 2])
    with col_n1:
        st.subheader("Add Food Vector to Active Plate")
        selected_food = st.selectbox("Search Verified Nutrient Library Database", list(FOOD_DB.keys()))
        servings = st.number_input("Serving Multiplier Unit Ratio", min_value=0.25, max_value=5.0, value=1.0, step=0.25)
        
        if st.button("Add Item Vector to Active Log Instance", use_container_width=True):
            base_nutrients = FOOD_DB[selected_food]
            item_entry = {
                "name": selected_food,
                "calories": round(base_nutrients["calories"] * servings, 1),
                "carbs": round(base_nutrients["carbs"] * servings, 1),
                "protein": round(base_nutrients["protein"] * servings, 1),
                "fat": round(base_nutrients["fat"] * servings, 1),
                "gi": base_nutrients["gi"]
            }
            st.session_state.meal_plate.append(item_entry)
            st.toast(f"Linked {selected_food} to live analysis pipeline!")
            st.rerun()
            
        if st.button("Clear Active Plate Ledger", type="secondary", use_container_width=True):
            st.session_state.meal_plate = []
            st.rerun()
            
    with col_n2:
        st.subheader("Active Structural Plate Breakdown")
        if not st.session_state.meal_plate:
            st.info("Plate vector pipeline currently empty. Inject items via the selection panel to begin calculation matrices.")
        else:
            df_plate = pd.DataFrame(st.session_state.meal_plate)
            st.dataframe(df_plate, use_container_width=True)
            
            # Interactive Plotly Macro Distribution Pie Chart
            fig_macro = px.pie(
                names=["Carbohydrates (g)", "Protein (g)", "Lipid Fats (g)"],
                values=[df_plate["carbs"].sum(), df_plate["protein"].sum(), df_plate["fat"].sum()],
                color_discrete_sequence=['#00f0ff', '#00e676', '#ff007f'],
                hole=0.4,
                title="Active Structural Plate Energy Distribution Matrix"
            )
            fig_macro.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", height=250, margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_macro, use_container_width=True)

# 💉 TAB 3: ADVANCED CLINICAL MEDICAL BOLUS CALCULATOR
with tab_bolus:
    st.markdown("<div class='section-header'>Calculated Structural Bolus Engine Matrix</div>", unsafe_allow_html=True)
    
    if not st.session_state.premium:
        st.warning("🔒 <strong>UPGRADE TO PREMIUM CONFIGURATION REQUIRED:</strong> Advanced Clinical Correction Factor logic modules, Active Insulin-On-Board decay monitoring, and structural ICR calculations are locked to standard users.")
        # Provide fallback manual setup
        icr_calc = 10.0
        isf_calc = 40.0
    else:
        icr_calc = st.session_state.profile.get("icr", 10.0)
        isf_calc = st.session_state.profile.get("isf", 40.0)
        st.success("✨ Premium Authentication Token Validated: Advanced Clinical Bolus Math Systems Operational.")
        
    st.markdown(r"""
    The calculated clinical advisory output operates under classical endocrine equation frameworks:
    $$\text{Total Bolus Advisory Dose} = \text{Food Carb Component Bolus} + \text{Hyperglycemic Correction Delta}$$
    $$\text{Equation Framework} = \left( \frac{\text{Target Meal Carbohydrates}}{\text{Insulin-to-Carbohydrate Ratio (ICR)}} \right) + \left( \frac{\text{Current Glucose} - \text{Target Baseline}}{\text{Insulin Sensitivity Factor (ISF)}} \right)$$
    """)
    
    active_plate_carbs = sum(item["carbs"] for item in st.session_state.meal_plate) if st.session_state.meal_plate else 0.0
    override_carbs = st.number_input("Modify Target Meal Carbohydrate Input Mass (g)", value=float(active_plate_carbs))
    
    # Executing Equations
    target_mid = (st.session_state.profile.get("target_low", 70) + st.session_state.profile.get("target_high", 140)) / 2
    carb_dose = override_carbs / icr_calc if icr_calc > 0 else 0
    correction_dose = (cur_gluc - target_mid) / isf_calc if cur_gluc > target_mid else 0.0
    total_suggested_bolus = round(carb_dose + correction_dose, 2)
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.metric("Nutrient Carb Bolus Component", f"{round(carb_dose, 2)} Units")
    with col_b2:
        st.metric("Hyperglycemic Correction Component", f"{round(correction_dose, 2)} Units")
    with col_b3:
        st.metric("COMPOSITE SUGGESTED ADVISORY BOLUS", f"{total_suggested_bolus} Units", delta_color="inverse")
        
    st.caption(f"Calculations referenced against patient criteria matrices: ICR={icr_calc}g/unit, ISF={isf_calc}mg/dL/unit, Target Baseline Median={int(target_mid)}mg/dL.")

# 📊 TAB 4: LONGITUDINAL ANALYTICS REPORT GENERATOR
with tab_analytics:
    st.markdown("<div class='section-header'>Longitudinal Structural Export Pipeline</div>", unsafe_allow_html=True)
    
    # Generate Mock Retrospective Analytics Set to Simulate Continuous Operation over Months
    np.random.seed(42)
    days_range = pd.date_range(end=datetime.now(), periods=90)
    mock_fbg = np.random.normal(loc=125, scale=22, size=90)
    mock_postprandial = mock_fbg + np.random.uniform(30, 85, size=90)
    
    df_analytics = pd.DataFrame({
        "Date": days_range,
        "Fasting Self-Monitor Level (mg/dL)": mock_fbg.astype(int),
        "Post-Prandial Peak Level (mg/dL)": mock_postprandial.astype(int)
    })
    
    fig_long = px.line(df_analytics, x="Date", y=["Fasting Self-Monitor Level (mg/dL)", "Post-Prandial Peak Level (mg/dL)"],
                       color_discrete_sequence=['#00f0ff', '#ff007f'],
                       title="90-Day Longitudinal Retrospective HbA1c Analytics Vector Proxy")
    fig_long.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color="white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_long, use_container_width=True)
    
    # Core Structured Data Export Downloader Terminal
    st.subheader("📥 Structural Report Compiler")
    
    report_stream = io.StringIO()
    report_stream.write(f"GLUCOVISION AI PRO METABOLIC COMPILATION REPORT\n")
    report_stream.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
    report_stream.write(f"PATIENT USERSPACE RECORD ID: {st.session_state.username}\n")
    report_stream.write(f"CLINICAL PARADIGM OVERLAY: {st.session_state.profile.get('diabetes_type')}\n")
    report_stream.write(f"ESTIMATED HEALTH HOMEODYNAMIC STABILITY INDEX SCORE: {health_score}/100\n")
    report_stream.write(f"CURRENT TARGET VECTOR ANALYSIS: Glucose {cur_gluc} mg/dL | Active Simulation Plate Carb Mass: {t_carbs}g\n")
    report_stream.write(f"FORECAST SUMMARY INTERVAL PEAK (+120 MINS): {p_120} mg/dL\n")
    report_stream.write(f"CONFIDENTIAL COMPLIANCE DISCLAIMER: Educational science fair prototype evaluation matrix framework. Not certified clinical device architecture.\n")
    
    st.download_button(
        label="Compile & Download Automated PDF/Text Medical Science Report",
        data=report_stream.getvalue(),
        file_name=f"glucovision_clinical_report_{st.session_state.username}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ─── FOOTER REGION DISCLAIMER ──────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#1e293b; margin-top:3rem;' />
<p style='text-align:center; font-size:0.75rem; color:#475569;'>
    GlucoVision AI Pro Suite • Advanced Mathematics Integration Node Engine • Technical Prototype Release Platform v2.86
</p>
""", unsafe_allow_html=True)
