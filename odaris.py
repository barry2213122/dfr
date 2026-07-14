"""
GLUCOVISION AI
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
import random

st.set_page_config(
    page_title="Unified AI Suite",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #ffffff; }
.stApp { background-color: #0d1117; }
section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 2px solid #00d9ff;
}
section[data-testid="stSidebar"] .block-container { padding: 1rem; }
label, .stTextInput label, .stNumberInput label,
.stSelectbox label, .stSlider label, .stMultiSelect label, .stRadio label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}
p, .stMarkdown p { color: #e6edf3 !important; font-weight: 600 !important; font-size: 0.95rem !important; }
.metric-card {
    background-color: #161b22;
    border: 2px solid #00d9ff;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-value { font-size: 1.9rem; font-weight: 800; color: #00d9ff; line-height: 1.2; }
.metric-label { font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #c9d1d9; margin-top: 0.3rem; }
.metric-icon { font-size: 1.3rem; margin-bottom: 0.25rem; }
.section-header {
    display: flex; align-items: center; gap: 0.7rem; margin-bottom: 1.2rem;
    padding-bottom: 0.6rem; border-bottom: 3px solid #00d9ff;
}
.section-icon {
    width: 36px; height: 36px; background-color: #00d9ff; border-radius: 6px;
    display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
}
.section-title { font-size: 1.1rem; font-weight: 800; color: #ffffff; letter-spacing: 0.02em; }
.sh-blue   { border-bottom-color: #1e90ff; } .sh-blue .section-icon { background-color: #1e90ff; }
.sh-green  { border-bottom-color: #00e676; } .sh-green .section-icon { background-color: #00e676; }
.sh-orange { border-bottom-color: #ff9100; } .sh-orange .section-icon { background-color: #ff9100; }
.sh-pink   { border-bottom-color: #ff2d95; } .sh-pink .section-icon { background-color: #ff2d95; }
.sh-purple { border-bottom-color: #a855f7; } .sh-purple .section-icon { background-color: #a855f7; }
.sh-yellow { border-bottom-color: #ffd60a; } .sh-yellow .section-icon { background-color: #ffd60a; }
.sh-red    { border-bottom-color: #ff3b3b; } .sh-red .section-icon { background-color: #ff3b3b; }
.sh-teal   { border-bottom-color: #00ffc8; } .sh-teal .section-icon { background-color: #00ffc8; }
.hero-header {
    text-align: center; padding: 1.8rem 1rem; background-color: #161b22;
    border-radius: 12px; border: 3px solid #00e676; margin-bottom: 1.5rem;
}
.hero-title { font-size: 2.7rem; font-weight: 800; color: #00d9ff; margin: 0; letter-spacing: -0.01em; }
.hero-subtitle { font-size: 0.95rem; color: #c9d1d9; margin: 0.5rem 0 0; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
.disclaimer {
    background-color: #3d0a0a; border: 3px solid #ff3b3b; border-radius: 8px; padding: 0.8rem 1.2rem;
    margin-bottom: 1.5rem; font-size: 0.85rem; font-weight: 700; color: #ff8080;
}
.risk-low   { color: #00e676; background: #0a2e1a; border: 2px solid #00e676; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }
.risk-medium{ color: #ffd60a; background: #332700; border: 2px solid #ffd60a; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }
.risk-high  { color: #ff3b3b; background: #3d0a0a; border: 2px solid #ff3b3b; border-radius:6px; padding:3px 10px; font-size:0.85rem; font-weight:800; }
.stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {
    background-color: #161b22 !important; border: 2px solid #30363d !important; color: #ffffff !important; font-weight: 700 !important;
}
div[data-testid="metric-container"] {
    background-color: #161b22; border: 2px solid #30363d; border-radius: 8px; padding: 0.5rem 1rem;
}
div[data-testid="metric-container"] label { color: #c9d1d9 !important; font-weight: 700 !important; }
div[data-testid="metric-container"] [data-testid="metric-value"] { color: #00d9ff !important; font-weight: 800 !important; }
.stButton > button {
    background-color: #00e676 !important; color: #0d1117 !important; border: none !important; border-radius: 6px !important;
    font-weight: 800 !important; font-size: 0.95rem !important; padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover { background-color: #5cffb0 !important; }
hr { border-color: #30363d !important; border-width: 1px !important; }
.sidebar-logo { text-align: center; padding: 1rem 0 1.5rem; border-bottom: 2px solid #00d9ff; margin-bottom: 1.5rem; }
.sidebar-logo-title { font-size: 1.4rem; font-weight: 800; color: #00d9ff; }
.sidebar-logo-sub { font-size: 0.7rem; color: #8b949e; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
.rec-card {
    background-color: #161b22; border: 2px solid #30363d; border-left: 5px solid #00d9ff;
    border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.8rem; font-size: 0.9rem; font-weight: 700; color: #e6edf3;
}
.rec-card.rc-0 { border-left-color: #00d9ff; } .rec-card.rc-1 { border-left-color: #00e676; }
.rec-card.rc-2 { border-left-color: #ffd60a; } .rec-card.rc-3 { border-left-color: #ff9100; }
.rec-card.rc-4 { border-left-color: #ff2d95; } .rec-card.rc-5 { border-left-color: #a855f7; }
.rec-card.rc-6 { border-left-color: #1e90ff; }
.glass-card {
    background-color: #161b22; border: 2px solid #30363d; border-radius: 10px; padding: 1.2rem; margin-bottom: 1rem;
}
.glass-card strong { color: #00d9ff; }
</style>
""", unsafe_allow_html=True)

