"""Content classifier - Main classification engine."""
from typing import Tuple
from src.classifier.rules import (
    is_formula,
   is_definition,
    is_question,
    is_example,
    is_highlight,
    is_concept
)


class ContentClassifier:
    """Main content classification engine."""
    
    # Priority order for classification (most specific first)
    CLASSIFICATION_ORDER = [
        ('formula', is_formula),
        ('definition', is_definition),
        ('pyq', is_question),
        ('example', is_example),
        ('highlight', is_highlight),
        ('concept', is_concept),
    ]
    
    def classify_text(self, text: str) -> Tuple[str, float]:
        """
        Classify text into content type.
        
        Args:
            text: Text to classify
            
        Returns:
            Tuple of (content_type, confidence_score)
        """
        if not text or len(text.strip()) < 10:
            return 'concept', 0.0
        
        # Try each classifier in priority order
        best_type = 'concept'
        best_confidence = 0.0
        
        for content_type, classifier_func in self.CLASSIFICATION_ORDER:
            is_type, confidence = classifier_func(text)
            
            if is_type and confidence > best_confidence:
                best_type = content_type
                best_confidence = confidence
        
        return best_type, best_confidence
    
    def classify_with_metadata(self, text: str) -> dict:
        """
        Classify text and return detailed metadata.
        
        Args:
            text: Text to classify
            
        Returns:
            Dictionary with classification results
        """
        content_type, confidence = self.classify_text(text)
        
        return {
            'content_type': content_type,
            'confidence_score': round(confidence, 2),
            'text_length': len(text),
            'alternative_types': self._get_alternative_types(text)
        }
    
    def _get_alternative_types(self, text: str, threshold: float = 0.3) -> list:
        """Get alternative content types above threshold."""
        alternatives = []
        
        for content_type, classifier_func in self.CLASSIFICATION_ORDER:
            is_type, confidence = classifier_func(text)
            
            if confidence >= threshold:
                alternatives.append({
                    'type': content_type,
                    'confidence': round(confidence, 2)
                })
        
        # Sort by confidence descending
        alternatives.sort(key=lambda x: x['confidence'], reverse=True)
        
        return alternatives[:3]  # Top 3 alternatives
