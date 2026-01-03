"""
Code analysis package for ChainCredit.
"""
from .language_detector import detect_languages, detect_frameworks
from .structure import analyze_structure
from .complexity import calculate_complexity
from .lint_metrics import analyze_code_quality
from .test_detector import detect_tests

__all__ = [
    'detect_languages',
    'detect_frameworks',
    'analyze_structure',
    'calculate_complexity',
    'analyze_code_quality',
    'detect_tests'
]