FOOD_DB = {
    "Cooked Rice (white) (100 g)": {"calories": 130.0, "carbs": 28.0, "protein": 2.7, "fat": 0.3},
    "Wheat Roti / Chapati (1 medium (40 g))": {"calories": 104.0, "carbs": 20.0, "protein": 3.0, "fat": 1.7},
    "Whole Wheat Flour (Atta) (100 g (raw))": {"calories": 341.0, "carbs": 72.0, "protein": 12.0, "fat": 1.7},
    "Basmati Rice (cooked) (100 g)": {"calories": 121.0, "carbs": 25.0, "protein": 2.7, "fat": 0.4},
    "Idli (2 pieces (~70 g))": {"calories": 78.0, "carbs": 16.0, "protein": 2.5, "fat": 0.4},
    "Dosa (plain) (1 medium (~80 g))": {"calories": 168.0, "carbs": 28.0, "protein": 3.9, "fat": 3.7},
    "Poha (flattened rice) (1 bowl (150 g cooked))": {"calories": 180.0, "carbs": 38.0, "protein": 3.6, "fat": 1.8},
    "Upma (semolina) (1 bowl (150 g cooked))": {"calories": 200.0, "carbs": 32.0, "protein": 4.5, "fat": 6.0},
    "Paratha (plain, with oil) (1 medium (60 g))": {"calories": 210.0, "carbs": 27.0, "protein": 4.0, "fat": 9.0},
    "Puri (1 piece (25 g))": {"calories": 101.0, "carbs": 11.0, "protein": 1.7, "fat": 5.5},
    "Toor / Arhar Dal (cooked) (1 bowl (150 g))": {"calories": 170.0, "carbs": 28.0, "protein": 10.5, "fat": 1.5},
    "Moong Dal (cooked) (1 bowl (150 g))": {"calories": 150.0, "carbs": 25.0, "protein": 10.0, "fat": 0.6},
    "Chana Dal (cooked) (1 bowl (150 g))": {"calories": 210.0, "carbs": 34.0, "protein": 12.0, "fat": 3.0},
    "Rajma (Kidney Beans, cooked) (1 bowl (150 g))": {"calories": 165.0, "carbs": 30.0, "protein": 10.5, "fat": 0.6},
    "Chole (Chickpeas, cooked) (1 bowl (150 g))": {"calories": 210.0, "carbs": 34.0, "protein": 11.0, "fat": 3.0},
    "Paneer (100 g)": {"calories": 265.0, "carbs": 1.2, "protein": 18.3, "fat": 20.8},
    "Curd / Yogurt (Dahi) (100 g)": {"calories": 60.0, "carbs": 4.7, "protein": 3.5, "fat": 3.3},
    "Milk (whole/full cream) (1 glass (200 ml))": {"calories": 134.0, "carbs": 9.6, "protein": 6.4, "fat": 8.0},
    "Buttermilk (Chaas) (1 glass (200 ml))": {"calories": 40.0, "carbs": 3.6, "protein": 2.0, "fat": 1.8},
    "Ghee (1 tsp (5 g))": {"calories": 45.0, "carbs": 0.0, "protein": 0.0, "fat": 5.0},
    "Butter (1 tsp (5 g))": {"calories": 36.0, "carbs": 0.0, "protein": 0.0, "fat": 4.1},
    "Egg (whole, boiled) (1 large (50 g))": {"calories": 78.0, "carbs": 0.6, "protein": 6.3, "fat": 5.3},
    "Chicken (cooked, breast) (100 g)": {"calories": 165.0, "carbs": 0.0, "protein": 31.0, "fat": 3.6},
    "Mutton (cooked) (100 g)": {"calories": 250.0, "carbs": 0.0, "protein": 25.0, "fat": 16.0},
    "Fish (Rohu, cooked) (100 g)": {"calories": 105.0, "carbs": 0.0, "protein": 20.0, "fat": 2.4},
    "Potato (boiled) (100 g)": {"calories": 87.0, "carbs": 20.0, "protein": 1.9, "fat": 0.1},
    "Onion (raw) (100 g)": {"calories": 40.0, "carbs": 9.3, "protein": 1.1, "fat": 0.1},
    "Tomato (raw) (100 g)": {"calories": 18.0, "carbs": 3.9, "protein": 0.9, "fat": 0.2},
    "Spinach / Palak (cooked) (100 g)": {"calories": 23.0, "carbs": 3.6, "protein": 2.9, "fat": 0.4},
    "Cauliflower (cooked) (100 g)": {"calories": 25.0, "carbs": 5.0, "protein": 1.8, "fat": 0.3},
    "Bhindi / Okra (cooked) (100 g)": {"calories": 35.0, "carbs": 7.5, "protein": 2.0, "fat": 0.2},
    "Brinjal / Baingan (cooked) (100 g)": {"calories": 25.0, "carbs": 5.9, "protein": 1.0, "fat": 0.2},
    "Green Peas (cooked) (100 g)": {"calories": 84.0, "carbs": 14.5, "protein": 5.4, "fat": 0.4},
    "Carrot (raw) (100 g)": {"calories": 41.0, "carbs": 9.6, "protein": 0.9, "fat": 0.2},
    "Cucumber (raw) (100 g)": {"calories": 15.0, "carbs": 3.6, "protein": 0.7, "fat": 0.1},
    "Banana (1 medium (120 g))": {"calories": 105.0, "carbs": 27.0, "protein": 1.3, "fat": 0.4},
    "Apple (1 medium (150 g))": {"calories": 78.0, "carbs": 21.0, "protein": 0.4, "fat": 0.3},
    "Mango (1 medium (200 g))": {"calories": 120.0, "carbs": 30.0, "protein": 1.6, "fat": 0.6},
    "Papaya (100 g)": {"calories": 43.0, "carbs": 11.0, "protein": 0.5, "fat": 0.3},
    "Orange (1 medium (130 g))": {"calories": 62.0, "carbs": 15.5, "protein": 1.2, "fat": 0.2},
    "Peanuts (roasted) (30 g (handful))": {"calories": 170.0, "carbs": 6.0, "protein": 7.7, "fat": 14.5},
    "Almonds (10 pieces (12 g))": {"calories": 70.0, "carbs": 2.6, "protein": 2.6, "fat": 6.0},
    "Cashews (10 pieces (15 g))": {"calories": 87.0, "carbs": 4.9, "protein": 2.8, "fat": 7.0},
    "Coconut (fresh) (30 g piece)": {"calories": 106.0, "carbs": 4.6, "protein": 1.0, "fat": 10.1},
    "Tea (with milk & sugar) (1 cup (150 ml))": {"calories": 55.0, "carbs": 8.5, "protein": 1.2, "fat": 1.8},
    "Coffee (with milk & sugar) (1 cup (150 ml))": {"calories": 60.0, "carbs": 9.0, "protein": 1.5, "fat": 1.8},
    "Sugar (1 tsp (5 g))": {"calories": 19.0, "carbs": 5.0, "protein": 0.0, "fat": 0.0},
    "Jaggery (Gur) (1 tsp (5 g))": {"calories": 19.0, "carbs": 4.8, "protein": 0.0, "fat": 0.0},
    "Samosa (1 piece (60 g))": {"calories": 260.0, "carbs": 24.0, "protein": 3.5, "fat": 17.0},
    "Glucose Biscuits (4 biscuits (25 g))": {"calories": 110.0, "carbs": 19.0, "protein": 1.7, "fat": 3.2},
    "Aloo Gobi (1 bowl (150 g))": {"calories": 150.0, "carbs": 18.0, "protein": 3.5, "fat": 7.0},
    "Baingan Bharta (1 bowl (150 g))": {"calories": 130.0, "carbs": 12.0, "protein": 2.5, "fat": 8.0},
    "Palak Paneer (1 bowl (150 g))": {"calories": 220.0, "carbs": 8.0, "protein": 9.0, "fat": 16.0},
    "Matar Paneer (1 bowl (150 g))": {"calories": 230.0, "carbs": 12.0, "protein": 10.0, "fat": 15.0},
    "Bhindi Masala (1 bowl (150 g))": {"calories": 140.0, "carbs": 10.0, "protein": 3.0, "fat": 9.0},
    "Dum Aloo (1 bowl (150 g))": {"calories": 200.0, "carbs": 20.0, "protein": 3.0, "fat": 12.0},
    "Aloo Methi (1 bowl (150 g))": {"calories": 160.0, "carbs": 17.0, "protein": 3.5, "fat": 8.0},
    "Lauki Sabzi (Bottle Gourd) (1 bowl (150 g))": {"calories": 90.0, "carbs": 10.0, "protein": 2.0, "fat": 4.0},
    "Kaddu Sabzi (Pumpkin) (1 bowl (150 g))": {"calories": 95.0, "carbs": 12.0, "protein": 2.0, "fat": 4.0},
    "Karela Sabzi (Bitter Gourd) (1 bowl (150 g))": {"calories": 110.0, "carbs": 9.0, "protein": 2.5, "fat": 7.0},
    "Gajar Matar (Carrot Peas) (1 bowl (150 g))": {"calories": 120.0, "carbs": 15.0, "protein": 4.0, "fat": 4.0},
    "Cabbage Sabzi (1 bowl (150 g))": {"calories": 100.0, "carbs": 11.0, "protein": 2.5, "fat": 5.0},
    "Mixed Vegetable Curry (1 bowl (150 g))": {"calories": 150.0, "carbs": 15.0, "protein": 4.0, "fat": 8.0},
    "Kofta Curry (2 kofta + gravy (150 g))": {"calories": 260.0, "carbs": 18.0, "protein": 6.0, "fat": 18.0},
    "Butter Chicken (1 bowl (200 g))": {"calories": 350.0, "carbs": 10.0, "protein": 20.0, "fat": 25.0},
    "Chicken Tikka Masala (1 bowl (200 g))": {"calories": 320.0, "carbs": 10.0, "protein": 24.0, "fat": 20.0},
    "Egg Curry (2 eggs + gravy (200 g))": {"calories": 280.0, "carbs": 10.0, "protein": 14.0, "fat": 20.0},
    "Fish Curry (1 bowl (200 g))": {"calories": 220.0, "carbs": 6.0, "protein": 20.0, "fat": 13.0},
    "Prawn Curry (1 bowl (200 g))": {"calories": 200.0, "carbs": 6.0, "protein": 18.0, "fat": 12.0},
    "Mutton Rogan Josh (1 bowl (200 g))": {"calories": 350.0, "carbs": 8.0, "protein": 22.0, "fat": 25.0},
    "Naan (1 piece (90 g))": {"calories": 260.0, "carbs": 45.0, "protein": 7.0, "fat": 6.0},
    "Kulcha (1 piece (80 g))": {"calories": 230.0, "carbs": 38.0, "protein": 6.0, "fat": 6.0},
    "Bhatura (1 piece (80 g))": {"calories": 280.0, "carbs": 35.0, "protein": 6.0, "fat": 13.0},
    "Missi Roti (1 piece (50 g))": {"calories": 120.0, "carbs": 20.0, "protein": 4.0, "fat": 3.0},
    "Thepla (1 piece (40 g))": {"calories": 110.0, "carbs": 15.0, "protein": 3.0, "fat": 4.0},
    "Chicken Biryani (1 plate (250 g))": {"calories": 450.0, "carbs": 55.0, "protein": 20.0, "fat": 15.0},
    "Veg Pulao (1 plate (200 g))": {"calories": 300.0, "carbs": 50.0, "protein": 6.0, "fat": 8.0},
    "Curd Rice (1 bowl (200 g))": {"calories": 220.0, "carbs": 35.0, "protein": 6.0, "fat": 5.0},
    "Lemon Rice (1 bowl (200 g))": {"calories": 250.0, "carbs": 40.0, "protein": 5.0, "fat": 8.0},
    "Khichdi (1 bowl (200 g))": {"calories": 220.0, "carbs": 35.0, "protein": 7.0, "fat": 5.0},
    "Jeera Rice (1 bowl (150 g))": {"calories": 220.0, "carbs": 38.0, "protein": 4.0, "fat": 5.0},
    "Sambar (1 bowl (200 g))": {"calories": 150.0, "carbs": 20.0, "protein": 6.0, "fat": 4.0},
    "Rasam (1 bowl (150 g))": {"calories": 60.0, "carbs": 8.0, "protein": 2.0, "fat": 2.0},
    "Uttapam (1 piece (100 g))": {"calories": 160.0, "carbs": 25.0, "protein": 4.0, "fat": 5.0},
    "Medu Vada (2 pieces (80 g))": {"calories": 180.0, "carbs": 18.0, "protein": 5.0, "fat": 10.0},
    "Appam (1 piece (60 g))": {"calories": 120.0, "carbs": 22.0, "protein": 2.0, "fat": 2.0},
    "Mixed Vegetable Pakora (100 g)": {"calories": 280.0, "carbs": 25.0, "protein": 5.0, "fat": 18.0},
    "Kachori (1 piece (60 g))": {"calories": 220.0, "carbs": 25.0, "protein": 4.0, "fat": 12.0},
    "Dhokla (2 pieces (80 g))": {"calories": 160.0, "carbs": 25.0, "protein": 5.0, "fat": 4.0},
    "Vada Pav (1 piece (120 g))": {"calories": 290.0, "carbs": 40.0, "protein": 7.0, "fat": 11.0},
    "Pav Bhaji (1 plate (250 g))": {"calories": 400.0, "carbs": 50.0, "protein": 8.0, "fat": 18.0},
    "Bhel Puri (1 plate (140 g))": {"calories": 220.0, "carbs": 35.0, "protein": 5.0, "fat": 7.0},
    "Sev Puri (6 pieces (120 g))": {"calories": 280.0, "carbs": 35.0, "protein": 5.0, "fat": 13.0},
    "Aloo Tikki (2 pieces (100 g))": {"calories": 220.0, "carbs": 28.0, "protein": 4.0, "fat": 10.0},
    "Sprouts Salad (Moong) (100 g)": {"calories": 150.0, "carbs": 20.0, "protein": 9.0, "fat": 3.0},
    "Oats (cooked with milk) (1 bowl (200 g))": {"calories": 180.0, "carbs": 28.0, "protein": 7.0, "fat": 4.0},
    "Cornflakes with Milk (1 bowl (150 g))": {"calories": 180.0, "carbs": 32.0, "protein": 5.0, "fat": 3.0},
    "Gulab Jamun (2 pieces (80 g))": {"calories": 300.0, "carbs": 40.0, "protein": 4.0, "fat": 14.0},
    "Jalebi (100 g)": {"calories": 350.0, "carbs": 60.0, "protein": 2.0, "fat": 12.0},
    "Kheer (1 bowl (150 g))": {"calories": 230.0, "carbs": 35.0, "protein": 5.0, "fat": 8.0},
}
INSULIN_TYPES = [
    "No Insulin",
    "Rapid-Acting (e.g., Lispro, Aspart)",
    "Short-Acting (Regular)",
    "Intermediate-Acting (NPH)",
    "Long-Acting (Glargine, Detemir)",
    "Mixed Insulin (70/30)",
]

