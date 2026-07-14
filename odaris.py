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

# ─── DATABASE & AUTHENTICATION SYSTEMS ────────────────────────────────────────
DB_FILE = 'glucovision_saas.db'

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

# Initialize local database
init_db()

# Initialize session states for authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'account_type' not in st.session_state:
    st.session_state.account_type = None

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GlucoVision AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
section[data-testid="stSidebar"] .block-container {
    padding: 1rem;
}

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
.metric-icon {
    font-size: 1.3rem;
    margin-bottom: 0.25rem;
}

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
    width: 36px;
    height: 36px;
    background-color: #00d9ff;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.02em;
}

/* Color variants for headers */
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

/* Upgrade Messaging Boxes */
.upgrade-box {
    background: #1c1917;
    border: 2px dashed #a855f7;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    margin: 1.5rem 0;
}
.upgrade-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #ffd60a;
    margin-bottom: 0.5rem;
}

/* Risk badges */
.risk-low {
    color: #00e676;
    background: #0a2e1a;
    border: 2px solid #00e676;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.85rem;
    font-weight: 800;
}
.risk-medium {
    color: #ffd60a;
    background: #332700;
    border: 2px solid #ffd60a;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.85rem;
    font-weight: 800;
}
.risk-high {
    color: #ff3b3b;
    background: #3d0a0a;
    border: 2px solid #ff3b3b;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.85rem;
    font-weight: 800;
}

