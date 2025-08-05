"""
RAI Test Engine

This module provides comprehensive testing capabilities for RAI analysis
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime


class RAITestEngine:
    """
    Test engine for running RAI analysis tests and generating metrics
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        
    async def run_test_suite(self, test_data: Dict[str, Any], analyzer) -> Dict[str, Any]:
        """Run a complete test suite"""
        results = {
            "test_session_id": f"test_{int(datetime.now().timestamp())}",
            "started_at": datetime.now().isoformat(),
            "config": self.config,
            "test_results": [],
            "summary": {}
        }
        
        test_samples = test_data.get("test_samples", [])
        
        for sample in test_samples:
            test_result = await self._run_single_test(sample, analyzer)
            results["test_results"].append(test_result)
        
        # Generate summary
        results["summary"] = self._generate_test_summary(results["test_results"])
        results["completed_at"] = datetime.now().isoformat()
        
        return results
    
    async def _run_single_test(self, test_sample: Dict[str, Any], analyzer) -> Dict[str, Any]:
        """Run a single test case"""
        try:
            content = test_sample.get("content", "")
            expected_type = test_sample.get("expected_type", "unknown")
            
            # Run analysis
            analysis_result = await analyzer.analyze_content(content, "test_input")
            
            # Determine if test passed
            passed = self._evaluate_test_result(analysis_result, expected_type)
            
            return {
                "test_id": test_sample.get("id", "unknown"),
                "content": content,
                "expected_type": expected_type,
                "analysis_result": analysis_result,
                "passed": passed,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Test failed: {e}")
            return {
                "test_id": test_sample.get("id", "unknown"),
                "error": str(e),
                "passed": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def _evaluate_test_result(self, analysis_result: Dict[str, Any], expected_type: str) -> bool:
        """Evaluate if the test result matches expectations"""
        risk_level = analysis_result.get("risk_level", "unknown")
        
        # Simple evaluation logic
        if expected_type == "safe" and risk_level == "low":
            return True
        elif expected_type == "toxic" and risk_level in ["medium", "high"]:
            return True
        elif expected_type == "biased" and risk_level in ["medium", "high"]:
            return True
        elif expected_type == "neutral" and risk_level == "low":
            return True
        
        return False
    
    def _generate_test_summary(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics from test results"""
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result.get("passed", False))
        failed_tests = total_tests - passed_tests
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "overall_score": passed_tests / total_tests if total_tests > 0 else 0
        }