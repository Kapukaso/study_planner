
"""ML-based content classification using spaCy."""
import spacy
from typing import Tuple, Dict, Any

class MLClassifier:
    """Uses spaCy for advanced linguistic analysis and classification."""
    
    def __init__(self, model: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            # Fallback if model not downloaded
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", model])
            self.nlp = spacy.load(model)
            
    def analyze_linguistics(self, text: str) -> Dict[str, Any]:
        """Analyze linguistic features of the text."""
        doc = self.nlp(text)
        
        # Count POS tags
        pos_counts = {}
        for token in doc:
            pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1
            
        # Check for sentence types
        is_interrogative = any(sent.text.strip().endswith('?') for sent in doc.sents)
        
        # Check for definition patterns (Subject-Verb-Complement)
        has_definition_syntax = self._check_definition_syntax(doc)
        
        # Check for imperative sentences (Instructions/Examples)
        has_imperative = self._check_imperative(doc)
        
        return {
            'pos_counts': pos_counts,
            'is_interrogative': is_interrogative,
            'has_definition_syntax': has_definition_syntax,
            'has_imperative': has_imperative,
            'sentence_count': len(list(doc.sents)),
            'token_count': len(doc)
        }
        
    def _check_definition_syntax(self, doc) -> bool:
        """Check for common definition syntax like 'X is a Y' or 'X refers to Y'."""
        for sent in doc.sents:
            has_subject = False
            has_copula = False # 'is', 'are'
            has_refers = False # 'refers to', 'defined as'
            
            for token in sent:
                if token.dep_ == "nsubj":
                    has_subject = True
                if token.lemma_ in ["be", "mean", "define"]:
                    has_copula = True
                if token.lemma_ in ["refer"]:
                    has_refers = True
                    
            if has_subject and (has_copula or has_refers):
                return True
        return False
        
    def _check_imperative(self, doc) -> bool:
        """Check for imperative verbs (often used in examples or instructions)."""
        for sent in doc.sents:
            # Check if the first non-punctuation token is a base form verb
            for token in sent:
                if token.is_punct:
                    continue
                if token.pos_ == "VERB" and token.dep_ == "ROOT" and token.tag_ == "VB":
                    return True
                break
        return False

    def get_ml_scores(self, text: str) -> Dict[str, float]:
        """Get confidence scores based on ML analysis."""
        analysis = self.analyze_linguistics(text)
        scores = {
            'definition': 0.0,
            'pyq': 0.0,
            'example': 0.0,
            'concept': 0.0,
            'formula': 0.0,
            'highlight': 0.0,
            'summary': 0.0
        }
        
        # Definition score
        if analysis['has_definition_syntax']:
            scores['definition'] += 0.7
        if analysis['pos_counts'].get('NOUN', 0) >= 2 and analysis['pos_counts'].get('VERB', 0) >= 1:
            scores['definition'] += 0.2
            
        # Question score (Only if not imperative)
        if analysis['is_interrogative']:
            scores['pyq'] += 0.8
        if any(token.tag_ == "WP" for token in self.nlp(text)): # Wh-pronoun
            scores['pyq'] += 0.2
            
        # Example score
        if analysis['has_imperative'] and not analysis['is_interrogative']:
            scores['example'] += 0.7
        if analysis['sentence_count'] > 1 and analysis['has_imperative']:
            scores['example'] += 0.2
        if "calculate" in text.lower() or "consider" in text.lower():
            scores['example'] += 0.3
            
        # Formula score
        if analysis['token_count'] < 20 and analysis['pos_counts'].get('SYM', 0) > 0:
            scores['formula'] += 0.4
            
        # Concept score
        if analysis['sentence_count'] >= 2:
            scores['concept'] += 0.3
        if analysis['pos_counts'].get('ADJ', 0) > 1:
            scores['concept'] += 0.2
            
        return {k: min(v, 1.0) for k, v in scores.items()}
