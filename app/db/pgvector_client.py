import psycopg2
import os
from app.utils.embedding import get_embedding


def get_similar_highlights(query: str, top_k: int = 3):
    query_embedding = get_embedding(query)

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "highlights_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT segment_path, description, llm_summary, timestamp
        FROM highlights
        ORDER BY embedding <-> %s
        LIMIT %s;
    """, (query_embedding, top_k))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "segment": row[0],
            "description": row[1],
            "summary": row[2],
            "timestamp": row[3]
        }
        for row in results
    ]
# This function retrieves similar video highlights based on a text query using vector similarity search.