/* Streamlit widget overrides */
.stSelectbox > div > div {
    background-color: #161b22 !important;
    border: 2px solid #30363d !important;
    color: #ffffff !important;
}
.stNumberInput > div > div > input {
    background-color: #161b22 !important;
    border: 2px solid #30363d !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
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
hr {
    border-color: #30363d !important;
    border-width: 1px !important;
}

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
.nav-pill:hover {
    background-color: #21262d;
    color: #ffffff;
}

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
.glass-card strong {
    color: #00d9ff;
}
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

# ─── CORE MODEL & HELPERS ─────────────────────────────────────────────────────
def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, "N/A"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:
        cat = "Underweight"
    elif bmi < 25:
        cat = "Normal"
    elif bmi < 30:
        cat = "Overweight"
    else:
        cat = "Obese"
    return round(bmi, 1), cat

def _smoothstep(edge0: float, edge1: float, x: float) -> float:
    if edge0 == edge1:
        return 0.0 if x < edge0 else 1.0
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

def _cumulative_insulin_fraction(minutes: float, onset: float, peak: float, end: float) -> float:
    if minutes <= onset:
        return 0.0
    if minutes <= peak:
        return 0.5 * _smoothstep(onset, peak, minutes)
    if minutes <= end:
        return 0.5 + 0.5 * _smoothstep(peak, end, minutes)
    return 1.0

def _carb_excursion_fraction(minutes: float, peak: float, decay: float) -> float:
    if minutes <= peak:
        return _smoothstep(0, peak, minutes)
    if minutes <= (peak + decay):
        return 1.0 - _smoothstep(peak, peak + decay, minutes)
    return 0.0

def _estimate_bmr(weight_kg: float, age: int = 35, gender: str = "Male") -> float:
    weight_kg = max(weight_kg, 30.0)
    if gender == "Female":
        bmr = 10 * weight_kg + 6.25 * 170 - 5 * age - 161
    else:
        bmr = 10 * weight_kg + 6.25 * 170 - 5 * age + 5
    return max(1200.0, bmr)

def glucose_prediction_model(
    current_glucose: float, carbs_g: float, diabetes_type: str, 
    insulin_type: str, insulin_dose: float, time_since_injection_hr: float = 0.0,
    weight_kg: float = 70.0, age: int = 35, gender: str = "Male", 
    calories_kcal: float = 0.0, time_since_meal_hr: float = 0.0,
    exercise_type: str = "No Exercise", exercise_duration_min: float = 0.0
) -> dict[int, float]:
    weight_kg = weight_kg if weight_kg and weight_kg > 0 else 70.0
    carb_factor = {"No Diabetes": 1.1, "Prediabetes": 1.6, "Type 2 Diabetes": 2.2, "Type 1 Diabetes": 3.0}.get(diabetes_type, 1.6)
    carb_peak_rise = carbs_g * carb_factor
    carb_profile = CARB_RESPONSE_PROFILE.get(diabetes_type, CARB_RESPONSE_PROFILE["Prediabetes"])
    meal_elapsed_min = time_since_meal_hr * 60.0

    def _carb_delta_at(future_min: float) -> float:
        at_future = _carb_excursion_fraction(meal_elapsed_min + future_min, carb_profile["peak"], carb_profile["decay"])
        at_now = _carb_excursion_fraction(meal_elapsed_min, carb_profile["peak"], carb_profile["decay"])
        return carb_peak_rise * (at_future - at_now)

    bmr_kcal_day = _estimate_bmr(weight_kg, age, gender)
    glucose_distribution_dl = max(60.0, weight_kg * 2.0)
    HEPATIC_COMPENSATORY_EFFICIENCY = 0.03

    def _bmr_drop(minutes: float) -> float:
        kcal = bmr_kcal_day * (minutes / 1440.0)
        grams = (kcal / 4.0) * HEPATIC_COMPENSATORY_EFFICIENCY
        return (grams * 1000.0) / glucose_distribution_dl

    exercise_rate = {"No Exercise": 0.0, "Light (walking, yoga)": 0.30, "Moderate (jogging, cycling)": 0.70, "Intense (running, gym, sports)": 1.20}.get(exercise_type, 0.0)

    def _exercise_drop(future_min: float) -> float:
        if exercise_duration_min <= 0 or exercise_type == "No Exercise":
            return 0.0
        hours_post = 1.0 + (future_min / 60.0)
        duration_factor = min(exercise_duration_min, 90.0) / 30.0
        afterburn_intensity = exercise_rate * 0.30 * duration_factor * (0.5 ** (hours_post / 1.5))
        return afterburn_intensity * future_min

    insulin_factor_map = {"No Insulin": 0, "Rapid-Acting (e.g., Lispro, Aspart)": 45, "Short-Acting (Regular)": 35, "Intermediate-Acting (NPH)": 25, "Long-Acting (Glargine, Detemir)": 20, "Mixed Insulin (70/30)": 30}
    weight_adj = max(0.6, min(1.6, 70.0 / weight_kg))
    factor_per_unit = insulin_factor_map.get(insulin_type, 0) * weight_adj
    total_insulin_effect = factor_per_unit * (insulin_dose or 0.0)
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

def health_score(glucose: float, bmi: float, diabetes_type: str, predicted_peak: float, carbs: float) -> tuple[float, str]:
    score = 100.0
    if glucose < 70 or glucose > 180:
        score -= 25
    elif glucose < 80 or glucose > 140:
        score -= 12
    elif glucose < 90 or glucose > 120:
        score -= 5

    if predicted_peak > 200:
        score -= 20
    elif predicted_peak > 160:
        score -= 10

    if bmi < 16 or bmi >= 35:
        score -= 20
    elif bmi < 18.5 or bmi >= 30:
        score -= 10
    elif bmi < 17 or bmi >= 27:
        score -= 4

    dm_penalty = {"No Diabetes": 0, "Prediabetes": 8, "Type 2 Diabetes": 15, "Type 1 Diabetes": 18}
    score -= dm_penalty.get(diabetes_type, 0)

    if carbs > 80:
        score -= 10
    elif carbs > 50:
        score -= 5

    score = max(0.0, min(100.0, score))
    if score >= 75:
        risk = "Low Risk"
    elif score >= 50:
        risk = "Medium Risk"
    else:
        risk = "High Risk"
    return round(score, 1), risk

def get_recommendations(diabetes_type: str, glucose: float, predicted_peak: float, bmi: float, bmi_cat: str, carbs: float) -> list[str]:
    recs = []
    if glucose < 70:
        recs.append("⚠️ Current glucose appears low. Consume fast-acting carbs.")
    elif glucose > 180:
        recs.append("🔴 Current glucose is elevated. Ensure hydration and consult provider.")
    elif 80 <= glucose <= 120:
        recs.append("✅ Glucose is within healthy range.")

    if predicted_peak > 200:
        recs.append("📈 Glucose predicted to rise significantly. A 15-20 min walk helps.")
    elif predicted_peak > 160:
        recs.append("📊 Moderate glucose rise predicted. Monitor closely.")

    if diabetes_type == "Type 1 Diabetes":
        recs.append("💉 Consistent carb-counting is essential.")
    elif diabetes_type == "Type 2 Diabetes":
        recs.append("🥗 Reducing refined carbs improves control.")
    elif diabetes_type == "Prediabetes":
        recs.append("🌿 Reversible with lifestyle changes.")
    else:
        recs.append("✅ No diabetes detected. Maintain active lifestyle.")

    if bmi_cat == "Obese":
        recs.append("⚖️ 5–10% weight reduction improves sensitivity.")
    elif bmi_cat == "Overweight":
        recs.append("⚖️ Regular cardio (30 min/day) improves health.")

    if carbs > 80:
        recs.append("🍽️ High carb intake. Split meals and pair with protein.")
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

    # Title Banner style
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=24,
        textColor=colors.HexColor('#0f172a'), spaceAfter=12, alignment=TA_CENTER
    )
    elements.append(Paragraph("🩺 GLUCOVISION AI — HEALTH INSIGHT REPORT", title_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#00d9ff'), spaceAfter=15))

    # Metadata Panel
    meta_text = f"<b>Patient Profile:</b> {patient.get('name','N/A')} ({patient.get('age','N/A')}y, {patient.get('gender','N/A')}) &nbsp;&nbsp;|&nbsp;&nbsp; <b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>" \
                f"<b>Clinical Status:</b> {patient.get('diabetes_type','N/A')} &nbsp;&nbsp;|&nbsp;&nbsp; <b>BMI:</b> {bmi} ({bmi_cat})"
    elements.append(Paragraph(meta_text, styles['Normal']))
    elements.append(Spacer(1, 15))

    # Metrics Grid Summary Table
    metric_data = [
        [Paragraph("<b>Metric</b>", styles['Normal']), Paragraph("<b>Value Assessed</b>", styles['Normal'])],
        [Paragraph("Current Blood Glucose", styles['Normal']), Paragraph(f"{glucose_now} mg/dL", styles['Normal'])],
        [Paragraph("Estimated Peak Excursion", styles['Normal']), Paragraph(f"{max(predictions.values())} mg/dL", styles['Normal'])],
        [Paragraph("Carbohydrates Logged", styles['Normal']), Paragraph(f"{nutrition.get('carbs', 0):.1f} g", styles['Normal'])],
        [Paragraph("Composite Health Score", styles['Normal']), Paragraph(f"<b>{score} / 100</b> ({risk})", styles['Normal'])]
    ]
    t = Table(metric_data, colWidths=[6*cm, 10*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))

    # Forecast section
    elements.append(Paragraph("<b>2-Hour Glucose Response Curve Projection</b>", styles['Heading2']))
    forecast_text = f"• 30 min forecast: {predictions[30]} mg/dL<br/>• 60 min forecast: {predictions[60]} mg/dL<br/>• 90 min forecast: {predictions[90]} mg/dL<br/>• 120 min forecast: {predictions[120]} mg/dL"
    elements.append(Paragraph(forecast_text, styles['Normal']))
    elements.append(Spacer(1, 15))

    # Clinical Insights section
    elements.append(Paragraph("<b>AI Actionable Health Recommendations</b>", styles['Heading2']))
    for r in recommendations:
        elements.append(Paragraph(f"• {r}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Science Fair Disclaimer
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ef4444'), spaceAfter=10))
    disclaimer_style = ParagraphStyle('DiscStyle', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#7f1d1d'), leading=11)
    elements.append(Paragraph("<b>IMPORTANT DISCLAIMER:</b> GlucoVision AI is an educational prototype created for science fair demonstration purposes. It is NOT a medical device and is NOT intended for diagnosis, treatment, or clinical decision-making. The predictions and health metrics are generated by educational models and do not reflect real world clinical validation.", disclaimer_style))

    doc.build(elements)
    buf.seek(0)
    return buf.read()

# ─── VISUALIZATION GRAPH UTILITIES ───────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(10,14,26,0)',
    plot_bgcolor='rgba(10,14,26,0)',
    font=dict(family='Inter', color='#94a3b8', size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor='rgba(0,217,255,0.15)', linecolor='rgba(0,217,255,0.25)', zerolinecolor='rgba(0,0,0,0)'),
    yaxis=dict(gridcolor='rgba(0,217,255,0.15)', linecolor='rgba(0,217,255,0.25)', zerolinecolor='rgba(0,0,0,0)'),
)

def glucose_trend_chart(glucose_now: float, predictions: dict[int, float]):
    times = [0, 30, 60, 90, 120]
    values = [glucose_now] + [predictions[t] for t in [30, 60, 90, 120]]
    labels = ['Now', '30m', '60m', '90m', '2hr']

    fig = go.Figure()
    fig.add_hrect(y0=70, y1=140, fillcolor='rgba(0,230,118,0.12)', line_color='rgba(0,230,118,0.25)', annotation_text='Normal Target Range (70-140 mg/dL)', annotation_position='top left', annotation_font=dict(size=9, color='#00e676'))
    fig.add_trace(go.Scatter(x=labels, y=values, mode='lines+markers', line=dict(color='#00d9ff', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(0,217,255,0.12)', marker=dict(size=8, color='#00e676', line=dict(color='#ffffff', width=1.5)), name='Glucose Tracking Line'))
    fig.update_layout(**CHART_LAYOUT, title=dict(text='Metabolic Curve Forecast Over 2 Hours', font=dict(size=14, color='#e2e8f0', weight=700), x=0.5))
    return fig

def nutrition_pie_chart(carbs: float, protein: float, fat: float):
    if carbs == 0 and protein == 0 and fat == 0:
        carbs, protein, fat = 1.0, 1.0, 1.0
    fig = go.Figure(go.Pie(labels=['Carbohydrates', 'Protein', 'Fat'], values=[carbs, protein, fat], hole=0.55, marker=dict(colors=['#1e90ff', '#00d9ff', '#a855f7']), textinfo='percent+label', textfont=dict(weight=700)))
    fig.update_layout(**CHART_LAYOUT, title=dict(text='Meal Macronutrient Composition Matrix', font=dict(size=14, color='#e2e8f0', weight=700), x=0.5), showlegend=False)
    return fig

def risk_gauge(score: float, risk: str):
    color = '#00e676' if risk == "Low Risk" else ('#ffd60a' if risk == "Medium Risk" else '#ff3b3b')
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        number={'font': {'size': 36, 'color': color, 'family': 'Inter', 'weight': 800}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#334155'},
            'bar': {'color': color, 'thickness': 0.25},
            'bgcolor': 'rgba(15,23,42,0.5)',
            'bordercolor': 'rgba(0,217,255,0.2)',
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255,59,59,0.05)'},
                {'range': [50, 75], 'color': 'rgba(255,214,10,0.05)'},
                {'range': [75, 100], 'color': 'rgba(0,230,118,0.05)'}
            ]
        },
        title={'text': f"Risk State Evaluation: {risk}", 'font': {'color': '#94a3b8', 'size': 13, 'weight': 700}}
    ))
    fig.update_layout(**CHART_LAYOUT, height=260)
    return fig

def calorie_summary_chart(food_log: list[dict]):
    if not food_log:
        return go.Figure().update_layout(**CHART_LAYOUT, title=dict(text='No meal components logged yet', x=0.5))
    labels = [f['name'].split('(')[0].strip() for f in food_log]
    cals = [f['calories'] for f in food_log]
    fig = go.Figure(go.Bar(x=cals, y=labels, orientation='h', marker=dict(color=cals, colorscale=[[0, '#1e90ff'], [1, '#00ffc8']], line=dict(color='#ffffff', width=0.5))))
    fig.update_layout(**CHART_LAYOUT, title=dict(text='Caloric Contribution Map by Selected Food Items', font=dict(size=14, color='#e2e8f0', weight=700), x=0.5))
    return fig

# ─── APP RENDERING & NAVIGATION FUNCTIONS ──────────────────────────────────────
def render_sidebar_navigation():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div style="font-size:2.2rem; margin-bottom:0.3rem">🩺</div>
            <div class="sidebar-logo-title">GlucoVision AI</div>
            <div class="sidebar-logo-sub">Glucose Prediction System</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"👤 **Active User:** `{st.session_state.username}`")
        if st.session_state.account_type == "PREMIUM":
            st.markdown("<div style='background-color:#332700; border:1px solid #ffd60a; padding:6px; border-radius:5px; text-align:center; margin-bottom:10px;'><span style='color:#ffd60a; font-weight:800; font-size:0.85rem;'>👑 PREMIUM ACCESS</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color:#1e1b4b; border:1px solid #a855f7; padding:6px; border-radius:5px; text-align:center; margin-bottom:10px;'><span style='color:#c084fc; font-weight:800; font-size:0.85rem;'>🔹 FREE PLAN</span></div>", unsafe_allow_html=True)
            if st.button("🚀 Upgrade to Premium", use_container_width=True):
                upgrade_user(st.session_state.username)
                st.success("Successfully upgraded to Premium plan!")
                st.rerun()

        st.markdown("### 📋 System Operations Navigation")
        nav_elements = [
            ("👤", "Patient Profile Tracker"),
            ("💉", "Insulin Dosage Calculator"),
            ("🍽️", "Diet Optimization Index"),
            ("🔬", "Digital Twin Engine"),
            ("📈", "AI Real-Time Predictor"),
            ("📊", "Bio-Metric Visualizations"),
            ("🧠", "Metabolic Analytics Ledger"),
            ("💡", "Advanced Health Recommendations " + ("👑" if st.session_state.account_type == "PREMIUM" else "🔒")),
            ("🔮", "Future Health Trend Insights " + ("👑" if st.session_state.account_type == "PREMIUM" else "🔒")),
            ("🧠", "MBTI Personality Diet Matcher " + ("👑" if st.session_state.account_type == "PREMIUM" else "🔒")),
            ("📄", "Export Personalized PDF Report " + ("👑" if st.session_state.account_type == "PREMIUM" else "🔒")),
        ]
        
        for icon, title in nav_elements:
            st.markdown(f'<div class="nav-pill">{icon} &nbsp;{title}</div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🚪 Logout Account", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.account_type = None
            st.rerun()

def run_main_application():
    render_sidebar_navigation()

    # HERO JUMBOTRON HEADER PANEL
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🩺 GlucoVision AI</div>
        <div class="hero-subtitle">AI-POWERED PERSONALIZED DIABETES MONITORING & GLUCOSE PREDICTION SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)

    # CRITICAL SCIENCE FAIR CLINICAL PRACTICE DISCLAIMER
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ CRITICAL EDUCATIONAL SYSTEM DISCLAIMER:</strong><br/>
        This system architecture is built entirely as an educational computer science research prototype demonstration. 
        It does NOT integrate authenticated hardware diagnostic systems, nor has it received regulatory authorization. It must not be utilized for human healthcare decisions, prescription processing, or formal diagnostic validation.
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 1: USER DEMOGRAPHICS PROFILE PATIENT DATASET
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-blue"><div class="section-icon">👤</div><div class="section-title">SECTION 1 — Patient Demographics Profile Dataset</div></div>', unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Patient Full Legal Name Identification", value=st.session_state.username)
            age = st.number_input("Biological Age Matrix (Years)", min_value=1, max_value=115, value=35)
            gender = st.selectbox("Biological Sex Classification", ["Select Classification", "Male", "Female", "Intersex", "Decline to State"])
        with col2:
            weight = st.number_input("Patient Body Mass Coefficient (Kilograms)", min_value=10.0, max_value=300.0, value=74.5, step=0.1)
            height = st.number_input("Patient Vertical Stature Metric (Centimeters)", min_value=50.0, max_value=250.0, value=174.0, step=0.1)
        with col3:
            diabetes_type = st.selectbox("Clinical Pathological Diabetes Classification", ["Select Condition State", "No Diabetes Profile", "Prediabetes Condition", "Type 1 Diabetes Mellitus", "Type 2 Diabetes Mellitus"])

        bmi, bmi_cat = calculate_bmi(weight, height)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("📊 Computed Body Mass Index (BMI)", f"{bmi}")
        col_m2.metric("🏷️ Categorical Weight Classification", bmi_cat)
        col_m3.metric("🧬 Evaluated Pathological Profile", diabetes_type.replace(" Profile","").replace(" Condition","").replace(" Mellitus","") if diabetes_type else "N/A")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 2: INSULIN DRUG INJECTION MANAGEMENT LOGIC
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-red"><div class="section-icon">💉</div><div class="section-title">SECTION 2 — Insulin Pharmacology Dosage Vector Input</div></div>', unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            if diabetes_type == "No Diabetes Profile":
                insulin_type = "No Insulin"
                st.markdown("<p style='color:#00e676 !important;'>💡 Non-diabetic metabolic tracking activated. Insulin configuration bypass engaged.</p>", unsafe_allow_html=True)
            else:
                insulin_type = st.selectbox("Pharmacological Insulin Variant Profile", INSULIN_TYPES)
        with col2:
            if diabetes_type == "No Diabetes Profile" or insulin_type == "No Insulin":
                insulin_dose = 0.0
                st.number_input("Injected Pharmacological Volume (International Units)", min_value=0.0, max_value=0.0, value=0.0, disabled=True)
            else:
                insulin_dose = st.number_input("Injected Pharmacological Volume (International Units)", min_value=0.0, max_value=150.0, value=4.5, step=0.5)
        with col3:
            if diabetes_type == "No Diabetes Profile" or insulin_type == "No Insulin":
                time_since_injection = 0.0
                st.number_input("Time Interval Since Medication Injection (Hours)", min_value=0.0, max_value=0.0, value=0.0, disabled=True)
            else:
                time_since_injection = st.number_input("Time Interval Since Medication Injection (Hours)", min_value=0.0, max_value=24.0, value=1.0, step=0.25)

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 3: DIET INTEGRITY & NUTRITIONAL INTELLIGENCE
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-orange"><div class="section-icon">🍽️</div><div class="section-title">SECTION 3 — Nutritional Intake Intelligence Database Matrix</div></div>', unsafe_allow_html=True)
    with st.container():
        selected_foods = st.multiselect("Query & Log Meal Component Ingredients Consumed", options=list(FOOD_DB.keys()), default=[])
        
        food_log = []
        total_cal = 0.0
        total_carbs = 0.0
        total_protein = 0.0
        total_fat = 0.0

        if selected_foods:
            st.markdown("<p style='font-size:0.85rem; color:#94a3b8;'>Adjust exact ingredient scaling weights below:</p>", unsafe_allow_html=True)
            food_cols = st.columns(min(len(selected_foods), 4))
            for idx, food_item in enumerate(selected_foods):
                with food_cols[idx % 4]:
                    servings = st.number_input(f"Portion Vector × {food_item.split('(')[0].strip()}", min_value=0.1, max_value=20.0, value=1.0, step=0.1, key=f"food_srv_{idx}")
                    base_nutr = FOOD_DB[food_item]
                    
                    item_cal = base_nutr["calories"] * servings
                    item_carb = base_nutr["carbs"] * servings
                    item_prot = base_nutr["protein"] * servings
                    item_fat = base_nutr["fat"] * servings
                    
                    food_log.append({"name": food_item, "calories": item_cal, "carbs": item_carb, "protein": item_prot, "fat": item_fat})
                    
                    total_cal += item_cal
                    total_carbs += item_carb
                    total_protein += item_prot
                    total_fat += item_fat

            st.markdown("<br/>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🔥 Total Energy Yielded", f"{total_cal:.1f} kcal")
            c2.metric("🍞 Total Carbs Mass Vector", f"{total_carbs:.1f} g")
            c3.metric("💪 Total Amino Protein Mass", f"{total_protein:.1f} g")
            c4.metric("🥑 Total Lipid Fat Density", f"{total_fat:.1f} g")
        else:
            st.info("💡 Nutritional ledger empty. Use drop down selectors above to construct current meal simulation parameters.")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 4: METABOLIC DIGITAL TWIN COMPUTATIONAL SIMULATION
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-teal"><div class="section-icon">🔬</div><div class="section-title">SECTION 4 — Real-time Metabolic Digital Twin Configuration</div></div>', unsafe_allow_html=True)
    with st.container():
        current_glucose = st.slider("🩸 Calibrate Real-time Plasma Blood Glucose Sensor Baseline (mg/dL)", min_value=40, max_value=400, value=112, step=1)
        
        predictions = glucose_prediction_model(
            current_glucose=current_glucose, carbs_g=total_carbs, diabetes_type=diabetes_type.replace(" Profile","").replace(" Condition","").replace(" Mellitus",""),
            insulin_type=insulin_type, insulin_dose=insulin_dose, time_since_injection_hr=time_since_injection,
            weight_kg=weight, age=int(age), gender=gender, calories_kcal=total_cal
        )
        
        predicted_60 = predictions[60]
        peak_excursion_val = max(predictions.values())
        hs, risk = health_score(current_glucose, bmi, diabetes_type.replace(" Profile","").replace(" Condition","").replace(" Mellitus",""), peak_excursion_val, total_carbs)

        st.markdown("<br/>", unsafe_allow_html=True)
        grid_c1, grid_c2, grid_c3, grid_c4, grid_c5, grid_c6 = st.columns(6)
        
        metrics_data_cards = [
            (grid_c1, '🩸', f"{current_glucose}", "Live Glucose"),
            (grid_c2, '📈', f"{predicted_60}", "Twin Pred (60m)"),
            (grid_c3, '🔥', f"{total_cal:.0f}", "Energy Vol"),
            (grid_c4, '🍞', f"{total_carbs:.0f}g", "Active Carbs"),
            (grid_c5, '⚖️', f"{bmi}", "BMI Stat"),
            (grid_c6, '💯', f"{hs}", "Health Score")
        ]
        
        for context_col, emoji_sym, data_val, caption_lbl in metrics_data_cards:
            context_col.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{emoji_sym}</div>
                <div class="metric-value">{data_val}</div>
                <div class="metric-label">{caption_lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTIONS 5, 6, 7: GRAPHICAL PREDICTION CHANNELS & VISUALIZATION FORECASTS
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-green"><div class="section-icon">📊</div><div class="section-title">SECTIONS 5, 6, 7 — Predictive Visualization Streams & Bio-Metric Graphs</div></div>', unsafe_allow_html=True)
    with st.container():
        vis_col1, vis_col2 = st.columns(2)
        with vis_col1:
            st.plotly_chart(glucose_trend_chart(current_glucose, predictions), use_container_width=True)
        with vis_col2:
            st.plotly_chart(risk_gauge(hs, risk), use_container_width=True)

        vis_col3, vis_col4 = st.columns(2)
        with vis_col3:
            st.plotly_chart(nutrition_pie_chart(total_carbs, total_protein, total_fat), use_container_width=True)
        with vis_col4:
            st.plotly_chart(calorie_summary_chart(food_log), use_container_width=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 8: ADVANCED HEALTH RECOMMENDATIONS INDEX (PREMIUM)
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-yellow"><div class="section-icon">💡</div><div class="section-title">SECTION 8 — AI Actionable Health Recommendation Framework</div></div>', unsafe_allow_html=True)
    if st.session_state.account_type == "PREMIUM":
        with st.container():
            recs_list = get_recommendations(
                diabetes_type=diabetes_type.replace(" Profile","").replace(" Condition","").replace(" Mellitus",""),
                glucose=current_glucose, predicted_peak=peak_excursion_val, bmi=bmi, bmi_cat=bmi_cat, carbs=total_carbs
            )
            for idx, recommendation_item in enumerate(recs_list):
                st.markdown(f'<div class="rec-card rc-{idx % 7}">{recommendation_item}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="upgrade-box">
            <div class="upgrade-title">🔒 Premium Health Recommendations Locked</div>
            <p>Upgrade your account to Premium to unlock AI-generated lifestyle modifications and nutritional balancing alerts based on your real-time metabolic twin status.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 9: FUTURE HEALTH INSIGHT ENGINE (PREMIUM)
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-purple"><div class="section-icon">🔮</div><div class="section-title">SECTION 9 — Predictive Future Health Insights Engine</div></div>', unsafe_allow_html=True)
    if st.session_state.account_type == "PREMIUM":
        with st.container():
            percentage_variance = ((predictions[120] - current_glucose) / current_glucose) * 100.0 if current_glucose > 0 else 0
            variance_vector_direction = "increase" if percentage_variance >= 0 else "decrease"
            
            st.markdown(f"""
            <div class="insight-box">
                <p>2-Hour Computational Projection Directional Excursion Analysis Index:</p>
                <div class="insight-value">{abs(percentage_variance):.1f}% Dynamic {variance_vector_direction.capitalize()}</div>
                <p style="margin-top:0.5rem; font-size:0.88rem; color:#94a3b8 !important;">
                    The digital clone mathematical matrix forecasts a localized stabilization index at approximately <strong>{predictions[120]} mg/dL</strong> at the 120-minute mark.
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="upgrade-box">
            <div class="upgrade-title">🔒 Premium Trend Analytics Locked</div>
            <p>Access advanced longitudinal metabolic modeling, percentage drift analysis, and multi-hour stabilization indexing by upgrading to Premium.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 10: MBTI DIET PERSONALITY ALIGNMENT ENGINE (PREMIUM)
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-pink"><div class="section-icon">🧠</div><div class="section-title">SECTION 10 — Cognitive MBTI Personality Diet Alignment Index</div></div>', unsafe_allow_html=True)
    if st.session_state.account_type == "PREMIUM":
        with st.container():
            mbti_profile_selected = st.selectbox("Calibrate Patient Cognitive MBTI Archetype Structure", ["INTJ - The Architect", "INTP - The Logician", "ENTJ - The Commander", "ENTP - The Debater", "INFJ - The Advocate", "INFP - The Mediator", "ENFJ - The Protagonist", "ENFP - The Campaigner", "ISTJ - The Logistician", "ISFJ - The Defender", "ESTJ - The Executive", "ESFJ - The Consul", "ISTP - The Virtuoso", "ISFP - The Adventurer", "ESTP - The Entrepreneur", "ESFP - The Entertainer"])
            
            mbti_clean = mbti_profile_selected.split(" - ")[0]
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid #ff2d95;">
                <p style="color:#ff2d95 !important; font-size:1.05rem; font-weight:800; margin-bottom:0.4rem;">🎯 Personalized Behavioral Health Strategy for Archetype Type: {mbti_clean}</p>
                According to cross-referenced cognitive archetype compliance indexing data, individuals belonging to the <strong>{mbti_clean}</strong> bracket respond with optimal statistical retention to data-driven, structured health parameters. Avoid generic dietary guidelines; prioritize macro tracking and precise scheduling logs to keep your analytic focus engaged with metabolic targets.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="upgrade-box">
            <div class="upgrade-title">🔒 Premium MBTI Diet Matcher Locked</div>
            <p>Unlock custom cognitive behavioral health coaching strategies mapped directly to your Myers-Briggs personality matrix. Premium accounts only.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SECTION 11: CUSTOM PDF EXPORT REPORT GENERATION SYSTEM (PREMIUM)
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header sh-blue"><div class="section-icon">📄</div><div class="section-title">SECTION 11 — Document Export System Pipeline</div></div>', unsafe_allow_html=True)
    if st.session_state.account_type == "PREMIUM":
        with st.container():
            st.markdown("""
            <div class="glass-card">
                <strong>📋 PDF Compiler Output Engine Active:</strong><br/>
                Click the execution trigger button below to consolidate your current digital twin profile metrics, predictive graphs, macro matrices, and safety fair documentation vectors into a publication-grade health dossier.
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📥 Compile Comprehensive PDF Dossier Data Document", use_container_width=True):
                patient_dataset_obj = {
                    "name": name if name else "Anonymous Demonstration Client",
                    "age": age,
                    "gender": gender,
                    "diabetes_type": diabetes_type
                }
                nutrition_dataset_obj = {
                    "calories": total_cal,
                    "carbs": total_carbs,
                    "protein": total_protein,
                    "fat": total_fat
                }
                recs_array = get_recommendations(
                    diabetes_type=diabetes_type.replace(" Profile","").replace(" Condition","").replace(" Mellitus",""),
                    glucose=current_glucose, predicted_peak=peak_excursion_val, bmi=bmi, bmi_cat=bmi_cat, carbs=total_carbs
                )
                
                pdf_binary_stream = generate_pdf_report(
                    patient=patient_dataset_obj, nutrition=nutrition_dataset_obj, glucose_now=current_glucose,
                    predictions=predictions, score=hs, risk=risk, recommendations=recs_array, bmi=bmi, bmi_cat=bmi_cat
                )
                
                st.download_button(
                    label="⬇️ Click to Download Generated PDF System Report File",
                    data=pdf_binary_stream,
                    file_name=f"GlucoVision_Health_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("✅ PDF compiled and ready for deployment transfer!")
    else:
        st.markdown("""
        <div class="upgrade-box">
            <div class="upgrade-title">🔒 Premium Report Export Locked</div>
            <p>Upgrade to Premium to compile and export clinical-style PDF data sheets summarizing your digital twin forecast arrays, food logs, and health score ledgers.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════════
    # SYSTEM INTERFACE FOOTER LEGAL DISCLAIMER
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="text-align:center; padding: 2rem 1rem 1rem; border-top: 1px solid rgba(0,217,255,0.2);">
        <div style="font-size:0.9rem; font-weight:700; color:#ff3b3b; margin-bottom:0.5rem">
            ⚠️ IMPORTANT SYSTEM INTERFACE DISCLAIMER
        </div>
        <div style="font-size:0.8rem; color:#8b949e; max-width:700px; margin:0 auto; line-height:1.7">
            GlucoVision AI is an <strong style="color:#ffffff">educational prototype</strong> created for
            science fair demonstration purposes. It is <strong style="color:#ff3b3b">NOT a medical device</strong>
            and is NOT intended for diagnosis, treatment, or any form of medical decision-making.
            The glucose predictions and health scores are generated by simplified educational models
            and do not reflect clinical accuracy. Always consult a qualified healthcare professional
            for any medical concerns.
        </div>
        <div style="font-size:0.72rem; color:#484f58; margin-top:1.5rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">
            © 2026 GLUCOVISION AI PROTOTYPE LABS INC. ALL METRICS ARE SIMULATED SCHEMATICS.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── ENTRY AUTH CONTROLLER ROUTING FLOW ───────────────────────────────────────
def render_authentication_portal():
    st.markdown("""
    <div style="text-align:center; padding: 2.5rem 1rem 1.5rem;">
        <h1 style="color:#00d9ff; font-size: 3.2rem; margin-bottom: 0; font-weight:800; letter-spacing:-0.02em;">🩺 GlucoVision AI</h1>
        <p style="color:#8b949e; font-size: 1.1rem; font-weight:600; margin-top:0.3rem;">SaaS Metabolic Modeling & Digital Twin Simulation Hub</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔒 Secure Account Login", "✨ Create New Account"])
        
        with tab_login:
            with st.form("auth_login_form"):
                user_input = st.text_input("Enter Account Username")
                pass_input = st.text_input("Enter Account Password", type="password")
                login_trigger = st.form_submit_button("Authenticate & Initialize Portal", use_container_width=True)
                
                if login_trigger:
                    if not user_input or not pass_input:
                        st.error("Please enter both username and password values.")
                    else:
                        is_authenticated, verified_plan = verify_user(user_input, pass_input)
                        if is_authenticated:
                            st.session_state.logged_in = True
                            st.session_state.username = user_input
                            st.session_state.account_type = verified_plan
                            st.success("Authentication successful! Loading metabolic workspace...")
                            st.rerun()
                        else:
                            st.error("Invalid username or password credentials provided.")
                            
        with tab_signup:
            with st.form("auth_signup_form"):
                reg_user = st.text_input("Choose Unique Account Username")
                reg_pass1 = st.text_input("Create Secure Password", type="password")
                reg_pass2 = st.text_input("Confirm Secure Password", type="password")
                signup_trigger = st.form_submit_button("Register New Free Tier Workspace", use_container_width=True)
                
                if signup_trigger:
                    if not reg_user or not reg_pass1:
                        st.error("Username and password fields cannot be left blank.")
                    elif reg_pass1 != reg_pass2:
                        st.error("Password confirmation mismatch. Input matching security values.")
                    elif len(reg_user) < 3 or len(reg_pass1) < 5:
                        st.error("Security Requirements: Username min 3 chars, Password min 5 chars.")
                    else:
                        if create_user(reg_user, reg_pass1):
                            st.success("Account successfully indexed into database structure! Please access the Login tab to authenticate.")
                        else:
                            st.error("Registration Collision: Username is already registered inside database registry.")

def main():
    if st.session_state.logged_in:
        run_main_application()
    else:
        render_authentication_portal()

if __name__ == "__main__":
    main()
