"""Content classification rules engine."""
from src.classifier.patterns import (
    CONTENT_KEYWORDS,
    has_formula_symbols,
    has_formula_vars,
    has_definition_pattern,
    has_question_pattern,
    has_pyq_markers,
    has_example_marker,
    has_highlight_markers,
    count_keyword_matches
)


def is_formula(text: str) -> tuple[bool, float]:
    """
    Check if text is a formula.
    
    Returns:
        (is_formula, confidence)
    """
    confidence = 0.0
    
    # Check for mathematical symbols
    if has_formula_symbols(text):
        confidence += 0.4
    
    # Check for formula variables
    if has_formula_vars(text):
        confidence += 0.3
    
    # Check for formula keywords
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['formula'])
    if keyword_count > 0:
        confidence += min(0.3, keyword_count * 0.1)
    
    # Short text with symbols is likely formula
    if len(text) < 100 and (has_formula_symbols(text) or has_formula_vars(text)):
        confidence += 0.2
    
    return confidence > 0.5, min(confidence, 1.0)


def is_definition(text: str) -> tuple[bool, float]:
    """
    Check if text is a definition.
    
    Returns:
        (is_definition, confidence)
    """
    confidence = 0.0
    
    # Check for definition pattern (Term: explanation)
    if has_definition_pattern(text):
        confidence += 0.5
    
    # Check for definition keywords
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['definition'])
    if keyword_count > 0:
        confidence += min(0.4, keyword_count * 0.15)
    
    # Definitions are usually concise
    if 50 < len(text) < 300 and keyword_count > 0:
        confidence += 0.2
    
    return confidence > 0.5, min(confidence, 1.0)


def is_question(text: str) -> tuple[bool, float]:
    """
    Check if text is a question/PYQ.
    
    Returns:
        (is_question, confidence)
    """
    confidence = 0.0
    
    # Check for question pattern
    if has_question_pattern(text):
        confidence += 0.4
    
    # Check for PYQ markers (marks, years)
    if has_pyq_markers(text):
        confidence += 0.4
    
    # Check for question keywords
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['pyq'])
    if keyword_count > 0:
        confidence += min(0.3, keyword_count * 0.1)
    
    return confidence > 0.5, min(confidence, 1.0)


def is_example(text: str) -> tuple[bool, float]:
    """
    Check if text is an example.
    
    Returns:
        (is_example, confidence)
    """
    confidence = 0.0
    
    # Check for example marker
    if has_example_marker(text):
        confidence += 0.6
    
    # Check for example keywords
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['example'])
    if keyword_count > 0:
        confidence += min(0.4, keyword_count * 0.15)
    
    return confidence > 0.5, min(confidence, 1.0)


def is_highlight(text: str) -> tuple[bool, float]:
    """
    Check if text is a highlight/important point.
    
    Returns:
        (is_highlight, confidence)
    """
    confidence = 0.0
    
    # Check for highlight markers
    if has_highlight_markers(text):
        confidence += 0.4
    
    # Check for highlight keywords
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['highlight'])
    if keyword_count > 0:
        confidence += min(0.4, keyword_count * 0.15)
    
    # Short, emphasized text
    if len(text) < 150 and (has_highlight_markers(text) or keyword_count > 0):
        confidence += 0.2
    
    return confidence > 0.5, min(confidence, 1.0)


def is_concept(text: str) -> tuple[bool, float]:
    """
    Check if text is a concept explanation.
    
    Returns:
        (is_concept, confidence)
    """
    confidence = 0.0
    
    # Check for concept keywords
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['concept'])
    if keyword_count > 0:
        confidence += min(0.5, keyword_count * 0.2)
    
    # Concepts are usually longer explanatory text
    if len(text) > 200 and keyword_count > 0:
        confidence += 0.3
    
    # If not clearly another type, likely concept
    if len(text) > 100:
        confidence += 0.2
    
    return confidence > 0.4, min(confidence, 1.0)
