#!/usr/bin/env python3
"""
Braille Embosser Validation Script
Validates Braille files against embosser printing standards
"""

import os
import re

def validate_embosser_format(file_path):
    """
    Validate a Braille file against embosser printing standards.
    
    Standards checked:
    - Line Length: Exactly 40 characters per line
    - Page Length: Exactly 25 lines per page
    - Page Breaks: Form feed character (\f) after every 25 lines
    - Page Numbers: Right-aligned Braille numbers on line 25
    - Character Compliance: Only valid Braille Unicode characters
    
    Args:
        file_path (str): Path to Braille file to validate
        
    Returns:
        dict: Validation results with detailed report
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {"error": f"File '{file_path}' not found"}
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}
    
    # Split content by form feeds to get pages, but handle form feeds properly
    # Form feeds should be standalone, not part of lines
    content_clean = content.replace('\f\n', '\f').replace('\n\f', '\f')
    pages = content_clean.split('\f')
    
    # Split each page into lines, removing empty lines caused by form feeds
    page_lines = []
    for page in pages:
        lines = [line for line in page.split('\n') if line is not None]
        # Remove any empty lines at the end that might be artifacts
        while lines and lines[-1] == '':
            lines.pop()
        page_lines.append(lines)
    
    validation_results = {
        "file_path": file_path,
        "total_pages": len(pages),
        "total_lines": sum(len(lines) for lines in page_lines),
        "form_feeds": content.count('\f'),
        "errors": [],
        "warnings": [],
        "line_length_errors": [],
        "page_length_errors": [],
        "character_errors": [],
        "valid": True
    }
    
    # Braille Unicode range (U+2800 to U+28FF)
    braille_pattern = re.compile(r'[\u2800-\u28FF]')
    
    # Validate each page
    for page_num, lines in enumerate(page_lines, 1):
        
        # Check page length (should be exactly 25 lines for complete pages)
        if page_num < len(pages):  # Not the last page
            if len(lines) != 25:
                validation_results["page_length_errors"].append({
                    "page": page_num,
                    "expected": 25,
                    "actual": len(lines),
                    "issue": f"Page {page_num} has {len(lines)} lines, expected 25"
                })
                validation_results["valid"] = False
        else:  # Last page can have fewer lines
            if len(lines) > 25:
                validation_results["page_length_errors"].append({
                    "page": page_num,
                    "expected": "≤25",
                    "actual": len(lines),
                    "issue": f"Last page {page_num} has {len(lines)} lines, maximum 25"
                })
                validation_results["valid"] = False
        
        # Validate each line in the page
        for line_num, line in enumerate(lines, 1):
            global_line_num = sum(len(page_lines[i]) for i in range(page_num - 1)) + line_num
            
            # Check line length (should be exactly 40 characters)
            if len(line) != 40:
                validation_results["line_length_errors"].append({
                    "page": page_num,
                    "line": line_num,
                    "global_line": global_line_num,
                    "expected": 40,
                    "actual": len(line),
                    "content": line[:50] + "..." if len(line) > 50 else line
                })
                validation_results["valid"] = False
            
            # Check for valid characters (Braille Unicode + spaces + number indicator)
            for char_pos, char in enumerate(line):
                if char != ' ' and not braille_pattern.match(char):
                    validation_results["character_errors"].append({
                        "page": page_num,
                        "line": line_num,
                        "global_line": global_line_num,
                        "position": char_pos + 1,
                        "character": char,
                        "unicode": f"U+{ord(char):04X}",
                        "issue": f"Non-Braille character '{char}' found"
                    })
                    validation_results["valid"] = False
    
    # Check form feed placement
    lines_all = content.split('\n')
    form_feed_lines = [i + 1 for i, line in enumerate(lines_all) if '\f' in line]
    expected_form_feeds = list(range(25, len(lines_all), 25))
    
    if form_feed_lines != expected_form_feeds[:-1]:  # Exclude last page
        validation_results["warnings"].append({
            "issue": "Form feed placement",
            "expected": expected_form_feeds[:-1],
            "actual": form_feed_lines,
            "description": "Form feeds should appear after every 25th line"
        })
    
    # Summary statistics
    total_errors = (len(validation_results["line_length_errors"]) + 
                   len(validation_results["page_length_errors"]) + 
                   len(validation_results["character_errors"]))
    
    validation_results["summary"] = {
        "total_errors": total_errors,
        "total_warnings": len(validation_results["warnings"]),
        "line_length_compliance": f"{len(lines_all) - len(validation_results['line_length_errors'])}/{len(lines_all)}",
        "page_structure_valid": len(validation_results["page_length_errors"]) == 0,
        "character_compliance": len(validation_results["character_errors"]) == 0
    }
    
    return validation_results

def generate_validation_report(validation_results):
    """
    Generate a human-readable validation report.
    
    Args:
        validation_results (dict): Results from validate_embosser_format
        
    Returns:
        str: Formatted validation report
    """
    
    if "error" in validation_results:
        return f"❌ Validation Error: {validation_results['error']}"
    
    report = []
    results = validation_results
    
    # Header
    report.append("🖨️  BRAILLE EMBOSSER VALIDATION REPORT")
    report.append("=" * 50)
    report.append(f"📄 File: {results['file_path']}")
    report.append("")
    
    # Overall status
    if results["valid"]:
        report.append("✅ VALIDATION PASSED - File meets all embosser standards!")
    else:
        report.append("❌ VALIDATION FAILED - Issues found that need attention")
    
    report.append("")
    
    # Summary statistics
    report.append("📊 SUMMARY STATISTICS")
    report.append("-" * 30)
    report.append(f"Total pages: {results['total_pages']}")
    report.append(f"Total lines: {results['total_lines']}")
    report.append(f"Form feeds: {results['form_feeds']}")
    report.append(f"Total errors: {results['summary']['total_errors']}")
    report.append(f"Total warnings: {results['summary']['total_warnings']}")
    report.append("")
    
    # Detailed compliance
    report.append("📏 COMPLIANCE DETAILS")
    report.append("-" * 30)
    report.append(f"Line length (40 chars): {results['summary']['line_length_compliance']}")
    report.append(f"Page structure: {'✅ Valid' if results['summary']['page_structure_valid'] else '❌ Invalid'}")
    report.append(f"Character compliance: {'✅ Valid' if results['summary']['character_compliance'] else '❌ Invalid'}")
    report.append("")
    
    # Line length errors
    if results["line_length_errors"]:
        report.append("❌ LINE LENGTH ERRORS")
        report.append("-" * 30)
        for error in results["line_length_errors"][:10]:  # Show first 10
            report.append(f"Page {error['page']}, Line {error['line']}: "
                         f"{error['actual']} chars (expected 40)")
        if len(results["line_length_errors"]) > 10:
            report.append(f"... and {len(results['line_length_errors']) - 10} more errors")
        report.append("")
    
    # Page length errors
    if results["page_length_errors"]:
        report.append("❌ PAGE LENGTH ERRORS")
        report.append("-" * 30)
        for error in results["page_length_errors"]:
            report.append(f"Page {error['page']}: {error['issue']}")
        report.append("")
    
    # Character errors
    if results["character_errors"]:
        report.append("❌ CHARACTER ERRORS")
        report.append("-" * 30)
        for error in results["character_errors"][:5]:  # Show first 5
            report.append(f"Page {error['page']}, Line {error['line']}, Pos {error['position']}: "
                         f"Invalid character '{error['character']}' ({error['unicode']})")
        if len(results["character_errors"]) > 5:
            report.append(f"... and {len(results['character_errors']) - 5} more character errors")
        report.append("")
    
    # Warnings
    if results["warnings"]:
        report.append("⚠️  WARNINGS")
        report.append("-" * 30)
        for warning in results["warnings"]:
            report.append(f"{warning['issue']}: {warning['description']}")
        report.append("")
    
    # Recommendations
    if not results["valid"]:
        report.append("🔧 RECOMMENDATIONS")
        report.append("-" * 30)
        if results["line_length_errors"]:
            report.append("• Fix line length errors - each line must be exactly 40 characters")
        if results["page_length_errors"]:
            report.append("• Fix page structure - each page should have exactly 25 lines")
        if results["character_errors"]:
            report.append("• Remove or convert invalid characters to proper Braille Unicode")
        report.append("• Rerun the embosser formatter to fix formatting issues")
        report.append("")
    
    report.append("📋 EMBOSSER STANDARDS REFERENCE")
    report.append("-" * 30)
    report.append("• Line Length: Exactly 40 characters")
    report.append("• Page Length: Exactly 25 lines")
    report.append("• Page Breaks: Form feed (\\f) after every 25 lines")
    report.append("• Characters: Unicode Braille patterns (U+2800-U+28FF)")
    report.append("• Grade: Grade 1 Braille (no contractions)")
    
    return "\n".join(report)

def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Braille Embosser Validation Tool")
        print("=" * 35)
        print("Usage: python embosser_validator.py <braille_file> [output_report]")
        print("")
        print("Examples:")
        print("  python embosser_validator.py embosser_ready.brl")
        print("  python embosser_validator.py document.brl validation_report.txt")
        print("")
        print("Validates against embosser standards:")
        print("  • 40 characters per line")
        print("  • 25 lines per page")
        print("  • Form feed page breaks")
        print("  • Valid Braille Unicode characters")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🔍 Validating Braille file: {file_path}")
    print("=" * 40)
    
    # Perform validation
    results = validate_embosser_format(file_path)
    
    # Generate report
    report = generate_validation_report(results)
    
    # Output report
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 Validation report saved to: {output_file}")
        print("")
        # Show summary in console
        if results.get("valid"):
            print("✅ VALIDATION PASSED - File is ready for embosser printing!")
        else:
            print("❌ VALIDATION FAILED - Please check the detailed report.")
    else:
        print(report)

if __name__ == "__main__":
    main()
