#!/usr/bin/env python3
"""
RAI Orchestrator - Complete Responsible AI Testing Suite

This script orchestrates the entire RAI testing pipeline:
1. Generates synthetic test data
2. Runs comprehensive test suite
3. Generates detailed HTML reports
4. Provides actionable insights and recommendations

Usage:
    python rai_orchestrator.py [--config CONFIG_PATH] [--output OUTPUT_DIR] [--quick]
"""

import os
import sys
import json
import logging
import argparse
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

# Add the API directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.dirname(current_dir)
sys.path.insert(0, api_dir)

# Import RAI components
from rai_synthetic_data import SyntheticDataGenerator
from rai_test_engine import RAITestEngine
from rai_report_generator import RAIReportGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RAIOrchestrator:
    """Orchestrates complete RAI testing and reporting pipeline."""
    
    def __init__(self, config_path: str = None, output_dir: str = None):
        """Initialize the RAI orchestrator."""
        
        # Set default paths
        if config_path is None:
            config_path = os.path.join(current_dir, 'rai_config.json')
            # If not found, try RAI/rai_config.json
            if not os.path.exists(config_path):
                config_path = os.path.join(current_dir, 'RAI', 'rai_config.json')
        if output_dir is None:
            output_dir = os.path.join(api_dir, 'rai_reports')
        
        self.config_path = config_path
        self.output_dir = output_dir
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.data_generator = SyntheticDataGenerator(self.config)
        self.test_engine = RAITestEngine(self.config)
        self.report_generator = RAIReportGenerator(self.config)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info(f"🚀 RAI Orchestrator initialized")
        logger.info(f"📁 Output directory: {self.output_dir}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load RAI configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"✅ Configuration loaded from {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"❌ Failed to load configuration: {e}")
            raise
    
    async def run_complete_rai_pipeline(self, quick_mode: bool = False) -> Dict[str, str]:
        """Run the complete RAI testing and reporting pipeline."""
        
        logger.info("🔄 Starting complete RAI pipeline...")
        
        # Track pipeline results
        pipeline_results = {
            'status': 'started',
            'timestamp': datetime.now().isoformat(),
            'files_generated': []
        }
        
        try:
            # Step 1: Generate synthetic test data
            logger.info("📊 Step 1: Generating synthetic test data...")
            synthetic_data_stats = await self._generate_synthetic_data(quick_mode)
            pipeline_results['synthetic_data_generated'] = True
            
            # Step 2: Run comprehensive test suite
            logger.info("🧪 Step 2: Running comprehensive test suite...")
            test_results = await self._run_test_suite(quick_mode)
            pipeline_results['tests_completed'] = True
            
            # Step 3: Generate comprehensive report
            logger.info("📋 Step 3: Generating comprehensive HTML report...")
            report_path = self._generate_comprehensive_report(
                test_results, synthetic_data_stats
            )
            pipeline_results['report_generated'] = report_path
            pipeline_results['files_generated'].append(report_path)
            
            # Step 4: Generate summary and recommendations
            logger.info("💡 Step 4: Generating summary and recommendations...")
            summary_path = self._generate_summary_report(
                test_results, synthetic_data_stats
            )
            pipeline_results['summary_generated'] = summary_path
            pipeline_results['files_generated'].append(summary_path)
            
            # Step 5: Save detailed results as JSON
            logger.info("💾 Step 5: Saving detailed results...")
            json_path = self._save_detailed_results(
                test_results, synthetic_data_stats, pipeline_results
            )
            pipeline_results['json_saved'] = json_path
            pipeline_results['files_generated'].append(json_path)
            
            pipeline_results['status'] = 'completed'
            logger.info("✅ RAI pipeline completed successfully!")
            
            # Print summary
            self._print_pipeline_summary(pipeline_results)
            
            return pipeline_results
            
        except Exception as e:
            pipeline_results['status'] = 'failed'
            pipeline_results['error'] = str(e)
            logger.error(f"❌ RAI pipeline failed: {e}")
            raise
    
    async def _generate_synthetic_data(self, quick_mode: bool = False) -> Dict[str, Any]:
        """Generate synthetic test data."""
        
        # Adjust sample count for quick mode
        sample_count = 100 if quick_mode else self.config.get('synthetic_data', {}).get('sample_count', 1000)
        
        logger.info(f"Generating {sample_count} synthetic samples...")
        
        # Generate data
        synthetic_data = await self.data_generator.generate_test_dataset(
            size=sample_count
        )
        
        # Save synthetic data to file
        data_path = os.path.join(self.output_dir, 'synthetic_test_data.json')
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(synthetic_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Synthetic data saved to {data_path}")
        
        # Return statistics
        return {
            'total_samples': sample_count,
            'demographic_distribution': synthetic_data.get('demographic_distribution', {}),
            'bias_test_data': synthetic_data.get('bias_test_data', []),
            'toxicity_test_data': synthetic_data.get('toxicity_test_data', []),
            'edge_cases': synthetic_data.get('edge_cases', []),
            'data_file': data_path
        }
    
    async def _run_test_suite(self, quick_mode: bool = False) -> Dict[str, Any]:
        """Run the comprehensive test suite."""
        
        # Load synthetic data
        data_path = os.path.join(self.output_dir, 'synthetic_test_data.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            synthetic_data = json.load(f)
        
        # Run comprehensive tests using the test engine
        test_size = 50 if quick_mode else 200
        logger.info("🧪 Running comprehensive test suite...")
        test_results = await self.test_engine.run_comprehensive_tests(
            test_size=test_size,
            include_stress_tests=not quick_mode  # Skip stress tests in quick mode
        )
        
        # Save test results
        results_path = os.path.join(self.output_dir, 'test_results.json')
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Test results saved to {results_path}")
        
        return test_results
    
    def _generate_comprehensive_report(
        self, 
        test_results: Dict[str, Any], 
        synthetic_data_stats: Dict[str, Any]
    ) -> str:
        """Generate comprehensive HTML report."""
        
        # Mock middleware metrics (would come from actual middleware in production)
        middleware_metrics = {
            'request_metrics': {
                'total_requests': 1000,
                'blocked_requests': 5,
                'flagged_content': 12,
                'avg_response_time': 0.65
            }
        }
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.output_dir, f'rai_comprehensive_report_{timestamp}.html')
        
        self.report_generator.generate_comprehensive_report(
            test_results, 
            synthetic_data_stats, 
            middleware_metrics,
            output_path=report_path
        )
        
        return report_path
    
    def _generate_summary_report(
        self, 
        test_results: Dict[str, Any], 
        synthetic_data_stats: Dict[str, Any]
    ) -> str:
        """Generate executive summary report."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_path = os.path.join(self.output_dir, f'rai_executive_summary_{timestamp}.txt')
        
        # Calculate key metrics
        bias_results = test_results.get('bias_tests', {})
        toxicity_results = test_results.get('toxicity_tests', {})
        performance_results = test_results.get('performance_tests', {})
        
        # Count issues
        high_bias_count = sum(1 for data in bias_results.values() 
                             if data.get('bias_score', 0) > 0.3)
        moderate_bias_count = sum(1 for data in bias_results.values() 
                                 if 0.1 < data.get('bias_score', 0) <= 0.3)
        
        toxicity_incidents = 0
        for category_results in toxicity_results.values():
            if isinstance(category_results, list):
                toxicity_incidents += sum(1 for r in category_results 
                                        if r.get('max_toxicity', 0) > 0.3)
        
        avg_response_time = performance_results.get('avg_response_time', 0)
        success_rate = performance_results.get('success_rate', 100)
        
        # Generate summary text
        summary_text = f"""
PRATIBIMB RESPONSIBLE AI - EXECUTIVE SUMMARY
==========================================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

OVERALL ASSESSMENT
------------------
✅ Tests Completed: {len(bias_results) + len(toxicity_results) + 1}
📊 Synthetic Samples: {synthetic_data_stats.get('total_samples', 0)}
⚡ Avg Response Time: {avg_response_time:.3f}s
📈 Success Rate: {success_rate:.1f}%

BIAS DETECTION RESULTS
----------------------
🔴 High Risk (>0.3): {high_bias_count} attributes
🟡 Moderate Risk (0.1-0.3): {moderate_bias_count} attributes
🟢 Low Risk (<0.1): {len(bias_results) - high_bias_count - moderate_bias_count} attributes

CONTENT SAFETY RESULTS
-----------------------
🚨 Toxicity Incidents: {toxicity_incidents}
📋 Categories Tested: {len(toxicity_results)}

KEY RECOMMENDATIONS
-------------------
"""
        
        # Add specific recommendations
        if high_bias_count > 0:
            summary_text += f"• URGENT: Address {high_bias_count} high-bias attributes immediately\n"
        if moderate_bias_count > 0:
            summary_text += f"• Monitor {moderate_bias_count} moderate-bias attributes closely\n"
        if toxicity_incidents > 0:
            summary_text += f"• Review {toxicity_incidents} toxicity incidents for content policy\n"
        if avg_response_time > 2.0:
            summary_text += f"• Optimize performance - response time ({avg_response_time:.3f}s) above target\n"
        if success_rate < 95:
            summary_text += f"• Investigate {100-success_rate:.1f}% failure rate\n"
        
        if high_bias_count == 0 and toxicity_incidents == 0 and avg_response_time < 2.0:
            summary_text += "• System operating within acceptable RAI parameters ✅\n"
        
        summary_text += f"""
NEXT STEPS
----------
1. Review detailed HTML report for specific findings
2. Implement recommended changes
3. Schedule follow-up RAI assessment
4. Monitor ongoing metrics through middleware

Files Generated:
• Comprehensive Report: rai_comprehensive_report_{timestamp}.html
• Test Results: test_results.json
• Synthetic Data: synthetic_test_data.json
• This Summary: rai_executive_summary_{timestamp}.txt
"""
        
        # Save summary
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        
        logger.info(f"✅ Executive summary saved to {summary_path}")
        
        return summary_path
    
    def _save_detailed_results(
        self, 
        test_results: Dict[str, Any], 
        synthetic_data_stats: Dict[str, Any],
        pipeline_results: Dict[str, Any]
    ) -> str:
        """Save detailed pipeline results as JSON."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(self.output_dir, f'rai_detailed_results_{timestamp}.json')
        
        detailed_results = {
            'metadata': {
                'timestamp': timestamp,
                'config_used': self.config,
                'pipeline_version': '1.0.0'
            },
            'synthetic_data_stats': synthetic_data_stats,
            'test_results': test_results,
            'pipeline_results': pipeline_results
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(detailed_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Detailed results saved to {json_path}")
        
        return json_path
    
    def _print_pipeline_summary(self, pipeline_results: Dict[str, Any]):
        """Print a summary of the pipeline execution."""
        
        print("\n" + "="*70)
        print("🛡️  PRATIBIMB RAI PIPELINE COMPLETED")
        print("="*70)
        print(f"📅 Timestamp: {pipeline_results.get('timestamp', 'Unknown')}")
        print(f"📊 Status: {pipeline_results.get('status', 'Unknown').upper()}")
        print(f"📁 Output Directory: {self.output_dir}")
        print("\nFiles Generated:")
        
        for i, file_path in enumerate(pipeline_results.get('files_generated', []), 1):
            filename = os.path.basename(file_path)
            print(f"  {i}. {filename}")
        
        print(f"\n💡 Open the HTML report in your browser for detailed analysis")
        print(f"📋 Review the executive summary for key findings")
        print("="*70 + "\n")


def main():
    """Main function to run the RAI orchestrator."""
    
    parser = argparse.ArgumentParser(description='Pratibimb RAI Orchestrator')
    parser.add_argument('--config', type=str, help='Path to RAI config file')
    parser.add_argument('--output', type=str, help='Output directory for reports')
    parser.add_argument('--quick', action='store_true', help='Run in quick mode (fewer tests)')
    
    args = parser.parse_args()
    
    try:
        # Initialize orchestrator
        orchestrator = RAIOrchestrator(
            config_path=args.config,
            output_dir=args.output
        )
        
        # Run complete pipeline
        results = asyncio.run(orchestrator.run_complete_rai_pipeline(quick_mode=args.quick))
        
        if results['status'] == 'completed':
            print(f"\n✅ RAI pipeline completed successfully!")
            print(f"📊 Check output directory: {orchestrator.output_dir}")
        else:
            print(f"\n❌ RAI pipeline failed: {results.get('error', 'Unknown error')}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⏹️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
