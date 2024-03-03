import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from database import nl_to_sql, execute_query, format_answer, detect_intent, gk_answer

app = FastAPI()

# List of allowed origins (i.e., the frontend URLs that can communicate with the backend)
# You can use ["*"] for development, but for production, specify the actual origins
origins = [
    "http://localhost:3000",  # Adjust this to your React app's URL
    "http://localhost:8000",  # The FastAPI server itself (if serving static content)
    # Add any other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


class Query(BaseModel):
    text: str

@app.post("/query/")
def handle_query(query: Query):
    print("Hello")
    # Load the OpenAI API key from an environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found.")

    # Determine the intent of the query (0 for DB question, 1 for general knowledge)
    try:
        intent = detect_intent(query.text, openai_api_key)  # Assuming detect_intent returns 'DB Question' or 'General Knowledge Question'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting query intent: {str(e)}")

    # Convert natural language to SQL only if it's a DB question
    if not intent:
        try:
            sql_query = nl_to_sql(query.text, openai_api_key)
            result = execute_query(sql_query=sql_query)
            formatted_response = format_answer(question=query.text, answer=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing database query: {str(e)}")
    else:
        sql_query = None
        result = None
        formatted_response = gk_answer(query.text)

    intent = "General Knowledge" if intent else "Database Query"

    # Return the NL query, SQL query, raw result, and formatted response
    response = {
        "natural_language_query": query.text,
        "intent": intent,
        "sqlquery": sql_query,
        "rawresult": result,
        "formattedresponse": formatted_response
    }

    print(response)

    return response
