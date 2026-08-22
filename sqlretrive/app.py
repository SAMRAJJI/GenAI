from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
genai.configure(api_key=os.getenv('google_api_key'))
db_path = os.path.join(os.path.dirname(__file__), "student.db")

def get_gemini(question, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    res = model.generate_content([prompt, question])
    
    sql = res.text.strip()

    # Remove markdown if Gemini adds it
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()
    
    return sql

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

prompt = """
You are an SQL query generator.

Your ONLY job is to convert the user's question into a SQLite SQL query.

Database:
Table: student

Columns:
name
class
section

IMPORTANT RULES:
- Return ONLY the SQL query.
- Do NOT say "Okay".
- Do NOT explain anything.
- Do NOT use markdown.
- Do NOT use ```sql.
- Do NOT use ```.
- Do NOT include any text before or after the SQL query.
- The output must be directly executable by SQLite.

Examples:

User: How many students are there?

Output:
SELECT COUNT(*) FROM student;

User: Show all students in AIDA class.

Output:
SELECT * FROM student WHERE class = 'AIDA';

User: Show students in section A.

Output:
SELECT * FROM student WHERE section = 'A';
"""

st.set_page_config(page_title="I can retrieve any sql query")
st.header("Gemini app to retrieve SQL Data")

question = st.text_input("Input", key="input")

submit = st.button("ask the question")

if submit:
    res=get_gemini(question, prompt)
    st.subheader("Generated SQL")
    st.code(res, language="sql")
    print("Generated SQL:", res)   
    data = read_sql_query(res, db_path)
    st.subheader("the response is")
    
    for i in data:
        print(i)
        st.header(i)
    