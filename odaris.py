import streamlit as st
from collections import defaultdict

st.set_page_config(
    page_title="PersonaLens AI",
    page_icon="🧠",
    layout="wide"
)

# ----------------- CUSTOM CSS ----------------- #
st.markdown("""
<style>
    .main-title {
        font-size: 54px;
        font-weight: 800;
        text-align: center;
        color: #66FCF1;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 20px;
        text-align: center;
        color: #d0d0d0;
        margin-top: 8px;
        margin-bottom: 25px;
    }
    .card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 22px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.18);
    }
    .metric {
        font-size: 34px;
        font-weight: 800;
        color: #66FCF1;
        text-align: center;
    }
    .metric-label {
        font-size: 15px;
        color: #d0d0d0;
        text-align: center;
    }
    .result-box {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(102,252,241,0.12), rgba(255,255,255,0.04));
        border: 1px solid rgba(102,252,241,0.25);
    }
    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.12);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE ----------------- #
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "result" not in st.session_state:
    st.session_state.result = None

# ----------------- QUESTIONS ----------------- #
questions = [
    {
        "id": 1,
        "text": "You feel energized after spending time with many people.",
        "dimension": "EI",
        "pole": "E"
    },
    {
        "id": 2,
        "text": "You prefer quiet time alone to recharge.",
        "dimension": "EI",
        "pole": "I"
    },
    {
        "id": 3,
        "text": "You focus more on facts and real details than possibilities.",
        "dimension": "SN",
        "pole": "S"
    },
    {
        "id": 4,
        "text": "You enjoy thinking about patterns, ideas, and future possibilities.",
        "dimension": "SN",
        "pole": "N"
    },
    {
        "id": 5,
        "text": "You usually make decisions based on logic and consistency.",
        "dimension": "TF",
        "pole": "T"
    },
    {
        "id": 6,
        "text": "You care deeply about people’s feelings when deciding something.",
        "dimension": "TF",
        "pole": "F"
    },
    {
        "id": 7,
        "text": "You like to plan things ahead and follow a schedule.",
        "dimension": "JP",
        "pole": "J"
    },
    {
        "id": 8,
        "text": "You prefer flexibility and keeping your options open.",
        "dimension": "JP",
        "pole": "P"
    },
    {
        "id": 9,
        "text": "In a group, you often speak up first.",
        "dimension": "EI",
        "pole": "E"
    },
    {
        "id": 10,
        "text": "You usually think carefully before sharing your thoughts.",
        "dimension": "EI",
        "pole": "I"
    },
    {
        "id": 11,
        "text": "You trust concrete experience more than theory.",
        "dimension": "SN",
        "pole": "S"
    },
    {
        "id": 12,
        "text": "You are drawn to abstract ideas and imagination.",
        "dimension": "SN",
        "pole": "N"
    },
    {
        "id": 13,
        "text": "You try to be fair and objective in difficult situations.",
        "dimension": "TF",
        "pole": "T"
    },
    {
        "id": 14,
        "text": "You often think about how your decisions affect others emotionally.",
        "dimension": "TF",
        "pole": "F"
    },
    {
        "id": 15,
        "text": "You like completing tasks early and staying organized.",
        "dimension": "JP",
        "pole": "J"
    },
    {
        "id": 16,
        "text": "You are comfortable improvising at the last minute.",
        "dimension": "JP",
        "pole": "P"
    }
]

options = [
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly Agree"
]

score_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# ----------------- HELPERS ----------------- #
def get_dimension_scores():
    scores = {
        "E": 0, "I": 0,
        "S": 0, "N": 0,
        "T": 0, "F": 0,
        "J": 0, "P": 0
    }
    for q in questions:
        ans = st.session_state.answers.get(q["id"], "Neutral")
        val = score_map[ans]
        scores[q["pole"]] += val
    return scores

def mbti_type_from_scores(scores):
    type_letters = []
    pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    for a, b in pairs:
        if scores[a] > scores[b]:
            type_letters.append(a)
        elif scores[b] > scores[a]:
            type_letters.append(b)
        else:
            if a in ["E", "S", "T", "J"]:
                type_letters.append(a)
            else:
                type_letters.append(b)
    return "".join(type_letters)

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

career_suggestions = {
    "E": ["Sales", "Marketing", "Public Relations", "Teaching"],
    "I": ["Research", "Writing", "Programming", "Analysis"],
    "S": ["Accounting", "Engineering", "Operations", "Healthcare"],
    "N": ["Design", "Strategy", "Entrepreneurship", "Innovation"],
    "T": ["Law", "Finance", "Technology", "Consulting"],
    "F": ["Counseling", "Human Resources", "Teaching", "Social Work"],
    "J": ["Management", "Planning", "Administration", "Project Coordination"],
    "P": ["Creative Work", "Freelancing", "Startup Roles", "Field Work"]
}

# ----------------- SIDEBAR ----------------- #
st.sidebar.title("🧠 PersonaLens AI")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📝 MBTI Test", "📊 Results", "ℹ About"]
)

st.sidebar.write("---")
if st.sidebar.button("Reset Test"):
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.result = None
    st.rerun()

# ----------------- HOME ----------------- #
if page == "🏠 Home":
    st.markdown("<div class='main-title'>PersonaLens AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Discover your MBTI personality type with a clean interactive test.</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
            <div class="metric">16</div>
            <div class="metric-label">MBTI Types</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card">
            <div class="metric">4</div>
            <div class="metric-label">Personality Dimensions</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card">
            <div class="metric">16</div>
            <div class="metric-label">Questions</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.info("Go to the MBTI Test page and answer all questions honestly to get your personality type.")

# ----------------- TEST ----------------- #
elif page == "📝 MBTI Test":
    st.title("MBTI Personality Test")
    st.write("Answer each statement based on what fits you best.")

    progress = len(st.session_state.answers) / len(questions)
    st.progress(progress)

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
        st.session_state.submitted = True
        scores = get_dimension_scores()
        mbti = mbti_type_from_scores(scores)
        st.session_state.result = {
            "type": mbti,
            "scores": scores
        }
        st.success("Your MBTI result has been generated.")
        st.balloons()

# ----------------- RESULTS ----------------- #
elif page == "📊 Results":
    st.title("Your MBTI Report")

    if not st.session_state.submitted or st.session_state.result is None:
        st.warning("Complete the MBTI test first.")
    else:
        result = st.session_state.result
        mbti = result["type"]
        scores = result["scores"]

        st.markdown(f"""
        <div class="result-box">
            <h1 style="margin-bottom:0;color:#66FCF1;">{mbti}</h1>
            <p style="color:#e0e0e0;font-size:18px;">{descriptions.get(mbti, "A balanced and unique personality type.")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.subheader("Dimension Scores")

        dimensions = [
            ("E", "I", "Extraversion / Introversion"),
            ("S", "N", "Sensing / Intuition"),
            ("T", "F", "Thinking / Feeling"),
            ("J", "P", "Judging / Perceiving")
        ]

        for a, b, label in dimensions:
            total = scores[a] + scores[b]
            left_pct = int((scores[a] / total) * 100) if total else 50
            right_pct = 100 - left_pct
            st.write(f"**{label}**")
            st.progress(left_pct / 100)
            st.caption(f"{a}: {scores[a]}   |   {b}: {scores[b]}   →   {a if scores[a] >= scores[b] else b}")

        st.write("")
        st.subheader("Suggested Careers")

        type_careers = []
        type_careers.extend(career_suggestions["E"] if mbti[0] == "E" else career_suggestions["I"])
        type_careers.extend(career_suggestions["S"] if mbti[1] == "S" else career_suggestions["N"])
        type_careers.extend(career_suggestions["T"] if mbti[2] == "T" else career_suggestions["F"])
        type_careers.extend(career_suggestions["J"] if mbti[3] == "J" else career_suggestions["P"])

        unique_careers = list(dict.fromkeys(type_careers))
        for career in unique_careers[:8]:
            st.write("✅", career)

        st.write("")
        st.subheader("Type Meaning")
        st.write(f"- **1st letter:** {mbti[0]} orientation")
        st.write(f"- **2nd letter:** {mbti[1]} information style")
        st.write(f"- **3rd letter:** {mbti[2]} decision style")
        st.write(f"- **4th letter:** {mbti[3]} lifestyle preference")

# ----------------- ABOUT ----------------- #
else:
    st.title("About PersonaLens AI")
    st.write("""
PersonaLens AI is a Streamlit-based personality assessment app.

It includes:
- Modern user interface
- MBTI personality test
- 4-dimension scoring
- Personality type report
- Career suggestions
- Reset and rerun support
    """)
    st.write("---")
    st.caption("© 2026 PersonaLens AI")
