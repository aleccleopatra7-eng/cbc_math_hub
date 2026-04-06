
import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import random
import uuid
from fractions import Fraction
from datetime import datetime
import time

# -------------------------
# PAGE SETTINGS
# -------------------------
st.set_page_config(page_title="Interactive Math Hub", page_icon="📊")

# -------------------------
# CREATE FOLDERS
# -------------------------
for f in ["scores", "groups", "feedback"]:
    os.makedirs(f, exist_ok=True)

# -------------------------
# SESSION STATE
# -------------------------
for key in ["learner_name", "group_name", "color_blind", "chat_input"]:
    if key not in st.session_state:
        st.session_state[key] = False

# -------------------------
# CBC TOPICS
# -------------------------
CBC_TOPICS = {
    "Grade 7": {
        "Numbers":["Whole numbers & operations","Even/Odd/Prime classification"],
        "Fractions/Decimals":["Simple fractions","Conversions","Comparing & ordering","Basic operations"],
        "Algebra":["Expressions","Simple linear equations","Patterns & generalisation","Using variables"],
        "Geometry":["Properties of 2D shapes","Angles & relationships","Symmetry & transformations"],
        "Measurement":["Length","Perimeter","Time","Unit conversions"],
        "Data/Probability":["Data collection","Charts & tables","Interpreting results","Introduction to probability"],
        "Problem Solving":["Real-life applications","Logical reasoning"]
    },
    "Grade 8": {
        "Numbers":["Operations with larger/negative numbers","Ratio, rates, proportions"],
        "Fractions/Decimals":["Advanced conversions","Discounts & interest calculations"],
        "Algebra":["Linear expressions & equations","Inequalities","Substitution & evaluation"],
        "Geometry":["Angle theorems","Properties of 2D & 3D shapes","Congruence & similarity","Area & perimeter extensions"],
        "Measurement":["Area & volume of solids","Composite shapes"],
        "Statistics/Probability":["Bar charts, pie charts","Mean, median, mode","Simple probability experiments"],
        "Financial Maths":["Budgeting","Profit & loss calculations"]
    },
    "Grade 9": {
        "Numbers":["Real numbers","Irrational numbers","Advanced operations & estimation"],
        "Algebra":["Linear functions & graphs","Algebraic simplification","Systems of equations"],
        "Geometry":["Advanced properties of shapes","Angles & proofs","Coordinate geometry basics"],
        "Measurement":["Surface area & volume of solids","Conversions & real-life measurement tasks"],
        "Statistics/Probability":["Interpreting survey data","Measures of central tendency","Probability rules"],
        "Problem Solving":["Higher-order multi-strand problems","Real-life mathematical modelling"]
    }
}

# -------------------------
# WELCOME
# -------------------------
st.markdown("<h1 style='text-align:center; color:orange;'>🎉 Welcome to My Math Interactive Hub</h1>", unsafe_allow_html=True)

# -------------------------
# SIDEBAR LOGIN
# -------------------------
st.sidebar.title("Learner Login")
learner_name = st.sidebar.text_input("Enter Your Name")
st.session_state.color_blind = st.sidebar.checkbox("🎨 Color-Blind Mode")
COLORS = {"A":"black","B":"gray","C":"blue","D":"purple"} if st.session_state.color_blind else {"A":"orange","B":"blue","C":"green","D":"red"}

# -------------------------
# GROUP SPACE
# -------------------------
st.sidebar.subheader("Group Space")
group_name = st.sidebar.text_input("Enter Group Name (optional)")
if st.sidebar.button("Join/Create Group"):
    if not learner_name.strip():
        st.sidebar.error("Please enter your name first")
    else:
        st.session_state.learner_name = learner_name
        if group_name.strip():
            st.session_state.group_name = group_name
            group_file = f"groups/{group_name}.json"
            if os.path.exists(group_file):
                with open(group_file) as f:
                    group_data = json.load(f)
            else:
                group_data = {"members": [], "scores": {}, "messages": []}
            if learner_name not in group_data["members"]:
                group_data["members"].append(learner_name)
            with open(group_file,"w") as f:
                json.dump(group_data, f)
            st.sidebar.success(f"Joined group: {group_name}")
        else:
            st.session_state.group_name = None
            st.sidebar.success(f"Logged in as {learner_name} (no group)")

