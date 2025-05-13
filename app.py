import streamlit as st
from rag_chain import answer_question
from db_connection import run_query

# Set page config for full width
st.set_page_config(
    page_title="📊 SQL RAG Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for full width
st.markdown(
    """
    <style>
        .main > div {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 SQL Vector DB Chat Assistant")

# Main panel
query = st.text_input("Ask a question about your database:")

if query:
    answer = answer_question(query)
    
    st.markdown("### 💡 Answer")
    if "error" in answer:
        st.error(answer["error"])
    else:
        st.success(answer.get("answer", "Answer:"))
    
    if "sql_query" in answer:
        st.code(answer["sql_query"], language="sql")
        
        # SQL Execution Panel
        st.markdown("## 🧪 Run SQL Against Live Database")
        with st.expander("🔍 Try this query or modify it"):
            modified_sql = st.text_area("SQL Query", value=answer["sql_query"])
            if st.button("Execute"):
                if modified_sql.lower().startswith("select"):
                    try:
                        results = run_query(modified_sql)
                        st.dataframe(results)
                    except Exception as e:
                        st.error(f"❌ Query failed: {e}")
                else:
                    st.warning("Only SELECT queries are allowed")
