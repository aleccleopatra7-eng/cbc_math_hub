import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from fractions import Fraction
from datetime import datetime
from sympy import symbols, Eq, solve
from streamlit_autorefresh import st_autorefresh

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

# -------------------------
# GROUP SPACE
# -------------------------
st.sidebar.subheader("Group Space")
group_name = st.sidebar.text_input("Enter Group Name (optional)")

if st.sidebar.button("Join/Create Group"):
    if not learner_name.strip():
        st.sidebar.error("Enter your name first")
    else:
        st.session_state.learner_name = learner_name
        if group_name.strip():
            st.session_state.group_name = group_name
            file = f"groups/{group_name}.json"

            if os.path.exists(file):
                with open(file) as f:
                    group_data = json.load(f)
            else:
                group_data = {"members": [], "scores": {}, "messages": []}

            if learner_name not in group_data["members"]:
                group_data["members"].append(learner_name)

            with open(file,"w") as f:
                json.dump(group_data, f)

            st.sidebar.success(f"Joined {group_name}")
        else:
            st.sidebar.success(f"Logged in as {learner_name}")

# -------------------------
# LOAD SCORES
# -------------------------
score_file = f"scores/{learner_name}.json"
if os.path.exists(score_file):
    with open(score_file) as f:
        scores = json.load(f)
else:
    scores = {}
    with open(score_file,"w") as f:
        json.dump(scores,f)

# -------------------------
# MAIN SYSTEM
# -------------------------
if learner_name:

    grade = st.selectbox("Select Grade", list(CBC_TOPICS.keys()))
    topics = CBC_TOPICS[grade]

    st.subheader(f"{grade} Topics")
    for strand, subs in topics.items():
        with st.expander(strand):
            for s in subs:
                st.write("-", s)

    chosen_strand = st.selectbox("Strand", list(topics.keys()))
    chosen_topic = st.selectbox("Topic", topics[chosen_strand])

    st.markdown("## 🧠 Concept Lab")

    # -------------------------
    # CONCEPT LAB
    # -------------------------
    def concept_lab():

        if chosen_strand == "Numbers":
            st.subheader("Numbers Lab")
            n = st.number_input("Enter number", 1, 500)

            st.write("Even" if n%2==0 else "Odd")

            if n>1 and all(n%i!=0 for i in range(2,int(math.sqrt(n))+1)):
                st.write("Prime")
            else:
                st.write("Not prime")

            st.write("Factors:", [i for i in range(1,n+1) if n%i==0])

        elif chosen_strand == "Fractions/Decimals":
            st.subheader("Fractions Lab")

            n1 = st.number_input("Num1",1,20)
            d1 = st.number_input("Den1",1,20)
            n2 = st.number_input("Num2",1,20)
            d2 = st.number_input("Den2",1,20)

            f1 = Fraction(n1,d1)
            f2 = Fraction(n2,d2)

            st.write(f1,"+",f2,"=",f1+f2)
            st.write(f1,"-",f2,"=",f1-f2)
            st.write(f1,"×",f2,"=",f1*f2)
            st.write(f1,"÷",f2,"=",f1/f2)

        elif chosen_strand == "Algebra":
            st.subheader("Algebra Lab")

            eq = st.text_input("Enter equation (2*x+3=7)")

            if eq:
                try:
                    x = symbols('x')
                    left,right = eq.split("=")
                    solution = solve(Eq(eval(left), eval(right)), x)

                    st.success(f"x = {solution[0]}")

                    x_vals = np.linspace(-10,10,400)
                    y_vals = [eval(left.replace("x",str(val))) for val in x_vals]

                    fig, ax = plt.subplots()
                    ax.plot(x_vals, y_vals)
                    ax.axhline(eval(right), linestyle="--")
                    ax.grid()
                    st.pyplot(fig)

                except:
                    st.error("Invalid format")

        elif chosen_strand == "Geometry":
            st.subheader("Geometry Lab")

            a1 = st.slider("Angle 1",0,180)
            a2 = st.slider("Angle 2",0,180)

            total = a1+a2
            st.write("Sum:", total)

            if total==180:
                st.success("Straight line")
            elif total==90:
                st.success("Complementary")

            fig, ax = plt.subplots()
            ax.bar(["A1","A2"],[a1,a2])
            st.pyplot(fig)

        elif chosen_strand == "Measurement":
            st.subheader("Measurement Lab")

            l = st.number_input("Length",1,100)
            w = st.number_input("Width",1,100)
            h = st.number_input("Height",1,100)

            st.write("Area:", l*w)
            st.write("Perimeter:", 2*(l+w))
            st.write("Volume:", l*w*h)

        elif "Statistics" in chosen_strand or "Probability" in chosen_strand:
            st.subheader("Statistics Lab")

            data = st.text_input("Enter numbers (comma separated)")

            if data:
                nums = [float(x) for x in data.split(",")]

                st.write("Mean:", sum(nums)/len(nums))
                st.write("Max:", max(nums))
                st.write("Min:", min(nums))

                fig, ax = plt.subplots()
                ax.hist(nums)
                st.pyplot(fig)

                success = st.slider("Success count",0,len(nums))
                st.write("Probability:", success/len(nums))

        elif chosen_strand == "Financial Maths":
            st.subheader("Financial Lab")

            p = st.number_input("Amount",1,10000)
            r = st.number_input("Rate %",1,100)
            t = st.number_input("Time",1,10)

            interest = p*r*t/100

            st.write("Interest:", interest)
            st.write("Total:", p+interest)

        elif chosen_strand == "Problem Solving":
            st.subheader("Problem Solving")

            prob = st.text_area("Enter problem")

            if prob:
                st.write("1. Understand")
                st.write("2. Plan")
                st.write("3. Solve")
                st.write("4. Check")

    concept_lab()

# -------------------------
# GROUP CHAT
# -------------------------
if st.session_state.group_name:

    file = f"groups/{st.session_state.group_name}.json"

    if os.path.exists(file):
        with open(file) as f:
            group_data = json.load(f)
    else:
        group_data = {"members": [], "scores": {}, "messages": []}

    st.subheader(f"Group: {st.session_state.group_name}")
    st.write("Members:", group_data["members"])

    group_data["scores"][learner_name] = scores
    with open(file,"w") as f:
        json.dump(group_data,f)

    st.write("### Leaderboard")
    leaderboard = {k:sum(v.values()) for k,v in group_data["scores"].items()}
    for k,v in sorted(leaderboard.items(), key=lambda x:x[1], reverse=True):
        st.write(f"{k}: {v}")

    msg = st.text_input("Message", key="chat_input")
    if st.button("Send"):
        if msg.strip():
            group_data["messages"].append({
                "user": learner_name,
                "message": msg,
                "time": str(datetime.now())
            })
            with open(file,"w") as f:
                json.dump(group_data,f)
            st.experimental_rerun()

    st.write("### Chat")
    for m in group_data["messages"][-10:]:
        st.write(f"{m['time'].split('.')[0]} - {m['user']}: {m['message']}")

    st_autorefresh(interval=5000, key="refresh")