def calculate_bmi(weight_kg: float, height_cm: float):
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, "N/A"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5: cat = "Underweight"
    elif bmi < 25: cat = "Normal"
    elif bmi < 30: cat = "Overweight"
    else: cat = "Obese"
    return round(bmi, 1), cat

def _smoothstep(edge0: float, edge1: float, x: float) -> float:
    if edge0 == edge1:
        return 0.0 if x < edge0 else 1.0
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

INSULIN_ACTION_PROFILE = {
    "No Insulin": {"onset": 0, "peak": 0, "end": 1},
    "Rapid-Acting (e.g., Lispro, Aspart)": {"onset": 15, "peak": 75, "end": 240},
    "Short-Acting (Regular)": {"onset": 45, "peak": 150, "end": 420},
    "Intermediate-Acting (NPH)": {"onset": 150, "peak": 480, "end": 900},
    "Long-Acting (Glargine, Detemir)": {"onset": 90, "peak": 360, "end": 1380},
    "Mixed Insulin (70/30)": {"onset": 30, "peak": 180, "end": 720},
}
CARB_RESPONSE_PROFILE = {
    "No Diabetes": {"peak": 45, "decay": 90},
    "Prediabetes": {"peak": 50, "decay": 115},
    "Type 2 Diabetes": {"peak": 60, "decay": 130},
    "Type 1 Diabetes": {"peak": 60, "decay": 165},
}

