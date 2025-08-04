#!/usr/bin/env python3
"""
Braille Art Demo Script
======================

Demonstrates the new image-to-Braille art conversion functionality.
This script shows how to use the enhanced Pratibimb converter with images.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pratibimb import (
    load_config, 
    text_to_braille_unicode, 
    process_image_to_braille_art,
    parse_image_references_in_text
)

def demo_braille_art():
    """Demonstrate Braille art conversion capabilities"""
    
    print("🖼️  Pratibimb Braille Art Demo")
    print("=" * 50)
    print()
    
    # Load configuration
    config = load_config()
    
    # Demo 1: Simple text with image reference
    print("📝 Demo 1: Text with Image Reference")
    print("-" * 40)
    
    demo_text = """
Welcome to Pratibimb Braille Art Demo!

[IMAGE: Pratibimb Logo.png | Pratibimb Logo | Official logo of the accessibility platform]

This demonstrates how images are converted to tactile Braille patterns for blind users.

The system automatically:
- Processes image references in text
- Converts images to optimal Braille patterns  
- Maintains professional formatting
- Includes descriptive information
"""
    
    print("Input text:")
    print(demo_text)
    print()
    
    print("Converting to Braille with art...")
    braille_output = text_to_braille_unicode(demo_text, config)
    
    print("✅ Conversion complete!")
    print()
    print("Braille output (first 200 characters):")
    print(braille_output[:200] + "..." if len(braille_output) > 200 else braille_output)
    print()
    
    # Demo 2: Direct image processing
    print("📝 Demo 2: Direct Image Processing")
    print("-" * 40)
    
    image_path = "Pratibimb Logo.png"
    if os.path.exists(image_path):
        print(f"Processing image: {image_path}")
        braille_art = process_image_to_braille_art(
            image_path, 
            title="Demo Logo", 
            description="Sample image converted to Braille art",
            config=config
        )
        
        print("Braille art output:")
        print(braille_art)
    else:
        print(f"⚠️  Image not found: {image_path}")
        print("Creating a simple test pattern instead...")
        
        # Create a simple demo pattern
        test_pattern = """
[Image: Test Pattern]

⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿
⠿⠀⠀⠓⠞⠑⠎⠞⠀⠏⠁⠞⠞⠑⠗⠝⠀⠀⠿
⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿
⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿

Description: A simple test pattern showing Braille art formatting
"""
        print(test_pattern)
    
    # Demo 3: Configuration options
    print("\n📝 Demo 3: Configuration Options")
    print("-" * 40)
    
    art_settings = config.get('braille_art_settings', {})
    print("Current Braille Art Settings:")
    for key, value in art_settings.items():
        print(f"  {key}: {value}")
    
    print()
    print("💡 Tips for better Braille art:")
    print("- Use high-contrast images")
    print("- Prefer simple, clear graphics")
    print("- Adjust contrast_boost for better definition")
    print("- Enable edge_enhance for sharper tactile output")
    print("- Use descriptive titles and alt text")
    
    print()
    print("🎉 Demo complete! Check the output files:")
    print(f"  Unicode Braille: {config.get('output_file')}")
    print(f"  Embosser BRF: {config.get('embosser_file')}")

def create_sample_images():
    """Create simple sample images for testing (if PIL is available)"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple logo-style image
        img = Image.new('RGB', (200, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw simple text
        draw.text((10, 30), "PRATIBIMB", fill='black')
        draw.text((10, 50), "Accessibility", fill='gray')
        
        # Draw a simple border
        draw.rectangle([5, 5, 195, 95], outline='black', width=2)
        
        # Save the sample image
        sample_path = "sample_logo.png"
        img.save(sample_path)
        print(f"✅ Created sample image: {sample_path}")
        
        return sample_path
    except ImportError:
        print("⚠️  PIL not available, cannot create sample images")
        return None

if __name__ == "__main__":
    try:
        # Create sample images if possible
        create_sample_images()
        
        # Run the demo
        demo_braille_art()
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure you have installed the required dependencies:")
        print("pip install Pillow numpy")
