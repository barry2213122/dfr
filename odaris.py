"""
GLUCOVISION AI - Freemium SaaS Edition
AI-Powered Personalized Diabetes Monitoring & Glucose Prediction System
Educational Prototype Only - Not a Medical Device
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
import sqlite3
import hashlib

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GlucoVision AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DATABASE SETUP ───────────────────────────────────────────────────────────
DB_FILE = 'glucovision_users.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT,
            account_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash, account_type) VALUES (?, ?, ?)",
                  (username, hash_password(password), 'FREE'))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success

def verify_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password_hash, account_type FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True, row[1]
    return False, None

def upgrade_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET account_type = 'PREMIUM' WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    st.session_state.account_type = 'PREMIUM'

# Initialize DB on load
init_db()

# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'account_type' not in st.session_state:
    st.session_state.account_type = None

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #ffffff;
}

/* Background - simple dark navy, no fancy gradient */
.stApp {
    background-color: #0d1117;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 2px solid #00d9ff;
}
section[data-testid="stSidebar"] .block-container { padding: 1rem; }

/* All labels and text - bright white, bold */
label, .stTextInput label, .stNumberInput label,
.stSelectbox label, .stSlider label, .stMultiSelect label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

p, .stMarkdown p {
    color: #e6edf3 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Metric cards - solid borders, bright values */
.metric-card {
    background-color: #161b22;
    border: 2px solid #00d9ff;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: #00d9ff;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #c9d1d9;
    margin-top: 0.3rem;
}
.metric-icon { font-size: 1.3rem; margin-bottom: 0.25rem; }

/* Section headers - each section gets its own bright color, not one matching brand color */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 3px solid #00d9ff;
}
.section-icon {
    width: 36px; height: 36px;
    background-color: #00d9ff;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.02em;
}
/* Color variants */
.sh-blue   { border-bottom-color: #1e90ff; }
.sh-blue   .section-icon { background-color: #1e90ff; }
.sh-green  { border-bottom-color: #00e676; }
.sh-green  .section-icon { background-color: #00e676; }
.sh-orange { border-bottom-color: #ff9100; }
.sh-orange .section-icon { background-color: #ff9100; }
.sh-pink   { border-bottom-color: #ff2d95; }
.sh-pink   .section-icon { background-color: #ff2d95; }
.sh-purple { border-bottom-color: #a855f7; }
.sh-purple .section-icon { background-color: #a855f7; }
.sh-yellow { border-bottom-color: #ffd60a; }
.sh-yellow .section-icon { background-color: #ffd60a; }
.sh-red    { border-bottom-color: #ff3b3b; }
.sh-red    .section-icon { background-color: #ff3b3b; }
.sh-teal   { border-bottom-color: #00ffc8; }
.sh-teal   .section-icon { background-color: #00ffc8; }

/* Hero header */
.hero-header {
    text-align: center;
    padding: 1.8rem 1rem;
    background-color: #161b22;
    border-radius: 12px;
    border: 3px solid #00e676;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 2.7rem;
    font-weight: 800;
    color: #00d9ff;
    margin: 0;
    letter-spacing: -0.01em;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #c9d1d9;
    margin: 0.5rem 0 0;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Disclaimer */
.disclaimer {
    background-color: #3d0a0a;
    border: 3px solid #ff3b3b;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
    font-weight: 700;
    color: #ff8080;
}

/* Premium Lock Box */
.premium-lock {
    background-color: #1a1500;
    border: 2px dashed #ffd60a;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.premium-lock h3 {
    color: #ffd60a;
    margin-top: 0;
}

/* Risk badges */
.risk-low   { color: #00e676; background: #0a2e1a; border: 2px solid #00e676; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }
.risk-medium{ color: #ffd60a; background: #332700; border: 2px solid #ffd60a; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }
.risk-high  { color: #ff3b3b; background: #3d0a0a; border: 2px solid #ff3b3b; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }

/* Streamlit widget overrides */
.stSelectbox > div > div {
    background-color: #161b22 !important;
    border: 2px solid #30363d !important;
    color: #ffffff !important;
}
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background-color: #161b22 !important;
    border: 2px solid #30363d !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
div[data-testid="metric-container"] {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-radius: 8px;
    padding: 0.5rem 1rem;
}
div[data-testid="metric-container"] label {
    color: #c9d1d9 !important;
    font-weight: 700 !important;
}
div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #00d9ff !important;
    font-weight: 800 !important;
}
.stButton > button {
    background-color: #00e676 !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover {
    background-color: #5cffb0 !important;
}
hr { border-color: #30363d !important; border-width: 1px !important; }

/* Sidebar logo */
.sidebar-logo {
    text-align: center;
    padding: 1rem 0 1.5rem;
    border-bottom: 2px solid #00d9ff;
    margin-bottom: 1.5rem;
}
.sidebar-logo-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #00d9ff;
}
.sidebar-logo-sub {
    font-size: 0.7rem;
    color: #8b949e;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Nav pills */
.nav-pill {
    display: block;
    padding: 0.5rem 1rem;
    margin: 0.2rem 0;
    border-radius: 6px;
    color: #c9d1d9;
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
}
.nav-pill:hover { background-color: #21262d; color: #ffffff; }

/* Recommendation cards */
.rec-card {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-left: 5px solid #00d9ff;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.8rem;
    font-size: 0.9rem;
    font-weight: 700;
    color: #e6edf3;
}
.rec-card.rc-0 { border-left-color: #00d9ff; }
.rec-card.rc-1 { border-left-color: #00e676; }
.rec-card.rc-2 { border-left-color: #ffd60a; }
.rec-card.rc-3 { border-left-color: #ff9100; }
.rec-card.rc-4 { border-left-color: #ff2d95; }
.rec-card.rc-5 { border-left-color: #a855f7; }
.rec-card.rc-6 { border-left-color: #1e90ff; }

/* Insight box */
.insight-box {
    background-color: #161b22;
    border: 2px solid #00d9ff;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.insight-value {
    font-size: 2rem;
    font-weight: 800;
    color: #00d9ff;
}

/* Glass card (used in export section) */
.glass-card {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.glass-card strong { color: #00d9ff; }
</style>
""", unsafe_allow_html=True)

