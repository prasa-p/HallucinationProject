import streamlit as st
import pandas as pd
import random
import time
from questions_data import experiment_data

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AI Fact-Checker Experiment", layout="centered")

# --- SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'intro' # Options: intro, game, post_survey, debrief
if 'group' not in st.session_state:
    # Randomly assign user to Group A (Control) or Group B (Experimental)
    st.session_state.group = random.choice(['A', 'B'])
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {} # Stores demographic info
if 'game_results' not in st.session_state:
    st.session_state.game_results = [] # Stores answers to 20 questions
if 'shuffled_questions' not in st.session_state:
    # Shuffle questions once per session so order is random
    q_copy = experiment_data.copy()
    random.shuffle(q_copy)
    st.session_state.shuffled_questions = q_copy

# --- PAGE 1: INTRODUCTION & PRE-SURVEY ---
if st.session_state.page == 'intro':
    st.title("AI Fact-Checker Study")
    st.write("Welcome! In this experiment, you will act as a 'Fact Checker' for an AI.")
    st.info("Your data will be anonymized. Please answer honestly.")

    st.markdown("""
    ### 📋 Your Mission
    AI models (like ChatGPT or Gemini) sometimes confidently make up fake information, known as **hallucinations**. 

    In this study, you are the final editor. You will review **20 short questions** answered by an AI. 
    * 🟢 **Publish:** Click this if you believe the AI's answer is a **Fact**.
    * 🔴 **Reject:** Click this if you believe the AI is **Hallucinating** (lying).

    *Note: You don't need to be a trivia expert! Just use your best judgment. The whole process takes about 3-5 minutes.*
    """)
    st.divider() 

    # Section 1: Demographics
    st.subheader("Part 1: About You")
    area_study = st.selectbox("Current Area of Study/Expertise", 
                              ["Computer Science/Engineering", "Natural Sciences", "Humanities/Arts", "Business", "Other"])
    age_group = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45+"])
    
    # Section 2: AI Familiarity
    ai_freq = st.radio("How often do you use AI tools (ChatGPT, Gemini, etc.)?", 
                       ["Daily", "Weekly", "Rarely", "Never"])
    
    # Section 3: AI Literacy (The "Mental Model" Question)
    ai_model = st.radio("To the best of your knowledge, how does an AI generate answers?",
                        ["A) It searches a database of facts (Database Retrieval)",
                         "B) It predicts the likely next word based on patterns (Next-Token Prediction)",
                         "C) It thinks like a human (Human Emulation)",
                         "D) I don't know"])
    
    # Section 4: Baseline Trust
    trust_level = st.slider("Generally, how accurate do you believe AI models are?", 1, 5)

    if st.button("Start Experiment"):
        # Save Pre-Survey Data
        st.session_state.user_data = {
            "group": st.session_state.group,
            "study_area": area_study,
            "age": age_group,
            "frequency": ai_freq,
            "mental_model": ai_model,
            "baseline_trust": trust_level
        }
        st.session_state.page = 'game'
        st.rerun()

