from sqlalchemy import create_engine, text
from openai import OpenAI

# ----------------------------
# CONFIG
# ----------------------------
client = OpenAI()

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
- Use only tables and columns from schema
- Return ONLY SQL, no explanation
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content.strip()

# ----------------------------
# MAIN
# ----------------------------
question = input("Ask your question: ")

sql = english_to_sql(question)
print("\nGenerated SQL:\n", sql)

cleaned_sql = clean_sql(sql)
print("\nCleaned SQL:\n", cleaned_sql)

rows = run_sql(cleaned_sql)

print("\nResult:")
for r in rows:
    print(r)
