"""Classification patterns and rules for content categorization."""
import re

# Content type keywords
CONTENT_KEYWORDS = {
    'concept': [
        'is defined as', 'refers to', 'concept of', 'introduction to',
        'overview', 'understanding', 'explained', 'meaning', 'describes'
    ],
    
    'definition': [
        'definition', 'is defined as', 'means', 'is called', 'known as',
        'termed as', 'refers to as', 'is the', 'can be defined'
    ],
    
    'formula': [
        'formula', 'equation', 'calculate', 'computation', 'mathematical',
        'expression', 'theorem', 'proof', 'derive'
    ],
    
    'example': [
        'example', 'for instance', 'e.g.', 'such as', 'for example',
        'instance', 'illustrated', 'demonstration', 'case study'
    ],
    
    'pyq': [
        'question', 'q.', 'q)', 'marks', 'exam', 'test', 'answer',
        'solve', 'explain', 'discuss', 'what', 'why', 'how'
    ],
    
    'highlight': [
        'important', 'note', 'remember', 'key point', 'crucial',
        'significant', 'essential', 'must', 'never forget', 'always'
    ]
}

# Regex patterns for content detection
PATTERNS = {
    # Mathematical formulas: contains =, symbols, equations
    'formula_symbols': r'[=∑∫∏√±≈≠≤≥∞πΔθλμσΩ]|\\frac|\\int|\\sum',
    
    # Formula variables: x, y, a, b with subscripts/superscripts
    'formula_vars': r'\b[a-zA-Z][_\d]*\s*=\s*',
    
    # Definition pattern: "Term: explanation" or "Term - explanation"
    'definition_colon': r'^[A-Z][A-Za-z\s]+:\s+',
    'definition_dash': r'^[A-Z][A-Za-z\s]+\s+-\s+',
    
    # Question patterns
    'question_mark': r'\?$',
    'question_start': r'^(Q\.|Q\d+|Question\s+\d+)',
    'question_keywords': r'\b(what|why|how|when|where|who|which|explain|discuss|describe|define)\b',
    
    # Marks indication: (5 marks), [10M], etc.
    'marks': r'\((\d+)\s*(marks|M|m)\)|\[(\d+)M\]',
    
    # Year patterns: 2019-2025, May 2023, etc.
    'year': r'\b(20[1-2]\d)\b|(\w+\s+20[1-2]\d)',
    
    # Example markers
    'example_marker': r'^(Example|Ex\.|E\.g\.|Instance)\s*\d*:?',
    
    # Highlight markers: bullet points, asterisks
    'bullet': r'^\s*[•●○■□▪▫-]\s+',
    'emphasis': r'\*\*.*?\*\*|\*.*?\*'
}


def compile_patterns():
    """Compile all regex patterns for efficiency."""
    return {key: re.compile(pattern, re.IGNORECASE) for key, pattern in PATTERNS.items()}


# Pre-compiled patterns
COMPILED_PATTERNS = compile_patterns()


def has_formula_symbols(text: str) -> bool:
    """Check if text contains mathematical symbols."""
    return bool(COMPILED_PATTERNS['formula_symbols'].search(text))


def has_formula_vars(text: str) -> bool:
    """Check if text contains formula variable assignments."""
    return bool(COMPILED_PATTERNS['formula_vars'].search(text))


def has_definition_pattern(text: str) -> bool:
    """Check if text follows definition pattern."""
    return bool(
        COMPILED_PATTERNS['definition_colon'].match(text) or
        COMPILED_PATTERNS['definition_dash'].match(text)
    )


def has_question_pattern(text: str) -> bool:
    """Check if text is a question."""
    return bool(
        COMPILED_PATTERNS['question_mark'].search(text) or
        COMPILED_PATTERNS['question_start'].match(text) or
        COMPILED_PATTERNS['question_keywords'].search(text)
    )


def has_pyq_markers(text: str) -> bool:
    """Check if text has PYQ markers (marks, years)."""
    return bool(
        COMPILED_PATTERNS['marks'].search(text) or
        COMPILED_PATTERNS['year'].search(text)
    )


def has_example_marker(text: str) -> bool:
    """Check if text starts with example marker."""
    return bool(COMPILED_PATTERNS['example_marker'].match(text))


def has_highlight_markers(text: str) -> bool:
    """Check if text has highlight markers."""
    return bool(
        COMPILED_PATTERNS['bullet'].match(text) or
        COMPILED_PATTERNS['emphasis'].search(text)
    )


def count_keyword_matches(text: str, keywords: list) -> int:
    """Count how many keywords appear in text."""
    text_lower = text.lower()
    return sum(1 for keyword in keywords if keyword.lower() in text_lower)
