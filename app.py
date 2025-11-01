import streamlit as st
from groq import Groq
import os
import random

# -------------------------------
# CONFIGURATION
# -------------------------------
st.set_page_config(page_title="AI Quiz Adventure 🎮", page_icon="🧠", layout="centered")
st.title("🧠 AI Quiz Adventure (Groq + Streamlit)")

# -------------------------------
# SETUP API CLIENT
# -------------------------------
api_key = st.text_input("🔑 Enter your Groq API key:", type="password")

if api_key:
    client = Groq(api_key=api_key)

    # -------------------------------
    # GAME STATE
    # -------------------------------
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "question" not in st.session_state:
        st.session_state.question = None
    if "correct_answer" not in st.session_state:
        st.session_state.correct_answer = None
    if "question_num" not in st.session_state:
        st.session_state.question_num = 1

    # -------------------------------
    # FUNCTION TO GET AI QUESTION
    # -------------------------------
    def get_ai_question():
        topics = ["science", "history", "math", "sports", "geography"]
        topic = random.choice(topics)
        prompt = f"Create a single {topic} multiple-choice question with 4 options. Mark the correct option with (*). Keep it concise."

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        return content

    # -------------------------------
    # GENERATE QUESTION
    # -------------------------------
    if st.button("🧩 New Question"):
        q_data = get_ai_question()

        # Parse question and options
        lines = q_data.strip().split("\n")
        question = lines[0]
        options = [line for line in lines[1:] if line.strip()]
        correct = [opt for opt in options if "(*)" in opt]
        if correct:
            correct_answer = correct[0].replace("(*)", "").strip()
        else:
            correct_answer = None

        st.session_state.question = question
        st.session_state.correct_answer = correct_answer
        st.session_state.options = [opt.replace("(*)", "").strip() for opt in options]

        st.session_state.question_num += 1

    # -------------------------------
    # DISPLAY QUESTION
    # -------------------------------
    if st.session_state.question:
        st.subheader(f"Question {st.session_state.question_num - 1}")
        st.write(st.session_state.question)

        selected = st.radio("Choose your answer:", st.session_state.options, index=None)

        if st.button("✅ Submit Answer"):
            if selected == st.session_state.correct_answer:
                st.success("🎉 Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct answer was: {st.session_state.correct_answer}")

        st.metric("Score", st.session_state.score)

else:
    st.info("Please enter your Groq API key above to start the game.")

st.caption("🚀 Powered by Streamlit + Groq AI")
