#!/usr/bin/env python3
"""
CLI tool for querying the Harry Potter RAG API
Usage: python query.py --question "Your question" --chapter <number>
"""

import argparse
import requests
import json
import sys
from typing import Optional

def query_api(question: str, chapter: int, base_url: str = "http://localhost:8001") -> Optional[dict]:
    """Make a query to the Harry Potter RAG API"""
    
    try:
        response = requests.post(
            f"{base_url}/query",
            json={
                "query": question,
                "chapter": chapter
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error: Could not connect to {base_url}")
        print("   Make sure the FastAPI server is running with: uvicorn app:app --reload --port 8001")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout: Request took too long")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def display_result(result: dict):
    """Display the API result in a formatted way"""
    
    print("\n" + "="*60)
    print("🎯 ANSWER")
    print("="*60)
    print(result.get("answer", "No answer provided"))
    
    quotes = result.get("quotes", [])
    if quotes:
        print("\n" + "="*60)
        print(f"📖 SUPPORTING QUOTES ({len(quotes)} found)")
        print("="*60)
        for i, quote in enumerate(quotes, 1):
            print(f"{i}. {quote}")
    else:
        print("\n📖 No supporting quotes provided")
    
    print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="Query the Harry Potter RAG API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python query.py --question "Who are the Dursleys?" --chapter 1
  python query.py --question "What happens when Harry gets his letter?" --chapter 3
  python query.py --question "What is the Sorting Hat?" --chapter 7
        """
    )
    
    parser.add_argument(
        "--question", "-q",
        required=True,
        help="Your question about Harry Potter"
    )
    
    parser.add_argument(
        "--chapter", "-c",
        type=int,
        required=True,
        help="Chapter number (1-17)"
    )
    
    parser.add_argument(
        "--url", "-u",
        default="http://localhost:8001",
        help="API base URL (default: http://localhost:8001)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate chapter number
    if args.chapter < 1 or args.chapter > 17:
        print("❌ Error: Chapter must be between 1 and 17")
        sys.exit(1)
    
    if args.verbose:
        print(f"🔍 Querying: {args.question}")
        print(f"📚 Chapter: {args.chapter}")
        print(f"🌐 API URL: {args.url}")
        print()
    
    # Make the query
    result = query_api(args.question, args.chapter, args.url)
    
    if result:
        display_result(result)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 