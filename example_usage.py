#!/usr/bin/env python3
"""
Example usage of the Harry Potter RAG API
This script demonstrates how to make requests to the API
"""

import requests
import json

def test_api_endpoint():
    """Test the API endpoint with sample queries"""
    
    # API base URL (adjust if running on different port)
    base_url = "http://localhost:8000"
    
    # Sample queries to test
    test_queries = [
        {
            "query": "Who are the Dursleys and what are they like?",
            "chapter": 1
        },
        {
            "query": "What happens when Harry receives his Hogwarts letter?",
            "chapter": 3
        },
        {
            "query": "What is the Sorting Hat and how does it work?",
            "chapter": 7
        }
    ]
    
    print("Harry Potter RAG API - Example Usage")
    print("=" * 50)
    print()
    
    for i, test_query in enumerate(test_queries, 1):
        print(f"Test {i}: Query about chapter {test_query['chapter']}")
        print(f"Question: {test_query['query']}")
        print("-" * 40)
        
        try:
            # Make POST request to /query endpoint
            response = requests.post(
                f"{base_url}/query",
                json=test_query,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✓ Success!")
                print(f"Answer: {result['answer'][:100]}...")
                print(f"Quotes: {len(result['quotes'])} found")
                for j, quote in enumerate(result['quotes'][:2], 1):  # Show first 2 quotes
                    print(f"  {j}. {quote[:80]}...")
            else:
                print(f"✗ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("✗ Connection error: Make sure the API server is running")
            print("  Run: python app.py")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
        
        print()

def show_api_documentation():
    """Show API documentation"""
    print("API Documentation")
    print("=" * 20)
    print()
    print("Endpoint: POST /query")
    print()
    print("Request Body:")
    print(json.dumps({
        "query": "Your question here",
        "chapter": 5
    }, indent=2))
    print()
    print("Response:")
    print(json.dumps({
        "answer": "The assistant's answer based on the specified chapters",
        "quotes": [
            "Exact quote 1 from the source material",
            "Exact quote 2 from the source material"
        ]
    }, indent=2))
    print()
    print("Notes:")
    print("- chapter must be between 1 and 17")
    print("- Only information from chapters 1 through the specified chapter is used")
    print("- All quotes are validated to exist word-for-word in the source material")

if __name__ == "__main__":
    show_api_documentation()
    print("\n" + "="*50 + "\n")
    test_api_endpoint() 