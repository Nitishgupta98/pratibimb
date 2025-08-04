"""
Pratibimb-Gemini Integration Example
This script shows how to integrate Gemini AI with the Pratibimb platform
for enhanced accessibility content generation
"""

import os
import sys
from typing import Dict, Any

# Add parent directory to path to import gemini_client
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gemini_client import GeminiClient
    GEMINI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Gemini client not available: {e}")
    GEMINI_AVAILABLE = False

class PratibimbGeminiIntegration:
    """
    Integration class for using Gemini AI within the Pratibimb platform
    """
    
    def __init__(self):
        """Initialize the Gemini integration"""
        self.gemini_client = None
        self.is_available = False
        
        if GEMINI_AVAILABLE:
            try:
                self.gemini_client = GeminiClient()
                self.is_available = True
                print("✅ Gemini AI integration initialized successfully!")
            except Exception as e:
                print(f"⚠️  Gemini initialization failed: {e}")
                self.is_available = False
        else:
            print("⚠️  Gemini not available - some features will be disabled")
    
    def enhance_text_for_braille(self, text: str) -> Dict[str, Any]:
        """
        Enhance text content for better braille accessibility
        
        Args:
            text (str): Original text content
            
        Returns:
            Dict containing enhanced content and metadata
        """
        if not self.is_available:
            return {
                "enhanced_text": text,
                "improvements": [],
                "ai_enhanced": False,
                "error": "Gemini AI not available"
            }
        
        try:
            prompt = f"""
            Please enhance the following text for braille accessibility by:
            1. Simplifying complex sentences
            2. Adding descriptive context where needed
            3. Ensuring clear spatial relationships
            4. Maintaining all essential information
            5. Using braille-friendly terminology
            
            Original text: {text}
            
            Please provide:
            1. Enhanced text
            2. List of improvements made
            3. Any important notes for braille conversion
            
            Format your response as:
            ENHANCED TEXT:
            [enhanced content here]
            
            IMPROVEMENTS:
            - [improvement 1]
            - [improvement 2]
            
            NOTES:
            [any special notes]
            """
            
            response = self.gemini_client.generate_text(prompt)
            
            # Parse the response
            enhanced_text = text  # Default fallback
            improvements = []
            notes = ""
            
            sections = response.split("ENHANCED TEXT:")
            if len(sections) > 1:
                content = sections[1].split("IMPROVEMENTS:")[0].strip()
                enhanced_text = content
                
                if "IMPROVEMENTS:" in response:
                    imp_section = response.split("IMPROVEMENTS:")[1].split("NOTES:")[0]
                    improvements = [line.strip()[2:] for line in imp_section.split('\n') if line.strip().startswith('- ')]
                
                if "NOTES:" in response:
                    notes = response.split("NOTES:")[1].strip()
            
            return {
                "enhanced_text": enhanced_text,
                "improvements": improvements,
                "notes": notes,
                "ai_enhanced": True,
                "original_length": len(text),
                "enhanced_length": len(enhanced_text)
            }
            
        except Exception as e:
            return {
                "enhanced_text": text,
                "improvements": [],
                "ai_enhanced": False,
                "error": f"Enhancement failed: {str(e)}"
            }
    
    def generate_audio_description(self, content_type: str, context: str) -> str:
        """
        Generate audio descriptions for visual content
        
        Args:
            content_type (str): Type of content (image, video, diagram, etc.)
            context (str): Context or description of the content
            
        Returns:
            str: Generated audio description
        """
        if not self.is_available:
            return f"Audio description not available. Original context: {context}"
        
        try:
            prompt = f"""
            Create a detailed audio description for a {content_type} that will be used in an accessibility platform.
            
            Context: {context}
            
            The description should be:
            1. Clear and concise
            2. Descriptive but not overwhelming
            3. Suitable for braille and audio conversion
            4. Include spatial relationships when relevant
            5. Focus on essential visual information
            
            Provide a professional audio description:
            """
            
            return self.gemini_client.generate_text(prompt)
            
        except Exception as e:
            return f"Error generating description: {str(e)}. Original context: {context}"
    
    def improve_learning_content(self, topic: str, content: str) -> Dict[str, Any]:
        """
        Improve learning content for accessibility
        
        Args:
            topic (str): Learning topic
            content (str): Original content
            
        Returns:
            Dict containing improved content and suggestions
        """
        if not self.is_available:
            return {
                "improved_content": content,
                "accessibility_tips": [],
                "ai_enhanced": False
            }
        
        try:
            prompt = f"""
            Improve the following learning content about "{topic}" for maximum accessibility:
            
            Original content: {content}
            
            Please provide:
            1. Improved content that is braille-friendly
            2. Accessibility tips for teachers/students
            3. Suggestions for tactile or audio enhancements
            
            Format as:
            IMPROVED CONTENT:
            [content here]
            
            ACCESSIBILITY TIPS:
            - [tip 1]
            - [tip 2]
            
            TACTILE/AUDIO SUGGESTIONS:
            - [suggestion 1]
            - [suggestion 2]
            """
            
            response = self.gemini_client.generate_text(prompt)
            
            # Parse response (simplified parsing)
            improved_content = content
            tips = []
            suggestions = []
            
            if "IMPROVED CONTENT:" in response:
                improved_content = response.split("IMPROVED CONTENT:")[1].split("ACCESSIBILITY TIPS:")[0].strip()
            
            if "ACCESSIBILITY TIPS:" in response:
                tips_section = response.split("ACCESSIBILITY TIPS:")[1].split("TACTILE/AUDIO SUGGESTIONS:")[0]
                tips = [line.strip()[2:] for line in tips_section.split('\n') if line.strip().startswith('- ')]
            
            if "TACTILE/AUDIO SUGGESTIONS:" in response:
                sugg_section = response.split("TACTILE/AUDIO SUGGESTIONS:")[1]
                suggestions = [line.strip()[2:] for line in sugg_section.split('\n') if line.strip().startswith('- ')]
            
            return {
                "improved_content": improved_content,
                "accessibility_tips": tips,
                "tactile_suggestions": suggestions,
                "ai_enhanced": True
            }
            
        except Exception as e:
            return {
                "improved_content": content,
                "accessibility_tips": [],
                "ai_enhanced": False,
                "error": f"Improvement failed: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of Gemini integration"""
        status = {
            "gemini_available": self.is_available,
            "model_info": None,
            "features_available": []
        }
        
        if self.is_available and self.gemini_client:
            status["model_info"] = self.gemini_client.get_model_info()
            status["features_available"] = [
                "Text Enhancement for Braille",
                "Audio Description Generation", 
                "Learning Content Improvement",
                "Accessibility Optimization"
            ]
        
        return status

def demo_integration():
    """Demonstrate the Gemini integration features"""
    print("🚀 Pratibimb-Gemini Integration Demo")
    print("=" * 50)
    
    # Initialize integration
    integration = PratibimbGeminiIntegration()
    
    # Show status
    status = integration.get_status()
    print(f"\n📊 Integration Status:")
    print(f"   Gemini Available: {status['gemini_available']}")
    
    if status['gemini_available']:
        print(f"   Features: {', '.join(status['features_available'])}")
        
        # Demo text enhancement
        print(f"\n🔤 Text Enhancement Demo:")
        sample_text = "The complex diagram shows multiple interconnected components with arrows indicating data flow."
        result = integration.enhance_text_for_braille(sample_text)
        
        print(f"   Original: {sample_text}")
        print(f"   Enhanced: {result['enhanced_text'][:100]}...")
        print(f"   Improvements: {len(result.get('improvements', []))}")
        
        # Demo audio description
        print(f"\n🎵 Audio Description Demo:")
        description = integration.generate_audio_description("diagram", "Network topology with servers and connections")
        print(f"   Description: {description[:100]}...")
        
    else:
        print("   ⚠️  Add your API key to config.env to enable features")
    
    print(f"\n✅ Demo completed!")

if __name__ == "__main__":
    demo_integration()
