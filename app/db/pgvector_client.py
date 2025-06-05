import psycopg2
import os
from app.utils.embedding import get_embedding

def get_similar_highlights(query: str, top_k: int = 3):
    embedding = get_embedding(query)

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "highlights_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT video_id, segment_path, timestamp, description, llm_summary
        FROM highlights
        ORDER BY embedding <-> %s::vector
        LIMIT %s
    """, (embedding, top_k))

    results = [
        {
            "video_id": row[0],
            "segment_path": row[1],
            "timestamp": row[2],
            "description": row[3],
            "summary": row[4]
        }
        for row in cur.fetchall()
    ]

    cur.close()
    conn.close()
    return results