def _cumulative_insulin_fraction(minutes: float, onset: float, peak: float, end: float) -> float:
    if minutes <= onset: return 0.0
    if minutes <= peak: return 0.5 * _smoothstep(onset, peak, minutes)
    if minutes <= end: return 0.5 + 0.5 * _smoothstep(peak, end, minutes)
    return 1.0

def _carb_excursion_fraction(minutes: float, peak: float, decay: float) -> float:
    if minutes <= peak:
        return _smoothstep(0, peak, minutes)
    return 1.0 - _smoothstep(peak, peak + decay, minutes)

def _estimate_bmr(weight_kg: float, age: int = 35, gender: str = "Male") -> float:
    weight_kg = max(weight_kg, 30.0)
    if gender == "Female":
        bmr = 10 * weight_kg + 6.25 * 170 - 5 * age - 161
    else:
        bmr = 10 * weight_kg + 6.25 * 170 - 5 * age + 5
    return max(1200.0, bmr)

def glucose_prediction_model(
    current_glucose: float,
    carbs_g: float,
    diabetes_type: str,
    insulin_type: str,
    insulin_dose: float,
    time_since_injection_hr: float = 0.0,
    weight_kg: float = 70.0,
    age: int = 35,
    gender: str = "Male",
    calories_kcal: float = 0.0,
    time_since_meal_hr: float = 0.0,
    exercise_type: str = "No Exercise",
    exercise_duration_min: float = 0.0,
) -> dict:
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
    HEPATIC_COMP = 0.03

    def _bmr_drop(minutes: float) -> float:
        kcal = bmr_kcal_day * (minutes / 1440)
        grams = (kcal / 4.0) * HEPATIC_COMP
        return (grams * 1000) / glucose_distribution_dl

    exercise_rate = {
        "No Exercise": 0.0,
        "Light (walking, yoga)": 0.30,
        "Moderate (jogging, cycling)": 0.70,
        "Intense (running, gym, sports)": 1.20,
    }.get(exercise_type, 0.0)

    def _exercise_drop(future_min: float) -> float:
        if exercise_duration_min <= 0 or exercise_type == "No Exercise":
            return 0.0
        hours_post = 1.0 + (future_min / 60.0)
        duration_factor = min(exercise_duration_min, 90.0) / 30.0
        afterburn = exercise_rate * 0.30 * duration_factor * (0.5 ** (hours_post / 1.5))
        return afterburn * future_min

    insulin_factor_map = {
        "No Insulin": 0,
        "Rapid-Acting (e.g., Lispro, Aspart)": 45,
        "Short-Acting (Regular)": 35,
        "Intermediate-Acting (NPH)": 25,
        "Long-Acting (Glargine, Detemir)": 20,
        "Mixed Insulin (70/30)": 30,
    }
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

