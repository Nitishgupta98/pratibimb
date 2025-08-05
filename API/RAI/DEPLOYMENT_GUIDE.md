# RAI Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Responsible AI (RAI) implementation in production environments.

## Prerequisites

- Python 3.8+ environment
- FastAPI application running
- Access to modify configuration files
- Required dependencies installed

## Quick Start

### 1. Install Dependencies

```bash
# Install RAI-specific dependencies
pip install -r RAI/rai_requirements.txt

# Or install specific packages if preferred:
pip install pandas scikit-learn matplotlib seaborn plotly jinja2 transformers faker pytest
```

### 2. Enable RAI Features

Edit `RAI/rai_config.json`:

```json
{
  "enabled": true,
  "rai_settings": {
    "enabled": true,
    "mode": "production",
    "strict_mode": true
  }
}
```

### 3. Start the Application

```bash
# The RAI middleware will be automatically loaded
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Configuration Options

### Production Configuration

For production environments, use these recommended settings:

```json
{
  "enabled": true,
  "rai_settings": {
    "enabled": true,
    "mode": "production",
    "strict_mode": true,
    "log_all_requests": false,
    "block_harmful_content": true,
    "content_safety_threshold": 0.8,
    "bias_detection_threshold": 0.7
  },
  "content_filters": {
    "toxicity": {
      "enabled": true,
      "threshold": 0.8,
      "action": "block"
    },
    "hate_speech": {
      "enabled": true,
      "threshold": 0.7,
      "action": "block"
    }
  }
}
```

### Development Configuration

For development and testing:

```json
{
  "enabled": true,
  "rai_settings": {
    "enabled": true,
    "mode": "development",
    "strict_mode": false,
    "log_all_requests": true,
    "block_harmful_content": true,
    "content_safety_threshold": 0.6,
    "bias_detection_threshold": 0.5
  }
}
```

### Disable RAI

To completely disable RAI features:

```json
{
  "enabled": false
}
```

## Testing and Validation

### Run RAI Tests

```bash
# Run the complete test suite
python RAI/rai_orchestrator.py

# This will generate:
# - Synthetic test data
# - Run comprehensive tests
# - Generate HTML reports in rai_reports/
```

### Validate Live API

```bash
# Test the live API with RAI
python test_live_rai.py
```

## Monitoring and Logging

### Log Messages

The RAI middleware provides detailed logging:

```
✅ Responsible AI middleware activated with safety monitoring
⚠️ Content blocked due to safety concerns: [details]
ℹ️ RAI analysis completed: bias_score=0.1, toxicity_score=0.05
```

### Key Metrics

Monitor these metrics in production:

- **Content Safety**: Toxicity detection rates
- **Bias Detection**: Demographic bias scores  
- **Privacy Protection**: PII detection accuracy
- **Performance**: Response latency impact
- **User Experience**: Blocked content rates

## Performance Optimization

### Production Optimizations

1. **Async Processing**: All RAI analysis runs asynchronously
2. **Caching**: Configure response caching for repeated content
3. **Batch Processing**: Process multiple requests efficiently
4. **Resource Limits**: Set appropriate memory and CPU limits

### Recommended Settings

```python
# In production environment
RAI_SETTINGS = {
    "enable_caching": True,
    "max_concurrent_requests": 100,
    "timeout_seconds": 30,
    "memory_limit_mb": 1024
}
```

## Troubleshooting

### Common Issues

#### 1. RAI Dependencies Missing

**Error**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
pip install -r RAI/rai_requirements.txt
```

#### 2. Configuration File Not Found

**Error**: `RAI configuration file not found`

**Solution**: Ensure `RAI/rai_config.json` exists and is properly formatted.

#### 3. High Latency

**Symptom**: API responses are slow

**Solutions**:
- Reduce analysis thresholds
- Enable caching
- Scale horizontally

#### 4. False Positives

**Symptom**: Safe content being blocked

**Solutions**:
- Adjust thresholds in configuration
- Review bias detection settings
- Add content whitelisting

### Debug Mode

Enable debug logging:

```json
{
  "rai_settings": {
    "debug_mode": true,
    "log_analysis_details": true
  }
}
```

## Security Considerations

### Data Protection

1. **PII Handling**: Detected PII is logged securely
2. **Content Logging**: Configure based on privacy requirements
3. **API Security**: RAI doesn't affect existing authentication

### Compliance

The RAI implementation supports:

- **GDPR**: PII detection and protection
- **Content Standards**: Toxicity and bias mitigation
- **Accessibility**: Integration with existing accessibility features

## Scaling and High Availability

### Horizontal Scaling

The RAI middleware is stateless and scales horizontally:

```yaml
# Docker deployment example
services:
  fastapi-app:
    image: pratibimb-api:latest
    replicas: 3
    environment:
      - RAI_ENABLED=true
      - RAI_MODE=production
```

### Load Balancing

Configure load balancers to distribute RAI processing:

```nginx
upstream fastapi_backend {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}
```

## API Documentation

### RAI-Enhanced Responses

When RAI is enabled, API responses include additional metadata:

```json
{
  "result": "...",
  "rai_analysis": {
    "safety_score": 0.95,
    "bias_detected": false,
    "pii_detected": false,
    "content_safe": true,
    "analysis_timestamp": "2024-01-01T12:00:00Z"
  }
}
```

### Error Responses

Blocked content returns HTTP 403:

```json
{
  "detail": "Content blocked due to safety concerns",
  "rai_reason": "High toxicity detected",
  "safety_score": 0.15,
  "blocked_categories": ["toxicity", "hate_speech"]
}
```

## Maintenance

### Regular Tasks

1. **Update Dependencies**: Monthly security updates
2. **Review Logs**: Weekly analysis of blocked content
3. **Adjust Thresholds**: Based on false positive rates
4. **Performance Monitoring**: Track latency and resource usage

### Update Process

```bash
# Update RAI dependencies
pip install -r RAI/rai_requirements.txt --upgrade

# Test updated configuration
python RAI/rai_orchestrator.py

# Deploy updates
systemctl restart fastapi-app
```

## Support and Documentation

### Additional Resources

- **README.md**: Complete feature documentation
- **VALIDATION_REPORT.md**: Implementation validation details
- **Generated Reports**: HTML reports in `rai_reports/`

### Contact

For RAI-related issues:
1. Check logs for detailed error messages
2. Review configuration settings
3. Run test suite for validation
4. Check generated reports for insights

## Conclusion

The RAI implementation is production-ready and provides comprehensive content safety, bias detection, and privacy protection. Follow this guide for successful deployment and ongoing maintenance.

**Status: ✅ Production Ready**