# -------------------------
# LOAD/INIT SCORES
# -------------------------
score_file = f"scores/{learner_name}.json"
if os.path.exists(score_file):
    with open(score_file) as f:
        scores = json.load(f)
else:
    scores = {}
    with open(score_file,"w") as f:
        json.dump(scores, f)

# -------------------------
# GRADE & TOPICS
# -------------------------
if learner_name:
    grade = st.selectbox("Select Grade", list(CBC_TOPICS.keys()))
    topics_for_grade = CBC_TOPICS[grade]
    st.subheader(f"{grade} Topics")
    for strand, subtopics in topics_for_grade.items():
        with st.expander(f"{strand}"):
            for sub in subtopics:
                st.write(f"- {sub}")

    chosen_strand = st.selectbox("Select Strand", list(topics_for_grade.keys()))
    chosen_topic = st.selectbox("Select Topic", topics_for_grade[chosen_strand])
    st.markdown("### Practice Simulation")

    # -------------------------
    # SIMULATIONS FUNCTIONS
    # -------------------------
    def simulate_numbers():
        if grade=="Grade 7" and chosen_strand=="Numbers" and chosen_topic=="Whole numbers & operations":
            st.info("LCM & GCD Simulation")
            a = st.number_input("A",2,50)
            b = st.number_input("B",2,50)
            gcd = math.gcd(a,b)
            lcm = a*b//gcd
            factors_a = [i for i in range(1,a+1) if a%i==0]
            factors_b = [i for i in range(1,b+1) if b%i==0]
            multiples_a = [a*i for i in range(1,6)]
            multiples_b = [b*i for i in range(1,6)]
            st.write("Factors A:", factors_a)
            st.write("Factors B:", factors_b)
            st.write("Multiples A:", multiples_a)
            st.write("Multiples B:", multiples_b)
            st.success(f"GCD={gcd}, LCM={lcm}")
            fig, ax = plt.subplots()
            ax.scatter(factors_a,[1]*len(factors_a))
            ax.scatter(factors_b,[2]*len(factors_b))
            for val in factors_a:
                ax.text(val,1,str(val))
            for val in factors_b:
                ax.text(val,2,str(val))
            ax.grid(True)
            st.pyplot(fig)
        else:
            a, b = random.randint(1,100), random.randint(1,100)
            st.write(f"Compute: {a} + {b}")
            ans = st.number_input("Your answer", value=0)
            if st.button("Check Answer"):
                if ans == a+b:
                    st.success("Correct!")
                    scores[f"{grade}_{chosen_strand}_{chosen_topic}"] = scores.get(f"{grade}_{chosen_strand}_{chosen_topic}",0)+1
                else:
                    st.error(f"Incorrect. Correct: {a+b}")
                with open(score_file,"w") as f:
                    json.dump(scores,f)

    def simulate_fractions():
        a,b,c,d = random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10)
        st.write(f"Solve: ({a}/{b}) + ({c}/{d})")
        ans = st.text_input("Enter answer as fraction a/b (simplified)")
        if st.button("Check Answer"):
            correct = Fraction(a,b)+Fraction(c,d)
            if ans == str(correct):
                st.success("Correct!")
                scores[f"{grade}_{chosen_strand}_{chosen_topic}"] = scores.get(f"{grade}_{chosen_strand}_{chosen_topic}",0)+1
            else:
                st.error(f"Incorrect. Correct: {correct}")
            with open(score_file,"w") as f:
                json.dump(scores,f)

    def simulate_algebra():
        if grade=="Grade 9" and chosen_strand=="Algebra" and chosen_topic=="Systems of equations":
            st.info("Simultaneous Equations Simulation")
            a1 = st.number_input("a1", value=2)
            b1 = st.number_input("b1", value=3)
            c1 = st.number_input("c1", value=11)
            a2 = st.number_input("a2", value=1)
            b2 = st.number_input("b2", value=-1)
            c2 = st.number_input("c2", value=1)
            method = st.radio("Choose Method", ["Elimination","Substitution"])
            st.latex(f"{a1}x + {b1}y = {c1}")
            st.latex(f"{a2}x + {b2}y = {c2}")
            if st.button("Solve"):
                det = a1*b2 - a2*b1
                if det == 0:
                    st.error("No unique solution")
                else:
                    x = (c1*b2 - c2*b1)/det
                    y = (a1*c2 - a2*c1)/det
                    if method=="Elimination":
                        st.write("Step 1: Multiply equations to eliminate one variable")
                        st.write("Step 2: Subtract equations")
                        st.write("Step 3: Solve remaining variable")
                        st.write("Step 4: Substitute back")
                    else:
                        st.write("Step 1: Make one variable subject")
                        st.write("Step 2: Substitute into other equation")
                        st.write("Step 3: Solve")
                        st.write("Step 4: Substitute back")
                    st.success(f"Solution: x = {x}, y = {y}")
                    x_vals = np.linspace(x-10, x+10, 400)
                    if b1 != 0:
                        y1 = (c1 - a1*x_vals)/b1
                    else:
                        y1 = None
                    if b2 != 0:
                        y2 = (c2 - a2*x_vals)/b2
                    else:
                        y2 = None
                    fig, ax = plt.subplots()
                    if y1 is not None:
                        ax.plot(x_vals,y1,label="Eq1")
                    else:
                        ax.axvline(x=c1/a1,label="Eq1")
                    if y2 is not None:
                        ax.plot(x_vals,y2,label="Eq2")
                    else:
                        ax.axvline(x=c2/a2,label="Eq2")
                    ax.scatter(x,y,s=250)
                    ax.text(x,y,f"({x:.2f},{y:.2f})")
                    ax.legend()
                    ax.grid(True)
                    st.pyplot(fig)
        else:
            a = random.randint(1,10)
            x_correct = random.randint(1,10)
            b = random.randint(1,20)
            c = a*x_correct + b
            st.write(f"Solve for x: {a}x + {b} = {c}")
            x_input = st.number_input("x:", value=0)
            if st.button("Check Answer"):
                if x_input == x_correct:
                    st.success("Correct!")
                    scores[f"{grade}_{chosen_strand}_{chosen_topic}"] = scores.get(f"{grade}_{chosen_strand}_{chosen_topic}",0)+1
                else:
                    st.error(f"Incorrect. Correct: {x_correct}")
                with open(score_file,"w") as f:
                    json.dump(scores,f)

    # -------------------------
    # LINK TOPIC TO SIMULATION
    # -------------------------
    if "Numbers" in chosen_strand:
        simulate_numbers()
    elif "Fractions" in chosen_strand or "Decimals" in chosen_strand:
        simulate_fractions()
    elif "Algebra" in chosen_strand:
        simulate_algebra()
    else:
        st.info("Simulation coming soon for this topic!")