def health_score(glucose: float, bmi: float, diabetes_type: str, predicted_peak: float, carbs: float):
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
    if glucose < 70:
        recs.append("⚠️ Current glucose appears low (hypoglycemia range). Consider consuming fast-acting carbohydrates like juice or glucose tablets immediately.")
    elif glucose > 180:
        recs.append("🔴 Current glucose is elevated. Ensure adequate hydration and consult your healthcare provider about medication adjustments.")
    elif 80 <= glucose <= 120:
        recs.append("✅ Your current glucose reading is within a healthy range. Maintain this with consistent meal timing and activity.")
    if predicted_peak > 200:
        recs.append("📈 Glucose is predicted to rise significantly. A 15–20 minute post-meal walk can reduce peak glucose by up to 30%.")
    elif predicted_peak > 160:
        recs.append("📊 Moderate glucose rise predicted. Monitor closely and consider light physical activity after eating.")
    if diabetes_type == "Type 1 Diabetes":
        recs.append("💉 As a Type 1 diabetic, consistent carb-counting and insulin-to-carb ratio management is essential. Discuss your I:C ratio with your endocrinologist.")
    elif diabetes_type == "Type 2 Diabetes":
        recs.append("🥗 For Type 2 management, reducing refined carbohydrates and increasing dietary fibre can significantly improve glucose control.")
    elif diabetes_type == "Prediabetes":
        recs.append("🌿 Prediabetes can often be reversed with lifestyle changes. Aim for 150 minutes of moderate exercise per week and reduce sugar intake.")
    else:
        recs.append("✅ No diabetes detected. Maintain a balanced diet and active lifestyle to prevent future risk.")
    if bmi_cat == "Obese":
        recs.append("⚖️ BMI indicates obesity, which significantly increases insulin resistance. A 5–10% weight reduction can improve glucose sensitivity meaningfully.")
    elif bmi_cat == "Overweight":
        recs.append("⚖️ Slightly elevated BMI noted. Regular cardiovascular exercise (30 min/day) can help improve metabolic health.")
    elif bmi_cat == "Underweight":
        recs.append("⚖️ BMI indicates underweight status. Adequate caloric intake with balanced nutrition is important for metabolic function.")
    if carbs > 80:
        recs.append("🍽️ High carbohydrate intake detected. Consider splitting this meal into smaller portions and pairing carbs with protein and healthy fats to blunt glucose spikes.")
    elif carbs > 50:
        recs.append("🥦 Moderate carb load. Including non-starchy vegetables can help slow carbohydrate absorption.")
    recs.append("💧 Staying well-hydrated (8–10 glasses of water daily) supports kidney function and glucose regulation.")
    recs.append("😴 Quality sleep (7–9 hours) is crucial for glucose regulation. Poor sleep is linked to increased insulin resistance.")
    return recs[:7]

def generate_pdf_report(*args, **kwargs) -> bytes:
    return b""

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "mbti_answers" not in st.session_state:
    st.session_state.mbti_answers = {}
if "mbti_done" not in st.session_state:
    st.session_state.mbti_done = False
if "mbti_result" not in st.session_state:
    st.session_state.mbti_result = None
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "game_won" not in st.session_state:
    st.session_state.game_won = False
if "player_y" not in st.session_state:
    st.session_state.player_y = 0
if "player_vy" not in st.session_state:
    st.session_state.player_vy = 0
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "game_frame" not in st.session_state:
    st.session_state.game_frame = 0
if "gluco_values" not in st.session_state:
    st.session_state.gluco_values = {}
