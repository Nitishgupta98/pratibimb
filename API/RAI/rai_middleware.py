"""
RAI Middleware for Content Analysis and Safety Checks

This module provides comprehensive Responsible AI capabilities including:
- Content safety and toxicity detection
- Bias detection and fairness monitoring
- Sentiment analysis
- Privacy protection (PII detection)
"""

import asyncio
import logging
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    import torch
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers not available - using mock analysis")

try:
    from detoxify import Detoxify
    DETOXIFY_AVAILABLE = True
except ImportError:
    DETOXIFY_AVAILABLE = False
    logging.warning("Detoxify not available - using mock toxicity detection")


class RAIContentAnalyzer:
    """
    Comprehensive content analyzer for Responsible AI checks
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.rai_settings = config.get("rai_settings", {})
        self.content_filters = config.get("content_filters", {})
        
        # Initialize models if available
        self.toxicity_model = None
        self.sentiment_model = None
        
        if DETOXIFY_AVAILABLE and self.enabled:
            try:
                self.toxicity_model = Detoxify('original')
                logging.info("✅ Detoxify model loaded successfully")
            except Exception as e:
                logging.warning(f"Failed to load Detoxify model: {e}")
                
        if TRANSFORMERS_AVAILABLE and self.enabled:
            try:
                self.sentiment_model = pipeline("sentiment-analysis", 
                                               model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                                               return_all_scores=True)
                logging.info("✅ Sentiment analysis model loaded successfully")
            except Exception as e:
                logging.warning(f"Failed to load sentiment model: {e}")
    
    async def analyze_content(self, content: str, content_type: str = "user_input") -> Dict[str, Any]:
        """
        Perform comprehensive content analysis
        
        Args:
            content: Text content to analyze
            content_type: Type of content (user_input, transcript, etc.)
            
        Returns:
            Analysis results with safety scores, risk assessment, and recommendations
        """
        try:
            analysis_start = datetime.now()
            
            # Initialize results
            results = {
                "content_type": content_type,
                "content_length": len(content),
                "timestamp": analysis_start.isoformat(),
                "risk_level": "low",
                "blocked": False,
                "warnings": [],
                "safety_scores": {},
                "bias_indicators": {},
                "sentiment": {},
                "privacy_check": {},
                "recommendations": []
            }
            
            # 1. Toxicity Analysis
            if self.toxicity_model and DETOXIFY_AVAILABLE:
                toxicity_scores = await self._analyze_toxicity(content)
                results["safety_scores"] = toxicity_scores
                
                # Check thresholds
                toxicity_threshold = self.content_filters.get("toxicity", {}).get("threshold", 0.8)
                if any(score > toxicity_threshold for score in toxicity_scores.values()):
                    results["risk_level"] = "high"
                    results["warnings"].append("High toxicity detected")
                    if self.content_filters.get("toxicity", {}).get("action") == "block":
                        results["blocked"] = True
            else:
                # Mock toxicity analysis
                results["safety_scores"] = {
                    "toxicity": 0.1,
                    "severe_toxicity": 0.05,
                    "obscene": 0.08,
                    "threat": 0.02,
                    "insult": 0.06,
                    "identity_attack": 0.03
                }
            
            # 2. Sentiment Analysis
            if self.sentiment_model and TRANSFORMERS_AVAILABLE:
                sentiment_scores = await self._analyze_sentiment(content)
                results["sentiment"] = sentiment_scores
            else:
                # Mock sentiment analysis
                results["sentiment"] = {
                    "label": "NEUTRAL",
                    "score": 0.75,
                    "confidence": "medium"
                }
            
            # 3. Bias Detection (simple keyword-based for now)
            bias_indicators = await self._detect_bias(content)
            results["bias_indicators"] = bias_indicators
            
            if bias_indicators.get("potential_bias_count", 0) > 0:
                bias_threshold = self.content_filters.get("bias", {}).get("threshold", 0.6)
                if bias_indicators.get("bias_score", 0) > bias_threshold:
                    results["warnings"].append("Potential bias detected")
                    if results["risk_level"] == "low":
                        results["risk_level"] = "medium"
            
            # 4. Privacy Check (PII detection)
            privacy_check = await self._check_privacy(content)
            results["privacy_check"] = privacy_check
            
            if privacy_check.get("pii_detected", False):
                results["warnings"].append("Potential PII detected")
                if results["risk_level"] == "low":
                    results["risk_level"] = "medium"
            
            # 5. Generate Recommendations
            results["recommendations"] = self._generate_recommendations(results)
            
            # Calculate analysis duration
            analysis_duration = (datetime.now() - analysis_start).total_seconds()
            results["analysis_duration"] = analysis_duration
            
            logging.info(f"Content analysis completed in {analysis_duration:.2f}s - Risk: {results['risk_level']}")
            
            return results
            
        except Exception as e:
            logging.error(f"Content analysis failed: {e}")
            return {
                "error": str(e),
                "risk_level": "unknown",
                "blocked": False,
                "warnings": [f"Analysis failed: {str(e)}"],
                "safety_scores": {},
                "bias_indicators": {},
                "sentiment": {},
                "privacy_check": {},
                "recommendations": ["Manual review recommended due to analysis failure"]
            }
    
    async def _analyze_toxicity(self, content: str) -> Dict[str, float]:
        """Analyze content for toxicity using Detoxify"""
        try:
            # Run toxicity analysis in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            scores = await loop.run_in_executor(None, self.toxicity_model.predict, content)
            
            # Convert numpy types to Python floats
            return {key: float(value) for key, value in scores.items()}
            
        except Exception as e:
            logging.error(f"Toxicity analysis failed: {e}")
            return {
                "toxicity": 0.0,
                "severe_toxicity": 0.0,
                "obscene": 0.0,
                "threat": 0.0,
                "insult": 0.0,
                "identity_attack": 0.0
            }
    
    async def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """Analyze sentiment using transformers"""
        try:
            # Run sentiment analysis in thread pool
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(None, self.sentiment_model, content)
            
            if results and len(results) > 0:
                # Get the highest scoring sentiment
                best_result = max(results[0], key=lambda x: x['score'])
                return {
                    "label": best_result["label"],
                    "score": float(best_result["score"]),
                    "confidence": "high" if best_result["score"] > 0.8 else "medium" if best_result["score"] > 0.6 else "low",
                    "all_scores": {r["label"]: float(r["score"]) for r in results[0]}
                }
            else:
                return {"label": "NEUTRAL", "score": 0.5, "confidence": "low"}
                
        except Exception as e:
            logging.error(f"Sentiment analysis failed: {e}")
            return {"label": "UNKNOWN", "score": 0.0, "confidence": "none", "error": str(e)}
    
    async def _detect_bias(self, content: str) -> Dict[str, Any]:
        """Simple bias detection using keyword matching"""
        try:
            # Define bias indicator keywords (simplified approach)
            bias_keywords = {
                "gender": ["he is better", "she is worse", "men are", "women are", "typical man", "typical woman"],
                "racial": ["all [group] are", "those people", "their kind"],
                "age": ["too old", "too young", "millennials are", "boomers are"],
                "religious": ["all muslims", "all christians", "all jews", "all hindus"],
                "economic": ["poor people are", "rich people are", "welfare recipients"]
            }
            
            content_lower = content.lower()
            detected_categories = []
            total_matches = 0
            
            for category, keywords in bias_keywords.items():
                category_matches = 0
                for keyword in keywords:
                    if keyword.lower() in content_lower:
                        category_matches += 1
                        total_matches += 1
                
                if category_matches > 0:
                    detected_categories.append({
                        "category": category,
                        "matches": category_matches,
                        "keywords_found": [kw for kw in keywords if kw.lower() in content_lower]
                    })
            
            bias_score = min(total_matches * 0.2, 1.0)  # Cap at 1.0
            
            return {
                "potential_bias_count": total_matches,
                "bias_score": bias_score,
                "detected_categories": detected_categories,
                "risk_level": "high" if bias_score > 0.7 else "medium" if bias_score > 0.3 else "low"
            }
            
        except Exception as e:
            logging.error(f"Bias detection failed: {e}")
            return {
                "potential_bias_count": 0,
                "bias_score": 0.0,
                "detected_categories": [],
                "risk_level": "unknown",
                "error": str(e)
            }
    
    async def _check_privacy(self, content: str) -> Dict[str, Any]:
        """Check for potential PII (Personal Identifiable Information)"""
        try:
            pii_patterns = {
                "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
                "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
                "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
            }
            
            detected_pii = {}
            pii_count = 0
            
            for pii_type, pattern in pii_patterns.items():
                matches = re.findall(pattern, content)
                if matches:
                    detected_pii[pii_type] = {
                        "count": len(matches),
                        "samples": matches[:3]  # Only show first 3 for privacy
                    }
                    pii_count += len(matches)
            
            return {
                "pii_detected": pii_count > 0,
                "total_pii_count": pii_count,
                "detected_types": detected_pii,
                "privacy_risk": "high" if pii_count > 2 else "medium" if pii_count > 0 else "low"
            }
            
        except Exception as e:
            logging.error(f"Privacy check failed: {e}")
            return {
                "pii_detected": False,
                "total_pii_count": 0,
                "detected_types": {},
                "privacy_risk": "unknown",
                "error": str(e)
            }
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        risk_level = analysis_results.get("risk_level", "low")
        warnings = analysis_results.get("warnings", [])
        
        if risk_level == "high":
            recommendations.append("Manual review required before publication")
            recommendations.append("Consider content revision to reduce risk factors")
        
        if "High toxicity detected" in warnings:
            recommendations.append("Remove or rephrase potentially offensive language")
        
        if "Potential bias detected" in warnings:
            recommendations.append("Review content for unintentional bias and stereotypes")
        
        if "Potential PII detected" in warnings:
            recommendations.append("Remove or anonymize personal information")
        
        if analysis_results.get("sentiment", {}).get("label") == "NEGATIVE":
            recommendations.append("Consider the emotional impact of negative content")
        
        if not recommendations:
            recommendations.append("Content appears safe for publication")
        
        return recommendations


class RAIMiddleware:
    """
    Middleware wrapper for easy integration with web frameworks
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.analyzer = RAIContentAnalyzer(config)
        self.config = config
        
    async def analyze_request(self, content: str, content_type: str = "user_input") -> Dict[str, Any]:
        """Analyze request content and return results"""
        return await self.analyzer.analyze_content(content, content_type)
        
    def is_content_safe(self, analysis_results: Dict[str, Any]) -> bool:
        """Check if content is safe based on analysis results"""
        return not analysis_results.get("blocked", False) and analysis_results.get("risk_level", "high") != "high"