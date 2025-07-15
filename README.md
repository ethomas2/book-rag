# Harry Potter RAG API

A FastAPI application that uses OpenAI Assistants API to answer questions about Harry Potter and the Sorcerer's Stone, with strict chapter-based access control and quote validation.

## Features

- **Chapter-based access control**: Only provides information from chapters up to the specified chapter number
- **Quote validation**: Ensures all quotes provided are word-for-word accurate from the source material
- **No spoilers**: Prevents revealing information from later chapters
- **Structured output**: Returns answers with supporting quotes

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

   Or with uvicorn:
   ```bash
   uvicorn app:app --reload
   ```

## API Usage

### POST /query

Query the Harry Potter chapters up to a specific chapter number.

**Request Body**:
```json
{
  "query": "What happens to Harry at the beginning of the story?",
  "chapter": 3
}
```

**Response**:
```json
{
  "answer": "Harry Potter is left as a baby on the doorstep of the Dursley family...",
  "quotes": [
    "Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal",
    "The Dursleys had everything they wanted, but they also had a secret"
  ]
}
```

## Data Structure

The application expects chapter files in the `data/` directory:
- `chapter-01.txt` through `chapter-17.txt`
- Each file contains the complete chapter text

## How it Works

1. **Assistant Creation**: Creates an OpenAI Assistant with uploaded chapter files up to the specified chapter
2. **Query Processing**: Sends the query to the assistant with strict instructions to only use uploaded files
3. **Quote Validation**: Validates that all returned quotes exist word-for-word in the source material
4. **Retry Logic**: If invalid quotes are found, sends correction request to the assistant
5. **Response**: Returns validated answer with accurate quotes

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required) 