if "app_page" not in st.session_state:
    st.session_state.app_page = "home"

def login_screen():
    st.markdown("<div class='hero-header'><h1 class='hero-title'>Unified AI Suite</h1><p class='hero-subtitle'>Login to access your website + GlucoVision</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
        if submit:
            if username.strip().lower() == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.caption("Demo login: username = admin, password = 1234")
        st.markdown("</div>", unsafe_allow_html=True)

mbti_questions = [
    {"id": 1, "text": "You feel energized after spending time with many people.", "pole": "E"},
    {"id": 2, "text": "You prefer quiet time alone to recharge.", "pole": "I"},
    {"id": 3, "text": "You focus more on facts and real details than possibilities.", "pole": "S"},
    {"id": 4, "text": "You enjoy thinking about patterns, ideas, and future possibilities.", "pole": "N"},
    {"id": 5, "text": "You usually make decisions based on logic and consistency.", "pole": "T"},
    {"id": 6, "text": "You care deeply about people’s feelings when deciding something.", "pole": "F"},
    {"id": 7, "text": "You like to plan things ahead and follow a schedule.", "pole": "J"},
    {"id": 8, "text": "You prefer flexibility and keeping your options open.", "pole": "P"},
    {"id": 9, "text": "In a group, you often speak up first.", "pole": "E"},
    {"id": 10, "text": "You usually think carefully before sharing your thoughts.", "pole": "I"},
    {"id": 11, "text": "You trust concrete experience more than theory.", "pole": "S"},
    {"id": 12, "text": "You are drawn to abstract ideas and imagination.", "pole": "N"},
    {"id": 13, "text": "You try to be fair and objective in difficult situations.", "pole": "T"},
    {"id": 14, "text": "You often think about how your decisions affect others emotionally.", "pole": "F"},
    {"id": 15, "text": "You like completing tasks early and staying organized.", "pole": "J"},
    {"id": 16, "text": "You are comfortable improvising at the last minute.", "pole": "P"},
]
mbti_options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
mbti_score_map = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}
mbti_desc = {
    "INTJ": "Strategic, independent, and future-focused.",
    "INTP": "Analytical, curious, and idea-driven.",
    "ENTJ": "Decisive, confident, and naturally leadership-oriented.",
    "ENTP": "Inventive, energetic, and quick-thinking.",
    "INFJ": "Insightful, idealistic, and deeply thoughtful.",
    "INFP": "Creative, empathetic, and guided by values.",
    "ENFJ": "Supportive, inspiring, and people-focused.",
    "ENFP": "Enthusiastic, imaginative, and expressive.",
    "ISTJ": "Reliable, structured, and detail-oriented.",
    "ISFJ": "Kind, responsible, and supportive.",
    "ESTJ": "Organized, practical, and efficient.",
    "ESFJ": "Warm, social, and attentive to others.",
    "ISTP": "Logical, calm, and hands-on.",
    "ISFP": "Gentle, adaptable, and artistic.",
    "ESTP": "Bold, practical, and action-oriented.",
    "ESFP": "Outgoing, lively, and spontaneous."
}
def mbti_scores():
    scores = {k: 0 for k in list("EISTNFJP")}
    for q in mbti_questions:
        ans = st.session_state.mbti_answers.get(q["id"], "Neutral")
        scores[q["pole"]] += mbti_score_map[ans]
    return scores
def mbti_type(scores):
    out = []
    for a, b in [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]:
        out.append(a if scores[a] >= scores[b] else b)
    return "".join(out)
def reset_game():
    st.session_state.game_started = False
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.player_y = 0
    st.session_state.player_vy = 0
    st.session_state.obstacles = []
    st.session_state.game_frame = 0
def init_game():
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.player_y = 0
    st.session_state.player_vy = 0
    st.session_state.game_frame = 0
    st.session_state.obstacles = [{"x": 65}, {"x": 110}, {"x": 155}, {"x": 200}, {"x": 245}]
def update_game(jump_pressed):
    gravity = 1
    jump_power = -11
    speed = 2
    player_x = 10
    player_size = 3
    if jump_pressed and st.session_state.player_y == 0:
        st.session_state.player_vy = jump_power
    st.session_state.player_vy += gravity
    st.session_state.player_y += st.session_state.player_vy
    if st.session_state.player_y > 0:
        st.session_state.player_y = 0
        st.session_state.player_vy = 0
    st.session_state.game_frame += 1
    for obs in st.session_state.obstacles:
        obs["x"] -= speed
    st.session_state.obstacles = [o for o in st.session_state.obstacles if o["x"] > -5]
    if st.session_state.obstacles and st.session_state.obstacles[-1]["x"] < 55 and len(st.session_state.obstacles) < 6:
        st.session_state.obstacles.append({"x": st.session_state.obstacles[-1]["x"] + random.randint(25, 35)})
    for obs in st.session_state.obstacles:
        if player_x + player_size > obs["x"] and player_x < obs["x"] + 2 and st.session_state.player_y == 0:
            st.session_state.game_over = True
    if st.session_state.game_frame >= 500:
        st.session_state.game_won = True

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    if bmi < 25: return "Healthy weight"
    if bmi < 30: return "Overweight"
    return "Obesity risk"

