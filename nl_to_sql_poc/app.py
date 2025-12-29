from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Import your existing functions
from tools.main import english_to_sql, clean_sql, run_sql

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sql": None,
            "rows": None
        }
    )


@app.post("/query", response_class=HTMLResponse)
def run_query(request: Request, question: str = Form(...)):
    sql = english_to_sql(question)
    cleaned_sql = clean_sql(sql)

    try:
        rows = run_sql(cleaned_sql)
    except Exception as e:
        rows = [("ERROR", str(e))]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "question": question,
            "sql": cleaned_sql,
            "rows": rows
        }
    )
