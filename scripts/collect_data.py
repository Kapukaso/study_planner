"""
Script to collect and prepare academic dataset for fine-tuning.
Datasets: 
- SQuAD v2 (Questions)
- AutoMathText (Math/Formulas/Concepts)
- MedQuAD (Definitions)
"""
import pandas as pd
from datasets import load_dataset
import os

# Target categories mapping
# 0: concept, 1: definition, 2: formula, 3: example, 4: pyq, 5: highlight, 6: summary

def collect_data():
    print("Collecting SQuAD v2 for 'pyq'...")
    squad = load_dataset("rajpurkar/squad_v2", split="train", trust_remote_code=True)
    questions = pd.DataFrame({"text": squad["question"], "label": 4})
    questions = questions.sample(min(2000, len(questions))) # Limit for demo
    
    print("Collecting MedQuAD for 'definition'...")
    # Using a subset of MedQuAD for definitions
    med = load_dataset("lavita/MedQuAD", split="train", trust_remote_code=True)
    # Questions like "What is (a) ..." are essentially definition requests
    definitions = pd.DataFrame({"text": med["answer"], "label": 1})
    definitions = definitions.sample(min(2000, len(definitions)))
    
    print("Collecting AutoMathText for 'formula' and 'concept'...")
    # Fix: Use correct config name 'web-full' or similar
    math = load_dataset("math-ai/AutoMathText", "web-full", split="train", streaming=True, trust_remote_code=True)
    
    formula_data = []
    concept_data = []
    
    count = 0
    for item in math:
        text = item["text"]
        if not text or len(text) < 50: continue
        
        # Heuristic split for this demo collection
        if any(sym in text for sym in ["=", "\\", "^", "sqrt"]):
            formula_data.append({"text": text[:500], "label": 2})
        else:
            concept_data.append({"text": text[:500], "label": 0})
            
        count += 1
        if count >= 4000: break
        
    formulas = pd.DataFrame(formula_data)
    concepts = pd.DataFrame(concept_data)
    
    # Merge all
    df = pd.concat([questions, definitions, formulas, concepts])
    
    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    output_path = "data/train.csv"
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path} with {len(df)} samples.")

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    collect_data()