def health_ai(height_cm, weight_kg, age, diet, exercise, sleep_hours, water_glasses, fast_food, smoking):
    h = height_cm / 100
    bmi = weight_kg / (h * h)
    cat = bmi_category(bmi)
    risk = 0
    issues, tips = [], []
    if bmi < 18.5:
        risk += 2; issues.append("Low weight-related energy or nutrient deficiency risk."); tips.append("Increase balanced calories, protein, and nutrient-rich foods.")
    elif bmi >= 25:
        risk += 2; issues.append("Weight-related risk may be higher."); tips.append("Focus on balanced meals and regular physical activity.")
    if exercise < 150:
        risk += 2; issues.append("Sedentary lifestyle risk."); tips.append("Try to reach at least 150 minutes of moderate activity per week.")
    if sleep_hours < 7:
        risk += 1; issues.append("Possible fatigue or poor recovery risk."); tips.append("Aim for 7 to 9 hours of sleep.")
    if water_glasses < 6:
        risk += 1; issues.append("Low hydration risk."); tips.append("Drink more water through the day.")
    if diet == "Poor":
        risk += 2; issues.append("Nutrient imbalance risk."); tips.append("Add fruits, vegetables, whole grains, and lean protein.")
    elif diet == "Average":
        risk += 1; tips.append("Improve meal quality with more whole foods.")
    if fast_food >= 4:
        risk += 1; issues.append("High fast-food intake may increase health risk."); tips.append("Reduce fast food and processed snacks.")
    if smoking:
        risk += 3; issues.append("Smoking increases long-term health risk."); tips.append("Stopping smoking can greatly improve health.")
    if age >= 45:
        tips.append("Regular health checkups become more important with age.")
    level = "Low" if risk <= 2 else "Moderate" if risk <= 5 else "Higher"
    return round(bmi, 1), cat, level, issues, tips

def glucose_monitor(current_glucose, carbs_g, bmi, exercise_min, insulin_dose, insulin_type, diabetes_type):
    peak = current_glucose + carbs_g * (3.0 if diabetes_type == "Type 1 Diabetes" else 2.2 if diabetes_type == "Type 2 Diabetes" else 1.6)
    peak -= min(exercise_min * 0.4, 40)
    peak -= insulin_dose * (8 if insulin_type != "No Insulin" else 0)
    peak -= max(0, (bmi - 22) * 0.8)
    pred30 = max(70, round(current_glucose + (peak - current_glucose) * 0.45, 1))
    pred60 = max(70, round(current_glucose + (peak - current_glucose) * 0.70, 1))
    pred90 = max(70, round(current_glucose + (peak - current_glucose) * 0.55, 1))
    pred120 = max(70, round(current_glucose + (peak - current_glucose) * 0.35, 1))
    return {30: pred30, 60: pred60, 90: pred90, 120: pred120}, round(peak, 1)

def credits_page():
    st.title("Special Credits")
    st.markdown("""
<div class='glass-card'>
<h3 style='color:#66FCF1;'>Created For</h3>
<p>This combined project includes your PersonaLens AI website and the GlucoVision-style website in one Streamlit app.</p>
<h3 style='color:#66FCF1;'>Features Included</h3>
<ul>
<li>Login page</li>
<li>MBTI personality test</li>
<li>Mini Geometry Dash-style game</li>
<li>Health AI wellness checker</li>
<li>GlucoVision glucose prediction</li>
</ul>
<h3 style='color:#66FCF1;'>Special Note</h3>
<p>Made with a simple, practical Streamlit structure using session state for smooth page flow.</p>
<p style='margin-top:20px;color:#bfbfbf;'>© 2026 Unified AI Suite</p>
</div>
""", unsafe_allow_html=True)

