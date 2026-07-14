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
hr{
    border: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "result" not in st.session_state:
    st.session_state.result = None
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

# ---------------- MBTI QUESTIONS ---------------- #
questions = [
    {"id": 1, "text": "You feel energized after spending time with many people.", "dimension": "EI", "pole": "E"},
    {"id": 2, "text": "You prefer quiet time alone to recharge.", "dimension": "EI", "pole": "I"},
    {"id": 3, "text": "You focus more on facts and real details than possibilities.", "dimension": "SN", "pole": "S"},
    {"id": 4, "text": "You enjoy thinking about patterns, ideas, and future possibilities.", "dimension": "SN", "pole": "N"},
    {"id": 5, "text": "You usually make decisions based on logic and consistency.", "dimension": "TF", "pole": "T"},
    {"id": 6, "text": "You care deeply about people’s feelings when deciding something.", "dimension": "TF", "pole": "F"},
    {"id": 7, "text": "You like to plan things ahead and follow a schedule.", "dimension": "JP", "pole": "J"},
    {"id": 8, "text": "You prefer flexibility and keeping your options open.", "dimension": "JP", "pole": "P"},
    {"id": 9, "text": "In a group, you often speak up first.", "dimension": "EI", "pole": "E"},
    {"id": 10, "text": "You usually think carefully before sharing your thoughts.", "dimension": "EI", "pole": "I"},
    {"id": 11, "text": "You trust concrete experience more than theory.", "dimension": "SN", "pole": "S"},
    {"id": 12, "text": "You are drawn to abstract ideas and imagination.", "dimension": "SN", "pole": "N"},
    {"id": 13, "text": "You try to be fair and objective in difficult situations.", "dimension": "TF", "pole": "T"},
    {"id": 14, "text": "You often think about how your decisions affect others emotionally.", "dimension": "TF", "pole": "F"},
    {"id": 15, "text": "You like completing tasks early and staying organized.", "dimension": "JP", "pole": "J"},
    {"id": 16, "text": "You are comfortable improvising at the last minute.", "dimension": "JP", "pole": "P"},
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
    pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    for a, b in pairs:
        if scores[a] > scores[b]:
            result.append(a)
        elif scores[b] > scores[a]:
            result.append(b)
        else:
            result.append(a)
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
    st.session_state.obstacles = [
        {"x": 65, "gap": False},
        {"x": 110, "gap": False},
        {"x": 155, "gap": False},
        {"x": 200, "gap": False},
        {"x": 245, "gap": False},
    ]

def update_game(jump_pressed):
    gravity = 1
    jump_power = -11
    speed = 2
    ground_y = 0
    player_x = 10
    player_size = 3

    if jump_pressed and st.session_state.player_y == ground_y:
        st.session_state.player_vy = jump_power

    st.session_state.player_vy += gravity
    st.session_state.player_y += st.session_state.player_vy

    if st.session_state.player_y > ground_y:
        st.session_state.player_y = ground_y
        st.session_state.player_vy = 0

    st.session_state.game_frame += 1
    for obs in st.session_state.obstacles:
        obs["x"] -= speed

    st.session_state.obstacles = [o for o in st.session_state.obstacles if o["x"] > -5]

    if st.session_state.obstacles and st.session_state.obstacles[-1]["x"] < 55:
        if len(st.session_state.obstacles) < 6:
            new_x = st.session_state.obstacles[-1]["x"] + random.randint(25, 35)
            st.session_state.obstacles.append({"x": new_x, "gap": False})

    for obs in st.session_state.obstacles:
        if player_x + player_size > obs["x"] and player_x < obs["x"] + 2:
            if st.session_state.player_y == 0:
                st.session_state.game_over = True

    if st.session_state.game_frame >= 500:
        st.session_state.game_won = True

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🧠 PersonaLens AI")
page = st.sidebar.radio("Navigation", ["🏠 Home", "📝 MBTI Test", "📊 Results", "🎮 Game", "ℹ About"])
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
    st.markdown("<div class='sub'>Discover your MBTI type and play a tiny Geometry Dash-style mini game.</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="card"><div class="metric">16</div><div class="small">MBTI Types</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card"><div class="metric">1</div><div class="small">Game Level</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card"><div class="metric">2</div><div class="small">Features</div></div>""", unsafe_allow_html=True)

    st.info("Use the sidebar to take the MBTI test or play the mini game.")

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
        for a, b, label in [("E","I","Extraversion / Introversion"), ("S","N","Sensing / Intuition"), ("T","F","Thinking / Feeling"), ("J","P","Judging / Perceiving")]:
            total = scores[a] + scores[b]
            pct = int((scores[a] / total) * 100) if total else 50
            st.write(f"**{label}**")
            st.progress(pct / 100)
            st.caption(f"{a}: {scores[a]} | {b}: {scores[b]}")

# ---------------- GAME ---------------- #
elif page == "🎮 Game":
    st.title("Mini Geometry Dash Game")
    st.write("A simple one-level jumping game. Press **Start Game** and use the **Jump** button.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Start Game"):
            init_game()
            st.rerun()
    with col2:
        jump_pressed = st.button("Jump")

    if st.session_state.game_started and not st.session_state.game_over and not st.session_state.game_won:
        update_game(jump_pressed)

    ground = "▁" * 55
    player_line = [" "] * 55
    obstacle_line = [" "] * 55

    player_pos = 10
    player_height = max(0, min(4, 4 - st.session_state.player_y))
    if player_height < 5:
        player_line[player_pos] = "🟦"

    for obs in st.session_state.obstacles:
        pos = int(obs["x"])
        if 0 <= pos < 55:
            obstacle_line[pos] = "🟥"
            if pos + 1 < 55:
                obstacle_line[pos + 1] = "🟥"

    st.markdown("<div class='game-box'>", unsafe_allow_html=True)
    st.code("".join(obstacle_line), language=None)
    st.code("".join(player_line), language=None)
    st.code(ground, language=None)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.game_over:
        st.error("Game Over. You hit an obstacle.")
    elif st.session_state.game_won:
        st.success("You completed the one-level game!")
        st.balloons()

    st.caption("Tip: Because Streamlit reruns on every interaction, this is a simple turn-based mini game instead of a true real-time arcade game.")

# ---------------- ABOUT ---------------- #
else:
    st.title("About PersonaLens AI")
    st.write("""
PersonaLens AI now includes:
- MBTI personality test
- Personality type report
- One-level Geometry Dash-style mini game
- Simple modern UI
    """)
    st.write("---")
    st.caption("© 2026 PersonaLens AI")
