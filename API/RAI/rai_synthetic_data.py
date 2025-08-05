"""
RAI Synthetic Data Generator

This module generates synthetic test data for RAI analysis testing
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging


class SyntheticDataGenerator:
    """
    Generate synthetic data for RAI testing and validation
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        
    def generate_test_content(self, content_types: List[str] = None, count: int = 10) -> Dict[str, Any]:
        """Generate synthetic test content"""
        if content_types is None:
            content_types = ["safe", "toxic", "biased", "neutral"]
        
        test_data = {
            "generated_at": datetime.now().isoformat(),
            "content_count": count,
            "content_types": content_types,
            "test_samples": []
        }
        
        for i in range(count):
            content_type = random.choice(content_types)
            sample = self._generate_sample(content_type, i)
            test_data["test_samples"].append(sample)
        
        return test_data
    
    def _generate_sample(self, content_type: str, index: int) -> Dict[str, Any]:
        """Generate a single test sample"""
        samples = {
            "safe": [
                "This is a wonderful educational video about nature.",
                "I enjoyed learning about sustainable technology solutions.",
                "The documentary provides great insights into history."
            ],
            "toxic": [
                "This content contains mild criticism but nothing harmful.",
                "Some people might disagree with this viewpoint.",
                "This topic can be controversial for some audiences."
            ],
            "biased": [
                "This content may contain subtle stereotypes.",
                "Some generalizations are made about different groups.",
                "There might be unconscious bias in the presentation."
            ],
            "neutral": [
                "This is factual information presented objectively.",
                "The content covers technical specifications and details.",
                "Statistical data and research findings are discussed."
            ]
        }
        
        content_options = samples.get(content_type, samples["neutral"])
        content = random.choice(content_options)
        
        return {
            "id": f"test_sample_{index}",
            "content": content,
            "expected_type": content_type,
            "length": len(content),
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_bias_test_cases(self) -> List[Dict[str, Any]]:
        """Generate specific test cases for bias detection"""
        return [
            {
                "content": "People from different backgrounds bring unique perspectives.",
                "expected_bias": False,
                "category": "diversity_positive"
            },
            {
                "content": "Technical documentation for software development.",
                "expected_bias": False,
                "category": "neutral_technical"
            }
        ]
    
    def generate_safety_test_cases(self) -> List[Dict[str, Any]]:
        """Generate specific test cases for safety detection"""
        return [
            {
                "content": "Educational content about conflict resolution.",
                "expected_safety": True,
                "category": "educational"
            },
            {
                "content": "Informative discussion about social issues.",
                "expected_safety": True,
                "category": "informative"
            }
        ]