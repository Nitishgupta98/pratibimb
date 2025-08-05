# Responsible AI (RAI) Module Documentation

## Overview

This module implements a comprehensive Responsible AI (RAI) solution for the Pratibimb FastAPI application, ensuring no harmful content reaches end-users while providing extensive testing capabilities and detailed analytics reporting.

## Requirements Specification

### Phase 1: Repository Analysis & Integration Points
- **Target Application**: FastAPI-based Pratibimb application with YouTube accessibility pipeline
- **Integration Points**: Content processing endpoints, Gemini API interactions
- **Configuration**: All RAI features must be togglable via configuration file

### Phase 2: Core RAI Implementation

#### 2.1 Dependency Management
- **RAI Toolkit**: Infosys Responsible AI Toolkit integration
- **Dependencies File**: `rai_requirements.txt` with all required packages
- **Installation**: Isolated dependency management for RAI components

#### 2.2 Configuration System
- **File**: `rai_config.json` 
- **Structure**: Hierarchical configuration with global enable/disable
- **Features**: Individual toggles for each RAI capability
- **Loading**: Runtime configuration loading with fallback defaults

#### 2.3 RAI Guardrails Implementation
- **Middleware**: `rai_middleware.py` - FastAPI middleware for request/response processing
- **Capabilities Required**:
  - Content Safety Detection (pornography, hate speech, violence, self-harm)
  - PII Detection and Protection
  - Hallucination Detection
  - Bias Analysis and Detection
  - Prompt Injection/Jailbreak Prevention
  - Explainability and Transparency

#### 2.4 Integration Requirements
- **Input Guardrails**: Pre-processing content before AI model calls
- **Output Guardrails**: Post-processing AI-generated content
- **Blocking Logic**: HTTP 400 for harmful inputs, HTTP 403 for blocked content
- **Response Enhancement**: Include RAI analysis results when enabled
- **Conditional Execution**: All RAI checks wrapped in configuration toggles

### Phase 3: Test Engine Architecture

#### 3.1 Testing Framework
- **Framework**: pytest with async support
- **HTTP Client**: httpx for API testing
- **Test Structure**: Modular test organization by RAI category

#### 3.2 Synthetic Data Generation
- **File**: `rai_synthetic_data.py`
- **Coverage Areas**:
  - Safety: Explicit content, hate speech, violence, self-harm, borderline cases
  - Privacy: PII scenarios (SSN, credit cards, emails, phones, addresses)
  - Hallucination: Non-existent entities, false information
  - Bias: Demographic stereotypes, occupational bias
  - Prompt Injection: Known attack patterns, jailbreak attempts
  - Baseline: Safe, unbiased content for comparison
- **Methodology**: Programmatic generation with statistical distributions

#### 3.3 Test Suite Implementation
- **File**: `rai_test_engine.py`
- **Test Categories**: Comprehensive coverage of all RAI scenarios
- **Assertions**: Status codes, RAI analysis results, content blocking
- **Toggle Testing**: Validation of RAI enable/disable functionality
- **Data Collection**: Capture all test metrics for reporting

### Phase 4: Reporting System

#### 4.1 Data Collection Requirements
- **Metrics**: Test results, latency, analysis scores, timestamps
- **Storage**: JSON format for report generation
- **Scope**: Input/output analysis, expected vs actual outcomes

#### 4.2 HTML Report Generation
- **File**: `rai_report_generator.py`
- **Output**: Responsive HTML reports with analytics
- **Features**:
  - Collapsible sidebar navigation
  - Interactive filtering and search
  - Visual analytics and charts
  - Detailed test case breakdowns
  - Performance metrics
- **Technologies**: HTML5, CSS3, JavaScript, Font Awesome icons

#### 4.3 Analytics & Visualization
- **Metrics**:
  - Pass/fail rates by category
  - Content type breakdowns
  - Performance statistics
  - Bias and safety analysis summaries
- **Presentation**: Charts, graphs, and tabular data
- **Interactivity**: Expandable sections, filtering, search

### Phase 5: Production Readiness

#### 5.1 Quality Assurance
- **Error Handling**: Robust exception management
- **Logging**: Comprehensive logging for monitoring
- **Performance**: Optimized for production workloads
- **Security**: Secure handling of sensitive content

#### 5.2 Documentation & Deployment
- **Documentation**: Complete API documentation and usage guides
- **Configuration**: Production-ready default settings
- **Integration**: Seamless FastAPI middleware integration
- **Monitoring**: Health checks and status endpoints

## File Structure

```
RAI/
├── __init__.py                 # Module initialization and exports
├── rai_config.json            # Configuration file for all RAI features
├── rai_requirements.txt       # RAI-specific dependencies
├── rai_middleware.py          # FastAPI middleware implementation
├── rai_synthetic_data.py      # Synthetic test data generation
├── rai_test_engine.py         # Comprehensive test suite
├── rai_report_generator.py    # HTML report generation
├── rai_orchestrator.py        # Test execution orchestration
└── README.md                  # This documentation file
```

## Configuration Schema

```json
{
  "enabled": true,
  "rai_settings": {
    "enabled": true,
    "mode": "development|production",
    "strict_mode": false,
    "log_all_requests": true,
    "block_harmful_content": true
  },
  "content_filters": {
    "toxicity": {"enabled": true, "threshold": 0.8},
    "hate_speech": {"enabled": true, "threshold": 0.7},
    "violence": {"enabled": true, "threshold": 0.8},
    "self_harm": {"enabled": true, "threshold": 0.9}
  },
  "privacy_protection": {
    "pii_detection": {"enabled": true, "action": "block"},
    "data_anonymization": {"enabled": false}
  },
  "bias_detection": {
    "enabled": true,
    "demographic_bias": {"enabled": true, "threshold": 0.6},
    "occupational_bias": {"enabled": true, "threshold": 0.6}
  }
}
```

## Usage Examples

### Basic Integration
```python
from RAI.rai_middleware import RAIMiddleware
app.add_middleware(RAIMiddleware, config=rai_config)
```

### Test Execution
```bash
python3 RAI/rai_orchestrator.py --quick
```

### Report Generation
Reports are automatically generated in `rai_reports/` directory with timestamped filenames.

## Production Deployment

1. **Configuration**: Set `"mode": "production"` in `rai_config.json`
2. **Dependencies**: Install via `pip install -r RAI/rai_requirements.txt`
3. **Integration**: Middleware automatically integrates when RAI is enabled
4. **Monitoring**: Check logs for RAI activity and performance metrics

## Testing & Validation

The RAI module includes comprehensive self-testing capabilities:
- Synthetic data generation for all threat scenarios
- Automated test execution with detailed reporting
- Performance benchmarking and analytics
- Configuration validation and toggle testing

All testing code is isolated and does not affect production operation.