# --- PAGE 2: THE GAME (20 QUESTIONS) ---
elif st.session_state.page == 'game':
    # Progress Bar
    progress = st.session_state.current_q_index / 20
    st.progress(progress)
    st.write(f"Question {st.session_state.current_q_index + 1} of 20")

    # Get current question
    q_data = st.session_state.shuffled_questions[st.session_state.current_q_index]

    # --- DISPLAY LOGIC (THE A/B TEST) ---
    st.markdown("### User Query:")
    st.write(q_data['prompt'])
    
    st.markdown("### AI Response:")
    st.info(q_data['ai_answer'])

    # --- GROUP B ONLY: THE SUPERVISOR WARNING ---
    if st.session_state.group == 'B':
        st.markdown("---")
        st.markdown("**🛡️ Supervisor AI Analysis:**")
        
        if q_data['is_hallucination']:
            # Show RED Warning
            st.error("⚠️ **HIGH RISK DETECTED**")
            st.caption("The system detected high uncertainty and inconsistency in this answer.")
        else:
            # Show GREEN Safe Label
            st.success("✅ **LOW RISK (Verified)**")
            st.caption("The system indicates this answer is consistent and confident.")
    
    st.markdown("---")
    
    # User Decision Inputs
    decision = st.radio("What is your decision?", ["Publish (I believe this is true)", "Reject (I believe this is a hallucination)", "I don't know"], key=f"dec_{st.session_state.current_q_index}")
    confidence = st.slider("How confident are you?", 0, 5, key=f"conf_{st.session_state.current_q_index}")

    if st.button("Next Question"):
        # Save Result
        is_correct = False
        # If it's a Fact (False Hallucination) and they Publish -> Correct
        if not q_data['is_hallucination'] and "Publish" in decision:
            is_correct = True
        # If it's a Hallucination (True) and they Reject -> Correct
        elif q_data['is_hallucination'] and "Reject" in decision:
            is_correct = True
        
        st.session_state.game_results.append({
            "q_id": q_data['id'],
            "is_hallucination": q_data['is_hallucination'],
            "user_decision": decision,
            "confidence": confidence,
            "user_is_correct": is_correct
        })

        # Move to next or finish
        if st.session_state.current_q_index < 19:
            st.session_state.current_q_index += 1
            st.rerun()
        else:
            st.session_state.page = 'post_survey'
            st.rerun()

# --- PAGE 3: POST-SURVEY ---
elif st.session_state.page == 'post_survey':
    st.title("Final Feedback")
    st.write("You have completed the task! Just a few final questions.")

    difficulty = st.slider("How difficult was it to distinguish facts from hallucinations?", 1, 5)
    
    strategy = st.radio("What strategy did you primarily use?",
                        ["Intuition/Prior Knowledge", "Plausibility Checking (Did it sound logical?)", "Guessing", "External Verification"])
    
    # Group B Specific Questions
    relied_on_warning = "N/A"
    warning_feedback = "N/A"
    
    if st.session_state.group == 'B':
        st.subheader("Tool Evaluation")
        relied_on_warning = st.slider("How much did you rely on the Risk Warnings?", 1, 5)
        warning_feedback = st.text_area("If you could change one thing about how the risk was presented, what would it be?")

    if st.button("Submit All Data"):
        # Combine all data into one CSV record
        correct_count = sum([r['user_is_correct'] for r in st.session_state.game_results])
        
        final_data = {
            **st.session_state.user_data,
            "score": correct_count,
            "difficulty": difficulty,
            "strategy": strategy,
            "relied_on_warning": relied_on_warning,
            "feedback": warning_feedback
        }
        
        # Convert to DataFrame and Append to CSV
        df = pd.DataFrame([final_data])
        
        try:
            df.to_csv("results.csv", mode='a', header=False, index=False)
        except FileNotFoundError:
            df.to_csv("results.csv", mode='w', header=True, index=False)
            
        st.session_state.page = 'debrief'
        st.rerun()

# --- PAGE 4: DEBRIEF & THANK YOU ---
elif st.session_state.page == 'debrief':
    st.balloons()
    st.title("Thank you for your participation!")
    st.success("Your data has been saved anonymously.")
    
    st.markdown("""
    ### Study Debrief
    The true purpose of this study was to measure **"Trust Calibration"**—how well users can identify AI hallucinations. 
    
    To test this, participants were randomly placed into one of two groups:
    * **Group A (Control):** Saw only the AI's text answers.
    * **Group B (Experimental):** Saw the AI's answers alongside visual "Warning Labels" indicating the likelihood of a hallucination (calculated behind the scenes using the AI's mathematical uncertainty and consistency).
    
    We are comparing the accuracy between these two groups to see if visual UI warnings effectively improve human trust in AI systems. 
    
    If you have any questions about this research or would like a summary of the final results, please contact the Student Investigator at **pira8349@mylaurier.ca**.
    
    **You may now close this tab.**
    """)