import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="Unified AI Suite",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# SESSION STATE
# =========================
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

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #090909, #151d35);
    color: white;
}
body {
    color: white;
}
.main-title{
    font-size: 54px;
    text-align: center;
    font-weight: 800;
    color: #66FCF1;
    margin-bottom: 0;
}
.sub{
    text-align: center;
    color: #d0d0d0;
    font-size: 20px;
}
.card{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 24px;
    backdrop-filter: blur(12px);
}
.metric{
    text-align: center;
    font-size: 35px;
    color: #66FCF1;
    font-weight: bold;
}
.small{
    text-align: center;
    color: #bfbfbf;
}
.game-box,.health-box,.gluco-box{
    background: rgba(13,18,36,0.92);
    border: 2px solid #66FCF1;
    border-radius: 18px;
    padding: 20px;
}
hr{
    border: 1px solid #333;
}
section[data-testid="stSidebar"]{
    background:#111827;
    border-right:2px solid #66FCF1;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================
def login_screen():
    st.markdown("<div class='main-title'>Welcome</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Login first to access PersonaLens AI and GlucoVision.</div>", unsafe_allow_html=True)
    st.write("")

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            if username.strip().lower() == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.caption("Demo login: username = admin, password = 1234")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# MBTI
# =========================
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

# =========================
# GAME
# =========================
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

# =========================
# HEALTH AI
# =========================
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Healthy weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity risk"

def health_ai(height_cm, weight_kg, age, diet, exercise, sleep_hours, water_glasses, fast_food, smoking):
    h = height_cm / 100
    bmi = weight_kg / (h * h)
    cat = bmi_category(bmi)
    risk = 0
    issues, tips = [], []

    if bmi < 18.5:
        risk += 2
        issues.append("Low weight-related energy or nutrient deficiency risk.")
        tips.append("Increase balanced calories, protein, and nutrient-rich foods.")
    elif bmi >= 25:
        risk += 2
        issues.append("Weight-related risk may be higher.")
        tips.append("Focus on balanced meals and regular physical activity.")

    if exercise < 150:
        risk += 2
        issues.append("Sedentary lifestyle risk.")
        tips.append("Try to reach at least 150 minutes of moderate activity per week.")
    if sleep_hours < 7:
        risk += 1
        issues.append("Possible fatigue or poor recovery risk.")
        tips.append("Aim for 7 to 9 hours of sleep.")
    if water_glasses < 6:
        risk += 1
        issues.append("Low hydration risk.")
        tips.append("Drink more water through the day.")
    if diet == "Poor":
        risk += 2
        issues.append("Nutrient imbalance risk.")
        tips.append("Add fruits, vegetables, whole grains, and lean protein.")
    elif diet == "Average":
        risk += 1
        tips.append("Improve meal quality with more whole foods.")
    if fast_food >= 4:
        risk += 1
        issues.append("High fast-food intake may increase health risk.")
        tips.append("Reduce fast food and processed snacks.")
    if smoking:
        risk += 3
        issues.append("Smoking increases long-term health risk.")
        tips.append("Stopping smoking can greatly improve health.")
    if age >= 45:
        tips.append("Regular health checkups become more important with age.")

    level = "Low" if risk <= 2 else "Moderate" if risk <= 5 else "Higher"
    return round(bmi, 1), cat, level, issues, tips

# =========================
# GLUCOVISION
# =========================
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

# =========================
# SPECIAL CREDITS
# =========================
def credits_page():
    st.title("Special Credits")
    st.markdown("""
<div class='card'>
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

# =========================
# MAIN NAV AFTER LOGIN
# =========================
def main_app():
    st.sidebar.title(f"🧠 Hi, {st.session_state.username}")
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📝 MBTI Test", "📊 MBTI Results", "🎮 Game", "🏥 Health AI", "🩺 GlucoVision", "⭐ Special Credits", "🚪 Logout"]
    )

    if page == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.app_page = "home"
        st.rerun()

    st.sidebar.write("---")
    if st.sidebar.button("Reset All"):
        st.session_state.mbti_answers = {}
        st.session_state.mbti_done = False
        st.session_state.mbti_result = None
        reset_game()
        st.session_state.gluco_values = {}
        st.rerun()

    if page == "🏠 Home":
        st.markdown("<div class='main-title'>Unified AI Suite</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub'>MBTI test + mini game + health AI + GlucoVision in one app.</div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""<div class='card'><div class='metric'>MBTI</div><div class='small'>Personality</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class='card'><div class='metric'>GAME</div><div class='small'>1 Level</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class='card'><div class='metric'>HEALTH</div><div class='small'>Wellness AI</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown("""<div class='card'><div class='metric'>GLUCO</div><div class='small'>Glucose AI</div></div>""", unsafe_allow_html=True)

        st.info("Use the sidebar to open any section.")

    elif page == "📝 MBTI Test":
        st.title("MBTI Personality Test")
        with st.form("mbti_form"):
            for q in mbti_questions:
                st.session_state.mbti_answers[q["id"]] = st.radio(
                    f"Q{q['id']}. {q['text']}",
                    mbti_options,
                    index=2,
                    key=f"m_{q['id']}"
                )
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
            st.markdown(f"""
            <div class='card'>
                <h1 style='color:#66FCF1;text-align:center;'>{result}</h1>
                <p style='text-align:center;color:#e0e0e0;font-size:18px;'>{mbti_desc.get(result, 'Balanced personality.')}</p>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            for a, b, label in [("E", "I", "Extraversion / Introversion"),
                                ("S", "N", "Sensing / Intuition"),
                                ("T", "F", "Thinking / Feeling"),
                                ("J", "P", "Judging / Perceiving")]:
                total = scores[a] + scores[b]
                pct = int((scores[a] / total) * 100) if total else 50
                st.write(f"**{label}**")
                st.progress(pct / 100)
                st.caption(f"{a}: {scores[a]} | {b}: {scores[b]}")

    elif page == "🎮 Game":
        st.title("Mini Geometry Dash Game")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Start Game"):
                init_game()
                st.rerun()
        with col2:
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

        st.markdown("<div class='game-box'>", unsafe_allow_html=True)
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
            bmi, cat, level, issues, tips = health_ai(
                height_cm, weight_kg, age, diet, exercise, sleep_hours, water_glasses, fast_food, smoking
            )
            st.success("Analysis completed.")
            c1, c2, c3 = st.columns(3)
            c1.metric("BMI", f"{bmi:.1f}")
            c2.metric("Weight Category", cat)
            c3.metric("Risk Level", level)
            st.markdown("<div class='health-box'>", unsafe_allow_html=True)
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
        st.title("GlucoVision Lite")
        st.write("A simple educational glucose estimator inspired by your attached app.")
        with st.form("gluco_form"):
            c1, c2 = st.columns(2)
            with c1:
                current_glucose = st.number_input("Current glucose (mg/dL)", min_value=40.0, max_value=600.0, value=110.0)
                carbs_g = st.number_input("Carbs (g)", min_value=0.0, max_value=500.0, value=45.0)
                diabetes_type = st.selectbox("Diabetes type", ["No Diabetes", "Prediabetes", "Type 2 Diabetes", "Type 1 Diabetes"])
                weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=65.0)
            with c2:
                exercise_min = st.number_input("Exercise minutes", min_value=0.0, max_value=300.0, value=20.0)
                insulin_type = st.selectbox("Insulin type", ["No Insulin", "Rapid-Acting", "Short-Acting", "Intermediate-Acting", "Long-Acting", "Mixed Insulin"])
                insulin_dose = st.number_input("Insulin dose (units)", min_value=0.0, max_value=100.0, value=0.0)
                bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=22.0)
            go = st.form_submit_button("Predict Glucose")

        if go:
            preds, peak = glucose_monitor(current_glucose, carbs_g, bmi, exercise_min, insulin_dose, insulin_type, diabetes_type)
            st.session_state.gluco_values = preds
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("30 min", f"{preds[30]} mg/dL")
            c2.metric("60 min", f"{preds[60]} mg/dL")
            c3.metric("90 min", f"{preds[90]} mg/dL")
            c4.metric("120 min", f"{preds[120]} mg/dL")
            st.markdown("<div class='gluco-box'>", unsafe_allow_html=True)
            st.write(f"Estimated peak/glucose response: **{peak} mg/dL**")
            st.write("This is only an educational estimate, not medical advice.")
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "⭐ Special Credits":
        credits_page()

# =========================
# ROUTING
# =========================
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
