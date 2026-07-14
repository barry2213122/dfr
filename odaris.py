import streamlit as st
import random
import time

st.set_page_config(page_title="PersonaLens AI", page_icon="🧠", layout="wide")

# ---------------- CSS ---------------- #
st.markdown("""
<style>
body{
    background: linear-gradient(135deg, #090909, #151d35);
}
.main-title{
    font-size: 54px;
    text-align: center;
    font-weight: 800;
    color: #66FCF1;
}
.sub{
    text-align: center;
    color: #d0d0d0;
    font-size: 20px;
}
.card{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
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
.game-box{
    background: #0d1224;
    border: 2px solid #66FCF1;
    border-radius: 18px;
    padding: 20px;
}
.health-box{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(102,252,241,0.25);
    border-radius: 18px;
    padding: 20px;
}
hr{
    border: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #
defaults = {
    "answers": {},
    "submitted": False,
    "result": None,
    "game_started": False,
    "game_over": False,
    "game_won": False,
    "player_y": 0,
    "player_vy": 0,
    "obstacles": [],
    "game_frame": 0
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- MBTI QUESTIONS ---------------- #
questions = [
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

options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
score_map = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}

def get_dimension_scores():
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for q in questions:
        ans = st.session_state.answers.get(q["id"], "Neutral")
        scores[q["pole"]] += score_map[ans]
    return scores

def mbti_type_from_scores(scores):
    result = []
    for a, b in [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]:
        result.append(a if scores[a] >= scores[b] else b)
    return "".join(result)

descriptions = {
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

# ---------------- GAME LOGIC ---------------- #
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

    if st.session_state.obstacles and st.session_state.obstacles[-1]["x"] < 55:
        if len(st.session_state.obstacles) < 6:
            st.session_state.obstacles.append({"x": st.session_state.obstacles[-1]["x"] + random.randint(25, 35)})

    for obs in st.session_state.obstacles:
        if player_x + player_size > obs["x"] and player_x < obs["x"] + 2:
            if st.session_state.player_y == 0:
                st.session_state.game_over = True

    if st.session_state.game_frame >= 500:
        st.session_state.game_won = True

# ---------------- HEALTH AI ---------------- #
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Healthy weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity risk"

def health_ai_assessment(height_cm, weight_kg, age, diet, exercise, sleep_hours, water_glasses, fast_food, smoking):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    category = bmi_category(bmi)
    risk_points = 0
    tips = []
    issues = []

    if bmi < 18.5:
        risk_points += 2
        issues.append("Low weight-related energy or nutrient deficiency risk.")
        tips.append("Increase balanced calories, protein, and nutrient-rich foods.")
    elif bmi >= 25:
        risk_points += 2
        issues.append("Weight-related risk may be higher.")
        tips.append("Focus on balanced meals and regular physical activity.")

    if exercise < 150:
        risk_points += 2
        issues.append("Sedentary lifestyle risk.")
        tips.append("Try to reach at least 150 minutes of moderate activity per week.")
    if sleep_hours < 7:
        risk_points += 1
        issues.append("Possible fatigue or poor recovery risk.")
        tips.append("Aim for 7 to 9 hours of sleep.")
    if water_glasses < 6:
        risk_points += 1
        issues.append("Low hydration risk.")
        tips.append("Drink more water through the day.")
    if diet == "Poor":
        risk_points += 2
        issues.append("Nutrient imbalance risk.")
        tips.append("Add fruits, vegetables, whole grains, and lean protein.")
    elif diet == "Average":
        risk_points += 1
        tips.append("Improve meal quality with more whole foods.")
    if fast_food >= 4:
        risk_points += 1
        issues.append("High fast-food intake may increase health risk.")
        tips.append("Reduce fast food and processed snacks.")
    if smoking:
        risk_points += 3
        issues.append("Smoking increases long-term health risk.")
        tips.append("Stopping smoking can greatly improve health.")

    if age >= 45:
        tips.append("Regular health checkups become more important with age.")

    if risk_points <= 2:
        level = "Low"
    elif risk_points <= 5:
        level = "Moderate"
    else:
        level = "Higher"

    return bmi, category, level, issues, tips

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🧠 PersonaLens AI")
page = st.sidebar.radio("Navigation", ["🏠 Home", "📝 MBTI Test", "📊 Results", "🎮 Game", "🏥 Health AI", "ℹ About"])
st.sidebar.write("---")
if st.sidebar.button("Reset All"):
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.result = None
    reset_game()
    st.rerun()

# ---------------- HOME ---------------- #
if page == "🏠 Home":
    st.markdown("<div class='main-title'>PersonaLens AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Discover your MBTI type, play a tiny game, and get simple wellness guidance.</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="card"><div class="metric">16</div><div class="small">MBTI Types</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card"><div class="metric">1</div><div class="small">Game Level</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card"><div class="metric">AI</div><div class="small">Health Guidance</div></div>""", unsafe_allow_html=True)

    st.info("Use the sidebar to open the MBTI test, game, or Health AI.")

