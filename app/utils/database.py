# app/utils/database.py
import psycopg2
import os

def save_highlight_to_db(data: dict):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "highlights_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO highlights (video_id, segment_path, timestamp, description, embedding, llm_summary)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["video_id"],
        os.path.basename(data["segment_path"]),  # <-- נקודה קריטית
        data["timestamp"],
        data["description"],
        data["embedding"],
        data["llm_summary"]
    ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Highlight for video {data['video_id']} saved to database.")