from fastapi import FastAPI, HTTPException, Body
from typing import List, Optional
from DatabaseAgent import Neo4jDatabase
from QnAAgent import QnAAgent
from FutureWorksAgent import FutureWorksAgent
from SummarizeFindingsAgent import SummarizeFindings

app = FastAPI()

neo4j_uri = "neo4j://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "password"
db = Neo4jDatabase(neo4j_uri, neo4j_user, neo4j_password)

@app.get("/get_papers/")
async def get_papers(start_year: int):
    papers = db.query_papers_by_year(start_year)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the specified year.")
    return papers

@app.post("/answer_question/")
async def answer_question(
    question: str = Body(..., embed=True),
    paper_id: str = Body(..., embed=True)  
):
    paper = db.get_paper_by_id(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")
    agent = QnAAgent([paper])
    answer = agent.answer_question(question, 0) 
    return {"answer": answer}

@app.post("/generate_future_works/")
async def future_works(paper_id: str = Body(..., embed=True)):
    paper = db.get_paper_by_id(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")
    agent = FutureWorksAgent([paper])
    future_work = agent.generate_future_work(0) 
    return {"future_work": future_work}

@app.post("/summarize_findings/")
async def summarize_findings(year: int = Body(..., embed=True)):
    papers = db.query_papers_by_year(year)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the specified year.")

    agent = SummarizeFindings(papers)
    findings_summary = agent.summarize_findings()
    return {"findings_summary": findings_summary}

@app.post("/generate_future_works_from_year/")
async def generate_future_works_from_year(year: int = Body(..., embed=True)):
    papers = db.query_papers_by_year(year)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the specified year.")

    agent = SummarizeFindings(papers)
    future_works_summary = agent.generate_future_works_from_year()
    return {"future_works_summary": future_works_summary}

@app.post("/extract_key_points/")
async def extract_key_points(year: int = Body(..., embed=True)):
    papers = db.query_papers_by_year(year)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the specified year.")

    agent = SummarizeFindings(papers)
    key_points_list = agent.extract_key_points()
    return {"key_points": key_points_list}

@app.on_event("shutdown")
def shutdown_event():
    db.close()
