"""Test script for Hybrid Content Classifier."""
from src.classifier.content_classifier import ContentClassifier

def test_classification():
    classifier = ContentClassifier()
    
    test_cases = [
        {
            "text": "What are the primary causes of global warming and how do they affect the polar ice caps?",
            "expected": "pyq"
        },
        {
            "text": "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll.",
            "expected": "definition"
        },
        {
            "text": "E = mc^2 is the most famous equation in physics, relating energy and mass.",
            "expected": "formula"
        },
        {
            "text": "Consider a ball falling from a height of 10 meters. Calculate its velocity just before hitting the ground.",
            "expected": "example"
        },
        {
            "text": "The industrial revolution began in Great Britain in the late 18th century and spread to other parts of the world.",
            "expected": "concept"
        }
    ]
    
    print(f"{'Text Sample':<50} | {'Expected':<12} | {'Actual':<12} | {'Conf'}")
    print("-" * 85)
    
    for case in test_cases:
        content_type, confidence = classifier.classify_text(case['text'])
        print(f"{case['text'][:47]+'...':<50} | {case['expected']:<12} | {content_type:<12} | {confidence:.2f}")

if __name__ == "__main__":
    test_classification()
