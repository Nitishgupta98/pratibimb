"""
Responsible AI (RAI) Module for Pratibimb

This module provides comprehensive Responsible AI capabilities including:
- Content safety and toxicity detection
- Bias detection and fairness monitoring
- Synthetic data generation for testing
- Automated test engine with analytics
- HTML report generation

All RAI features are configurable and can be toggled on/off via rai_config.json
"""

__version__ = "1.0.0"
__author__ = "Pratibimb AI Team"

# Import main RAI components for easy access
try:
    from .rai_middleware import RAIMiddleware, RAIContentAnalyzer
    from .rai_synthetic_data import SyntheticDataGenerator
    from .rai_test_engine import RAITestEngine
    from .rai_report_generator import RAIReportGenerator
    
    __all__ = ['RAIMiddleware', 'RAIContentAnalyzer', 'SyntheticDataGenerator', 'RAITestEngine', 'RAIReportGenerator']
except ImportError as e:
    # If dependencies are not installed, provide a graceful fallback
    print(f"Warning: RAI dependencies not fully available: {e}")
    __all__ = []
