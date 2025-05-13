import re
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = PersistentClient(path="./vector_db")
collection = client.get_or_create_collection(name="shopping_schema")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def index_knowledge_base():
    """Index both natural language questions and SQL examples"""
    # Load and combine both files
    try:
        with open("nlp_sample_questions.txt", "r", encoding="utf-8") as f1, \
             open("sample_sql_queries.sql", "r", encoding="utf-8") as f2:
            
            content = """-- NATURAL LANGUAGE QUESTIONS
{}

-- SQL QUERY EXAMPLES
{}""".format(f1.read(), f2.read())
            
        logger.info("Indexing combined knowledge base")
        
        # Split into logical chunks
        chunks = re.split(r"(?i)(?=-- [A-Z]+ TABLE|-- QUESTIONS|-- EXAMPLES|-- SQL QUERIES)", content)
        chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 30]

        # Generate embeddings
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        embeddings = embedding_model.encode(chunks).tolist()

        # Update vector database
        try:
            collection.delete(ids=ids)
        except:
            pass
        
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )
        logger.info(f"Indexed {len(chunks)} chunks from combined knowledge base")
        return True
        
    except Exception as e:
        logger.error(f"Failed to index knowledge base: {e}")
        return False

def semantic_search(query, k=6):
    query_vector = embedding_model.encode([query])[0].tolist()
    results = collection.query(query_embeddings=[query_vector], n_results=k)
    return results