# ─── FOOD DATABASE & CONSTANTS ────────────────────────────────────────────────
FOOD_DB = {
    "Cooked Rice (white) (100 g)": {"calories": 130.0, "carbs": 28.0, "protein": 2.7, "fat": 0.3},
    "Wheat Roti / Chapati (1 medium (40 g))": {"calories": 104.0, "carbs": 20.0, "protein": 3.0, "fat": 1.7},
    "Paneer (100 g)": {"calories": 265.0, "carbs": 1.2, "protein": 18.3, "fat": 20.8},
    "Curd / Yogurt (Dahi) (100 g)": {"calories": 60.0, "carbs": 4.7, "protein": 3.5, "fat": 3.3},
    "Apple (1 medium (150 g))": {"calories": 78.0, "carbs": 21.0, "protein": 0.4, "fat": 0.3},
    "Banana (1 medium (120 g))": {"calories": 105.0, "carbs": 27.0, "protein": 1.3, "fat": 0.4},
    "Chicken (cooked, breast) (100 g)": {"calories": 165.0, "carbs": 0.0, "protein": 31.0, "fat": 3.6},
    "Egg (whole, boiled) (1 large (50 g))": {"calories": 78.0, "carbs": 0.6, "protein": 6.3, "fat": 5.3},
    "Oats (cooked with milk) (1 bowl (200 g))": {"calories": 180.0, "carbs": 28.0, "protein": 7.0, "fat": 4.0},
    "Milk (whole/full cream) (1 glass (200 ml))": {"calories": 134.0, "carbs": 9.6, "protein": 6.4, "fat": 8.0},
}
INSULIN_TYPES = [
    "No Insulin",
    "Rapid-Acting (e.g., Lispro, Aspart)",
    "Short-Acting (Regular)",
    "Intermediate-Acting (NPH)",
    "Long-Acting (Glargine, Detemir)",
    "Mixed Insulin (70/30)",
]

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────
def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    if height_cm <= 0 or weight_kg <= 0: return 0.0, "N/A"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:   cat = "Underweight"
    elif bmi < 25:   cat = "Normal"
    elif bmi < 30:   cat = "Overweight"
    else:            cat = "Obese"
    return round(bmi, 1), cat

