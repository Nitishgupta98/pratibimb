# RAI Content Analysis API Endpoint Documentation

## Overview

The `/rai-content-analysis` endpoint provides comprehensive Responsible AI content analysis with safety checks, bias detection, and detailed reporting capabilities. This endpoint integrates the complete RAI pipeline into the modular pipeline API.

## Endpoint Details

**URL:** `POST /rai-content-analysis`  
**Content-Type:** `application/json`

## Features

### 🛡️ Content Safety Analysis
- **Toxicity Detection**: Identifies harmful, toxic, or offensive content
- **Hate Speech Detection**: Detects hate speech targeting individuals or groups
- **Violence Detection**: Identifies violent or threatening content
- **Self-Harm Detection**: Detects content promoting self-harm or suicide

### ⚖️ Bias Detection
- **Demographic Bias**: Identifies bias based on gender, race, age, religion
- **Linguistic Bias**: Detects bias in language patterns and terminology
- **Cultural Bias**: Identifies cultural stereotypes and prejudices

### 🔒 Privacy Protection
- **PII Detection**: Identifies personally identifiable information
- **Data Privacy**: Ensures sensitive information is flagged

### 📊 Comprehensive Reporting
- **Interactive HTML Reports**: Downloadable reports with charts and analytics
- **Detailed Analytics**: Risk assessment, safety scores, recommendations
- **Visual Insights**: Charts showing bias distribution, safety metrics

## Request Format

```json
{
  "content": "string",              // Required: Content to analyze
  "analysis_type": "string",       // Optional: "safety", "bias", "comprehensive" (default)
  "include_report": boolean,       // Optional: Generate HTML report (default: true)
  "report_format": "string"        // Optional: "html", "json" (default: "html")
}
```

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content` | string | Yes | - | The text content to analyze |
| `analysis_type` | string | No | "comprehensive" | Type of analysis: "safety", "bias", or "comprehensive" |
| `include_report` | boolean | No | true | Whether to generate a downloadable HTML report |
| `report_format` | string | No | "html" | Format of the report: "html" or "json" |

## Response Format

### Success Response (200 OK)

```json
{
  "status": "success",
  "verdict": "SAFE|WARNING|UNSAFE",
  "message": "🔍 RAI analysis completed: SAFE",
  "analysis": {
    "content_length": 150,
    "analysis_type": "comprehensive",
    "risk_level": "low|medium|high",
    "blocked": false,
    "warnings_count": 0,
    "safety_scores": {
      "toxicity": 0.05,
      "hate_speech": 0.02,
      "threat": 0.01,
      "insult": 0.03
    },
    "bias_indicators": {
      "demographic_bias": 0.1,
      "linguistic_bias": 0.0,
      "cultural_bias": 0.0,
      "detected_terms": [],
      "confidence": 0.1
    },
    "sentiment": {
      "label": "POSITIVE",
      "score": 0.85,
      "confidence": "high"
    },
    "recommendations": [
      "Content appears safe for general use"
    ],
    "analysis_duration_seconds": 0.45
  },
  "detailed_results": {
    // Complete analysis results with all metrics
  },
  "report": {
    "format": "html",
    "filename": "rai_content_analysis_report_20250731_143022.html",
    "content": "base64_encoded_html_content",
    "size_bytes": 125000,
    "download_instructions": "Decode the base64 content and save as .html file to view the report"
  },
  "timestamp": "2025-07-31T14:30:22.123456"
}
```

### Error Responses

#### 400 Bad Request - Empty Content
```json
{
  "status": "error",
  "message": "❌ Content cannot be empty for RAI analysis",
  "timestamp": "2025-07-31T14:30:22.123456"
}
```

#### 503 Service Unavailable - RAI Not Available
```json
{
  "status": "error",
  "message": "❌ RAI services are not available. Please install RAI dependencies.",
  "timestamp": "2025-07-31T14:30:22.123456"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "❌ RAI content analysis failed: [error details]",
  "timestamp": "2025-07-31T14:30:22.123456"
}
```

## Verdict Categories

### 🟢 SAFE
- Content is safe for general use
- Low risk scores across all categories
- No harmful content detected
- Minimal or no bias indicators

### 🟡 WARNING
- Content has potential issues but is not critically harmful
- Medium risk scores in some categories
- Minor bias indicators detected
- Content may require review

### 🔴 UNSAFE
- Content contains harmful, toxic, or dangerous material
- High risk scores in safety categories
- Content should be blocked or heavily moderated
- Significant bias or harmful content detected

## Usage Examples

### Basic Content Analysis

```bash
curl -X POST "http://localhost:8001/rai-content-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a sample text for analysis",
    "analysis_type": "comprehensive",
    "include_report": true
  }'
