from vector_db import semantic_search
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from db_connection import run_query
import os
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = OpenAI(temperature=0)

template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
        You are a helpful MySQL schema expert.

        Given the following SQL table definitions, relational notes, and examples,
        deduce relationships across tables and answer the user's question clearly.

        Context:
        {context}

        User Question:
        {question}
        """
)

def extract_sql_query(response):
    """Extract SQL query from LLM response"""
    match = re.search(r'(SELECT|INSERT|UPDATE|DELETE).*?;', response, re.DOTALL)
    return match.group(0) if match else None

def get_table_columns(table_name):
    """Discover columns in a table"""
    try:
        results = run_query(f"DESCRIBE {table_name};")
        return [row['Field'] for row in results]
    except Exception as e:
        logger.error(f"Failed to describe table {table_name}: {e}")
        return None

def get_schema_context():
    """Get context about the database schema"""
    schema = {
        "users": ["user_id", "full_name", "email", "phone", "created_at"],
        "products": [],
        "categories": []
    }
    
    # Discover schema for other tables if needed
    for table in ["products", "categories", "addresses"]:
        try:
            schema[table] = get_table_columns(table)
        except:
            continue
            
    return "\n".join([f"{table}: {', '.join(columns)}" for table, columns in schema.items() if columns])

def answer_question(query):
    """Enhanced with schema awareness"""
    results = semantic_search(query)
    context_docs = "\n\n".join(results['documents'][0][:5])[:4000]
    
    # Add schema context
    schema_context = get_schema_context()
    full_context = f"{context_docs}\n\nDatabase Schema:\n{schema_context}"
    
    # Generate and execute SQL
    sql_prompt = sql_template.format(context=full_context, question=query)
    sql_response = llm(sql_prompt)
    sql_query = extract_sql_query(sql_response)
    
    if sql_query:
        try:
            db_results = run_query(sql_query)
            return {
                "answer": "Generated SQL query:",
                "sql_query": sql_query
            }
        except Exception as e:
            logger.error(f"SQL query failed: {e}")
            return {"error": f"Database query failed: {e}", "sql_query": sql_query}
    
    # Fallback to regular RAG answer
    prompt = template.format(context=full_context, question=query)
    return llm(prompt)