def _smoothstep(edge0: float, edge1: float, x: float) -> float:
    if edge0 == edge1: return 0.0 if x < edge0 else 1.0
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

INSULIN_ACTION_PROFILE = {
    "No Insulin":                           {"onset": 0,   "peak": 0,   "end": 1},
    "Rapid-Acting (e.g., Lispro, Aspart)":  {"onset": 15,  "peak": 75,  "end": 240},
    "Short-Acting (Regular)":               {"onset": 45,  "peak": 150, "end": 420},
    "Intermediate-Acting (NPH)":            {"onset": 150, "peak": 480, "end": 900},
    "Long-Acting (Glargine, Detemir)":      {"onset": 90,  "peak": 360, "end": 1380},
    "Mixed Insulin (70/30)":                {"onset": 30,  "peak": 180, "end": 720},
}

CARB_RESPONSE_PROFILE = {
    "No Diabetes":      {"peak": 45,  "decay": 90},
    "Prediabetes":      {"peak": 50,  "decay": 115},
    "Type 2 Diabetes":  {"peak": 60,  "decay": 130},
    "Type 1 Diabetes":  {"peak": 60,  "decay": 165},
}

def _cumulative_insulin_fraction(minutes, onset, peak, end):
    if minutes <= onset: return 0.0
    if minutes <= peak:  return 0.5 * _smoothstep(onset, peak, minutes)
    if minutes <= end:   return 0.5 + 0.5 * _smoothstep(peak, end, minutes)
    return 1.0

def _carb_excursion_fraction(minutes, peak, decay):
    if minutes <= peak: return _smoothstep(0, peak, minutes)
    return 1.0 - _smoothstep(peak, peak + decay, minutes)

def _estimate_bmr(weight_kg, age=35, gender="Male"):
    weight_kg = max(weight_kg, 30.0)
    if gender == "Female": bmr = 10 * weight_kg + 6.25 * 170 - 5 * age - 161
    else:                  bmr = 10 * weight_kg + 6.25 * 170 - 5 * age + 5
    return max(1200.0, bmr)

