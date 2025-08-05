"""
RAI HTML Report Generator

This module generates comprehensive HTML reports for Responsible AI testing and monitoring.
It creates detailed analytics, visualizations, and insights from RAI test results.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import base64
from io import BytesIO

# For HTML generation and styling
from jinja2 import Template, Environment, BaseLoader
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class RAIReportGenerator:
    """Generate comprehensive HTML reports for RAI testing and analytics."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the report generator with configuration."""
        self.config = config or {}
        self.report_config = self.config.get('reporting', {})
        
        # Set up matplotlib for web-safe plotting
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
        sns.set_palette("husl")
        
    def generate_comprehensive_report(
        self, 
        test_results: Dict[str, Any],
        synthetic_data_stats: Dict[str, Any],
        middleware_metrics: Dict[str, Any],
        output_path: str = None
    ) -> str:
        """Generate a comprehensive HTML report combining all RAI metrics."""
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"rai_comprehensive_report_{timestamp}.html"
        
        try:
            # Prepare data for visualization
            charts_data = self._prepare_chart_data(test_results, synthetic_data_stats, middleware_metrics)
            
            # Generate charts as base64 encoded images
            charts = self._generate_charts(charts_data)
            
            # Create the HTML report
            html_content = self._create_html_report(
                test_results, 
                synthetic_data_stats, 
                middleware_metrics, 
                charts
            )
            
            # Save the report
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Comprehensive RAI report generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error generating comprehensive report: {e}")
            raise
    
    def _prepare_chart_data(
        self, 
        test_results: Dict[str, Any],
        synthetic_data_stats: Dict[str, Any],
        middleware_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare data structures for chart generation."""
        
        charts_data = {}
        
        # Bias detection results
        if 'bias_tests' in test_results:
            bias_data = test_results['bias_tests']
            charts_data['bias_scores'] = {
                attr: results.get('bias_score', 0) 
                for attr, results in bias_data.items()
            }
            charts_data['fairness_metrics'] = {
                attr: results.get('fairness_metrics', {}) 
                for attr, results in bias_data.items()
            }
        
        # Toxicity detection results
        if 'toxicity_tests' in test_results:
            toxicity_data = test_results['toxicity_tests']
            charts_data['toxicity_scores'] = {
                category: np.mean([result.get('max_toxicity', 0) for result in results])
                for category, results in toxicity_data.items()
            }
        
        # Performance metrics
        if 'performance_tests' in test_results:
            perf_data = test_results['performance_tests']
            charts_data['response_times'] = [
                result.get('response_time', 0) for result in perf_data.get('results', [])
            ]
            charts_data['success_rates'] = perf_data.get('success_rate', 0)
        
        # Synthetic data distribution
        if 'demographic_distribution' in synthetic_data_stats:
            charts_data['demographic_dist'] = synthetic_data_stats['demographic_distribution']
        
        # Middleware metrics over time
        if 'request_metrics' in middleware_metrics:
            charts_data['request_metrics'] = middleware_metrics['request_metrics']
        
        return charts_data
    
    def _generate_charts(self, charts_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate all charts and return them as base64 encoded strings."""
        
        charts = {}
        
        try:
            # Bias Scores Bar Chart
            if 'bias_scores' in charts_data:
                charts['bias_chart'] = self._create_bias_chart(charts_data['bias_scores'])
            
            # Toxicity Scores Radar Chart
            if 'toxicity_scores' in charts_data:
                charts['toxicity_chart'] = self._create_toxicity_chart(charts_data['toxicity_scores'])
            
            # Performance Metrics
            if 'response_times' in charts_data:
                charts['performance_chart'] = self._create_performance_chart(charts_data['response_times'])
            
            # Demographic Distribution
            if 'demographic_dist' in charts_data:
                charts['demographic_chart'] = self._create_demographic_chart(charts_data['demographic_dist'])
            
            # Fairness Metrics Heatmap
            if 'fairness_metrics' in charts_data:
                charts['fairness_chart'] = self._create_fairness_heatmap(charts_data['fairness_metrics'])
                
        except Exception as e:
            logger.warning(f"⚠️ Error generating charts: {e}")
        
        return charts
    
    def _create_bias_chart(self, bias_scores: Dict[str, float]) -> str:
        """Create bias scores bar chart."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        attributes = list(bias_scores.keys())
        scores = list(bias_scores.values())
        
        colors = ['red' if score > 0.3 else 'orange' if score > 0.1 else 'green' for score in scores]
        
        bars = ax.bar(attributes, scores, color=colors, alpha=0.7)
        ax.set_ylabel('Bias Score')
        ax.set_title('Bias Detection Results by Protected Attribute')
        ax.set_ylim(0, 1)
        
        # Add threshold lines
        ax.axhline(y=0.1, color='orange', linestyle='--', alpha=0.5, label='Caution Threshold')
        ax.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='High Risk Threshold')
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{score:.3f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def _create_toxicity_chart(self, toxicity_scores: Dict[str, float]) -> str:
        """Create toxicity scores radar chart."""
        categories = list(toxicity_scores.keys())
        scores = list(toxicity_scores.values())
        
        # Number of variables
        N = len(categories)
        
        # Angle for each category
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        # Values
        scores += scores[:1]  # Complete the circle
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Plot
        ax.plot(angles, scores, 'o-', linewidth=2, label='Toxicity Scores')
        ax.fill(angles, scores, alpha=0.25)
        
        # Add category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        
        # Set y-axis limits
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'])
        
        # Add grid
        ax.grid(True)
        
        # Add title
        plt.title('Toxicity Detection Results', size=16, y=1.1)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_performance_chart(self, response_times: List[float]) -> str:
        """Create performance metrics histogram."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Response time histogram
        ax1.hist(response_times, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_xlabel('Response Time (seconds)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Response Time Distribution')
        ax1.axvline(np.mean(response_times), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(response_times):.3f}s')
        ax1.legend()
        
        # Performance metrics over time (simulated)
        time_points = range(len(response_times))
        ax2.plot(time_points, response_times, marker='o', alpha=0.7)
        ax2.set_xlabel('Request Number')
        ax2.set_ylabel('Response Time (seconds)')
        ax2.set_title('Response Time Over Requests')
        
        # Add trend line
        z = np.polyfit(time_points, response_times, 1)
        p = np.poly1d(z)
        ax2.plot(time_points, p(time_points), "r--", alpha=0.8, label='Trend')
        ax2.legend()
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_demographic_chart(self, demographic_dist: Dict[str, Any]) -> str:
        """Create demographic distribution pie charts."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        demographic_categories = ['gender', 'ethnicity', 'age_group', 'disability_status']
        
        for i, category in enumerate(demographic_categories):
            if category in demographic_dist and i < len(axes):
                data = demographic_dist[category]
                if data:
                    labels = list(data.keys())
                    sizes = list(data.values())
                    
                    axes[i].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                    axes[i].set_title(f'{category.replace("_", " ").title()} Distribution')
                else:
                    axes[i].text(0.5, 0.5, f'No {category} data', 
                               ha='center', va='center', transform=axes[i].transAxes)
                    axes[i].set_title(f'{category.replace("_", " ").title()} Distribution')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_fairness_heatmap(self, fairness_metrics: Dict[str, Dict]) -> str:
        """Create fairness metrics heatmap."""
        # Prepare data for heatmap
        metrics_data = []
        attributes = []
        metric_names = set()
        
        for attr, metrics in fairness_metrics.items():
            if metrics:
                attributes.append(attr)
                for metric_name in metrics.keys():
                    metric_names.add(metric_name)
        
        metric_names = sorted(list(metric_names))
        
        # Create matrix
        matrix = []
        for attr in attributes:
            row = []
            for metric in metric_names:
                value = fairness_metrics.get(attr, {}).get(metric, 0)
                row.append(value)
            matrix.append(row)
        
        if matrix:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create heatmap
            im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=1)
            
            # Set ticks and labels
            ax.set_xticks(range(len(metric_names)))
            ax.set_yticks(range(len(attributes)))
            ax.set_xticklabels(metric_names, rotation=45, ha='right')
            ax.set_yticklabels(attributes)
            
            # Add colorbar
            plt.colorbar(im, ax=ax, label='Unfairness Score (0=Fair, 1=Unfair)')
            
            # Add text annotations
            for i in range(len(attributes)):
                for j in range(len(metric_names)):
                    text = ax.text(j, i, f'{matrix[i][j]:.3f}',
                                 ha="center", va="center", color="black")
            
            plt.title('Fairness Metrics Heatmap')
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
        else:
            # Return empty chart if no data
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No fairness metrics data available', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Fairness Metrics Heatmap')
            return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string."""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close(fig)
        return image_base64
    
    def _create_html_report(
        self, 
        test_results: Dict[str, Any],
        synthetic_data_stats: Dict[str, Any],
        middleware_metrics: Dict[str, Any],
        charts: Dict[str, str]
    ) -> str:
        """Create the complete HTML report."""
        
        # HTML template
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pratibimb RAI Comprehensive Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        .header {
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            color: #7f8c8d;
            font-size: 1.2em;
        }
        
        .section {
            margin-bottom: 40px;
            border-left: 4px solid #3498db;
            padding-left: 20px;
        }
        
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .metric-card h3 {
            margin-top: 0;
            font-size: 1.2em;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .chart-container {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 10px;
        }
        
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            margin: 5px;
        }
        
        .status-pass {
            background-color: #27ae60;
        }
        
        .status-warning {
            background-color: #f39c12;
        }
        
        .status-fail {
            background-color: #e74c3c;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        .data-table th,
        .data-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        .data-table th {
            background-color: #3498db;
            color: white;
        }
        
        .data-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🛡️ Pratibimb Responsible AI Report</h1>
            <div class="subtitle">Comprehensive Analysis & Safety Monitoring</div>
            <div class="subtitle">Generated on: {{ report_date }}</div>
        </div>
        
        <!-- Executive Summary -->
        <div class="section">
            <h2>📊 Executive Summary</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h3>Overall Safety Score</h3>
                    <div class="metric-value">{{ overall_score }}%</div>
                </div>
                <div class="metric-card">
                    <h3>Tests Executed</h3>
                    <div class="metric-value">{{ total_tests }}</div>
                </div>
                <div class="metric-card">
                    <h3>Bias Issues Found</h3>
                    <div class="metric-value">{{ bias_issues }}</div>
                </div>
                <div class="metric-card">
                    <h3>Toxicity Incidents</h3>
                    <div class="metric-value">{{ toxicity_incidents }}</div>
                </div>
            </div>
        </div>
        
        <!-- Bias Detection Results -->
        <div class="section">
            <h2>⚖️ Bias Detection Analysis</h2>
            {% if charts.bias_chart %}
            <div class="chart-container">
                <img src="data:image/png;base64,{{ charts.bias_chart }}" alt="Bias Detection Chart">
            </div>
            {% endif %}
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Protected Attribute</th>
                        <th>Bias Score</th>
                        <th>Status</th>
                        <th>Recommendations</th>
                    </tr>
                </thead>
                <tbody>
                    {% for attr, data in bias_results.items() %}
                    <tr>
                        <td>{{ attr.replace('_', ' ').title() }}</td>
                        <td>{{ "%.3f"|format(data.bias_score) }}</td>
                        <td>
                            {% if data.bias_score < 0.1 %}
                                <span class="status-badge status-pass">PASS</span>
                            {% elif data.bias_score < 0.3 %}
                                <span class="status-badge status-warning">CAUTION</span>
                            {% else %}
                                <span class="status-badge status-fail">HIGH RISK</span>
                            {% endif %}
                        </td>
                        <td>{{ data.recommendation }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- Toxicity Analysis -->
        <div class="section">
            <h2>🚨 Content Safety Analysis</h2>
            {% if charts.toxicity_chart %}
            <div class="chart-container">
                <img src="data:image/png;base64,{{ charts.toxicity_chart }}" alt="Toxicity Analysis Chart">
            </div>
            {% endif %}
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Content Category</th>
                        <th>Average Toxicity</th>
                        <th>Max Toxicity</th>
                        <th>Incidents</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for category, data in toxicity_results.items() %}
                    <tr>
                        <td>{{ category.replace('_', ' ').title() }}</td>
                        <td>{{ "%.3f"|format(data.avg_toxicity) }}</td>
                        <td>{{ "%.3f"|format(data.max_toxicity) }}</td>
                        <td>{{ data.incidents }}</td>
                        <td>
                            {% if data.max_toxicity < 0.3 %}
                                <span class="status-badge status-pass">SAFE</span>
                            {% elif data.max_toxicity < 0.7 %}
                                <span class="status-badge status-warning">MODERATE</span>
                            {% else %}
                                <span class="status-badge status-fail">HIGH RISK</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- Performance Metrics -->
        <div class="section">
            <h2>⚡ Performance Analysis</h2>
            {% if charts.performance_chart %}
            <div class="chart-container">
                <img src="data:image/png;base64,{{ charts.performance_chart }}" alt="Performance Metrics Chart">
            </div>
            {% endif %}
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <h3>Average Response Time</h3>
                    <div class="metric-value">{{ avg_response_time }}ms</div>
                </div>
                <div class="metric-card">
                    <h3>Success Rate</h3>
                    <div class="metric-value">{{ success_rate }}%</div>
                </div>
                <div class="metric-card">
                    <h3>Throughput</h3>
                    <div class="metric-value">{{ throughput }} req/s</div>
                </div>
                <div class="metric-card">
                    <h3>Error Rate</h3>
                    <div class="metric-value">{{ error_rate }}%</div>
                </div>
            </div>
        </div>
        
        <!-- Synthetic Data Analysis -->
        <div class="section">
            <h2>🧪 Synthetic Data Analysis</h2>
            {% if charts.demographic_chart %}
            <div class="chart-container">
                <img src="data:image/png;base64,{{ charts.demographic_chart }}" alt="Demographic Distribution Chart">
            </div>
            {% endif %}
            
            <p><strong>Total Synthetic Samples Generated:</strong> {{ synthetic_stats.total_samples }}</p>
            <p><strong>Bias Scenarios Covered:</strong> {{ synthetic_stats.bias_scenarios }}</p>
            <p><strong>Toxicity Test Cases:</strong> {{ synthetic_stats.toxicity_cases }}</p>
        </div>
        
        <!-- Fairness Metrics -->
        <div class="section">
            <h2>🎯 Fairness Analysis</h2>
            {% if charts.fairness_chart %}
            <div class="chart-container">
                <img src="data:image/png;base64,{{ charts.fairness_chart }}" alt="Fairness Metrics Heatmap">
            </div>
            {% endif %}
        </div>
        
        <!-- Recommendations -->
        <div class="section">
            <h2>💡 Recommendations</h2>
            <ul>
                {% for recommendation in recommendations %}
                <li>{{ recommendation }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Report generated by Pratibimb RAI Toolkit v1.0.0</p>
            <p>For questions or support, contact the Pratibimb AI Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Prepare template variables
        template_vars = self._prepare_template_variables(
            test_results, synthetic_data_stats, middleware_metrics, charts
        )
        
        # Render template
        template = Template(html_template)
        return template.render(**template_vars)
    
    def _prepare_template_variables(
        self, 
        test_results: Dict[str, Any],
        synthetic_data_stats: Dict[str, Any],
        middleware_metrics: Dict[str, Any],
        charts: Dict[str, str]
    ) -> Dict[str, Any]:
        """Prepare all variables for HTML template rendering."""
        
        # Calculate summary metrics
        bias_results = test_results.get('bias_tests', {})
        toxicity_results = test_results.get('toxicity_tests', {})
        performance_results = test_results.get('performance_tests', {})
        
        # Overall safety score calculation
        bias_scores = [data.get('bias_score', 0) for data in bias_results.values()]
        avg_bias_score = np.mean(bias_scores) if bias_scores else 0
        
        toxicity_scores = []
        for category_results in toxicity_results.values():
            if isinstance(category_results, list):
                toxicity_scores.extend([r.get('max_toxicity', 0) for r in category_results])
        avg_toxicity_score = np.mean(toxicity_scores) if toxicity_scores else 0
        
        # Calculate overall safety score (inverse of risk)
        overall_score = max(0, 100 - (avg_bias_score * 50 + avg_toxicity_score * 50))
        
        # Count issues
        bias_issues = sum(1 for data in bias_results.values() if data.get('bias_score', 0) > 0.1)
        toxicity_incidents = sum(
            1 for category_results in toxicity_results.values()
            for result in (category_results if isinstance(category_results, list) else [])
            if result.get('max_toxicity', 0) > 0.3
        )
        
        # Performance metrics
        response_times = performance_results.get('response_times', [])
        avg_response_time = int(np.mean(response_times) * 1000) if response_times else 0
        success_rate = performance_results.get('success_rate', 100)
        
        # Prepare bias results for table
        formatted_bias_results = {}
        for attr, data in bias_results.items():
            bias_score = data.get('bias_score', 0)
            if bias_score < 0.1:
                recommendation = "Bias levels within acceptable range. Continue monitoring."
            elif bias_score < 0.3:
                recommendation = "Moderate bias detected. Consider data augmentation and model retraining."
            else:
                recommendation = "High bias detected. Immediate intervention required."
            
            formatted_bias_results[attr] = {
                'bias_score': bias_score,
                'recommendation': recommendation
            }
        
        # Prepare toxicity results for table
        formatted_toxicity_results = {}
        for category, results in toxicity_results.items():
            if isinstance(results, list) and results:
                toxicity_scores = [r.get('max_toxicity', 0) for r in results]
                formatted_toxicity_results[category] = {
                    'avg_toxicity': np.mean(toxicity_scores),
                    'max_toxicity': max(toxicity_scores),
                    'incidents': sum(1 for score in toxicity_scores if score > 0.3)
                }
        
        # Generate recommendations
        recommendations = []
        if bias_issues > 0:
            recommendations.append(f"Address {bias_issues} bias issues found in protected attributes")
        if toxicity_incidents > 0:
            recommendations.append(f"Review {toxicity_incidents} high-toxicity content incidents")
        if avg_response_time > 5000:
            recommendations.append("Optimize performance - response times above 5 seconds detected")
        if not recommendations:
            recommendations.append("System operating within acceptable RAI parameters")
        
        return {
            'report_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'overall_score': int(overall_score),
            'total_tests': len(bias_results) + len(toxicity_results) + 1,
            'bias_issues': bias_issues,
            'toxicity_incidents': toxicity_incidents,
            'charts': charts,
            'bias_results': formatted_bias_results,
            'toxicity_results': formatted_toxicity_results,
            'avg_response_time': avg_response_time,
            'success_rate': int(success_rate),
            'throughput': 10,  # Placeholder
            'error_rate': max(0, 100 - int(success_rate)),
            'synthetic_stats': {
                'total_samples': synthetic_data_stats.get('total_samples', 0),
                'bias_scenarios': len(synthetic_data_stats.get('bias_test_data', [])),
                'toxicity_cases': len(synthetic_data_stats.get('toxicity_test_data', []))
            },
            'recommendations': recommendations
        }


# Example usage function
def generate_sample_report():
    """Generate a sample RAI report with mock data for demonstration."""
    
    # Mock test results
    test_results = {
        'bias_tests': {
            'gender': {'bias_score': 0.05, 'fairness_metrics': {'demographic_parity': 0.02}},
            'ethnicity': {'bias_score': 0.15, 'fairness_metrics': {'demographic_parity': 0.12}},
            'age': {'bias_score': 0.08, 'fairness_metrics': {'demographic_parity': 0.06}}
        },
        'toxicity_tests': {
            'safe_content': [{'max_toxicity': 0.1}, {'max_toxicity': 0.05}],
            'moderate_content': [{'max_toxicity': 0.4}, {'max_toxicity': 0.35}]
        },
        'performance_tests': {
            'response_times': [0.5, 0.7, 0.6, 0.8, 0.9],
            'success_rate': 98.5
        }
    }
    
    # Mock synthetic data stats
    synthetic_data_stats = {
        'total_samples': 1000,
        'demographic_distribution': {
            'gender': {'male': 45, 'female': 45, 'non_binary': 10},
            'ethnicity': {'caucasian': 30, 'asian': 25, 'african': 20, 'hispanic': 25}
        },
        'bias_test_data': ['scenario1', 'scenario2', 'scenario3'],
        'toxicity_test_data': ['case1', 'case2', 'case3', 'case4']
    }
    
    # Mock middleware metrics
    middleware_metrics = {
        'request_metrics': {
            'total_requests': 1500,
            'blocked_requests': 15,
            'flagged_content': 25
        }
    }
    
    # Generate report
    generator = RAIReportGenerator()
    report_path = generator.generate_comprehensive_report(
        test_results, synthetic_data_stats, middleware_metrics
    )
    
    return report_path


if __name__ == "__main__":
    # Generate sample report for testing
    try:
        report_path = generate_sample_report()
        print(f"Sample RAI report generated: {report_path}")
    except Exception as e:
        print(f"Error generating sample report: {e}")
