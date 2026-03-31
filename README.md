# Hybrid Supervisor for LLM Hallucination Detection
**Student Name:** Prasa Pirabagaran
**Course:** CP493 - Directed Research Project

## Project Overview
This project implements a "Supervisor" system that detects hallucinations in Large Language Models (LLMs) by correlating **Predictive Uncertainty (Entropy)** and **Semantic Consistency**. It includes a user study interface to measure "Trust Calibration."

## File Structure
* `backend.py`: The core logic. Loads Llama-3, calculates Entropy and Consistency scores, and acts as the "Lie Detector."
* `app.py`: The Streamlit User Interface for the Controlled Experiment (A/B Test).
* `questions_data.py`: The static dataset of 20 Q&A pairs (10 Facts, 10 Hallucinations) used in the experiment.
* `results.csv`: Stores the anonymized data collected from the user study.

## Setup & Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt