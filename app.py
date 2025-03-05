from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configuration our API Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

load_dotenv() ## load all the environemnt variables

# Function to Load the Google Gemini Module and Providw sql query as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

# Function to retrieve the query from the sqllit database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows
# Define your Prompt

prompt = [
    """
    You are an expert in converting English questions into SQL queries!  
The database is named STUDENT and contains the following columns: NAME, CLASS, SECTION.  

For instance,  
Example 1 - "How many records are there?"  
The SQL query would be: `SELECT COUNT(*) FROM STUDENT;`  

Example 2 - "Who are the students studying in the Data Science class?"  
The SQL query would be: `SELECT * FROM STUDENT WHERE CLASS = 'Data Science';`  

Note: The SQL code should not start or end with backticks, nor should it include the word "SQL" in the output.

    """
]

# Stream App framework

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App to retrieve SQL Data")

question=st.text_input("input: ",key="input")

submit=st.button("Ask the Question")

#if Submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)