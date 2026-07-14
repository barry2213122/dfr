import streamlit as st
import random

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="PersonaLens AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
body{
    background:linear-gradient(135deg,#090909,#151d35);
}
.main-title{
    font-size:55px;
    text-align:center;
    font-weight:800;
    color:#66FCF1;
}

.sub{
    text-align:center;
    color:#d0d0d0;
    font-size:20px;
}

.card{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:18px;
    padding:25px;
    backdrop-filter:blur(12px);
}

.metric{
    text-align:center;
    font-size:35px;
    color:#66FCF1;
    font-weight:bold;
}

.small{
    text-align:center;
    color:#bfbfbf;
}

hr{
    border:1px solid #333;
}
</style>
""",unsafe_allow_html=True)

# ---------------- DATABASE ---------------- #

questions=[
("I enjoy meeting new people.","Extraversion"),
("I stay calm under pressure.","Emotional Stability"),
("I enjoy solving difficult problems.","Openness"),
("I like leading teams.","Leadership"),
("I finish work before deadlines.","Discipline"),
("I easily understand other people's emotions.","Empathy"),
("I like trying new things.","Creativity"),
("I think before speaking.","Communication"),
("I enjoy taking responsibility.","Confidence"),
("I keep my promises.","Conscientiousness"),
("I recover quickly from failure.","Resilience"),
("I enjoy public speaking.","Confidence"),
("I learn quickly.","Learning"),
("I like planning everything.","Discipline"),
("I stay positive during challenges.","Optimism")
]

traits={}

for q in questions:
    traits[q[1]]=0

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🧠 PersonaLens AI")

page=st.sidebar.radio(
"Navigation",
[
"🏠 Home",
"📝 Personality Test",
"📊 Results",
"ℹ About"
]
)

st.sidebar.write("---")

st.sidebar.info("Built using Python + Streamlit")

# ---------------- HOME ---------------- #

if page=="🏠 Home":

    st.markdown("<div class='main-title'>PersonaLens AI</div>",unsafe_allow_html=True)

    st.markdown("<div class='sub'>Discover your personality using interactive psychological questions.</div>",unsafe_allow_html=True)

    st.write("")

    c1,c2,c3=st.columns(3)

    with c1:
        st.markdown("""
<div class="card">
<div class="metric">100+</div>
<div class="small">Questions</div>
</div>
""",unsafe_allow_html=True)

    with c2:
        st.markdown("""
<div class="card">
<div class="metric">15</div>
<div class="small">Traits</div>
</div>
""",unsafe_allow_html=True)

    with c3:
        st.markdown("""
<div class="card">
<div class="metric">AI</div>
<div class="small">Analysis</div>
</div>
""",unsafe_allow_html=True)

    st.write("")

    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3",use_container_width=True)

    st.write("")

    st.success("Click Personality Test from the sidebar to begin.")

# ---------------- TEST ---------------- #

elif page=="📝 Personality Test":

    st.title("Personality Assessment")

    st.progress(0.35)

    answers=[]

    options=[
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly Agree"
    ]

    score_map={
    "Strongly Disagree":1,
    "Disagree":2,
    "Neutral":3,
    "Agree":4,
    "Strongly Agree":5
    }

    for i,(question,trait) in enumerate(questions):

        st.write(f"### Q{i+1}. {question}")

        ans=st.radio(
        "",
        options,
        key=i
        )

        answers.append((trait,score_map[ans]))

    if st.button("Generate Report"):

        for t,s in answers:
            traits[t]+=s

        st.session_state["traits"]=traits

        st.success("Assessment Completed!")

        st.balloons()

# ---------------- RESULTS ---------------- #

elif page=="📊 Results":

    st.title("Your Personality Report")

    if "traits" not in st.session_state:

        st.warning("Complete the test first.")

    else:

        traits=st.session_state["traits"]

        st.write("## Trait Scores")

        for k,v in traits.items():

            percent=min(int(v/25*100),100)

            st.write(k)

            st.progress(percent/100)

            st.write(f"{percent}%")

        dominant=max(traits,key=traits.get)

        st.write("---")

        st.subheader("Dominant Personality Trait")

        st.success(dominant)

        descriptions={
        "Leadership":"You naturally guide others.",
        "Confidence":"You believe in your abilities.",
        "Empathy":"You understand people's emotions.",
        "Creativity":"You enjoy innovation.",
        "Discipline":"You stay organized.",
        "Communication":"You express yourself well.",
        "Openness":"You enjoy new experiences.",
        "Learning":"You love learning.",
        "Resilience":"You recover from setbacks.",
        "Optimism":"You look at the brighter side.",
        "Conscientiousness":"You are dependable.",
        "Extraversion":"You enjoy social interaction.",
        "Emotional Stability":"You remain calm under stress."
        }

        st.info(descriptions.get(dominant,"Balanced personality."))

        st.write("### Career Suggestions")

        careers={
        "Leadership":["CEO","Manager","Entrepreneur"],
        "Creativity":["Designer","Artist","Architect"],
        "Confidence":["Sales","Public Speaker","Lawyer"],
        "Empathy":["Psychologist","Teacher","Doctor"],
        "Discipline":["Engineer","Pilot","Accountant"]
        }

        if dominant in careers:

            for c in careers[dominant]:
                st.write("✅",c)

        else:

            st.write("Research, Business, Technology")

# ---------------- ABOUT ---------------- #

else:

    st.title("About PersonaLens AI")

    st.write("""
PersonaLens AI is a modern personality assessment platform
built using Streamlit.

Features:

- Beautiful UI
- Personality Questions
- Progress Tracking
- Trait Analysis
- Career Suggestions
- Interactive Dashboard

Future Version:

- 100 Questions
- Radar Charts
- PDF Report
- AI Analysis
- Login System
- Database
- Dark/Light Mode
- Animated Dashboard
""")

    st.write("---")

    st.caption("© 2026 PersonaLens AI")