# ---------------- MBTI TEST ---------------- #
elif page == "📝 MBTI Test":
    st.title("MBTI Personality Test")
    st.write("Answer honestly to get your likely MBTI type.")

    with st.form("mbti_form"):
        for q in questions:
            st.session_state.answers[q["id"]] = st.radio(
                f"Q{q['id']}. {q['text']}",
                options,
                index=2,
                key=f"q_{q['id']}"
            )
            st.write("")
        submitted = st.form_submit_button("Generate MBTI Result")

    if submitted:
        scores = get_dimension_scores()
        mbti = mbti_type_from_scores(scores)
        st.session_state.submitted = True
        st.session_state.result = {"type": mbti, "scores": scores}
        st.success("MBTI result generated.")
        st.balloons()

# ---------------- RESULTS ---------------- #
elif page == "📊 Results":
    st.title("Your MBTI Report")
    if not st.session_state.submitted or st.session_state.result is None:
        st.warning("Complete the MBTI test first.")
    else:
        result = st.session_state.result
        mbti = result["type"]
        scores = result["scores"]

        st.markdown(f"""
        <div class="card">
            <h1 style="color:#66FCF1;text-align:center;">{mbti}</h1>
            <p style="text-align:center;color:#e0e0e0;font-size:18px;">{descriptions.get(mbti, "A balanced and unique personality type.")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.subheader("Dimension Scores")
        for a, b, label in [("E", "I", "Extraversion / Introversion"), ("S", "N", "Sensing / Intuition"), ("T", "F", "Thinking / Feeling"), ("J", "P", "Judging / Perceiving")]:
            total = scores[a] + scores[b]
            pct = int((scores[a] / total) * 100) if total else 50
            st.write(f"**{label}**")
            st.progress(pct / 100)
            st.caption(f"{a}: {scores[a]} | {b}: {scores[b]}")

# ---------------- GAME ---------------- #
elif page == "🎮 Game":
    st.title("Mini Geometry Dash Game")
    st.write("A simple one-level jumping game.")

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

    player_pos = 10
    player_line[player_pos] = "🟦"

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

    st.caption("This is a simple Streamlit mini game, not a full real-time game engine.")

# ---------------- HEALTH AI ---------------- #
elif page == "🏥 Health AI":
    st.title("Health AI Assistant")
    st.write("This tool gives general wellness guidance from a few inputs. It is not a medical diagnosis tool.")

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
        bmi, category, level, issues, tips = health_ai_assessment(
            height_cm, weight_kg, age, diet, exercise, sleep_hours, water_glasses, fast_food, smoking
        )

        st.success("Analysis completed.")

        c1, c2, c3 = st.columns(3)
        c1.metric("BMI", f"{bmi:.1f}")
        c2.metric("Weight Category", category)
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

        st.caption("This is only a general wellness estimate, not a medical diagnosis.")

# ---------------- ABOUT ---------------- #
else:
    st.title("About PersonaLens AI")
    st.write("""
PersonaLens AI includes:
- MBTI personality test
- Personality type report
- One-level Geometry Dash-style mini game
- Health AI wellness guidance
- Simple modern UI
    """)
    st.write("---")
    st.caption("© 2026 PersonaLens AI")