# -------------------------
# REAL-TIME GROUP CHAT
# -------------------------
if st.session_state.group_name:
    group_file = f"groups/{st.session_state.group_name}.json"
    if os.path.exists(group_file):
        with open(group_file) as f:
            group_data = json.load(f)
    else:
        group_data = {"members": [], "scores": {}, "messages": []}

    st.subheader(f"Group: {st.session_state.group_name}")
    st.write("**Members:**", group_data["members"])

    # Update leaderboard
    group_data["scores"][learner_name] = scores
    with open(group_file,"w") as f:
        json.dump(group_data,f)

    st.write("### Leaderboard")
    leaderboard = {}
    for member, mscores in group_data["scores"].items():
        total = sum(mscores.values())
        leaderboard[member] = total
    leaderboard_sorted = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))
    for k,v in leaderboard_sorted.items():
        st.write(f"{k}: {v} points")

    # Chat input
    msg_input = st.text_input("Send message", key="chat_input")
    if st.button("Post Message"):
        if msg_input.strip():
            group_data["messages"].append({
                "user": learner_name,
                "message": msg_input,
                "time": str(datetime.now())
            })
            with open(group_file,"w") as f:
                json.dump(group_data,f)
            st.session_state.chat_input = ""  # Clear input
            st.experimental_rerun()  # Refresh to show message immediately

    st.write("### Group Chat (Latest 10)")
    # Reload messages to show updates
    if os.path.exists(group_file):
        with open(group_file) as f:
            group_data = json.load(f)
    for msg in group_data["messages"][-10:]:
        st.write(f"{msg['time'].split('.')[0]} - {msg['user']}: {msg['message']}")

    # Auto-refresh every 5 seconds
    time.sleep(5)
    st.experimental_rerun()