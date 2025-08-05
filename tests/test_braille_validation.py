"""
Comprehensive Braille Validation Test Script

This script validates that the generated Unicode Braille output matches the original 
English text according to Grade 1 Braille mapping rules. It checks:
- Character-by-character mapping
- Punctuation preservation
- Grammar and capitalization
- Line breaks and formatting
- Whitespace handling
- Tab preservation

Author: Braille Converter System
Date: 2025
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Optional

class BrailleValidator:
    """Validates Braille output against original English text"""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize validator with configuration"""
        self.config = self.load_config(config_path)
        self.braille_map = self.create_braille_map()
        self.errors = []
        self.warnings = []
        
    def load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def create_braille_map(self) -> Dict[str, str]:
        """Create comprehensive English to Braille mapping"""
        return {
            # Letters (lowercase)
            'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛',
            'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝',
            'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥',
            'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
            
            # Letters (uppercase) - capital indicator + lowercase
            'A': '⠠⠁', 'B': '⠠⠃', 'C': '⠠⠉', 'D': '⠠⠙', 'E': '⠠⠑', 'F': '⠠⠋',
            'G': '⠠⠛', 'H': '⠠⠓', 'I': '⠠⠊', 'J': '⠠⠚', 'K': '⠠⠅', 'L': '⠠⠇',
            'M': '⠠⠍', 'N': '⠠⠝', 'O': '⠠⠕', 'P': '⠠⠏', 'Q': '⠠⠟', 'R': '⠠⠗',
            'S': '⠠⠎', 'T': '⠠⠞', 'U': '⠠⠥', 'V': '⠠⠧', 'W': '⠠⠺', 'X': '⠠⠭',
            'Y': '⠠⠽', 'Z': '⠠⠵',
            
            # Numbers (with number indicator)
            '0': '⠼⠚', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙',
            '5': '⠼⠑', '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊',
            
            # Punctuation
            '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ':': '⠒', ';': '⠆',
            "'": '⠄', '"': '⠶', '(': '⠶', ')': '⠶', '-': '⠤', '—': '⠤',
            
            # Whitespace
            ' ': ' ',
            '\t': ' ' * self.config.get('tab_width', 4),
            '\n': '\n',
            '\r': '',  # Carriage returns are ignored
        }
    
    def read_file(self, file_path: str) -> str:
        """Read file content with proper encoding"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"Cannot decode file: {file_path}")
    
    def convert_to_braille(self, text: str) -> str:
        """Convert English text to expected Braille output"""
        result = []
        
        for char in text:
            if char in self.braille_map:
                result.append(self.braille_map[char])
            else:
                # Handle unknown characters
                result.append('?')
                self.warnings.append(f"Unknown character encountered: '{char}' (Unicode: {ord(char)})")
        
        return ''.join(result)
    
    def validate_character_mapping(self, original: str, braille: str) -> List[str]:
        """Validate character-by-character mapping"""
        errors = []
        expected_braille = self.convert_to_braille(original)
        
        if len(braille) != len(expected_braille):
            errors.append(f"Length mismatch: Original produces {len(expected_braille)} Braille characters, but output has {len(braille)}")
        
        # Compare character by character
        min_len = min(len(braille), len(expected_braille))
        for i in range(min_len):
            if braille[i] != expected_braille[i]:
                orig_char = original[i] if i < len(original) else '?'
                errors.append(f"Character mismatch at position {i}: Expected '{expected_braille[i]}' for '{orig_char}', got '{braille[i]}'")
        
        return errors
    
    def validate_line_breaks(self, original: str, braille: str) -> List[str]:
        """Validate line breaks and formatting"""
        errors = []
        
        orig_lines = original.split('\n')
        braille_lines = braille.split('\n')
        
        if len(orig_lines) != len(braille_lines):
            errors.append(f"Line count mismatch: Original has {len(orig_lines)} lines, Braille has {len(braille_lines)} lines")
        
        # Check each line
        for i, (orig_line, braille_line) in enumerate(zip(orig_lines, braille_lines)):
            expected_braille_line = self.convert_to_braille(orig_line)
            if braille_line != expected_braille_line:
                errors.append(f"Line {i+1} mismatch:")
                errors.append(f"  Original: '{orig_line}'")
                errors.append(f"  Expected: '{expected_braille_line}'")
                errors.append(f"  Got:      '{braille_line}'")
        
        return errors
    
    def validate_punctuation(self, original: str, braille: str) -> List[str]:
        """Validate punctuation preservation"""
        errors = []
        
        # Group punctuation by their Braille representation
        # In Grade 1 Braille, quotes, parentheses all use ⠶
        braille_group_mapping = {
            '⠶': ['"', '(', ')'],  # All use the same Braille character
            '⠲': ['.'],
            '⠂': [','],
            '⠦': ['?'],
            '⠖': ['!'],
            '⠄': ["'"],
            '⠤': ['-', '—'],  # Both hyphen and em-dash use same character
            '⠒': [':'],
            '⠆': [';'],
        }
        
        # Validate each Braille punctuation group
        for braille_char, punct_chars in braille_group_mapping.items():
            # Count total occurrences of all punctuation in this group in original
            orig_total = sum(original.count(char) for char in punct_chars)
            
            # Count Braille character occurrences
            braille_count = braille.count(braille_char)
            
            if orig_total != braille_count:
                punct_list = "', '".join(punct_chars)
                errors.append(f"Punctuation group ['{punct_list}'] count mismatch: Original has {orig_total}, Braille has {braille_count}")
        
        return errors
    
    def validate_capitalization(self, original: str, braille: str) -> List[str]:
        """Validate capitalization handling"""
        errors = []
        capital_indicator = '⠠'
        
        # Count uppercase letters in original
        uppercase_count = sum(1 for c in original if c.isupper())
        
        # Count capital indicators in braille
        capital_indicators = braille.count(capital_indicator)
        
        if uppercase_count != capital_indicators:
            errors.append(f"Capitalization mismatch: Original has {uppercase_count} uppercase letters, Braille has {capital_indicators} capital indicators")
        
        return errors
    
    def validate_numbers(self, original: str, braille: str) -> List[str]:
        """Validate number handling"""
        errors = []
        number_indicator = '⠼'
        
        # Count digits in original
        digit_count = sum(1 for c in original if c.isdigit())
        
        # Count number indicators in braille
        number_indicators = braille.count(number_indicator)
        
        if digit_count != number_indicators:
            errors.append(f"Number handling mismatch: Original has {digit_count} digits, Braille has {number_indicators} number indicators")
        
        return errors
    
    def validate_whitespace(self, original: str, braille: str) -> List[str]:
        """Validate whitespace preservation"""
        errors = []
        
        # Count spaces (accounting for tab expansion)
        orig_spaces = original.count(' ')
        orig_tabs = original.count('\t')
        expected_spaces = orig_spaces + (orig_tabs * self.config.get('tab_width', 4))
        
        actual_spaces = braille.count(' ')
        
        if expected_spaces != actual_spaces:
            errors.append(f"Whitespace mismatch: Expected {expected_spaces} spaces (including {orig_tabs} tabs), got {actual_spaces}")
        
        return errors
    
    def generate_detailed_report(self, original: str, braille: str) -> str:
        """Generate detailed validation report"""
        report = []
        report.append("=" * 80)
        report.append("BRAILLE VALIDATION REPORT")
        report.append("=" * 80)
        report.append(f"Original text length: {len(original)} characters")
        report.append(f"Braille output length: {len(braille)} characters")
        report.append(f"Original lines: {len(original.split(chr(10)))}")
        report.append(f"Braille lines: {len(braille.split(chr(10)))}")
        report.append("")
        
        # Character statistics
        report.append("CHARACTER STATISTICS:")
        report.append(f"  Uppercase letters: {sum(1 for c in original if c.isupper())}")
        report.append(f"  Lowercase letters: {sum(1 for c in original if c.islower())}")
        report.append(f"  Digits: {sum(1 for c in original if c.isdigit())}")
        report.append(f"  Spaces: {original.count(' ')}")
        report.append(f"  Tabs: {original.count(chr(9))}")
        report.append(f"  Line breaks: {original.count(chr(10))}")
        report.append("")
        
        # Braille statistics
        report.append("BRAILLE STATISTICS:")
        report.append(f"  Capital indicators (⠠): {braille.count('⠠')}")
        report.append(f"  Number indicators (⠼): {braille.count('⠼')}")
        report.append(f"  Spaces: {braille.count(' ')}")
        report.append(f"  Line breaks: {braille.count(chr(10))}")
        report.append("")
        
        return '\n'.join(report)
    
    def validate_files(self, original_path: str, braille_path: str) -> bool:
        """Main validation function"""
        print(f"Validating Braille conversion...")
        print(f"Original file: {original_path}")
        print(f"Braille file: {braille_path}")
        print("-" * 60)
        
        try:
            # Read files
            original_text = self.read_file(original_path)
            braille_text = self.read_file(braille_path)
            
            # Perform validations
            self.errors = []
            self.warnings = []
            
            # Character mapping validation
            char_errors = self.validate_character_mapping(original_text, braille_text)
            self.errors.extend(char_errors)
            
            # Line breaks validation
            line_errors = self.validate_line_breaks(original_text, braille_text)
            self.errors.extend(line_errors)
            
            # Punctuation validation
            punct_errors = self.validate_punctuation(original_text, braille_text)
            self.errors.extend(punct_errors)
            
            # Capitalization validation
            cap_errors = self.validate_capitalization(original_text, braille_text)
            self.errors.extend(cap_errors)
            
            # Number validation
            num_errors = self.validate_numbers(original_text, braille_text)
            self.errors.extend(num_errors)
            
            # Whitespace validation
            ws_errors = self.validate_whitespace(original_text, braille_text)
            self.errors.extend(ws_errors)
            
            # Generate report
            report = self.generate_detailed_report(original_text, braille_text)
            print(report)
            
            # Display warnings
            if self.warnings:
                print("WARNINGS:")
                for warning in self.warnings:
                    print(f"  ⚠️  {warning}")
                print()
            
            # Display errors
            if self.errors:
                print("VALIDATION ERRORS:")
                for error in self.errors:
                    print(f"  ❌ {error}")
                print()
                print(f"Total errors: {len(self.errors)}")
                return False
            else:
                print("✅ VALIDATION PASSED: All checks successful!")
                print("The Braille output perfectly matches the original English text.")
                return True
                
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            return False

def main():
    """Main function to run validation tests"""
    print("Braille Validation Test Script")
    print("=" * 40)
    
    # Initialize validator
    validator = BrailleValidator()
    
    # Get file paths from config
    input_file = validator.config.get('input_file', 'input_text.txt')
    output_file = validator.config.get('output_file', 'braille_output.txt')
    
    # Run validation
    success = validator.validate_files(input_file, output_file)
    
    # Also test with test files if they exist
    test_input = validator.config.get('test_input_file', 'test_input.txt')
    test_output = validator.config.get('test_output_file', 'test_braille_output.txt')
    
    if os.path.exists(test_input) and os.path.exists(test_output):
        print("\n" + "=" * 60)
        print("TESTING WITH TEST FILES")
        print("=" * 60)
        test_success = validator.validate_files(test_input, test_output)
        success = success and test_success
    
    # Exit with appropriate code
    if success:
        print("\n🎉 All validations passed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some validations failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
