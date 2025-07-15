#!/usr/bin/env python3
"""
Test script for the Harry Potter RAG API
This script tests the core functionality without requiring external dependencies
"""

import json
import re
from pathlib import Path

def test_chapter_loading():
    """Test that chapters can be loaded"""
    print("Testing chapter loading...")
    
    for i in range(1, 18):
        chapter_file = Path(f"data/chapter-{i:02d}.txt")
        if chapter_file.exists():
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✓ Chapter {i}: {len(content)} characters")
        else:
            print(f"✗ Chapter {i}: File not found")
    
    print()

def test_quote_validation():
    """Test quote validation functionality"""
    print("Testing quote validation...")
    
    # Load a chapter for testing
    chapter_file = Path("data/chapter-01.txt")
    if not chapter_file.exists():
        print("✗ Chapter 1 not found for testing")
        return
    
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter_text = f.read()
    
    # Test valid quotes
    valid_quotes = [
        "Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal",
        "The Dursleys had everything they wanted, but they also had a secret"
    ]
    
    # Test invalid quotes
    invalid_quotes = [
        "This quote does not exist in the text",
        "Harry Potter and the Chamber of Secrets"  # Wrong book
    ]
    
    def validate_quotes(quotes, chapter_text):
        valid = []
        invalid = []
        
        for quote in quotes:
            cleaned_quote = ' '.join(quote.split())
            if cleaned_quote in chapter_text:
                valid.append(quote)
            else:
                invalid.append(quote)
        
        return valid, invalid
    
    valid_results, invalid_results = validate_quotes(valid_quotes, chapter_text)
    print(f"✓ Valid quotes found: {len(valid_results)}/{len(valid_quotes)}")
    print(f"✓ Invalid quotes detected: {len(invalid_results)}/{len(invalid_quotes)}")
    
    print()

def test_json_parsing():
    """Test JSON response parsing"""
    print("Testing JSON parsing...")
    
    # Test valid JSON response
    valid_response = '''
    Based on the information available, here is my answer:
    {
        "answer": "Harry Potter is left as a baby on the doorstep",
        "quotes": ["Mr. and Mrs. Dursley were perfectly normal", "The Dursleys had a secret"]
    }
    '''
    
    # Test invalid JSON response
    invalid_response = '''
    Here is my answer without proper JSON formatting.
    The Dursleys were normal people.
    '''
    
    def extract_json(response_text):
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"answer": response_text, "quotes": []}
        except json.JSONDecodeError:
            return {"answer": response_text, "quotes": []}
    
    valid_result = extract_json(valid_response)
    invalid_result = extract_json(invalid_response)
    
    print(f"✓ Valid JSON parsed: {valid_result.get('answer', '')[:50]}...")
    print(f"✓ Invalid JSON handled: {invalid_result.get('answer', '')[:50]}...")
    
    print()

def main():
    """Run all tests"""
    print("Harry Potter RAG API - Test Suite")
    print("=" * 40)
    print()
    
    test_chapter_loading()
    test_quote_validation()
    test_json_parsing()
    
    print("All tests completed!")

if __name__ == "__main__":
    main() 