def glucose_prediction_model(
    current_glucose, carbs_g, diabetes_type, insulin_type, insulin_dose,
    time_since_injection_hr=0.0, weight_kg=70.0, age=35, gender="Male",
    calories_kcal=0.0, time_since_meal_hr=0.0, exercise_type="No Exercise",
    exercise_duration_min=0.0
):
    weight_kg = weight_kg if weight_kg and weight_kg > 0 else 70.0
    carb_factor = {"No Diabetes": 1.1, "Prediabetes": 1.6, "Type 2 Diabetes": 2.2, "Type 1 Diabetes": 3.0}.get(diabetes_type, 1.6)
    carb_peak_rise = carbs_g * carb_factor
    carb_profile = CARB_RESPONSE_PROFILE.get(diabetes_type, CARB_RESPONSE_PROFILE["Prediabetes"])
    meal_elapsed_min = time_since_meal_hr * 60.0

    def _carb_delta_at(future_min):
        at_future = _carb_excursion_fraction(meal_elapsed_min + future_min, carb_profile["peak"], carb_profile["decay"])
        at_now = _carb_excursion_fraction(meal_elapsed_min, carb_profile["peak"], carb_profile["decay"])
        return carb_peak_rise * (at_future - at_now)

    bmr_kcal_day = _estimate_bmr(weight_kg, age, gender)
    glucose_distribution_dl = max(60.0, weight_kg * 2.0)
    HEPATIC_COMP = 0.03

    def _bmr_drop(minutes):
        kcal = bmr_kcal_day * (minutes / 1440)
        grams = (kcal / 4.0) * HEPATIC_COMP
        return (grams * 1000) / glucose_distribution_dl

    exercise_rate = {"No Exercise": 0.0, "Light (walking, yoga)": 0.30, "Moderate (jogging, cycling)": 0.70, "Intense (running, gym, sports)": 1.20}.get(exercise_type, 0.0)

    def _exercise_drop(future_min):
        if exercise_duration_min <= 0 or exercise_type == "No Exercise": return 0.0
        hours_post = 1.0 + (future_min / 60.0)
        duration_factor = min(exercise_duration_min, 90.0) / 30.0
        afterburn = exercise_rate * 0.30 * duration_factor * (0.5 ** (hours_post / 1.5))
        return afterburn * future_min

    insulin_factor_map = {"No Insulin": 0, "Rapid-Acting (e.g., Lispro, Aspart)": 45, "Short-Acting (Regular)": 35, "Intermediate-Acting (NPH)": 25, "Long-Acting (Glargine, Detemir)": 20, "Mixed Insulin (70/30)": 30}
    weight_adj = max(0.6, min(1.6, 70.0 / weight_kg))
    factor_per_unit = insulin_factor_map.get(insulin_type, 0) * weight_adj
    total_insulin_effect = factor_per_unit * (insulin_dose or 0)
    ins_profile = INSULIN_ACTION_PROFILE.get(insulin_type, INSULIN_ACTION_PROFILE["No Insulin"])
    elapsed_min = max(0.0, time_since_injection_hr) * 60.0

    predictions = {}
    for t in (30, 60, 90, 120):
        carb_delta = _carb_delta_at(t)
        already_delivered = _cumulative_insulin_fraction(elapsed_min, ins_profile["onset"], ins_profile["peak"], ins_profile["end"])
        delivered_by_t = _cumulative_insulin_fraction(elapsed_min + t, ins_profile["onset"], ins_profile["peak"], ins_profile["end"])
        insulin_delta = total_insulin_effect * max(0.0, delivered_by_t - already_delivered)
        bmr_delta = _bmr_drop(t)
        exercise_delta = _exercise_drop(t)
        predicted = current_glucose + carb_delta - insulin_delta - bmr_delta - exercise_delta
        fasting_floor = current_glucose * 0.88 if insulin_delta > 5 else current_glucose * 0.95
        predicted = max(fasting_floor, predicted)
        predictions[t] = round(min(600.0, predicted), 1)

    return predictions

def health_score(glucose, bmi, diabetes_type, predicted_peak, carbs):
    score = 100.0
    if glucose < 70 or glucose > 180: score -= 25
    elif glucose < 80 or glucose > 140: score -= 12
    elif glucose < 90 or glucose > 120: score -= 5

    if predicted_peak > 200: score -= 20
    elif predicted_peak > 160: score -= 10

    if bmi < 16 or bmi >= 35: score -= 20
    elif bmi < 18.5 or bmi >= 30: score -= 10
    elif bmi < 17 or bmi >= 27: score -= 4

    dm_penalty = {"No Diabetes": 0, "Prediabetes": 8, "Type 2 Diabetes": 15, "Type 1 Diabetes": 18}
    score -= dm_penalty.get(diabetes_type, 0)

    if carbs > 80: score -= 10
    elif carbs > 50: score -= 5

    score = max(0, min(100, score))
    if score >= 75: risk = "Low Risk"
    elif score >= 50: risk = "Medium Risk"
    else: risk = "High Risk"
    return round(score, 1), risk

