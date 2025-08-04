#!/usr/bin/env python3
"""
Braille Statistics and Analysis Tool
Analyze Braille text files for detailed statistics and insights
"""

import json
import os
import re
import sys
from collections import Counter
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from braille_converter import load_config

def analyze_braille_text(braille_text):
    """
    Analyze Braille text and return detailed statistics
    
    Args:
        braille_text (str): Unicode Braille text to analyze
        
    Returns:
        dict: Dictionary containing analysis results
    """
    
    # Braille character ranges
    BRAILLE_RANGE = range(0x2800, 0x2900)  # Unicode Braille patterns
    
    # Special Braille characters
    CAPITAL_INDICATOR = '\u2820'  # ⠠
    NUMBER_INDICATOR = '\u283c'   # ⠼
    
    # Count different character types
    braille_chars = []
    regular_chars = []
    
    for char in braille_text:
        if ord(char) in BRAILLE_RANGE:
            braille_chars.append(char)
        else:
            regular_chars.append(char)
    
    # Analyze Braille patterns
    braille_counter = Counter(braille_chars)
    
    # Count special indicators
    capital_indicators = braille_text.count(CAPITAL_INDICATOR)
    number_indicators = braille_text.count(NUMBER_INDICATOR)
    
    # Count structural elements
    lines = braille_text.split('\n')
    paragraphs = [p for p in braille_text.split('\n\n') if p.strip()]
    words = len(re.findall(r'\S+', braille_text))
    
    # Calculate density and complexity
    total_chars = len(braille_text)
    braille_density = len(braille_chars) / total_chars if total_chars > 0 else 0
    unique_patterns = len(set(braille_chars))
    
    return {
        'total_characters': total_chars,
        'braille_characters': len(braille_chars),
        'regular_characters': len(regular_chars),
        'braille_density': braille_density,
        'unique_braille_patterns': unique_patterns,
        'capital_indicators': capital_indicators,
        'number_indicators': number_indicators,
        'lines': len(lines),
        'paragraphs': len(paragraphs),
        'words': words,
        'most_common_patterns': braille_counter.most_common(10),
        'line_lengths': [len(line) for line in lines],
        'avg_line_length': sum(len(line) for line in lines) / len(lines) if lines else 0,
        'max_line_length': max(len(line) for line in lines) if lines else 0,
        'min_line_length': min(len(line) for line in lines) if lines else 0
    }

def generate_analysis_report(analysis, file_path):
    """
    Generate a detailed analysis report
    
    Args:
        analysis (dict): Analysis results from analyze_braille_text
        file_path (str): Path to the analyzed file
        
    Returns:
        str: Formatted report
    """
    
    report = []
    report.append("🔍 BRAILLE TEXT ANALYSIS REPORT")
    report.append("=" * 50)
    report.append(f"📄 File: {file_path}")
    report.append("")
    
    # Basic statistics
    report.append("📊 BASIC STATISTICS")
    report.append("-" * 30)
    report.append(f"Total characters: {analysis['total_characters']:,}")
    report.append(f"Braille characters: {analysis['braille_characters']:,}")
    report.append(f"Regular characters: {analysis['regular_characters']:,}")
    report.append(f"Braille density: {analysis['braille_density']:.1%}")
    report.append("")
    
    # Structure analysis
    report.append("🏗️  STRUCTURE ANALYSIS")
    report.append("-" * 30)
    report.append(f"Lines: {analysis['lines']:,}")
    report.append(f"Paragraphs: {analysis['paragraphs']:,}")
    report.append(f"Words: {analysis['words']:,}")
    report.append(f"Average line length: {analysis['avg_line_length']:.1f} characters")
    report.append(f"Longest line: {analysis['max_line_length']:,} characters")
    report.append(f"Shortest line: {analysis['min_line_length']:,} characters")
    report.append("")
    
    # Braille-specific analysis
    report.append("⠿ BRAILLE-SPECIFIC ANALYSIS")
    report.append("-" * 30)
    report.append(f"Unique Braille patterns: {analysis['unique_braille_patterns']:,}")
    report.append(f"Capital indicators (⠠): {analysis['capital_indicators']:,}")
    report.append(f"Number indicators (⠼): {analysis['number_indicators']:,}")
    report.append("")
    
    # Most common patterns
    if analysis['most_common_patterns']:
        report.append("🔤 MOST COMMON BRAILLE PATTERNS")
        report.append("-" * 30)
        for i, (pattern, count) in enumerate(analysis['most_common_patterns'], 1):
            percentage = count / analysis['braille_characters'] * 100
            report.append(f"{i:2d}. {pattern} - {count:,} times ({percentage:.1f}%)")
        report.append("")
    
    # Line length distribution
    if analysis['line_lengths']:
        line_lengths = analysis['line_lengths']
        short_lines = sum(1 for length in line_lengths if length < 50)
        medium_lines = sum(1 for length in line_lengths if 50 <= length < 100)
        long_lines = sum(1 for length in line_lengths if length >= 100)
        
        report.append("📏 LINE LENGTH DISTRIBUTION")
        report.append("-" * 30)
        report.append(f"Short lines (<50 chars): {short_lines:,}")
        report.append(f"Medium lines (50-99 chars): {medium_lines:,}")
        report.append(f"Long lines (≥100 chars): {long_lines:,}")
        report.append("")
    
    return "\n".join(report)

def analyze_file(file_path, output_file=None, config_file='config.json'):
    """
    Analyze a Braille file and generate a report
    
    Args:
        file_path (str): Path to Braille file to analyze
        output_file (str): Optional output file for report
        config_file (str): Configuration file path
    """
    
    # Load configuration
    config = load_config(config_file)
    
    try:
        print(f"🔍 Braille Text Analyzer")
        print("=" * 40)
        print(f"📖 Reading file '{file_path}'...")
        
        # Read file
        with open(file_path, 'r', encoding=config.get('encoding', 'utf-8')) as f:
            braille_text = f.read()
        
        print(f"🔄 Analyzing Braille content...")
        
        # Perform analysis
        analysis = analyze_braille_text(braille_text)
        
        # Generate report
        report = generate_analysis_report(analysis, file_path)
        
        # Output report
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Analysis report saved to '{output_file}'")
        else:
            print("\n" + report)
        
        return analysis
        
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found!")
        return None
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return None

def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python braille_analyzer.py <braille_file> [output_report_file]")
        print("Example: python braille_analyzer.py braille_output.txt analysis_report.txt")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    analyze_file(file_path, output_file)

if __name__ == "__main__":
    main()
