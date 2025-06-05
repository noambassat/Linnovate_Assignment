# app/utils/check_existence.py

import os
import psycopg2

def highlight_exists(video_id: str, segment_path: str) -> bool:
    filename_only = os.path.basename(segment_path)
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "highlights_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM highlights
            WHERE video_id = %s AND segment_path = %s
        """, (video_id, filename_only))
        exists = cur.fetchone()[0] > 0
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"DB check error: {e}")
        return False