def get_recommendations(diabetes_type, glucose, predicted_peak, bmi, bmi_cat, carbs):
    recs = []
    if glucose < 70: recs.append("⚠️ Current glucose appears low. Consume fast-acting carbs.")
    elif glucose > 180: recs.append("🔴 Current glucose is elevated. Ensure hydration and consult provider.")
    elif 80 <= glucose <= 120: recs.append("✅ Glucose is within healthy range.")

    if predicted_peak > 200: recs.append("📈 Glucose predicted to rise significantly. A 15-20 min walk helps.")
    elif predicted_peak > 160: recs.append("📊 Moderate glucose rise predicted. Monitor closely.")

    if diabetes_type == "Type 1 Diabetes": recs.append("💉 Consistent carb-counting is essential.")
    elif diabetes_type == "Type 2 Diabetes": recs.append("🥗 Reducing refined carbs improves control.")
    elif diabetes_type == "Prediabetes": recs.append("🌿 Reversible with lifestyle changes.")
    else: recs.append("✅ No diabetes detected. Maintain active lifestyle.")

    if bmi_cat == "Obese": recs.append("⚖️ 5–10% weight reduction improves sensitivity.")
    elif bmi_cat == "Overweight": recs.append("⚖️ Regular cardio (30 min/day) improves health.")

    if carbs > 80: recs.append("🍽️ High carb intake. Split meals and pair with protein.")
    recs.append("💧 Hydration (8-10 glasses) supports kidney function.")
    return recs[:7]

def generate_pdf_report(patient, nutrition, glucose_now, predictions, score, risk, recommendations, bmi, bmi_cat):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=26, textColor=colors.HexColor('#00d9ff'), alignment=TA_CENTER)
    elements.append(Paragraph("🩺 GLUCOVISION AI PREMIUM REPORT", title_style))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"Patient: {patient.get('name', 'N/A')} | Score: {score} | Risk: {risk}"))
    doc.build(elements)
    buf.seek(0)
    return buf.read()

# ─── PLOTLY CHART HELPERS ─────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(10,14,26,0)', plot_bgcolor='rgba(10,14,26,0)',
    font=dict(family='Inter', color='#94a3b8', size=11), margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor='rgba(0,217,255,0.15)', linecolor='rgba(0,217,255,0.25)', zerolinecolor='rgba(0,0,0,0)'),
    yaxis=dict(gridcolor='rgba(0,217,255,0.15)', linecolor='rgba(0,217,255,0.25)', zerolinecolor='rgba(0,0,0,0)'),
)

