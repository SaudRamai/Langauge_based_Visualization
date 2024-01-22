from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import DatabaseConnection


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask-question")
async def ask_question(question: Question):
    user_question_prompt = f"I dont know my database try to fix the db column names and find me {question.question} and return a string value"
    response = DatabaseConnection.agent_executor.run(input={'query': user_question_prompt}, handle_parsing_errors=True)

    if isinstance(response, (tuple, list)) and len(response) >= 2:
        _, data_for_visualization_json = response
    else:
        data_for_visualization_json = response

    if not isinstance(data_for_visualization_json, str):
        return JSONResponse(content={"error": "Unexpected response format. Expected a string."}, status_code=500)

    return JSONResponse(content={"response": data_for_visualization_json}, status_code=200)
