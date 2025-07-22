from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import time

from llm.llm_interface import question_to_sql
from query_engine.sql_executor import execute_query, visualize_query
from utils.formatter import format_response

app = FastAPI()

# ✅ CORS: Allow all for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with ["http://localhost:5500"] etc. for tighter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def answer_question(req: QueryRequest):
    sql = question_to_sql(req.question)
    result = execute_query(sql)
    answer = format_response(result)
    return {"sql": sql, "answer": answer}

@app.post("/query/stream")
def stream_answer(req: QueryRequest):
    sql = question_to_sql(req.question)
    result = execute_query(sql)
    answer = format_response(result)

    def generate():
        for char in answer:
            yield char
            time.sleep(0.03)

    return StreamingResponse(generate(), media_type="text/plain")

@app.post("/query/visualize")
def visualize(req: QueryRequest):
    sql = question_to_sql(req.question)
    image = visualize_query(sql)
    if not image:
        return {"error": "Unable to generate visualization"}
    return {"image": image}