def glucose_trend_chart(glucose_now, predictions):
    times = [0, 30, 60, 90, 120]
    values = [glucose_now] + [predictions[t] for t in [30, 60, 90, 120]]
    labels = ['Now', '30m', '60m', '90m', '2hr']
    fig = go.Figure()
    fig.add_hrect(y0=70, y1=140, fillcolor='rgba(0,230,118,0.12)', line_color='rgba(0,230,118,0.25)', annotation_text='Normal')
    fig.add_trace(go.Scatter(x=labels, y=values, mode='lines+markers', line=dict(color='#00d9ff', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(0,217,255,0.12)', name='Glucose'))
    fig.update_layout(**CHART_LAYOUT, title=dict(text='Glucose Trend Forecast', font=dict(size=14, color='#e2e8f0'), x=0.5))
    return fig

def nutrition_pie_chart(carbs, protein, fat):
    if carbs + protein + fat == 0: carbs, protein, fat = 1, 1, 1
    fig = go.Figure(go.Pie(labels=['Carbohydrates', 'Protein', 'Fat'], values=[carbs, protein, fat], hole=0.55, marker=dict(colors=['#1e90ff', '#00d9ff', '#a855f7'])))
    fig.update_layout(**CHART_LAYOUT, title=dict(text='Macronutrient Breakdown', font=dict(size=14, color='#e2e8f0'), x=0.5))
    return fig

def risk_gauge(score, risk):
    color = '#00e676' if risk == 'Low Risk' else ('#ffd60a' if risk == 'Medium Risk' else '#ff3b3b')
    fig = go.Figure(go.Indicator(
        mode='gauge+number', value=score,
        number={'font': {'size': 36, 'color': color}},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color, 'thickness': 0.25}, 'bgcolor': 'rgba(15,23,42,0.5)'},
        title={'text': 'Health Score', 'font': {'color': '#94a3b8', 'size': 13}}
    ))
    fig.update_layout(**CHART_LAYOUT, height=260)
    return fig

def calorie_summary_chart(food_log):
    if not food_log: return go.Figure().update_layout(**CHART_LAYOUT, title=dict(text='No foods selected', x=0.5))
    labels = [f['name'][:20] for f in food_log]
    cals = [f['calories'] for f in food_log]
    fig = go.Figure(go.Bar(x=cals, y=labels, orientation='h', marker=dict(color=cals, colorscale='Viridis')))
    fig.update_layout(**CHART_LAYOUT, title=dict(text='Calorie Breakdown', font=dict(size=14, color='#e2e8f0'), x=0.5))
    return fig

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div style="font-size:2.2rem; margin-bottom:0.3rem">🩺</div>
            <div class="sidebar-logo-title">GlucoVision AI</div>
            <div class="sidebar-logo-sub">Glucose Prediction System</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**Welcome, {st.session_state.username}**")
        if st.session_state.account_type == "PREMIUM":
            st.markdown("<span style='color:#ffd60a; font-weight:bold'>👑 PREMIUM PLAN</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#a855f7; font-weight:bold'>🔹 FREE PLAN</span>", unsafe_allow_html=True)
            if st.button("🚀 Upgrade to Premium"):
                upgrade_user(st.session_state.username)
                st.success("Upgraded to Premium successfully!")
                st.rerun()

        st.markdown("### 📋 Navigation")
        sections = [
            ("👤", "Patient Profile"),
            ("💉", "Insulin Management"),
            ("🍽️", "Food Intelligence"),
            ("🔬", "Digital Twin"),
            ("📈", "AI Predictions"),
            ("📊", "Visualizations"),
            ("🧠", "Health Analytics"),
            ("💡", "Recommendations 🔒"),
            ("🔮", "Future Insights 🔒"),
            ("🧠", "MBTI & Diet 🔒"),
            ("📄", "Export Report 🔒"),
        ]
        
        for icon, name in sections:
            if "🔒" in name and st.session_state.account_type == "PREMIUM":
                name = name.replace("🔒", "👑")
            st.markdown(f'<div class="nav-pill">{icon} &nbsp;{name}</div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.account_type = None
            st.rerun()

def premium_gate(feature_name):
    if st.session_state.account_type == "PREMIUM":
        return True
    else:
        st.markdown(f"""
        <div class="premium-lock">
            <h3>🔒 {feature_name} is a Premium Feature</h3>
            <p>Upgrade to GlucoVision Premium to unlock personalized AI insights, advanced forecasting, and export capabilities.</p>
        </div>
        """, unsafe_allow_html=True)
        return False

# ─── MAIN APP ─────────────────────────────────────────────────────────────────
def glucovision_app():
    render_sidebar()

    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🩺 GlucoVision AI</div>
        <div class="hero-subtitle">AI-Powered Personalized Diabetes Monitoring & Glucose Prediction System</div>
    </div>
    """, unsafe_allow_html=True)

    # ══ SECTION 1: PROFILE ══
    st.markdown('<div class="section-header sh-blue"><div class="section-icon">👤</div><div class="section-title">SECTION 1 — Patient Profile</div></div>', unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            name   = st.text_input("Full Name", value=st.session_state.username)
            age    = st.number_input("Age (years)", min_value=0, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Select Gender", "Male", "Female", "Other"])
        with col2:
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=250.0, value=70.0, step=0.5)
            height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, value=170.0, step=0.5)
        with col3:
            diabetes_type = st.selectbox("Diabetes Status", ["Select Status", "No Diabetes", "Prediabetes", "Type 1 Diabetes", "Type 2 Diabetes"])

        bmi, bmi_cat = calculate_bmi(weight, height)
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("⚖️ BMI", f"{bmi}")
        col_b.metric("🏷️ BMI Category", bmi_cat)
        col_c.metric("🧬 Diabetes Status", diabetes_type.split()[0] if diabetes_type else "N/A")
    st.markdown("---")

    # ══ SECTION 2: INSULIN ══
    st.markdown('<div class="section-header sh-red"><div class="section-icon">💉</div><div class="section-title">SECTION 2 — Insulin Management</div></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if diabetes_type == "No Diabetes":
            insulin_type = "No Insulin"
            st.info("💡 No insulin required.")
        else:
            insulin_type = st.selectbox("Insulin Type", INSULIN_TYPES)
    with col2:
        insulin_dose = 0.0 if (insulin_type == "No Insulin" or diabetes_type == "No Diabetes") else st.number_input("Insulin Dose (units)", 0.0, 100.0, 0.0)
    with col3:
        time_since_injection = 0.0 if (insulin_type == "No Insulin" or diabetes_type == "No Diabetes") else st.number_input("Hours Since Injection", 0.0, 24.0, 0.0)
    st.markdown("---")

    # ══ SECTION 3: FOOD ══
    st.markdown('<div class="section-header sh-orange"><div class="section-icon">🍽️</div><div class="section-title">SECTION 3 — Food Intelligence System</div></div>', unsafe_allow_html=True)
    selected_foods = st.multiselect("Select Foods Consumed", options=list(FOOD_DB.keys()), default=[])
    food_log, total_cal, total_carbs, total_protein, total_fat = [], 0.0, 0.0, 0.0, 0.0
    if selected_foods:
        cols = st.columns(min(len(selected_foods), 3))
        for i, food_name in enumerate(selected_foods):
            with cols[i % 3]:
                qty = st.number_input(f"× {food_name.split('(')[0].strip()}", 0.5, 10.0, 1.0, key=f"qty_{i}")
                fd = FOOD_DB[food_name]
                food_log.append({'name': food_name, 'calories': fd['calories']*qty})
                total_cal += fd['calories']*qty; total_carbs += fd['carbs']*qty; total_protein += fd['protein']*qty; total_fat += fd['fat']*qty
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🔥 Calories", f"{total_cal:.0f} kcal")
        c2.metric("🍞 Carbohydrates", f"{total_carbs:.1f} g")
        c3.metric("💪 Protein", f"{total_protein:.1f} g")
        c4.metric("🥑 Fat", f"{total_fat:.1f} g")
    st.markdown("---")

    # ══ SECTION 4: TWIN ══
    st.markdown('<div class="section-header sh-teal"><div class="section-icon">🔬</div><div class="section-title">SECTION 4 — Metabolic Digital Twin</div></div>', unsafe_allow_html=True)
    current_glucose = st.slider("🩸 Current Blood Glucose Level (mg/dL)", 40, 400, 100, 1)
    
    predictions = glucose_prediction_model(current_glucose, total_carbs, diabetes_type, insulin_type, insulin_dose, weight_kg=weight, age=int(age), gender=gender, calories_kcal=total_cal)
    predicted_60 = predictions[60]
    hs, risk = health_score(current_glucose, bmi, diabetes_type, max(predictions.values()), total_carbs)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    for col, icon, value, label in [(c1, '🩸', f'{current_glucose}', 'Current Glucose'), (c2, '📈', f'{predicted_60}', 'Pred (60m)'), (c3, '🔥', f'{total_cal:.0f}', 'Kcal'), (c4, '🍞', f'{total_carbs:.0f}','Carbs (g)'), (c5, '⚖️', f'{bmi}', 'BMI'), (c6, '💯', f'{hs}', 'Score')]:
        col.markdown(f'<div class="metric-card"><div class="metric-icon">{icon}</div><div class="metric-value">{value}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)
    st.markdown("---")

    # ══ SECTION 5 & 6 & 7: FREE CHARTS ══
    st.markdown('<div class="section-header sh-green"><div class="section-icon">📈</div><div class="section-title">SECTION 5/6/7 — AI Charts & Analytics</div></div>', unsafe_allow_html=True)
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1: st.plotly_chart(glucose_trend_chart(current_glucose, predictions), use_container_width=True)
    with col_chart2: st.plotly_chart(risk_gauge(hs, risk), use_container_width=True)
    st.markdown("---")

    # ══ PREMIUM GATED SECTIONS ══
    # SECTION 8
    st.markdown('<div class="section-header sh-yellow"><div class="section-icon">💡</div><div class="section-title">SECTION 8 — AI Health Recommendations</div></div>', unsafe_allow_html=True)
    if premium_gate("Advanced AI Health Recommendations"):
        recs = get_recommendations(diabetes_type, current_glucose, max(predictions.values()), bmi, bmi_cat, total_carbs)
        for i, rec in enumerate(recs):
            st.markdown(f'<div class="rec-card rc-{i % 7}">{rec}</div>', unsafe_allow_html=True)
    st.markdown("---")

    # SECTION 9
    st.markdown('<div class="section-header sh-purple"><div class="section-icon">🔮</div><div class="section-title">SECTION 9 — Future Health Insight</div></div>', unsafe_allow_html=True)
    if premium_gate("Future Trend Analysis"):
        pct_change = ((predictions[120] - current_glucose) / current_glucose) * 100 if current_glucose > 0 else 0
        direction = "increase" if pct_change > 0 else "decrease"
        st.markdown(f'<div class="insight-box"><div class="insight-value">{abs(pct_change):.1f}% {direction}</div><p>Predicted at 2 hours: {predictions[120]} mg/dL</p></div>', unsafe_allow_html=True)
    st.markdown("---")

    # SECTION 10
    st.markdown('<div class="section-header sh-pink"><div class="section-icon">🧠</div><div class="section-title">SECTION 10 — MBTI & Diet Matcher</div></div>', unsafe_allow_html=True)
    if premium_gate("MBTI Personality Diet Recommendations"):
        mbti_type = st.selectbox("Select your MBTI Type", ["INTJ", "ENTP", "ISFJ", "ESFP", "INFJ", "ENFP", "ISTP", "ESTJ"])
        st.success(f"**{mbti_type} Diet Strategy:** Based on your personality, structured meal prepping and macro tracking suits your analytical nature perfectly!")
    st.markdown("---")

    # SECTION 11
    st.markdown('<div class="section-header sh-blue"><div class="section-icon">📄</div><div class="section-title">SECTION 11 — Export Health Report</div></div>', unsafe_allow_html=True)
    if premium_gate("PDF Report Generation"):
        if st.button("📥 Generate & Download PDF", key="pdf_btn"):
            pdf_bytes = generate_pdf_report({'name': name}, {}, current_glucose, predictions, hs, risk, [], bmi, bmi_cat)
            st.download_button(label="⬇️ Click to Download PDF", data=pdf_bytes, file_name="GlucoVision_Premium_Report.pdf", mime="application/pdf")
    st.markdown("---")

# ─── AUTH CONTROLLER ──────────────────────────────────────────────────────────
def login_page():
    st.markdown("""
    <div style="text-align:center; padding: 2rem;">
        <h1 style="color:#00d9ff; font-size: 3rem; margin-bottom: 0;">🩺 GlucoVision AI</h1>
        <p style="color:#8b949e; font-size: 1.2rem;">Log in to access your metabolic dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login to Dashboard")
                
                if submit:
                    is_valid, acc_type = verify_user(u, p)
                    if is_valid:
                        st.session_state.logged_in = True
                        st.session_state.username = u
                        st.session_state.account_type = acc_type
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                        
        with tab2:
            with st.form("signup_form"):
                new_u = st.text_input("Choose a Username")
                new_p = st.text_input("Choose a Password", type="password")
                new_p2 = st.text_input("Confirm Password", type="password")
                submit_signup = st.form_submit_button("Create Free Account")
                
                if submit_signup:
                    if new_p != new_p2:
                        st.error("Passwords do not match!")
                    elif len(new_u) < 3 or len(new_p) < 4:
                        st.error("Username/Password too short.")
                    else:
                        if create_user(new_u, new_p):
                            st.success("Account created! Please log in from the Login tab.")
                        else:
                            st.error("Username already exists. Please choose another.")

def main():
    if st.session_state.logged_in:
        glucovision_app()
    else:
        login_page()

if __name__ == "__main__":
    main()
