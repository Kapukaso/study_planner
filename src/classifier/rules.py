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
    has_summary_marker,
    count_keyword_matches
)


def is_formula(text: str) -> tuple[bool, float]:
    """
    Check if text is a formula.
    
    Returns:
        (is_formula, confidence)
    """
    confidence = 0.0
    
    if has_formula_symbols(text):
        confidence += 0.5
    
    if has_formula_vars(text):
        confidence += 0.4
    
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['formula'])
    if keyword_count > 0:
        confidence += min(0.3, keyword_count * 0.15)
    
    if len(text) < 100 and (has_formula_symbols(text) or has_formula_vars(text)):
        confidence += 0.2
    
    return confidence > 0.6, min(confidence, 1.0)


def is_definition(text: str) -> tuple[bool, float]:
    """
    Check if text is a definition.
    
    Returns:
        (is_definition, confidence)
    """
    confidence = 0.0
    
    if has_definition_pattern(text):
        confidence += 0.6
    
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['definition'])
    if keyword_count > 0:
        confidence += min(0.4, keyword_count * 0.2)
    
    if 50 < len(text) < 350 and keyword_count > 0:
        confidence += 0.1
    
    return confidence > 0.5, min(confidence, 1.0)


def is_question(text: str) -> tuple[bool, float]:
    """
    Check if text is a question/PYQ.
    
    Returns:
        (is_question, confidence)
    """
    confidence = 0.0
    
    if has_question_pattern(text):
        confidence += 0.5
    
    if has_pyq_markers(text):
        confidence += 0.4
    
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['pyq'])
    if keyword_count > 0:
        confidence += min(0.3, keyword_count * 0.1)
    
    return confidence > 0.6, min(confidence, 1.0)


def is_example(text: str) -> tuple[bool, float]:
    """
    Check if text is an example.
    
    Returns:
        (is_example, confidence)
    """
    confidence = 0.0
    
    if has_example_marker(text):
        confidence += 0.7
    
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['example'])
    if keyword_count > 0:
        confidence += min(0.4, keyword_count * 0.15)
    
    return confidence > 0.6, min(confidence, 1.0)


def is_highlight(text: str) -> tuple[bool, float]:
    """
    Check if text is a highlight/important point.
    
    Returns:
        (is_highlight, confidence)
    """
    confidence = 0.0
    
    if has_highlight_markers(text):
        confidence += 0.5
    
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['highlight'])
    if keyword_count > 0:
        confidence += min(0.5, keyword_count * 0.2)
    
    if len(text) < 150 and (has_highlight_markers(text) or keyword_count > 0):
        confidence += 0.1
    
    return confidence > 0.5, min(confidence, 1.0)


def is_summary(text: str) -> tuple[bool, float]:
    """
    Check if text is a summary.

    Returns:
        (is_summary, confidence)
    """
    confidence = 0.0

    if has_summary_marker(text):
        confidence += 0.7

    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['summary'])
    if keyword_count > 0:
        confidence += min(0.4, keyword_count * 0.2)

    return confidence > 0.6, min(confidence, 1.0)


def is_concept(text: str) -> tuple[bool, float]:
    """
    Check if text is a concept explanation.
    
    Returns:
        (is_concept, confidence)
    """
    confidence = 0.0
    
    keyword_count = count_keyword_matches(text, CONTENT_KEYWORDS['concept'])
    if keyword_count > 0:
        confidence += min(0.6, keyword_count * 0.25)
    
    # Concepts are usually longer and descriptive
    if len(text) > 300:
        confidence += 0.3
    elif len(text) > 100:
        confidence += 0.15
    
    # If it doesn't match other specific types, it's more likely a concept
    return confidence > 0.25, min(confidence, 1.0)
