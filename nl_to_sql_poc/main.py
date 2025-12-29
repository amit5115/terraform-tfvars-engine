from sqlalchemy import create_engine, text

import requests
import os

# ----------------------------
# COMPANY GPT CONFIG
# ----------------------------
os.environ["NO_PROXY"] = os.environ["no_proxy"] = "ai-framework1"

PROXY_ENDPOINT = "https://ai-framework1:8085"
API_KEY = ""   # use env var in real life
NTNET_USER = "amitk30@amdocs.com"
LLM_MODEL = "gpt-4.1"

HEADERS = {
    "Content-Type": "application/json",
    "API-Key": API_KEY,
    "X-Effective-Caller": NTNET_USER
}


# ----------------------------
# CONFIG
# ----------------------------

engine = create_engine("postgresql+psycopg2://localhost/pocdb")

# ----------------------------
# READ DATABASE SCHEMA
# ----------------------------
def get_schema():
    query = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """
    with engine.connect() as conn:
        rows = conn.execute(text(query)).fetchall()

    schema = {}
    for table, column, dtype in rows:
        schema.setdefault(table, []).append(f"{column} ({dtype})")

    return schema

# ----------------------------
# CLEAN SQL (REMOVE MARKDOWN)
# ----------------------------
def clean_sql(sql: str) -> str:
    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "")

    return sql.strip()

# ----------------------------
# RUN SQL SAFELY
# ----------------------------
def run_sql(sql: str):
    if not sql.lower().strip().startswith("select"):
        raise Exception("Only SELECT queries are allowed")

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return result.fetchall()
    
def call_company_llm(messages):
    payload = {
        "llm_model": LLM_MODEL,
        "messages": messages
    }

    response = requests.post(
        f"{PROXY_ENDPOINT}/api/v1/call_llm",
        headers=HEADERS,
        json=payload,
        verify=False
    )

    if response.status_code != 200:
        raise Exception(f"LLM Error: {response.status_code} - {response.text}")

    result = response.json()
    return result["message"]


# ----------------------------
# LLM → SQL
# ----------------------------
def english_to_sql(question: str):
    schema = get_schema()

    system_prompt = f"""
You are a PostgreSQL expert.

Database schema:
{schema}

Rules:
- Generate ONLY valid PostgreSQL SQL
- Use SELECT queries only
- Use ONLY tables and columns from schema
- ALWAYS double-quote table and column names exactly as shown in schema
- Return ONLY SQL, no explanation
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    sql = call_company_llm(messages)
    return sql.strip()


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    question = input("Ask your question: ")

    sql = english_to_sql(question)
    cleaned_sql = clean_sql(sql)
    rows = run_sql(cleaned_sql)

    for r in rows:
        print(r)
