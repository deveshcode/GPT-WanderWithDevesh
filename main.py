import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from database import nl_to_sql, execute_query, format_answer

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
    # Load the OpenAI API key from an environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found.")

    # Convert natural language to SQL
    try:
        sql_query = nl_to_sql(query.text, openai_api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting NL to SQL: {str(e)}")

    # Execute the SQL query and get results
    try:
        result = execute_query(sql_query=sql_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing SQL query: {str(e)}")

    # Format the result
    try:
        formatted_response = format_answer(question=query.text, answer=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting response: {str(e)}")

    # Return the NL query, SQL query, raw result, and formatted response
    ans = {
        "natural_language_query": query.text,
        "sqlquery": sql_query,
        "rawresult": result,
        "formattedresponse": formatted_response
    }

    print(ans)

    return ans