```

### Safety-Only Analysis

```bash
curl -X POST "http://localhost:8001/rai-content-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Check this content for safety issues",
    "analysis_type": "safety",
    "include_report": false
  }'
```

### Python Example

```python
import requests
import base64

# Analyze content
response = requests.post(
    "http://localhost:8001/rai-content-analysis",
    json={
        "content": "Your content here...",
        "analysis_type": "comprehensive",
        "include_report": True,
        "report_format": "html"
    }
)

result = response.json()

# Check verdict
verdict = result["verdict"]  # SAFE, WARNING, or UNSAFE
risk_level = result["analysis"]["risk_level"]

# Download HTML report
if "report" in result:
    report_content = base64.b64decode(result["report"]["content"])
    with open("rai_report.html", "wb") as f:
        f.write(report_content)
    print("Report saved as rai_report.html")
```

## HTML Report Features

The generated HTML reports include:

### 📊 Executive Dashboard
- Overall verdict and risk assessment
- Key safety metrics at a glance
- Analysis summary and recommendations

### 📈 Detailed Analytics
- Interactive charts showing safety scores
- Bias detection breakdowns
- Sentiment analysis results
- Content categorization

### 🔍 Content Analysis
- Detailed breakdown of detected issues
- Explanations for flagged content
- Confidence scores for each category

### 💡 Recommendations
- Actionable advice for content improvement
- Best practices for responsible content
- Risk mitigation suggestions

## Integration with Modular Pipeline

The RAI endpoint integrates seamlessly with the existing modular pipeline:

1. **Standalone Analysis**: Use independently for content validation
2. **Pipeline Integration**: Integrate into content processing workflows
3. **Quality Assurance**: Add as a validation step in content pipelines
4. **Monitoring**: Use for ongoing content quality monitoring

## Performance Considerations

- **Analysis Time**: Typically 0.5-2 seconds per request
- **Content Length**: Optimized for text up to 10,000 characters
- **Report Generation**: Adds 1-3 seconds for HTML report creation
- **Concurrent Requests**: Supports multiple simultaneous analyses

## Security and Privacy

- **No Content Storage**: Content is analyzed in-memory only
- **Temporary Files**: Reports are generated temporarily and cleaned up
- **Privacy Protection**: PII detection helps identify sensitive information
- **Audit Trail**: Analysis results can be logged for compliance

## Testing

Use the provided test script to validate the endpoint:

```bash
python3 test_rai_endpoint.py
```

This will run comprehensive tests covering:
- Safe content scenarios
- Bias detection tests
- Toxic content handling
- Error case validation
- Report generation verification

## Troubleshooting

### Common Issues

1. **503 Service Unavailable**
   - Install RAI dependencies: `pip install -r RAI/rai_requirements.txt`
   - Ensure RAI configuration is properly set up

2. **Slow Response Times**
   - Reduce content length for faster analysis
   - Disable report generation for quicker responses

3. **Memory Issues**
   - Monitor memory usage during report generation
   - Consider processing smaller content chunks

### Debug Mode

Enable debug logging in the RAI configuration:

```json
{
  "rai_settings": {
    "debug_mode": true,
    "log_analysis_details": true
  }
}
```

## Configuration

The endpoint uses the RAI configuration from `RAI/rai_config.json`:

```json
{
  "enabled": true,
  "rai_settings": {
    "enabled": true,
    "mode": "production",
    "strict_mode": false
  },
  "content_filters": {
    "toxicity": {
      "enabled": true,
      "threshold": 0.8,
      "action": "warn"
    },
    "bias": {
      "enabled": true,
      "threshold": 0.6,
      "action": "warn"
    }
  }
}
```

## Support

For issues or questions about the RAI content analysis endpoint:

1. Check the generated HTML reports for detailed insights
2. Review the API logs for error details
3. Use the test script to validate functionality
4. Ensure all RAI dependencies are properly installed

---

**Status: ✅ Production Ready**

The RAI content analysis endpoint provides enterprise-grade content safety and bias detection with comprehensive reporting capabilities.
