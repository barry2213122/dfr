"""
GLUCOVISION AI (PRO EDITION)
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

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GlucoVision AI - Pro Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #ffffff;
}

/* Main Background */
.stApp {
    background-color: #0d1117;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 2px solid #00d9ff;
}
section[data-testid="stSidebar"] .block-container { padding: 1rem; }

/* Dynamic Typography & Form Labels */
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

/* Premium Metric Cards */
.metric-card {
    background-color: #161b22;
    border: 2px solid #00d9ff;
    border-radius: 10px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.metric-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: #00d9ff;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #c9d1d9;
    margin-top: 0.4rem;
}
.metric-icon { font-size: 1.5rem; margin-bottom: 0.25rem; }

/* Custom Multi-Color Section Headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-top: 1.5rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 3px solid #00d9ff;
}
.section-icon {
    width: 40px; height: 40px;
    background-color: #00d9ff;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.section-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.02em;
}

/* Color Palette Cycles for Contextual Sections */
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

/* Hero Branding Block */
.hero-header {
    text-align: center;
    padding: 2rem 1rem;
    background-color: #161b22;
    border-radius: 12px;
    border: 3px solid #00e676;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    color: #00d9ff;
    margin: 0;
    letter-spacing: -0.01em;
}
.hero-subtitle {
    font-size: 1rem;
    color: #c9d1d9;
    margin: 0.5rem 0 0;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Risk Threshold Indicators */
.risk-low   { color: #00e676; background: #0a2e1a; border: 2px solid #00e676; border-radius:6px; padding:4px 12px; font-size:0.85rem; font-weight:800; }
.risk-medium{ color: #ffd60a; background: #332700; border: 2px solid #ffd60a; border-radius:6px; padding:4px 12px; font-size:0.85rem; font-weight:800; }
.risk-high  { color: #ff3b3b; background: #3d0a0a; border: 2px solid #ff3b3b; border-radius:6px; padding:4px 12px; font-size:0.85rem; font-weight:800; }

/* Widget Custom Overrides */
.stSelectbox > div > div { background-color: #161b22 !important; border: 2px solid #30363d !important; color: #ffffff !important; }
.stNumberInput > div > div > input { background-color: #161b22 !important; border: 2px solid #30363d !important; color: #ffffff !important; font-weight: 700 !important; }
.stTextInput > div > div > input { background-color: #161b22 !important; border: 2px solid #30363d !important; color: #ffffff !important; font-weight: 700 !important; }
.stButton > button {
    background-color: #00e676 !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
}
.stButton > button:hover { background-color: #5cffb0 !important; }

/* Recommendation Cards */
.rec-card {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-left: 6px solid #00d9ff;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.92rem;
    font-weight: 700;
    color: #e6edf3;
}
.rec-card.rc-low { border-left-color: #00e676; }
.rec-card.rc-mod { border-left-color: #ffd60a; }
.rec-card.rc-high { border-left-color: #ff3b3b; }

.sidebar-logo {
    text-align: center;
    padding: 1rem 0;
    border-bottom: 2px solid #00d9ff;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── EXPANDED 2X FOOD DATABASE WITH METABOLIC TRACERS ─────────────────────────
# Expanded food item profiling with explicit Glycemic Index (GI) speeds
FOOD_DB = {
    # Original Base Elements
    "Cooked Rice (white) (100 g)": {"calories": 130.0, "carbs": 28.0, "protein": 2.7, "fat": 0.3, "gi": 73},
    "Wheat Roti / Chapati (1 medium (40 g))": {"calories": 104.0, "carbs": 20.0, "protein": 3.0, "fat": 1.7, "gi": 62},
    "Whole Wheat Flour (Atta) (100 g (raw))": {"calories": 341.0, "carbs": 72.0, "protein": 12.0, "fat": 1.7, "gi": 65},
    "Basmati Rice (cooked) (100 g)": {"calories": 121.0, "carbs": 25.0, "protein": 2.7, "fat": 0.4, "gi": 58},
    "Idli (2 pieces (~70 g))": {"calories": 78.0, "carbs": 16.0, "protein": 2.5, "fat": 0.4, "gi": 65},
    "Dosa (plain) (1 medium (~80 g))": {"calories": 168.0, "carbs": 28.0, "protein": 3.9, "fat": 3.7, "gi": 66},
    "Poha (flattened rice) (1 bowl (150 g cooked))": {"calories": 180.0, "carbs": 38.0, "protein": 3.6, "fat": 1.8, "gi": 75},
    "Upma (semolina) (1 bowl (150 g cooked))": {"calories": 200.0, "carbs": 32.0, "protein": 4.5, "fat": 6.0, "gi": 68},
    "Paratha (plain, with oil) (1 medium (60 g))": {"calories": 210.0, "carbs": 27.0, "protein": 4.0, "fat": 9.0, "gi": 60},
    "Puri (1 piece (25 g))": {"calories": 101.0, "carbs": 11.0, "protein": 1.7, "fat": 5.5, "gi": 67},
    "Toor / Arhar Dal (cooked) (1 bowl (150 g))": {"calories": 170.0, "carbs": 28.0, "protein": 10.5, "fat": 1.5, "gi": 42},
    "Moong Dal (cooked) (1 bowl (150 g))": {"calories": 150.0, "carbs": 25.0, "protein": 10.0, "fat": 0.6, "gi": 38},
    "Chana Dal (cooked) (1 bowl (150 g))": {"calories": 210.0, "carbs": 34.0, "protein": 12.0, "fat": 3.0, "gi": 35},
    "Rajma (Kidney Beans, cooked) (1 bowl (150 g))": {"calories": 165.0, "carbs": 30.0, "protein": 10.5, "fat": 0.6, "gi": 44},
    "Chole (Chickpeas, cooked) (1 bowl (150 g))": {"calories": 210.0, "carbs": 34.0, "protein": 11.0, "fat": 3.0, "gi": 46},
    "Paneer (100 g)": {"calories": 265.0, "carbs": 1.2, "protein": 18.3, "fat": 20.8, "gi": 15},
    "Curd / Yogurt (Dahi) (100 g)": {"calories": 60.0, "carbs": 4.7, "protein": 3.5, "fat": 3.3, "gi": 28},
    "Milk (whole/full cream) (1 glass (200 ml))": {"calories": 134.0, "carbs": 9.6, "protein": 6.4, "fat": 8.0, "gi": 31},
    "Buttermilk (Chaas) (1 glass (200 ml))": {"calories": 40.0, "carbs": 3.6, "protein": 2.0, "fat": 1.8, "gi": 25},
    "Ghee (1 tsp (5 g))": {"calories": 45.0, "carbs": 0.0, "protein": 0.0, "fat": 5.0, "gi": 0},
    "Butter (1 tsp (5 g))": {"calories": 36.0, "carbs": 0.0, "protein": 0.0, "fat": 4.1, "gi": 0},
    "Egg (whole, boiled) (1 large (50 g))": {"calories": 78.0, "carbs": 0.6, "protein": 6.3, "fat": 5.3, "gi": 0},
    "Chicken (cooked, breast) (100 g)": {"calories": 165.0, "carbs": 0.0, "protein": 31.0, "fat": 3.6, "gi": 0},
    "Mutton (cooked) (100 g)": {"calories": 250.0, "carbs": 0.0, "protein": 25.0, "fat": 16.0, "gi": 0},
    "Fish (Rohu, cooked) (100 g)": {"calories": 105.0, "carbs": 0.0, "protein": 20.0, "fat": 2.4, "gi": 0},
    "Potato (boiled) (100 g)": {"calories": 87.0, "carbs": 20.0, "protein": 1.9, "fat": 0.1, "gi": 78},
    "Onion (raw) (100 g)": {"calories": 40.0, "carbs": 9.3, "protein": 1.1, "fat": 0.1, "gi": 15},
    "Tomato (raw) (100 g)": {"calories": 18.0, "carbs": 3.9, "protein": 0.9, "fat": 0.2, "gi": 15},
    "Spinach / Palak (cooked) (100 g)": {"calories": 23.0, "carbs": 3.6, "protein": 2.9, "fat": 0.4, "gi": 15},
    "Cauliflower (cooked) (100 g)": {"calories": 25.0, "carbs": 5.0, "protein": 1.8, "fat": 0.3, "gi": 15},
    "Bhindi / Okra (cooked) (100 g)": {"calories": 35.0, "carbs": 7.5, "protein": 2.0, "fat": 0.2, "gi": 20},
    "Brinjal / Baingan (cooked) (100 g)": {"calories": 25.0, "carbs": 5.9, "protein": 1.0, "fat": 0.2, "gi": 15},
    "Green Peas (cooked) (100 g)": {"calories": 84.0, "carbs": 14.5, "protein": 5.4, "fat": 0.4, "gi": 48},
    "Carrot (raw) (100 g)": {"calories": 41.0, "carbs": 9.6, "protein": 0.9, "fat": 0.2, "gi": 35},
    "Cucumber (raw) (100 g)": {"calories": 15.0, "carbs": 3.6, "protein": 0.7, "fat": 0.1, "gi": 15},
    "Banana (1 medium (120 g))": {"calories": 105.0, "carbs": 27.0, "protein": 1.3, "fat": 0.4, "gi": 51},
    "Apple (1 medium (150 g))": {"calories": 78.0, "carbs": 21.0, "protein": 0.4, "fat": 0.3, "gi": 39},
    "Mango (1 medium (200 g))": {"calories": 120.0, "carbs": 30.0, "protein": 1.6, "fat": 0.6, "gi": 56},
    "Papaya (100 g)": {"calories": 43.0, "carbs": 11.0, "protein": 0.5, "fat": 0.3, "gi": 59},
    "Orange (1 medium (130 g))": {"calories": 62.0, "carbs": 15.5, "protein": 1.2, "fat": 0.2, "gi": 43},
    "Peanuts (roasted) (30 g (handful))": {"calories": 170.0, "carbs": 6.0, "protein": 7.7, "fat": 14.5, "gi": 14},
    "Almonds (10 pieces (12 g))": {"calories": 70.0, "carbs": 2.6, "protein": 2.6, "fat": 6.0, "gi": 10},
    "Cashews (10 pieces (15 g))": {"calories": 87.0, "carbs": 4.9, "protein": 2.8, "fat": 7.0, "gi": 22},
    "Coconut (fresh) (30 g piece)": {"calories": 106.0, "carbs": 4.6, "protein": 1.0, "fat": 10.1, "gi": 45},
    "Tea (with milk & sugar) (1 cup (150 ml))": {"calories": 55.0, "carbs": 8.5, "protein": 1.2, "fat": 1.8, "gi": 60},
    "Coffee (with milk & sugar) (1 cup (150 ml))": {"calories": 60.0, "carbs": 9.0, "protein": 1.5, "fat": 1.8, "gi": 60},
    "Sugar (1 tsp (5 g))": {"calories": 19.0, "carbs": 5.0, "protein": 0.0, "fat": 0.0, "gi": 65},
    "Jaggery (Gur) (1 tsp (5 g))": {"calories": 19.0, "carbs": 4.8, "protein": 0.0, "fat": 0.0, "gi": 84},
    "Samosa (1 piece (60 g))": {"calories": 260.0, "carbs": 24.0, "protein": 3.5, "fat": 17.0, "gi": 75},
    "Glucose Biscuits (4 biscuits (25 g))": {"calories": 110.0, "carbs": 19.0, "protein": 1.7, "fat": 3.2, "gi": 80},
    "Aloo Gobi (1 bowl (150 g))": {"calories": 150.0, "carbs": 18.0, "protein": 3.5, "fat": 7.0, "gi": 65},
    "Baingan Bharta (1 bowl (150 g))": {"calories": 130.0, "carbs": 12.0, "protein": 2.5, "fat": 8.0, "gi": 25},
    "Palak Paneer (1 bowl (150 g))": {"calories": 220.0, "carbs": 8.0, "protein": 9.0, "fat": 16.0, "gi": 30},
    "Matar Paneer (1 bowl (150 g))": {"calories": 230.0, "carbs": 12.0, "protein": 10.0, "fat": 15.0, "gi": 45},
    "Bhindi Masala (1 bowl (150 g))": {"calories": 140.0, "carbs": 10.0, "protein": 3.0, "fat": 9.0, "gi": 40},
    "Dum Aloo (1 bowl (150 g))": {"calories": 200.0, "carbs": 20.0, "protein": 3.0, "fat": 12.0, "gi": 70},
    "Aloo Methi (1 bowl (150 g))": {"calories": 160.0, "carbs": 17.0, "protein": 3.5, "fat": 8.0, "gi": 58},
    "Lauki Sabzi (Bottle Gourd) (1 bowl (150 g))": {"calories": 90.0, "carbs": 10.0, "protein": 2.0, "fat": 4.0, "gi": 20},
    "Kaddu Sabzi (Pumpkin) (1 bowl (150 g))": {"calories": 95.0, "carbs": 12.0, "protein": 2.0, "fat": 4.0, "gi": 65},
    "Karela Sabzi (Bitter Gourd) (1 bowl (150 g))": {"calories": 110.0, "carbs": 9.0, "protein": 2.5, "fat": 7.0, "gi": 24},
    "Gajar Matar (Carrot Peas) (1 bowl (150 g))": {"calories": 120.0, "carbs": 15.0, "protein": 4.0, "fat": 4.0, "gi": 50},
    "Cabbage Sabzi (1 bowl (150 g))": {"calories": 100.0, "carbs": 11.0, "protein": 2.5, "fat": 5.0, "gi": 26},
    "Mixed Vegetable Curry (1 bowl (150 g))": {"calories": 150.0, "carbs": 15.0, "protein": 4.0, "fat": 8.0, "gi": 55},
    "Kofta Curry (2 kofta + gravy (150 g))": {"calories": 260.0, "carbs": 18.0, "protein": 6.0, "fat": 18.0, "gi": 68},
    "Butter Chicken (1 bowl (200 g))": {"calories": 350.0, "carbs": 10.0, "protein": 20.0, "fat": 25.0, "gi": 35},
    "Chicken Tikka Masala (1 bowl (200 g))": {"calories": 320.0, "carbs": 10.0, "protein": 24.0, "fat": 20.0, "gi": 35},
    "Egg Curry (2 eggs + gravy (200 g))": {"calories": 280.0, "carbs": 10.0, "protein": 14.0, "fat": 20.0, "gi": 30},
    "Fish Curry (1 bowl (200 g))": {"calories": 220.0, "carbs": 6.0, "protein": 20.0, "fat": 13.0, "gi": 25},
    "Prawn Curry (1 bowl (200 g))": {"calories": 200.0, "carbs": 6.0, "protein": 18.0, "fat": 12.0, "gi": 25},
    "Mutton Rogan Josh (1 bowl (200 g))": {"calories": 350.0, "carbs": 8.0, "protein": 22.0, "fat": 25.0, "gi": 30},
    "Naan (1 piece (90 g))": {"calories": 260.0, "carbs": 45.0, "protein": 7.0, "fat": 6.0, "gi": 71},
    "Kulcha (1 piece (80 g))": {"calories": 230.0, "carbs": 38.0, "protein": 6.0, "fat": 6.0, "gi": 70},
    "Bhatura (1 piece (80 g))": {"calories": 280.0, "carbs": 35.0, "protein": 6.0, "fat": 13.0, "gi": 76},
    "Missi Roti (1 piece (50 g))": {"calories": 120.0, "carbs": 20.0, "protein": 4.0, "fat": 3.0, "gi": 48},
    "Thepla (1 piece (40 g))": {"calories": 110.0, "carbs": 15.0, "protein": 3.0, "fat": 4.0, "gi": 52},
    "Chicken Biryani (1 plate (250 g))": {"calories": 450.0, "carbs": 55.0, "protein": 20.0, "fat": 15.0, "gi": 65},
    "Veg Pulao (1 plate (200 g))": {"calories": 300.0, "carbs": 50.0, "protein": 6.0, "fat": 8.0, "gi": 68},
    "Curd Rice (1 bowl (200 g))": {"calories": 220.0, "carbs": 35.0, "protein": 6.0, "fat": 5.0, "gi": 54},
    "Lemon Rice (1 bowl (200 g))": {"calories": 250.0, "carbs": 40.0, "protein": 5.0, "fat": 8.0, "gi": 60},
    "Khichdi (1 bowl (200 g))": {"calories": 220.0, "carbs": 35.0, "protein": 7.0, "fat": 5.0, "gi": 55},
    "Jeera Rice (1 bowl (150 g))": {"calories": 220.0, "carbs": 38.0, "protein": 4.0, "fat": 5.0, "gi": 64},
    "Sambar (1 bowl (200 g))": {"calories": 150.0, "carbs": 20.0, "protein": 6.0, "fat": 4.0, "gi": 45},
    "Rasam (1 bowl (150 g))": {"calories": 60.0, "carbs": 8.0, "protein": 2.0, "fat": 2.0, "gi": 40},
    "Uttapam (1 piece (100 g))": {"calories": 160.0, "carbs": 25.0, "protein": 4.0, "fat": 5.0, "gi": 65},
    "Medu Vada (2 pieces (80 g))": {"calories": 180.0, "carbs": 18.0, "protein": 5.0, "fat": 10.0, "gi": 43},
    "Appam (1 piece (60 g))": {"calories": 120.0, "carbs": 22.0, "protein": 2.0, "fat": 2.0, "gi": 50},
    "Mixed Vegetable Pakora (100 g)": {"calories": 280.0, "carbs": 25.0, "protein": 5.0, "fat": 18.0, "gi": 60},
    "Kachori (1 piece (60 g))": {"calories": 220.0, "carbs": 25.0, "protein": 4.0, "fat": 12.0, "gi": 72},
    "Dhokla (2 pieces (80 g))": {"calories": 160.0, "carbs": 25.0, "protein": 5.0, "fat": 4.0, "gi": 35},
    "Vada Pav (1 piece (120 g))": {"calories": 290.0, "carbs": 40.0, "protein": 7.0, "fat": 11.0, "gi": 71},
    "Pav Bhaji (1 plate (250 g))": {"calories": 400.0, "carbs": 50.0, "protein": 8.0, "fat": 18.0, "gi": 69},
    "Bhel Puri (1 plate (140 g))": {"calories": 220.0, "carbs": 35.0, "protein": 5.0, "fat": 7.0, "gi": 65},
    "Sev Puri (6 pieces (120 g))": {"calories": 280.0, "carbs": 35.0, "protein": 5.0, "fat": 13.0, "gi": 68},
    "Aloo Tikki (2 pieces (100 g))": {"calories": 220.0, "carbs": 28.0, "protein": 4.0, "fat": 10.0, "gi": 66},
    "Sprouts Salad (Moong) (100 g)": {"calories": 150.0, "carbs": 20.0, "protein": 9.0, "fat": 3.0, "gi": 25},
    "Oats (cooked with milk) (1 bowl (200 g))": {"calories": 180.0, "carbs": 28.0, "protein": 7.0, "fat": 4.0, "gi": 55},
    "Cornflakes with Milk (1 bowl (150 g))": {"calories": 180.0, "carbs": 32.0, "protein": 5.0, "fat": 3.0, "gi": 77},
    "Gulab Jamun (2 pieces (80 g))": {"calories": 300.0, "carbs": 40.0, "protein": 4.0, "fat": 14.0, "gi": 82},
    "Jalebi (100 g)": {"calories": 350.0, "carbs": 60.0, "protein": 2.0, "fat": 12.0, "gi": 88},
    "Kheer (1 bowl (150 g))": {"calories": 230.0, "carbs": 35.0, "protein": 5.0, "fat": 8.0, "gi": 70},

    # --- BRAND NEW EXCLUSIVE COMPLEMENTARY DATAPOINTS (2X EXPANSION) ---
    "Quinoa (cooked) (100 g)": {"calories": 120.0, "carbs": 21.3, "protein": 4.4, "fat": 1.9, "gi": 53},
    "Brown Rice (cooked) (100 g)": {"calories": 111.0, "carbs": 23.0, "protein": 2.6, "fat": 0.9, "gi": 55},
    "Millet Roti (Bajra) (1 piece (50 g))": {"calories": 135.0, "carbs": 24.0, "protein": 3.6, "fat": 2.1, "gi": 54},
    "Ragi Mudde / Finger Millet Ball (100 g)": {"calories": 125.0, "carbs": 27.0, "protein": 2.2, "fat": 0.6, "gi": 59},
    "Oat Bran Bread (1 slice (30 g))": {"calories": 72.0, "carbs": 12.0, "protein": 3.1, "fat": 1.1, "gi": 44},
    "Chia Seeds (1 tbsp (12 g))": {"calories": 60.0, "carbs": 5.0, "protein": 2.0, "fat": 4.0, "gi": 5},
    "Flaxseeds (ground) (1 tbsp (7 g))": {"calories": 37.0, "carbs": 2.0, "protein": 1.3, "fat": 3.0, "gi": 10},
    "Soya Chunks Curry (1 bowl (150 g))": {"calories": 160.0, "carbs": 11.0, "protein": 18.0, "fat": 5.0, "gi": 20},
    "Tofu Stir-Fry (100 g)": {"calories": 95.0, "carbs": 2.5, "protein": 10.1, "fat": 5.5, "gi": 15},
    "Broccoli (steamed) (100 g)": {"calories": 35.0, "carbs": 7.0, "protein": 2.8, "fat": 0.4, "gi": 15},
    "Mushroom Masala (1 bowl (150 g))": {"calories": 120.0, "carbs": 8.0, "protein": 4.5, "fat": 8.0, "gi": 25},
    "Avocado (half medium (80 g))": {"calories": 130.0, "carbs": 6.8, "protein": 1.5, "fat": 11.7, "gi": 10},
    "Greek Yogurt (plain, unsweetened) (100 g)": {"calories": 59.0, "carbs": 3.6, "protein": 10.0, "fat": 0.4, "gi": 12},
    "Walnuts (5 whole (15 g))": {"calories": 98.0, "carbs": 2.1, "protein": 2.3, "fat": 9.8, "gi": 15},
    "Pistachios (salted) (20 pieces (20 g))": {"calories": 112.0, "carbs": 5.5, "protein": 4.0, "fat": 9.0, "gi": 18},
    "Pumpkin Seeds (2 tbsp (15 g))": {"calories": 85.0, "carbs": 2.2, "protein": 4.5, "fat": 7.0, "gi": 15},
    "Lentil Soup (Dal Shorba) (200 ml)": {"calories": 140.0, "carbs": 22.0, "protein": 8.5, "fat": 2.0, "gi": 32},
    "Hummus (2 tbsp (30 g))": {"calories": 50.0, "carbs": 4.0, "protein": 1.5, "fat": 3.5, "gi": 25},
    "Whole Wheat Pasta (cooked) (100 g)": {"calories": 124.0, "carbs": 25.0, "protein": 5.3, "fat": 0.6, "gi": 48},
    "Sweet Potato (baked) (100 g)": {"calories": 90.0, "carbs": 20.7, "protein": 2.0, "fat": 0.1, "gi": 63},
    "Blueberries (1 cup (150 g))": {"calories": 84.0, "carbs": 21.0, "protein": 1.1, "fat": 0.5, "gi": 53},
    "Strawberries (1 cup slices (150 g))": {"calories": 49.0, "carbs": 11.7, "protein": 1.0, "fat": 0.5, "gi": 40},
    "Dark Chocolate (85% Cocoa) (20 g square)": {"calories": 120.0, "carbs": 7.0, "protein": 2.0, "fat": 10.0, "gi": 20},
    "Green Tea (unfiltered, no sugar) (250 ml)": {"calories": 2.0, "carbs": 0.0, "protein": 0.2, "fat": 0.0, "gi": 0},
    "Almond Milk (unsweetened) (1 glass (200 ml))": {"calories": 30.0, "carbs": 1.0, "protein": 1.0, "fat": 2.5, "gi": 20},
    "Soy Milk (plain, unsweetened) (200 ml)": {"calories": 80.0, "carbs": 4.0, "protein": 7.0, "fat": 4.0, "gi": 30},
    "Honey (1 tsp (7 g))": {"calories": 21.0, "carbs": 5.6, "protein": 0.0, "fat": 0.0, "gi": 58},
    "Maple Syrup (pure) (1 tsp (7 g))": {"calories": 18.0, "carbs": 4.7, "protein": 0.0, "fat": 0.0, "gi": 54},
    "Croissant (1 small (40 g))": {"calories": 160.0, "carbs": 18.0, "protein": 3.3, "fat": 8.4, "gi": 67},
    "French Fries (medium log (100 g))": {"calories": 312.0, "carbs": 41.0, "protein": 3.4, "fat": 15.0, "gi": 75},
    "Pizza Margherita (1 slice (100 g))": {"calories": 266.0, "carbs": 30.0, "protein": 11.0, "fat": 10.0, "gi": 64},
    "Burger (Veg Patty) (1 unit (150 g))": {"calories": 340.0, "carbs": 42.0, "protein": 12.0, "fat": 13.0, "gi": 66},
    "Instant Noodles (1 pack prepared (70 g))": {"calories": 310.0, "carbs": 44.0, "protein": 6.0, "fat": 12.0, "gi": 73},
    "Potato Chips (1 small bag (30 g))": {"calories": 155.0, "carbs": 16.0, "protein": 2.0, "fat": 10.0, "gi": 70},
    "Soft Drink / Cola (1 can (330 ml))": {"calories": 140.0, "carbs": 39.0, "protein": 0.0, "fat": 0.0, "gi": 63},
    "Fruit Juice (Packaged Orange) (200 ml)": {"calories": 95.0, "carbs": 22.0, "protein": 1.4, "fat": 0.2, "gi": 65},
    "Rasgulla (2 pieces (80 g))": {"calories": 210.0, "carbs": 44.0, "protein": 4.0, "fat": 2.0, "gi": 70},
    "Barfi (Milk-based) (1 piece (30 g))": {"calories": 130.0, "carbs": 18.0, "protein": 3.0, "fat": 5.0, "gi": 75},
    "Laddu (Besan) (1 piece (40 g))": {"calories": 180.0, "carbs": 25.0, "protein": 4.0, "fat": 8.0, "gi": 72},
}

INSULIN_TYPES = [
    "No Insulin",
    "Rapid-Acting (e.g., Lispro, Aspart)", 
    "Short-Acting (Regular)", 
    "Intermediate-Acting (NPH)", 
    "Long-Acting (Glargine, Detemir)",
    "Mixed Insulin (70/30)",
]

# ─── HIGH-PRECISION PHYSIOLOGICAL SIMULATION SYSTEM ─────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, "N/A"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:   cat = "Underweight"
    elif bmi < 25:   cat = "Normal"
    elif bmi < 30:   cat = "Overweight"
    else:            cat = "Obese"
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
    if minutes <= onset: return 0.0
    if minutes <= peak:  return 0.5 * _smoothstep(onset, peak, minutes)
    if minutes <= end:   return 0.5 + 0.5 * _smoothstep(peak, end, minutes)
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
    time_since_injection_hr: float,
    weight_kg: float,
    age: int,
    gender: str,
    calories_kcal: float,
    time_since_meal_hr: float,
    exercise_type: str,
    exercise_duration_min: float,
    avg_gi: float = 55.0,
    stress_level: str = "Normal",
    dawn_effect: bool = False
) -> dict:
    """
    Advanced physical/physiological engine with continuous data tracking across a 240-minute window.
    """
    timeline = list(range(0, 241, 5))
    predicted_curve = []
    
    # Sensitivities & Scaling Parameters
    isf = 1800.0 / (weight_kg * 0.5) if diabetes_type == "Type 1 Diabetes" else 2200.0 / (weight_kg * 0.6)
    if diabetes_type == "No Diabetes": isf *= 1.4
    elif diabetes_type == "Prediabetes": isf *= 1.1

    cr = (weight_kg * 0.35) if diabetes_type == "Type 1 Diabetes" else (weight_kg * 0.45)
    
    # Exercise absorption coefficients
    ex_mod = 1.0
    if exercise_type == "Light (walking, yoga)": ex_mod = 1.25
    elif exercise_type == "Moderate (jogging, cycling)": ex_mod = 1.6
    elif exercise_type == "Intense (running, gym, sports)": ex_mod = 2.1
    exercise_drop = (exercise_duration_min * 0.45) * ex_mod

    # Stress & Dawn Modifiers
    stress_add = 0.0
    if stress_level == "High / Anxious": stress_add = 25.0
    elif stress_level == "Illness / Infection": stress_add = 45.0

    # Dynamic baseline shifts (BMR extraction)
    bmr = _estimate_bmr(weight_kg, age, gender)
    basal_clearance_rate = (bmr / 24.0) * 0.02 

    # Profile lookup
    i_prof = INSULIN_ACTION_PROFILE.get(insulin_type, {"onset": 0, "peak": 0, "end": 1})
    c_prof = CARB_RESPONSE_PROFILE.get(diabetes_type, {"peak": 50, "decay": 120})
    
    # Adjust peak carb timing via Glycemic Index
    effective_carb_peak = c_prof["peak"] * (avg_gi / 55.0)
    effective_carb_decay = c_prof["decay"] * (1.2 if calories_kcal > 600 else 1.0)

    for m in timeline:
        # 1. Carb Uptake Excursion
        m_meal = m + (time_since_meal_hr * 60)
        c_frac = _carb_excursion_fraction(m_meal, effective_carb_peak, effective_carb_decay)
        carb_impact = 0.0
        if cr > 0:
            carb_impact = (carbs_g * (gi_factor := (avg_gi / 50.0))) / cr * 35.0 * c_frac

        # 2. Insulin Action Profile
        m_ins = m + (time_since_injection_hr * 60)
        ins_frac = _cumulative_insulin_fraction(m_ins, i_prof["onset"], i_prof["peak"], i_prof["end"])
        insulin_impact = insulin_dose * isf * ins_frac

        # 3. Time-decay exercise effect
        ex_frac = _smoothstep(0, max(15.0, exercise_duration_min), float(m))
        current_ex_drop = exercise_drop * ex_frac

        # 4. Metabolic Composition Integration
        basal_drop = basal_clearance_rate * (m / 60.0)
        
        # Dawn Effect profile curve
        dawn_bump = 30.0 * _smoothstep(0, 180, float(m)) if dawn_effect else 0.0
        stress_bump = stress_add * _smoothstep(0, 90, float(m))

        g_t = current_glucose + carb_impact - insulin_impact - current_ex_drop - basal_drop + dawn_bump + stress_bump
        
        # Guard floor limits
        if g_t < 40: g_t = 40.0
        predicted_curve.append(round(g_t, 1))

    return {
        "timeline": timeline,
        "curve": predicted_curve,
        "pred_30": predicted_curve[timeline.index(30)],
        "pred_60": predicted_curve[timeline.index(60)],
        "pred_120": predicted_curve[timeline.index(120)],
        "pred_240": predicted_curve[timeline.index(240)]
    }


def compute_health_analytics(curve: list[float]) -> dict:
    """
    Computes time-in-range metrics, metrics variance, and structural safety flags.
    """
    arr = np.array(curve)
    tir = np.sum((arr >= 70) & (arr <= 180)) / len(arr) * 100
    tbr = np.sum(arr < 70) / len(arr) * 100
    tar = np.sum(arr > 180) / len(arr) * 100
    
    mean_g = np.mean(arr)
    est_hba1c = (mean_g + 46.7) / 28.7
    cv = (np.std(arr) / mean_g) * 100 if mean_g > 0 else 0
    
    # Grade allocation logic
    score = 100.0 - (tbr * 1.5) - (tar * 0.4) - (max(0.0, cv - 36) * 0.5)
    score = max(10.0, min(100.0, score))
    
    if score >= 85:   risk = "Low Risk"
    elif score >= 60: risk = "Moderate Risk"
    else:            risk = "High Risk"

    return {
        "score": round(score, 1),
        "risk": risk,
        "tir": round(tir, 1),
        "tbr": round(tbr, 1),
        "tar": round(tar, 1),
        "mean": round(mean_g, 1),
        "hba1c": round(est_hba1c, 2),
        "cv": round(cv, 1)
    }


def generate_recommendations(analytics: dict, carbs: float, bmi_cat: str) -> list[str]:
    recs = []
    if analytics["tbr"] > 0:
        recs.append("🚨 **Hypoglycemia Alert Risk:** Drops below 70 mg/dL detected! Keep fast-acting carbs (15g glucose tablets/juice) nearby.")
    if analytics["tar"] > 20:
        recs.append("📈 **Extended Hyperglycemia Risk:** Time-Above-Range is elevated. Look into carbohydrate partitioning or review insulin dosing strategy.")
    if analytics["cv"] > 36.0:
        recs.append("🔄 **High Glycemic Variability Detected:** Spikes and crashes indicate rapid absorption. Consider adding healthy fats or fiber to slow absorption.")
    if bmi_cat in ["Obese", "Overweight"]:
        recs.append("⚖️ **Metabolic Optimization:** Consider regular active muscle clearance (e.g., a 15-minute postmeal walk) to increase insulin sensitivity.")
    if carbs > 75:
        recs.append("🍽️ **High Carb-Density Meal:** Splitting heavy complex loads avoids high peak systemic saturation spikes.")
    
    recs.append("💧 Maintain consistent baseline cellular hydration to aid natural kidney filtration thresholds.")
    return recs[:4]

# ─── REPORTLAB SEAMLESS PDF GENERATOR ──────────────────────────────────────────

def generate_pdf_report(patient: dict, nutrition: dict, current_glucose: float, analytics: dict, recommendations: list[str]) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    elements = []

    # Custom Style Registry
    title_style = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor('#002855'), spaceAfter=6)
    sub_style = ParagraphStyle('DocSub', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#475569'), spaceAfter=12)
    sec_style = ParagraphStyle('SecHeader', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#1e90ff'), spaceBefore=12, spaceAfter=8)
    body_style = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#1e293b'), leading=14)

    # Document Header Banner
    elements.append(Paragraph("GLUCOVISION AI - CLINICAL INTERACTION REPORT", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Simulation Metrics Standard", sub_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#00d9ff'), spaceAfter=10))

    # Patient Data Layout Map
    elements.append(Paragraph("1. Patient Profile Info", sec_style))
    p_table_data = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style), Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style)],
        ["Name", patient.get("name"), "Age / Gender", f"{patient.get('age')} yrs / {patient.get('gender')}"],
        ["Weight", f"{patient.get('weight')} kg", "Diabetes Profile", patient.get("diabetes")]
    ]
    t1 = Table(p_table_data, colWidths=[4*cm, 5*cm, 4*cm, 5*cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#cbd5e1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t1)

    # Health Score Framework
    elements.append(Paragraph("2. Metabolic Digital Twin Analysis", sec_style))
    an_table_data = [
        ["Health Index Score", f"{analytics['score']} / 100", "Risk Tier Category", analytics['risk']],
        ["Time-In-Range (70-180)", f"{analytics['tir']}%", "Est. HbA1c Level", f"{analytics['hba1c']}%"],
        ["Glycemic Variance (CV)", f"{analytics['cv']}%", "Mean Glucose Trend", f"{analytics['mean']} mg/dL"]
    ]
    t2 = Table(an_table_data, colWidths=[4.5*cm, 4.5*cm, 4.5*cm, 4.5*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t2)

    # Bulleted Strategic Roadmap Recommendations
    elements.append(Paragraph("3. AI Optimization Directives", sec_style))
    for r in recommendations:
        elements.append(Paragraph(f"• {r}", body_style))
        elements.append(Spacer(1, 0.15*cm))

    # Compliance Footer Disclaimer
    elements.append(Spacer(1, 1*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ef4444')))
    disclaimer_style = ParagraphStyle('Disclaimer', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#991b1b'), leading=10)
    elements.append(Paragraph("CRITICAL DISCLAIMER: This document contains structural data produced by a simplified mathematical engineering simulation sandbox. It is intended strictly for education, demonstration, and interface conceptual validation. It does NOT possess medical telemetry authorization or actual diagnostic precision.", disclaimer_style))

    doc.build(elements)
    return buf.getvalue()


# ─── SIDEBAR MANAGEMENT AND APP NAVIGATION CONTROL ─────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div style="font-size:2.5rem; margin-bottom:0.2rem">🩺</div>
            <div style="font-size:1.5rem; font-weight:800; color:#00d9ff;">GlucoVision AI</div>
            <div style="font-size:0.75rem; color:#8b949e; font-weight:700; letter-spacing:0.06em;">PRO SIMULATION HUB</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Navigation Core")
        view_mode = st.radio(
            "Select Interface Panel",
            ["Full Integrated Ecosystem", "Nutritional Inventory Search", "Digital Twin Calibration"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Engine Multi-Modifiers")
        stress_level = st.selectbox("Current System Stress / Illness Level", ["Normal", "High / Anxious", "Illness / Infection"])
        dawn_effect = st.checkbox("Simulate Dawn Phenomenon (Cortisol Spike Effect)", value=False)
        
        return view_mode, stress_level, dawn_effect

# ─── CORE DASHBOARD LOGIC RENDER ───────────────────────────────────────────────

def main():
    view_mode, stress_level, dawn_effect = render_sidebar()

    # Application Branding Banner Banner
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">GlucoVision AI 🚀</h1>
        <p class="hero-subtitle">Advanced Physiological Simulation Engine & Clinical Prediction Grid</p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # PANEL VIEW 1: COMPLETE INTEGRATED SAAS INFRASTRUCTURE
    # -------------------------------------------------------------------------
    if view_mode == "Full Integrated Ecosystem":
        
        # --- SECTION 1: PATIENT MATRIX ---
        st.markdown("""
        <div class="section-header sh-green">
            <div class="section-icon">👤</div>
            <div class="section-title">SECTION 1 — Patient Core Profile</div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: name = st.text_input("Patient Full Name", value="Alexander Mercer")
        with c2: age = st.number_input("Biological Age (Years)", min_value=1, max_value=120, value=42)
        with c3: gender = st.selectbox("Biological Sex", ["Male", "Female"])
        with c4: diabetes_type = st.selectbox("Diabetes Classification Profile", ["Type 1 Diabetes", "Type 2 Diabetes", "Prediabetes", "No Diabetes"])

        c5, c6, c7 = st.columns(3)
        with c5: weight = st.number_input("Body Weight (kg)", min_value=10.0, max_value=250.0, value=78.5, step=0.1)
        with c6: height = st.number_input("Stature Height (cm)", min_value=50.0, max_value=250.0, value=176.0, step=0.5)
        with c7:
            bmi, bmi_cat = calculate_bmi(weight, height)
            st.markdown(f"<div style='margin-top:1.8rem; font-weight:700;'>Calculated Metrics Index: <span style='color:#00d9ff;'>{bmi} ({bmi_cat})</span></div>", unsafe_allow_html=True)

        # --- SECTION 2: INSULIN LOGISTICS ---
        st.markdown("""
        <div class="section-header sh-purple">
            <div class="section-icon">💉</div>
            <div class="section-title">SECTION 2 — Exogenous Insulin Profile</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_i1, col_i2, col_i3 = st.columns(3)
        with col_i1:
            insulin_type = st.selectbox("Active Action Category", INSULIN_TYPES, index=1 if diabetes_type == "Type 1 Diabetes" else 0)
        with col_i2:
            is_no_ins = (insulin_type == "No Insulin" or diabetes_type == "No Diabetes")
            insulin_dose = st.number_input("Administered Dose (Units)", min_value=0.0, max_value=80.0, value=0.0 if is_no_ins else 6.0, step=0.5, disabled=is_no_ins)
        with col_i3:
            time_since_injection = st.number_input("Time Elapsed Since Administration (Hours)", min_value=0.0, max_value=24.0, value=0.0 if is_no_ins else 0.5, step=0.25, disabled=is_no_ins)

        # --- SECTION 3: FOOD INTELLIGENCE GRID ---
        st.markdown("""
        <div class="section-header sh-orange">
            <div class="section-icon">🍽️</div>
            <div class="section-title">SECTION 3 — Advanced Nutritional Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("⚡ **Multi-Meal Simulation Buffer:** Add the precise array of elements ingested during this meal cycle to test immediate dynamic tracking.")
        selected_foods = st.multiselect("Query / Select Ingested Food Items", options=sorted(list(FOOD_DB.keys())), default=["Basmati Rice (cooked) (100 g)", "Toor / Arhar Dal (cooked) (1 bowl (150 g))"])

        total_cal = total_carbs = total_protein = total_fat = total_gi_weight = 0.0
        
        if selected_foods:
            st.markdown("<p style='color:#00d9ff; font-weight:700;'>🔢 Fine-Tune Intake Quantities (Portion Scales):</p>", unsafe_allow_html=True)
            f_cols = st.columns(min(len(selected_foods), 3))
            
            for idx, item in enumerate(selected_foods):
                with f_cols[idx % 3]:
                    multiplier = st.number_input(f"Scale Factor: {item.split('(')[0]}", min_value=0.1, max_value=10.0, value=1.0, step=0.1, key=f"food_{idx}")
                    db_metrics = FOOD_DB[item]
                    total_cal += db_metrics["calories"] * multiplier
                    total_carbs += db_metrics["carbs"] * multiplier
                    total_protein += db_metrics["protein"] * multiplier
                    total_fat += db_metrics["fat"] * multiplier
                    total_gi_weight += db_metrics["gi"] * (db_metrics["carbs"] * multiplier)
            
            # Weighted average glycemic tracking computation
            calculated_avg_gi = (total_gi_weight / total_carbs) if total_carbs > 0 else 55.0
        else:
            calculated_avg_gi = 55.0

        # Global macro review metrics readout
        nm_c1, nm_c2, nm_c3, nm_c4, nm_c5 = st.columns(5)
        nm_c1.metric("Meal Calories", f"{round(total_cal, 1)} kcal")
        nm_c2.metric("Net Carbohydrates", f"{round(total_carbs, 1)} g")
        nm_c3.metric("Proteins", f"{round(total_protein, 1)} g")
        nm_c4.metric("Lipid Fats", f"{round(total_fat, 1)} g")
        nm_c5.metric("Aggressive Glycemic GI Index", f"{round(calculated_avg_gi, 1)}")

        # --- SECTION 4: INTEGRATED TIME-VARIANCE & COMPLEMENTARY BIOMETRICS ---
        st.markdown("""
        <div class="section-header sh-teal">
            <div class="section-icon">🏃</div>
            <div class="section-title">SECTION 4 — Active Metabolic Interventions</div>
        </div>
        """, unsafe_allow_html=True)
        
        ex_c1, ex_c2, ex_c3 = st.columns(3)
        with ex_c1:
            time_since_meal = st.number_input("Time Elapsed Since Meal Ingestion (Hours)", min_value=0.0, max_value=12.0, value=0.0, step=0.25)
        with ex_c2:
            exercise_type = st.selectbox("Physical Activity Profile Interventions", ["No Exercise", "Light (walking, yoga)", "Moderate (jogging, cycling)", "Intense (running, gym, sports)"])
        with ex_c3:
            exercise_duration = st.number_input("Activity Execution Windows (Minutes)", min_value=0, max_value=180, value=0, step=5, disabled=(exercise_type == "No Exercise"))

        # Baseline entering glucose profile reading
        st.markdown("<br>", unsafe_allow_html=True)
        g_c1, g_c2 = st.columns(2)
        with g_c1:
            current_glucose = st.number_input("Baseline Real-Time Capillary Glucose Reading (mg/dL)", min_value=40, max_value=500, value=135)
        with g_c2:
            st.markdown("<div style='padding-top:1.8rem; color:#8b949e; font-size:0.85rem; font-weight:600;'>System runs prediction architecture against target indices utilizing structural baseline parameters.</div>", unsafe_allow_html=True)

        # --- RUN BIO-ENGINE PROCESS AT CELLULAR LAYERS ---
        sim_data = glucose_prediction_model(
            current_glucose=float(current_glucose),
            carbs_g=total_carbs,
            diabetes_type=diabetes_type,
            insulin_type=insulin_type,
            insulin_dose=insulin_dose,
            time_since_injection_hr=time_since_injection,
            weight_kg=weight,
            age=age,
            gender=gender,
            calories_kcal=total_cal,
            time_since_meal_hr=time_since_meal,
            exercise_type=exercise_type,
            exercise_duration_min=float(exercise_duration),
            avg_gi=calculated_avg_gi,
            stress_level=stress_level,
            dawn_effect=dawn_effect
        )
        
        analytics = compute_health_analytics(sim_data["curve"])
        recommendations = generate_recommendations(analytics, total_carbs, bmi_cat)

        # --- SECTION 5 & 6: ADVANCED HEALTH ENGINE SCOREBOARDS ---
        st.markdown("""
        <div class="section-header sh-yellow">
            <div class="section-icon">🧠</div>
            <div class="section-title">SECTION 5 & 6 — Time-In-Range (TIR) & Realtime Telemetry Grid</div>
        </div>
        """, unsafe_allow_html=True)

        # UI Visual Grid Readouts
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            risk_class = f"risk-{analytics['risk'].split()[0].lower()}"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🛡️</div>
                <div class="metric-value">{analytics['score']}</div>
                <div class="metric-label">METABOLIC HEALTH SCORE</div>
                <span class="{risk_class}">{analytics['risk']}</span>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🎯</div>
                <div class="metric-value">{analytics['tir']}%</div>
                <div class="metric-label">TIME IN RANGE (70-180 mg/dL)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🧪</div>
                <div class="metric-value">{analytics['hba1c']}%</div>
                <div class="metric-label">ESTIMATED GLYCO HbA1C</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-value">{analytics['cv']}%</div>
                <div class="metric-label">GLYCEAMIC VARIANCE (CV)</div>
            </div>
            """, unsafe_allow_html=True)

        # --- SECTION 7: INTERACTIVE PLOTLY DATAFRAME VISUALIZATION ---
        st.markdown("""
        <div class="section-header sh-blue">
            <div class="section-icon">📊</div>
            <div class="section-title">SECTION 7 — Predictive Continuous Glucose Timeline Projection</div>
        </div>
        """, unsafe_allow_html=True)

        # Plotly Graph Constructor
        fig = go.Figure()
        timeline = sim_data["timeline"]
        curve = sim_data["curve"]

        # Target Range Envelope Mapping
        fig.add_shape(type="rect", x0=0, y0=70, x1=240, y1=180, fillcolor="rgba(0, 230, 118, 0.08)", line_width=0, name="Target Euglycemia")
        # Critical Hypo Warning Zone Border Lines
        fig.add_shape(type="rect", x0=0, y0=40, x1=240, y1=70, fillcolor="rgba(255, 59, 59, 0.06)", line_width=0, name="Hypoglycemia Critical Warning")

        fig.add_trace(go.Scatter(x=timeline, y=curve, mode='lines+markers', name='Twin Prediction Vector', line=dict(color='#00d9ff', width=3.5), marker=dict(size=6, color='#ffffff', line=dict(color='#00d9ff', width=1.5))))

        # Precise temporal callout points mapping
        times_to_mark = [30, 60, 120, 240]
        vals_to_mark = [sim_data["pred_30"], sim_data["pred_60"], sim_data["pred_120"], sim_data["pred_240"]]
        fig.add_trace(go.Scatter(x=times_to_mark, y=vals_to_mark, mode='markers+text', text=[f"{v} mg/dL" for v in vals_to_mark], textposition="top center", marker=dict(color='#ff2d95', size=10, symbol='diamond'), name='Crucial Milestones'))

        fig.update_layout(
            paper_bgcolor='#0d1117', plot_bgcolor='#161b22',
            title=dict(text="Continuous Biological Simulation Envelope (4-Hour Projection Window)", font=dict(color="#ffffff", size=16), x=0.5),
            xaxis=dict(title="Timeline Intercept Vector (Minutes)", gridcolor="#30363d", color="#ffffff"),
            yaxis=dict(title="Systemic Blood Glucose Density (mg/dL)", gridcolor="#30363d", color="#ffffff", range=[30, max(250, max(curve)+30)]),
            legend=dict(font=dict(color="#ffffff")), margin=dict(l=40, r=40, t=50, b=40), height=480
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- SECTION 8 & 9: ADVISORY BLOCKS ---
        st.markdown("""
        <div class="section-header sh-pink">
            <div class="section-icon">💡</div>
            <div class="section-title">SECTION 8 & 9 — Automated Engine Intelligence Recommendations</div>
        </div>
        """, unsafe_allow_html=True)
        
        rec_cols = st.columns(len(recommendations) if recommendations else 1)
        for r_idx, r_text in enumerate(recommendations):
            with rec_cols[r_idx]:
                card_type = "rc-high" if "🚨" in r_text or "📈" in r_text else "rc-low"
                st.markdown(f"<div class='rec-card {card_type}'>{r_text}</div>", unsafe_allow_html=True)

        # --- SECTION 10: AUTOMATED EXPORT ENGINE FOR MEDICAL REVIEW ---
        st.markdown("""
        <div class="section-header sh-blue">
            <div class="section-icon">📄</div>
            <div class="section-title">SECTION 10 — Clinical Quality PDF Reporting System</div>
        </div>
        """, unsafe_allow_html=True)
        
        patient_payload = {"name": name, "age": age, "gender": gender, "diabetes": diabetes_type, "weight": weight, "height": height}
        nutrition_payload = {"calories": total_cal, "carbs": total_carbs, "protein": total_protein, "fat": total_fat}
        
        pdf_bytes = generate_pdf_report(patient_payload, nutrition_payload, float(current_glucose), analytics, recommendations)
        
        st.markdown("""
        <div style="background-color:#161b22; border: 2px solid #30363d; padding:1.2rem; border-radius:8px;">
            <p style="margin-top:0;">📋 <strong>Compile and locks all dashboard components:</strong> Exports comprehensive state matrix indicators, full 240-minute cellular digital twin projection tracks, and automated recommendations vector matrixes into a unified professional dossier print layout.</p>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        st.download_button(
            label="📥 DOWNLOAD EXECUTIVE COMPREHENSIVE MEDICAL HEALTH REPORT",
            data=pdf_bytes,
            file_name=f"GlucoVision_Pro_Report_{name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

    # -------------------------------------------------------------------------
    # PANEL VIEW 2: COMPLETE ISOLATED NUTRIENT DATA DISCOVERY EXPLORER
    # -------------------------------------------------------------------------
    elif view_mode == "Nutritional Inventory Search":
        st.markdown("""
        <div class="section-header sh-orange">
            <div class="section-icon">🔍</div>
            <div class="section-title">Metabolic Nutrition Index Database Explorer</div>
        </div>
        """, unsafe_allow_html=True)
        
        search_query = st.text_input("Search Food Item Registry Engine (e.g., Rice, Oats, Chicken, Ragi)...", value="")
        
        filtered_foods = []
        for k, v in FOOD_DB.items():
            if search_query.lower() in k.lower():
                filtered_foods.append({
                    "Food Description Core Tag": k,
                    "Calories (kcal)": v["calories"],
                    "Carbohydrates (g)": v["carbs"],
                    "Protein (g)": v["protein"],
                    "Lipids/Fat (g)": v["fat"],
                    "Glycemic Speed Rating (GI)": v["gi"],
                    "Glycemic Tier Load Classification": "HIGH (Spiker)" if v["gi"] >= 70 else ("MEDIUM (Moderate)" if v["gi"] >= 55 else "LOW (Stable/Blunted)")
                })
        
        if filtered_foods:
            df_food = pd.DataFrame(filtered_foods)
            st.dataframe(df_food.style.background_gradient(cmap="Blues", subset=["Glycemic Speed Rating (GI)"]), use_container_width=True, height=500)
        else:
            st.error("No metabolic profile match located for target parameters inside database arrays.")

    # -------------------------------------------------------------------------
    # PANEL VIEW 3: ADVANCED STRESS / GLYCEMIC DIGITAL TWIN SIMULATION SANDBOX
    # -------------------------------------------------------------------------
    elif view_mode == "Digital Twin Calibration":
        st.markdown("""
        <div class="section-header sh-purple">
            <div class="section-icon">🔬</div>
            <div class="section-title">Physiological Stress Matrix Sandbox Model</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning("🧪 **Advanced Medical Physics Simulation:** This visualization mode runs hyper-isolated variations to verify how extreme changes in Glycemic Index (GI) impact human biology under varying biological settings.")

        sandbox_gi = st.slider("Target Isolated Glycemic Index Shift Profile", min_value=10, max_value=100, value=65, step=5)
        sandbox_carbs = st.slider("Target Ingested Carbohydrate Mass Payload (grams)", min_value=5, max_value=150, value=60, step=5)
        sandbox_insulin = st.slider("Target Micro-Dose Rapid Insulin Vector Correction (Units)", min_value=0.0, max_value=25.0, value=4.0, step=0.5)

        # Simulation processing
        res_baseline = glucose_prediction_model(140.0, sandbox_carbs, "Type 1 Diabetes", "Rapid-Acting (e.g., Lispro, Aspart)", sandbox_insulin, 0.0, 75.0, 35, "Male", 300, 0.0, "No Exercise", 0, avg_gi=float(sandbox_gi))
        res_stressed = glucose_prediction_model(140.0, sandbox_carbs, "Type 1 Diabetes", "Rapid-Acting (e.g., Lispro, Aspart)", sandbox_insulin, 0.0, 75.0, 35, "Male", 300, 0.0, "No Exercise", 0, avg_gi=float(sandbox_gi), stress_level="High / Anxious")

        fig_sb = go.Figure()
        fig_sb.add_trace(go.Scatter(x=res_baseline["timeline"], y=res_baseline["curve"], name="Normal Physiology Configuration", line=dict(color="#00e676", width=3)))
        fig_sb.add_trace(go.Scatter(x=res_stressed["timeline"], y=res_stressed["curve"], name="Elevated Autonomic Cortisol Stress Configuration", line=dict(color="#ff3b3b", width=3, dash='dash')))
        
        fig_sb.update_layout(
            paper_bgcolor='#0d1117', plot_bgcolor='#161b22',
            title="Twin System Intercept Cross-Comparison Curves",
            xaxis=dict(title="Time Vector Minutes", color="#ffffff"),
            yaxis=dict(title="Glucose Vector Target mg/dL", color="#ffffff"),
            legend=dict(font=dict(color="#ffffff")), height=450
        )
        st.plotly_chart(fig_sb, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════════
    # PROFESSIONAL COMPLIANCE AND SAFETY DISCLAIMER
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding: 2rem 1rem 1rem; border-top: 1px solid rgba(0,217,255,0.2);">
        <div style="font-size:0.95rem; font-weight:700; color:#ff3b3b; margin-bottom:0.5rem">
            ⚠️ IMPORTANT REGULATORY & COMPLIANCE DISCLAIMER NOTICE
        </div>
        <div style="font-size:0.82rem; color:#c9d1d9; max-width:850px; margin:0 auto; line-height:1.7; font-weight:600;">
            GlucoVision AI is an <strong>educational engineering algorithmic prototype simulation sandbox</strong> built exclusively 
            for validation, display UI architecture, and pedagogical concept exhibition. It is <strong>NOT a certified medical device</strong> 
            and must never under any circumstances be utilized for metabolic diagnostics, actionable patient prescriptions, 
            insulin dosing calibrations, or real therapeutic decision-making matrices. The math calculations executed by the system 
            are non-clinical estimations and do not correspond to precise real-world human biochemical responses. Always prioritize direct consultation 
            with a qualified Endocrinologist or certified healthcare practitioner team for authentic medical management.
        </div>
        <div style="font-size:0.75rem; color:#8b949e; margin-top:1rem; font-weight:500;">
            GlucoVision AI Framework Pro • Streamlit Environment Deployment Build v4.9.2
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
