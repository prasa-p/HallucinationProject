import torch
import streamlit as st
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import CrossEncoder
from scipy.stats import entropy

# --- CONFIGURATION ---
HF_TOKEN = st.secrets["HUGGINGFACE_TOKEN"]
MODEL_ID = "gpt2" 
# Use "cpu" if you don't have a GPU, but it will be slow. Use "cuda" for NVIDIA GPU.
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading models on {DEVICE}... this may take a minute.")

# 1. Load the Generator (Llama-)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, 
    token=HF_TOKEN, 
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map="auto" if DEVICE == "cuda" else None
)
if DEVICE == "cpu": model.to("cpu")

# 2. Load the Consistency Checker (NLI Model)
# We use a Cross-Encoder that predicts: 0=Contradiction, 1=Entailment, 2=Neutral
nli_model = CrossEncoder('cross-encoder/nli-deberta-v3-base')

print("System ready.")

# --- MODULE A: GENERATOR ---
def get_llama_response(prompt):
    """
    Generates a single response and captures the raw scores (logits)
    for the 'Sweat Test'.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=100, 
            return_dict_in_generate=True, 
            output_scores=True,  # Crucial: This gives us the raw math!
            temperature=0.7,
            do_sample=True
        )

    # Decode the answer text
    generated_ids = outputs.sequences[0]
    response_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
    
    # Extract only the newly generated part (remove input prompt)
    response_only = response_text.replace(prompt, "").strip()
    
    # Get the logits (raw scores) for the generated tokens
    # Stack them into a tensor: (Sequence Length, Vocabulary Size)
    logits = torch.stack(outputs.scores, dim=1).squeeze(0)
    
    return response_only, logits

# --- MODULE B1: UNCERTAINTY (THE SWEAT TEST) ---
def calculate_entropy(logits):
    """
    Calculates the average Shannon Entropy of the generated tokens.
    High Entropy = High Uncertainty (The model was 'sweating').
    """
    # Convert logits to probabilities using Softmax
    probs = torch.nn.functional.softmax(logits, dim=-1)
    
    # Move to CPU for numpy calculation
    probs = probs.cpu().numpy()
    
    # Calculate entropy for each token step: -sum(p * log(p))
    # axis=1 calculates it across the vocabulary for each token
    token_entropies = entropy(probs, axis=1)
    
    # Average the entropy over the whole sentence
    avg_entropy = np.mean(token_entropies)
    
    return avg_entropy

# --- MODULE B2: CONSISTENCY (THE STORY TEST) ---
def check_consistency(prompt):
    """
    Asks the model the same question 3 times (reduced from 5 for speed)
    and checks if the answers agree using an NLI model.
    """
    samples = []
    print("  Running Story Test (Sampling)...")
    
    # Generate 3 samples
    for _ in range(3):
        inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
        out = model.generate(**inputs, max_new_tokens=100, do_sample=True, temperature=0.7)
        text = tokenizer.decode(out[0], skip_special_tokens=True).replace(prompt, "").strip()
        samples.append(text)

    # Compare pairs: (Sample 1 vs 2), (Sample 1 vs 3), (Sample 2 vs 3)
    pairs = []
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            pairs.append((samples[i], samples[j]))

    # Predict Entailment (Does A agree with B?)
    # The model outputs scores for [Contradiction, Entailment, Neutral]
    scores = nli_model.predict(pairs)
    
    # We only care about the "Entailment" score (Index 1)
    # Higher entailment score means they agree.
    entailment_scores = scores[:, 1] 
    
    # Average consistency score (0 to 1 ideally, though logits can vary)
    avg_consistency = np.mean(entailment_scores)
    
    return avg_consistency

# --- MODULE C: THE JUDGE ---
def get_risk_score(entropy_score, consistency_score):
    """
    Decides if the response is HIGH RISK or LOW RISK.
    Current Logic: 
    - If Entropy is HIGH (> 3.0) -> Confused -> Risk
    - If Consistency is LOW (< 2.0) -> Changing Story -> Risk
    """
    # Thresholds (You will tune these after your first few tests!)
    ENTROPY_THRESHOLD = 3.5  # If higher than this, it's risky
    CONSISTENCY_THRESHOLD = 0.5 # If lower than this, it's risky
    
    risk_reasons = []
    
    if entropy_score > ENTROPY_THRESHOLD:
        risk_reasons.append("High Uncertainty (Math)")
        
    if consistency_score < CONSISTENCY_THRESHOLD:
        risk_reasons.append("Inconsistent Answers (Story)")
        
    if len(risk_reasons) > 0:
        return "HIGH RISK", risk_reasons
    else:
        return "LOW RISK", ["Safe"]

# --- TEST BLOCK (Run this file directly to check) ---
if __name__ == "__main__":
    test_prompt = "Who directed the movie The Godfather?"
    
    print(f"\n--- Analyzing: '{test_prompt}' ---")
    
    # 1. Get Response & Logic
    ans, logits = get_llama_response(test_prompt)
    print(f"AI Answer: {ans}")
    
    # 2. Sweat Test
    ent_score = calculate_entropy(logits)
    print(f"Entropy Score: {ent_score:.4f}")
    
    # 3. Story Test
    # consistency = check_consistency(test_prompt) 
    # (Commented out for speed during simple test, uncomment to run full logic)
    consistency = 2.5 # Fake score for testing logic
    print(f"Consistency Score: {consistency:.4f}")
    
    # 4. Judge
    verdict, reasons = get_risk_score(ent_score, consistency)
    print(f"FINAL VERDICT: {verdict}")
    print(f"Reasons: {reasons}")