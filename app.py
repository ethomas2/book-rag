from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import openai
import os
import json
import re
from pathlib import Path

app = FastAPI(title="Harry Potter RAG API", description="Query Harry Potter chapters using OpenAI Assistants API")

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QueryRequest(BaseModel):
    query: str
    chapter: int

class QueryResponse(BaseModel):
    answer: str
    quotes: List[str]

def load_chapter_text(chapter_num: int) -> str:
    """Load chapter text from file"""
    chapter_file = Path(f"data/chapter-{chapter_num:02d}.txt")
    if not chapter_file.exists():
        raise HTTPException(status_code=404, detail=f"Chapter {chapter_num} not found")
    
    with open(chapter_file, 'r', encoding='utf-8') as f:
        return f.read()

def validate_quotes(quotes: List[str], chapter_text: str) -> tuple[List[str], List[str]]:
    """Validate that all quotes exist word-for-word in the chapter text"""
    valid_quotes = []
    invalid_quotes = []
    
    for quote in quotes:
        # Clean the quote (remove extra whitespace)
        cleaned_quote = ' '.join(quote.split())
        if cleaned_quote in chapter_text:
            valid_quotes.append(quote)
        else:
            invalid_quotes.append(quote)
    
    return valid_quotes, invalid_quotes

def create_assistant_with_chapters(chapter_num: int) -> str:
    """Create an assistant with uploaded chapters up to the specified chapter"""
    
    # Upload chapter files first
    file_ids = []
    for i in range(1, chapter_num + 1):
        chapter_file = Path(f"data/chapter-{i:02d}.txt")
        if chapter_file.exists():
            with open(chapter_file, 'rb') as f:
                file = client.files.create(
                    file=f,
                    purpose='assistants'
                )
                file_ids.append(file.id)
                print(f"Uploaded chapter {i} file: {file.id}")
    
    # Create assistant
    assistant = client.beta.assistants.create(
        name=f"Harry Potter Chapter {chapter_num} Assistant",
        instructions=f"""You are a Harry Potter expert assistant. You can ONLY answer questions based on the uploaded chapter files (chapters 1 through {chapter_num}). 

IMPORTANT RULES:
1. NEVER provide information from chapters beyond chapter {chapter_num}
2. If the answer requires information from later chapters, say "I cannot answer this question based on the information available in chapters 1-{chapter_num}"
3. Always provide specific quotes from the source material to support your answers
4. Make sure all quotes are word-for-word accurate from the uploaded files
5. Use structured output with the exact quotes from the text""",
        model="gpt-4-turbo-preview",
        tools=[{"type": "file_search"}]
    )
    
    print(f"Created assistant with {len(file_ids)} files ready for thread attachment")
    return assistant.id


def query_assistant_with_validation(assistant_id: str, query: str, chapter_text: str, chapter_num: int) -> QueryResponse:
    """Query the assistant and validate quotes, retrying if needed"""
    
    # Load all chapter content up to the specified chapter
    all_chapters_content = ""
    for i in range(1, chapter_num + 1):
        chapter_file = Path(f"data/chapter-{i:02d}.txt")
        if chapter_file.exists():
            with open(chapter_file, 'r', encoding='utf-8') as f:
                all_chapters_content += f"\n\n--- CHAPTER {i} ---\n\n"
                all_chapters_content += f.read()
    
    # Create thread
    thread = client.beta.threads.create()
    
    # Add message to thread with chapter content included
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"""Here is the content from chapters 1 through {chapter_num}:

{all_chapters_content}

Please answer this question: {query}

IMPORTANT: You must respond with a JSON object in this exact format:
{{
    "answer": "your answer here",
    "quotes": ["exact quote 1", "exact quote 2", "exact quote 3"]
}}

Make sure all quotes are word-for-word from the chapter content provided above."""
    )
    
    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
    # Wait for completion
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        import time
        time.sleep(1)
    
    if run.status == "failed":
        raise HTTPException(status_code=500, detail="Assistant run failed")
    
    # Get the response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response_text = messages.data[0].content[0].text.value
    
    # Try to parse JSON response
    try:
        # Extract JSON from response (handle cases where there's extra text)
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_data = json.loads(json_match.group())
        else:
            # If no JSON found, create a simple response
            response_data = {
                "answer": response_text,
                "quotes": []
            }
    except json.JSONDecodeError:
        # If JSON parsing fails, create a simple response
        response_data = {
            "answer": response_text,
            "quotes": []
        }
    
    # Validate quotes
    valid_quotes, invalid_quotes = validate_quotes(response_data.get("quotes", []), chapter_text)
    
    # If there are invalid quotes, retry with correction
    if invalid_quotes:
        correction_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"""Some of your quotes were not found word-for-word in the source material. Please provide only quotes that exist exactly as written in the uploaded files.

Invalid quotes: {invalid_quotes}

Please respond with a JSON object in this format:
{{
    "answer": "your answer here", 
    "quotes": ["exact quote 1", "exact quote 2"]
}}

Make sure ALL quotes are word-for-word from the uploaded files."""
        )
        
        # Run again
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        while run.status in ["queued", "in_progress"]:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            import time
            time.sleep(1)
        
        # Get the corrected response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response_text = messages.data[0].content[0].text.value
        
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_data = json.loads(json_match.group())
            else:
                response_data = {
                    "answer": response_text,
                    "quotes": []
                }
        except json.JSONDecodeError:
            response_data = {
                "answer": response_text,
                "quotes": []
            }
        
        # Final validation
        valid_quotes, _ = validate_quotes(response_data.get("quotes", []), chapter_text)
    
    return QueryResponse(
        answer=response_data.get("answer", response_text),
        quotes=valid_quotes
    )

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Query the Harry Potter chapters up to the specified chapter"""
    
    if request.chapter < 1 or request.chapter > 17:
        raise HTTPException(status_code=400, detail="Chapter must be between 1 and 17")
    
    try:
        # Load chapter text for validation
        chapter_text = load_chapter_text(request.chapter)
        
        # Create assistant with chapters up to the requested chapter
        assistant_id = create_assistant_with_chapters(request.chapter)
        
        # Query the assistant and validate quotes
        response = query_assistant_with_validation(assistant_id, request.query, chapter_text, request.chapter)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Harry Potter RAG API", "endpoints": ["POST /query"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 