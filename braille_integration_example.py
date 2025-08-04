#!/usr/bin/env python3
"""
Pratibimb Integration Example
============================

This file shows how to integrate Pratibimb into a larger solution.
Copy this pattern to embed Braille conversion functionality.

Dependencies: None (uses only Python standard library)
Required Files: pratibimb.py, config.json
"""

import os
import sys
import json
from pathlib import Path

class BrailleIntegration:
    """
    Professional Braille converter integration class.
    Embeds Pratibimb functionality into larger solutions.
    """
    
    def __init__(self, config_path=None):
        """Initialize the Braille converter with custom config path."""
        
        # Default to local config if not specified
        if config_path is None:
            config_path = Path(__file__).parent / 'config.json'
        
        # Import Pratibimb modules (ensure they're available)
        try:
            from pratibimb import (
                load_config, setup_logging, 
                text_to_braille_unicode, format_for_embosser,
                validate_embosser_output, analyze_braille_content
            )
            self.pratibimb = {
                'load_config': load_config,
                'setup_logging': setup_logging,
                'text_to_braille_unicode': text_to_braille_unicode,
                'format_for_embosser': format_for_embosser,
                'validate_embosser_output': validate_embosser_output,
                'analyze_braille_content': analyze_braille_content
            }
        except ImportError as e:
            raise ImportError(f"Pratibimb module not found. Ensure pratibimb.py is in the Python path. Error: {e}")
        
        # Load configuration
        self.config = self.pratibimb['load_config'](str(config_path))
        self.logger = self.pratibimb['setup_logging'](self.config)
        
        self.logger.info("🔤 Braille Integration initialized successfully")
    
    def convert_text_to_braille(self, text, output_files=True):
        """
        Convert text to Braille formats.
        
        Args:
            text (str): Input text to convert
            output_files (bool): Whether to save output files
            
        Returns:
            dict: Contains braille text, embosser format, and analysis
        """
        
        self.logger.info(f"🔄 Converting {len(text):,} characters to Braille")
        
        # Convert to Unicode Braille
        braille_text = self.pratibimb['text_to_braille_unicode'](text, self.config)
        
        # Format for embosser
        embosser_content = self.pratibimb['format_for_embosser'](braille_text, self.config)
        
        # Analyze content
        analysis = self.pratibimb['analyze_braille_content'](braille_text, text)
        
        # Validate embosser output
        validation = self.pratibimb['validate_embosser_output'](embosser_content, self.config)
        
        # Save files if requested
        if output_files:
            self._save_output_files(braille_text, embosser_content)
        
        result = {
            'unicode_braille': braille_text,
            'embosser_ready': embosser_content,
            'analysis': analysis,
            'validation': validation,
            'success': validation['valid'],
            'file_paths': {
                'braille': self.config['output_file'],
                'embosser': self.config['embosser_file'],
                'log': self.config['logging_settings']['log_file']
            }
        }
        
        self.logger.info(f"✅ Conversion completed: {len(braille_text):,} Braille characters")
        return result
    
    def convert_file_to_braille(self, input_file_path, output_dir=None):
        """
        Convert a text file to Braille formats.
        
        Args:
            input_file_path (str): Path to input text file
            output_dir (str): Optional output directory override
            
        Returns:
            dict: Conversion results and file paths
        """
        
        # Read input file
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            self.logger.error(f"❌ Failed to read input file: {e}")
            return {'success': False, 'error': str(e)}
        
        # Override output directory if specified
        if output_dir:
            self._update_output_paths(output_dir)
        
        # Convert the text
        return self.convert_text_to_braille(text, output_files=True)
    
    def validate_braille_file(self, embosser_file_path):
        """
        Validate an existing Braille embosser file.
        
        Args:
            embosser_file_path (str): Path to BRF file to validate
            
        Returns:
            dict: Validation results
        """
        
        try:
            with open(embosser_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'valid': False, 'error': f"Cannot read file: {e}"}
        
        return self.pratibimb['validate_embosser_output'](content, self.config)
    
    def _save_output_files(self, braille_text, embosser_content):
        """Save Braille outputs to configured file paths."""
        
        # Ensure output directories exist
        os.makedirs(os.path.dirname(self.config['output_file']), exist_ok=True)
        os.makedirs(os.path.dirname(self.config['embosser_file']), exist_ok=True)
        
        # Save Unicode Braille file
        with open(self.config['output_file'], 'w', encoding='utf-8') as f:
            f.write(braille_text)
        
        # Save embosser-ready file
        with open(self.config['embosser_file'], 'w', encoding='utf-8') as f:
            f.write(embosser_content)
    
    def _update_output_paths(self, output_dir):
        """Update output file paths to use specified directory."""
        
        output_dir = Path(output_dir)
        
        # Update config paths
        self.config['output_file'] = str(output_dir / 'braille_output.txt')
        self.config['embosser_file'] = str(output_dir / 'embosser_ready.brf')
        
        # Ensure directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

# Example usage and testing
if __name__ == "__main__":
    """
    Example of how to use the BrailleIntegration class in your larger solution.
    """
    
    print("🔤 Pratibimb Integration Example")
    print("=" * 50)
    
    try:
        # Initialize Braille converter
        braille = BrailleIntegration()
        
        # Example 1: Convert text directly
        sample_text = "Hello World! This is a test of the Braille conversion system."
        result = braille.convert_text_to_braille(sample_text)
        
        if result['success']:
            print(f"✅ Conversion successful!")
            print(f"📊 Analysis: {result['analysis']['word_count']} words")
            print(f"📁 Files saved to: {result['file_paths']['braille']}")
        else:
            print(f"❌ Conversion failed")
        
        # Example 2: Convert file (if input file exists)
        input_file = 'examples/input_text.txt'
        if os.path.exists(input_file):
            file_result = braille.convert_file_to_braille(input_file)
            print(f"📄 File conversion: {'✅ Success' if file_result['success'] else '❌ Failed'}")
        
        # Example 3: Validate existing BRF file
        embosser_file = result['file_paths']['embosser']
        if os.path.exists(embosser_file):
            validation = braille.validate_braille_file(embosser_file)
            print(f"🔍 Validation: {'✅ Valid' if validation['valid'] else '❌ Invalid'}")
        
        print(f"\n📋 Complete log available: {result['file_paths']['log']}")
        
    except Exception as e:
        print(f"❌ Integration error: {e}")
        print("💡 Ensure pratibimb.py and config.json are in the correct location")
