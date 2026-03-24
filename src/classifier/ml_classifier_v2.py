"""Fine-tuned ML-based content classification using Hugging Face."""
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict

class FineTunedClassifier:
    """Uses fine-tuned DistilBERT for academic content classification."""
    
    def __init__(self, model_dir: str = "models/academic_classifier"):
        self.model_dir = model_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.is_loaded = False
        
        # We will load the model lazily to prevent blocking startup if weights aren't ready
        if os.path.exists(model_dir):
            self.load_model()
            
    def load_model(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_dir)
            self.model.to(self.device)
            self.model.eval()
            self.is_loaded = True
        except Exception as e:
            print(f"Warning: Could not load fine-tuned model from {self.model_dir}: {e}")
            self.is_loaded = False

    def get_ml_scores(self, text: str) -> Dict[str, float]:
        """Get confidence scores from the fine-tuned model."""
        # Fallback to zero scores if model isn't trained yet
        if not self.is_loaded:
            return {
                'concept': 0.0, 'definition': 0.0, 'formula': 0.0, 
                'example': 0.0, 'pyq': 0.0, 'highlight': 0.0, 'summary': 0.0
            }
            
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Apply softmax to get probabilities
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
            
        # Map probabilities back to labels
        scores = {}
        for i, prob in enumerate(probabilities):
            label = self.model.config.id2label[i]
            scores[label] = float(prob.cpu().numpy())
            
        return scores
