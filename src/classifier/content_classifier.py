"""Content classifier - Hybrid classification engine."""
from typing import Tuple, Dict, List
from src.classifier.rules import (
    is_formula,
    is_definition,
    is_question,
    is_example,
    is_highlight,
    is_summary,
    is_concept
)
from src.classifier.ml_classifier import MLClassifier
from src.classifier.ml_classifier_v2 import FineTunedClassifier


class ContentClassifier:
    """Hybrid content classification engine (Rules + SpaCy + FineTuned BERT)."""
    
    def __init__(self):
        self.spacy_classifier = MLClassifier()
        self.bert_classifier = FineTunedClassifier()
        
        # Priority order for classification (most specific first)
        self.RULE_CLASSIFIERS = [
            ('formula', is_formula),
            ('definition', is_definition),
            ('pyq', is_question),
            ('example', is_example),
            ('highlight', is_highlight),
            ('summary', is_summary),
            ('concept', is_concept),
        ]
        
        # Weighting factors:
        # If the BERT model is loaded, we give it high weight.
        # Otherwise, we rely entirely on Rules + SpaCy.
        if self.bert_classifier.is_loaded:
            self.RULE_WEIGHT = 0.4
            self.SPACY_WEIGHT = 0.2
            self.BERT_WEIGHT = 0.4
        else:
            self.RULE_WEIGHT = 0.7
            self.SPACY_WEIGHT = 0.3
            self.BERT_WEIGHT = 0.0
    
    def classify_text(self, text: str) -> Tuple[str, float]:
        """
        Classify text into content type using hybrid approach.
        """
        if not text or len(text.strip()) < 10:
            return 'concept', 0.0
            
        # 1. Get Rule-based scores
        rule_scores = {}
        for content_type, classifier_func in self.RULE_CLASSIFIERS:
            _, confidence = classifier_func(text)
            rule_scores[content_type] = confidence
            
        # 2. Get SpaCy ML-based scores
        spacy_scores = self.spacy_classifier.get_ml_scores(text)
        
        # 3. Get Fine-tuned BERT scores
        bert_scores = self.bert_classifier.get_ml_scores(text)
        
        # 4. Combine scores
        combined_scores = {}
        all_types = set(rule_scores.keys()) | set(spacy_scores.keys()) | set(bert_scores.keys())
        
        for c_type in all_types:
            r_score = rule_scores.get(c_type, 0.0)
            s_score = spacy_scores.get(c_type, 0.0)
            b_score = bert_scores.get(c_type, 0.0)
            
            # Boost: If rules and at least one ML model agree strongly
            boost = 0.1 if (r_score > 0.5 and (s_score > 0.5 or b_score > 0.5)) else 0.0
            
            combined_scores[c_type] = (
                (r_score * self.RULE_WEIGHT) + 
                (s_score * self.SPACY_WEIGHT) + 
                (b_score * self.BERT_WEIGHT) + 
                boost
            )
            
        # 5. Find best match
        best_type = 'concept'
        best_confidence = 0.0
        
        # Respect priority order if scores are close
        for content_type, _ in self.RULE_CLASSIFIERS:
            score = combined_scores.get(content_type, 0.0)
            if score > best_confidence:
                best_type = content_type
                best_confidence = score
                
        return best_type, min(best_confidence, 1.0)
    
    def classify_with_metadata(self, text: str) -> dict:
        """Classify text and return detailed metadata."""
        content_type, confidence = self.classify_text(text)
        
        return {
            'content_type': content_type,
            'confidence_score': round(confidence, 2),
            'text_length': len(text),
            'alternative_types': self._get_alternative_types(text),
            'analysis': self.spacy_classifier.analyze_linguistics(text),
            'used_bert': self.bert_classifier.is_loaded
        }
    
    def _get_alternative_types(self, text: str, threshold: float = 0.3) -> list:
        """Get alternative content types based on hybrid scores."""
        rule_scores = {ct: f(text)[1] for ct, f in self.RULE_CLASSIFIERS}
        spacy_scores = self.spacy_classifier.get_ml_scores(text)
        bert_scores = self.bert_classifier.get_ml_scores(text)
        
        alternatives = []
        for c_type in rule_scores.keys():
            r_score = rule_scores.get(c_type, 0.0)
            s_score = spacy_scores.get(c_type, 0.0)
            b_score = bert_scores.get(c_type, 0.0)
            
            combined = (
                (r_score * self.RULE_WEIGHT) + 
                (s_score * self.SPACY_WEIGHT) + 
                (b_score * self.BERT_WEIGHT)
            )
            
            if combined >= threshold:
                alternatives.append({
                    'type': c_type,
                    'confidence': round(combined, 2)
                })
        
        alternatives.sort(key=lambda x: x['confidence'], reverse=True)
        return alternatives[:3]
