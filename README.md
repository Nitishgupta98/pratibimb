# Pratibimb - Professional Grade Braille Conversion System

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![Braille Standards](https://img.shields.io/badge/Braille-Grade%201-purple.svg)](https://www.brailleauthority.org/)

## 🎯 Overview

Pratibimb is a comprehensive accessibility and educational platform that combines professional-grade Braille conversion with community-driven learning and support. At its core, it transforms video content into accessible, embosser-ready Braille documents, while also providing a rich ecosystem of learning tools, audio resources, and community features. The platform serves as a bridge between visually impaired users, educators, volunteers, and content creators, fostering an inclusive environment for learning and collaboration.

### 🌈 Platform Vision
- **Accessibility First**: Making digital content accessible through Braille and audio
- **Community-Powered**: Connecting learners, educators, and volunteers
- **DIY Innovation**: Encouraging accessibility-focused projects and innovations
- **Collaborative Learning**: Building a supportive ecosystem for visually impaired education

### 👥 Team

- **Team Name:** Pratibimb
- **Members:**
  - Bhupinder Singh Chawla
  - Nitish Gupta

## 🌟 Key Features

### Core Accessibility Features
- 📹 Automatic YouTube video transcription
- 🔊 Enhanced audio descriptions
- 🖼️ Visual content interpretation
- ⠃ Grade 1 Braille conversion (Unicode)
- 🖨️ Professional embosser-ready output (BRF format)
- 🌐 Multi-language support (English, Telugu, Kannada)
- 🎨 ASCII/Braille art generation for visual elements
- 🤖 Responsible AI content analysis
- 📊 Comprehensive analytics and validation

### Dhvani Learning Assistant
- 🎧 Audio book library and management
- 📱 Smart device integration for audio learning
- 📲 Device assignment and management system
- 📤 Content push functionality to student devices
- 👥 Role-based access control (School Admin, Teacher, Student)
- 📚 Interactive learning tools and resources

### Educational Tools
- 📖 Interactive Braille learning modules
- 🎮 Practice exercises
- 📝 Progress tracking and assessment
- 🗂️ Structured learning paths
- 👨‍🏫 Teacher-student interaction tools

### Marketplace Integration
- 🛒 Access to educational resources
- 📦 Content distribution system
- 🔄 Resource sharing between institutions
- 📱 Device and content synchronization
- 🎯 Personalized content recommendations

### Community & Collaboration Features
- 👥 Volunteer program for content creation and support
- 🔧 DIY Projects platform for accessibility innovations
- 🤝 Connect with experienced volunteers and mentors
- 📝 Project sharing and documentation
- ⭐ Community ratings and reviews system
- 📢 Task posting and volunteer matching
- 🏆 Recognition system for community contributors
- 💡 Knowledge sharing and best practices
- 🌟 Featured projects and success stories

## 🔧 Technologies Used

### Core Technologies
- Python 3.13+
- FastAPI
- React.js
- SQLite

### Key Libraries and Models
- `transformers` (BLIP model for visual descriptions)
- `pytorch` (Deep learning)
- Gemini Pro 2.5 (Multi-purpose AI model for):
  - Language translation
  - Transcript enhancement
  - ASCII art generation
  - Braille art conversion
  - Content merging and analysis
- Custom Braille conversion engine

### Infrastructure
- RESTful API architecture
- Content-based modular pipeline
- Professional Braille embosser compatibility
- Infosys RAI (Responsible AI) integration

## 🚀 Getting Started

### Prerequisites
- Python 3.13 or higher
- Node.js 14+
- SQLite3
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
   \`\`\`bash
   git clone <repository-url>
   cd Pratibimb-codebase
   \`\`\`

2. **Set up Python environment:**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   \`\`\`

3. **Install Python dependencies:**
   \`\`\`bash
   cd API
   pip install -r requirements.txt
   pip install -r rai_requirements.txt  # For RAI features
   \`\`\`

4. **Set up UI dependencies:**
   \`\`\`bash
   cd ../ui/react-app
   npm install
   \`\`\`

### Configuration

1. **API Configuration:**
   - Copy \`API/config.json.example\` to \`API/config.json\`
   - Update settings for your environment

2. **Database Setup:**
   \`\`\`bash
   cd db
   python create_database.py
   \`\`\`

### Running the Application

1. **Start the API server:**
   \`\`\`bash
   cd API
   ./start_api.sh  # On Windows: start_api.bat
   \`\`\`
   Server will be available at: http://localhost:8001

2. **Start the UI development server:**
   \`\`\`bash
   cd ui/react-app
   npm start
   \`\`\`
   UI will be available at: http://localhost:3000

## 📖 API Documentation

The API provides 14 modular endpoints for the Braille conversion pipeline:

1. \`/validate-youtube-url\` - Validate YouTube URL
2. \`/download-video\` - Download video from YouTube
3. \`/extract-audio-transcript\` - Extract audio transcript
4. \`/extract-video-frames\` - Extract video frames
5. \`/deduplicate-frames\` - Remove duplicate frames
6. \`/generate-visual-descriptions\` - Generate descriptions for frames
7. \`/merge-audio-visual\` - Merge audio and visual transcripts
8. \`/rai-content-analysis\` - Responsible AI Content Analysis
9. \`/extract-visual-objects\` - Extract relevant visual objects
10. \`/enrich-with-figure-tags\` - Add figure tags to transcript
11. \`/generate-ascii-art\` - Generate ASCII art from objects
12. \`/generate-braille-art\` - Convert ASCII to Braille art
13. \`/assemble-final-document\` - Combine transcript with Braille art
14. \`/finalize-output\` - Generate final downloadable files

Detailed API documentation is available at: http://localhost:8001/docs

## 🧪 Testing

Run the comprehensive test suite:

\`\`\`bash
cd API/tests
python test_braille_validation.py
python test_database.py
./test_workflow.sh
\`\`\`

## 📊 Output Formats

The system generates multiple output formats:

1. **Enhanced Transcript** (\`.txt\`)
   - Enhanced description for visually impaired users
   - Includes visual and audio context

2. **Unicode Braille** (\`.txt\`)
   - Grade 1 Braille with proper formatting
   - Compatible with screen readers

3. **Embosser File** (\`.brf\`)
   - Professional Braille Ready Format
   - Compatible with all major embossers
   - 40 characters per line, 25 lines per page

4. **Braille Art** (\`.txt\`)
   - Tactile representations of visual elements
   - ASCII art converted to Braille patterns

## 🔍 Quality Assurance

- **Validation Engine**: Ensures embosser compliance
- **Line Format**: Strict 40x25 character pages
- **Character Set**: Grade 1 Braille standards
- **RAI Analysis**: Content safety and bias detection
- **Quality Reports**: Detailed validation statistics

## 🌐 Supported Languages

- English (Grade 1 Braille)
- Telugu (With Unicode conversion)
- Kannada (With Unicode conversion)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - See [LICENSE](LICENSE) for details.

The Apache License 2.0 is a permissive open-source license that allows you to:
- Use the software for any purpose
- Distribute it
- Modify it
- Distribute modified versions of it

under the condition that you include the original copyright and license notice.

## 🙏 Acknowledgments

- [Salesforce BLIP Model](https://github.com/salesforce/BLIP)
- [FastAPI Framework](https://fastapi.tiangolo.com/)
- [Braille Authority of North America](https://www.brailleauthority.org/)
- [YouTube Data API](https://developers.google.com/youtube/v3)

---

_Built for the InfyHack2025 Challenge_