def app():
    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-title">Unified AI Suite</div>
        <div class="sidebar-logo-sub">PersonaLens + GlucoVision</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📝 MBTI Test", "📊 MBTI Results", "🎮 Game", "🏥 Health AI", "🩺 GlucoVision", "⭐ Special Credits", "🚪 Logout"]
    )

    st.sidebar.write("---")
    if st.sidebar.button("Reset All"):
        st.session_state.mbti_answers = {}
        st.session_state.mbti_done = False
        st.session_state.mbti_result = None
        reset_game()
        st.session_state.gluco_values = {}
        st.rerun()

    if page == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    if page == "🏠 Home":
        st.markdown("<div class='hero-header'><h1 class='hero-title'>Unified AI Suite</h1><p class='hero-subtitle'>MBTI + Game + Health AI + GlucoVision</p></div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown("<div class='metric-card'><div class='metric-value'>MBTI</div><div class='metric-label'>Personality</div></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'><div class='metric-value'>GAME</div><div class='metric-label'>Mini Game</div></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-card'><div class='metric-value'>HEALTH</div><div class='metric-label'>Wellness AI</div></div>", unsafe_allow_html=True)
        with c4: st.markdown("<div class='metric-card'><div class='metric-value'>GLUCO</div><div class='metric-label'>Glucose AI</div></div>", unsafe_allow_html=True)
        st.info("Use the sidebar to open any section.")
    elif page == "📝 MBTI Test":
        st.title("MBTI Personality Test")
        with st.form("mbti_form"):
            for q in mbti_questions:
                st.session_state.mbti_answers[q["id"]] = st.radio(f"Q{q['id']}. {q['text']}", mbti_options, index=2, key=f"m_{q['id']}")
                st.write("")
            submitted = st.form_submit_button("Generate MBTI Result")
        if submitted:
            scores = mbti_scores()
            result = mbti_type(scores)
            st.session_state.mbti_done = True
            st.session_state.mbti_result = {"type": result, "scores": scores}
            st.success("MBTI result generated.")
    elif page == "📊 MBTI Results":
        st.title("Your MBTI Report")
        if not st.session_state.mbti_done or st.session_state.mbti_result is None:
            st.warning("Complete the MBTI test first.")
        else:
            result = st.session_state.mbti_result["type"]
            scores = st.session_state.mbti_result["scores"]
            st.markdown(f"<div class='metric-card'><h1 style='color:#66FCF1;text-align:center;'>{result}</h1><p style='text-align:center;color:#e0e0e0;font-size:18px;'>{mbti_desc.get(result, 'Balanced personality.')}</p></div>", unsafe_allow_html=True)
            st.write("")
            for a, b, label in [("E", "I", "Extraversion / Introversion"), ("S", "N", "Sensing / Intuition"), ("T", "F", "Thinking / Feeling"), ("J", "P", "Judging / Perceiving")]:
                total = scores[a] + scores[b]
                pct = int((scores[a] / total) * 100) if total else 50
                st.write(f"**{label}**")
                st.progress(pct / 100)
                st.caption(f"{a}: {scores[a]} | {b}: {scores[b]}")
    elif page == "🎮 Game":
        st.title("Mini Geometry Dash Game")
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Start Game"):
                init_game()
                st.rerun()
        with c2:
            jump_pressed = st.button("Jump")
        if st.session_state.game_started and not st.session_state.game_over and not st.session_state.game_won:
            update_game(jump_pressed)
        width = 55
        player_line = [" "] * width
        obstacle_line = [" "] * width
        player_line[10] = "🟦"
        for obs in st.session_state.obstacles:
            pos = int(obs["x"])
            if 0 <= pos < width:
                obstacle_line[pos] = "🟥"
                if pos + 1 < width:
                    obstacle_line[pos + 1] = "🟥"
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.code("".join(obstacle_line), language=None)
        st.code("".join(player_line), language=None)
        st.code("▁" * width, language=None)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.session_state.game_over:
            st.error("Game Over. You hit an obstacle.")
        elif st.session_state.game_won:
            st.success("You completed the one-level game!")
            st.balloons()
    elif page == "🏥 Health AI":
        st.title("Health AI Assistant")
        st.write("General wellness estimates only, not a medical diagnosis.")
        with st.form("health_form"):
            c1, c2 = st.columns(2)
            with c1:
                height_cm = st.number_input("Height (cm)", min_value=80, max_value=250, value=170)
                weight_kg = st.number_input("Weight (kg)", min_value=20, max_value=300, value=65)
                age = st.number_input("Age", min_value=5, max_value=120, value=25)
                diet = st.selectbox("Diet quality", ["Good", "Average", "Poor"])
            with c2:
                exercise = st.number_input("Exercise minutes per week", min_value=0, max_value=2000, value=120)
                sleep_hours = st.number_input("Sleep hours per day", min_value=0.0, max_value=16.0, value=7.0, step=0.5)
                water_glasses = st.number_input("Water glasses per day", min_value=0, max_value=20, value=6)
                fast_food = st.number_input("Fast food meals per week", min_value=0, max_value=30, value=2)
            smoking = st.checkbox("Do you smoke?")
            submitted = st.form_submit_button("Analyze Health Pattern")
        if submitted:
            bmi, cat, level, issues, tips = health_ai(height_cm, weight_kg, age, diet, exercise, sleep_hours, water_glasses, fast_food, smoking)
            st.success("Analysis completed.")
            c1, c2, c3 = st.columns(3)
            c1.metric("BMI", f"{bmi:.1f}")
            c2.metric("Weight Category", cat)
            c3.metric("Risk Level", level)
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("Possible Health Concerns")
            if issues:
                for item in issues:
                    st.write("•", item)
            else:
                st.write("No major warning signs from these inputs.")
            st.subheader("AI Suggestions")
            for tip in tips:
                st.write("✅", tip)
            st.markdown("</div>", unsafe_allow_html=True)
    elif page == "🩺 GlucoVision":
        st.title("GlucoVision AI")
        st.write("Educational diabetes monitoring and glucose prediction prototype.")
        with st.form("gluco_form"):
            c1, c2 = st.columns(2)
            with c1:
                current_glucose = st.number_input("Current glucose (mg/dL)", min_value=40.0, max_value=600.0, value=110.0)
                carbs_g = st.number_input("Carbs (g)", min_value=0.0, max_value=500.0, value=45.0)
                diabetes_type = st.selectbox("Diabetes type", ["No Diabetes", "Prediabetes", "Type 2 Diabetes", "Type 1 Diabetes"])
                weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=65.0)
            with c2:
                exercise_min = st.number_input("Exercise minutes", min_value=0.0, max_value=300.0, value=20.0)
                insulin_type = st.selectbox("Insulin type", INSULIN_TYPES)
                insulin_dose = st.number_input("Insulin dose (units)", min_value=0.0, max_value=100.0, value=0.0)
                bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=22.0)
            go = st.form_submit_button("Predict Glucose")
        if go:
            preds = glucose_prediction_model(current_glucose, carbs_g, diabetes_type, insulin_type, insulin_dose, weight_kg=weight_kg)
            peak = max(preds.values())
            score, risk = health_score(current_glucose, bmi, diabetes_type, peak, carbs_g)
            recs = get_recommendations(diabetes_type, current_glucose, peak, bmi, bmi_category(bmi), carbs_g)
            st.session_state.gluco_values = preds
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("30 min", f"{preds[30]} mg/dL")
            c2.metric("60 min", f"{preds[60]} mg/dL")
            c3.metric("90 min", f"{preds[90]} mg/dL")
            c4.metric("120 min", f"{preds[120]} mg/dL")
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.write(f"Predicted peak: **{peak} mg/dL**")
            st.write(f"Health score: **{score}/100**")
            st.write(f"Risk level: **{risk}**")
            st.write("Recommendations:")
            for r in recs:
                st.write("•", r)
            st.markdown("</div>", unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[30, 60, 90, 120], y=[preds[30], preds[60], preds[90], preds[120]], mode="lines+markers"))
            fig.update_layout(template="plotly_dark", height=400, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
    elif page == "⭐ Special Credits":
        credits_page()

if not st.session_state.logged_in:
    login_screen()
else:
    app()
